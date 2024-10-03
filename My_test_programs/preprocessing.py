import openai
from data import document

import json
import aiohttp
import asyncio
theme = 'What information sources did participants use to learn about the flu and vaccine?'
documents = list(document.keys())

def format_documents(doc_dict):
    formatted_text = ""
    for filename, text in doc_dict.items():
        formatted_text += f"# {filename}\n\n{text}\n\n####\n\n"
    return formatted_text

contexts = format_documents(document)

generate_topics_instructions = f'''Identify 2-6 topics that directly answer the question/ theme: "{theme}". 
                                To do so, generate a JSON. First, provide a list of preliminary topics under `"preliminary_topics"`, including a name and detailed description for each topic. Next, evaluate and describe whether the topics are mutually exclusive and if they collectively cover all relevant areas in the `"mutual_exclusivity_check"` and `"collective_exhaustiveness_check"` fields, respectively. Finally, offer any suggestions for refining the topics in the `"recommendations"` field and finalize the list of topics in `"final_topics"`, ensuring they are distinct and clearly defined.'''


generate_topics_json_schema = {
        "type": "object",
        "properties": {
            "preliminary_topics": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                "preliminary_topic": {
                    "type": "string",
                    "description": "The name of the topic."
                },
                "preliminary_description": {
                    "type": "string",
                    "description": "A detailed description of the topic."
                }
                },
                "required": ["preliminary_topic", "preliminary_description"],
                "additionalProperties": False
            },
            "description": "A list of preliminary topics with descriptions. Ensure there are between 2 and 6 topics included in this list. Each topic should be described clearly and comprehensively."
            },
            "mutual_exclusivity_check": {
            "type": "string",
            "description": "A thorough evaluation of whether the topics are mutually exclusive, meaning they do not overlap in content or subject matter. This involves analyzing each topic to ensure that its scope does not intersect with that of any other topic in the list."
            },
            "collective_exhaustiveness_check": {
            "type": "string",
            "description": "A thorough evaluation of whether the list of topics collectively addresses all relevant areas of interest, ensuring comprehensive coverage without leaving out significant topics."
            },
            "recommendations": {
            "type": "string",
            "description": "Suggestions for refining the list of topics to enhance coverage and relevance. This may include adding new topics, removing redundant ones, or redefining existing ones to improve clarity and comprehensiveness."
            },
            "final_topics": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                "final_topic": {
                    "type": "string",
                    "description": "The name of the topic."
                },
                "final_description": {
                    "type": "string",
                    "description": "A detailed description of the topic."
                }
                },
                "required": ["final_topic", "final_description"],
                "additionalProperties": False
            },
            "description": "A final list of topics with descriptions. Ensure that this list also contains between 2 and 6 topics. Each topic should be clearly defined and distinct from the others."
            }
        },
        "required": ["preliminary_topics", "mutual_exclusivity_check", "collective_exhaustiveness_check", "recommendations", "final_topics"],
        "additionalProperties": False
        }

response = client.chat.completions.create(
                model='gpt-4o-mini',
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "generate_topics",
                        "strict": True,
                        "schema": generate_topics_json_schema,
                    },
                },
                messages=[
                    {"role": "system", "content": generate_topics_instructions},
                    {
                        "role": "user",
                        "content":  f"""# Analyses of the documents

{contexts}

###

# JSON Output:"""
                },
            ],
        )
print(json.loads(response.choices[0].message.content))

from jsonschema import validate

topics_response = json.loads(response.choices[0].message.content)

#Abhay to implement retry mechanism. If not valid JSON, then retry the OpenAI call
validate(instance=topics_response, schema=generate_topics_json_schema)

topics = topics_response.get("final_topics", [])


def create_identify_quotes_for_topic_json_schema(documents, topic, topic_description):
    schema = {
        "type": "object",
        "properties": {
            "topic": {
                "type": "string",
                "enum": [topic],
                "description": topic_description
            },
            "quotes": {
                "type": "object",
                "properties": {},
                "additionalProperties": False
            },
            "elaboration": {
                "type": "string",
                "description": f"Elaboration on the topic {topic}"
            }
        },
        "required": ["topic", "quotes", "elaboration"],
        "additionalProperties": False
    }

    # Adding document properties to 'quotes'
    schema["properties"]["quotes"]["properties"] = {
        document: {
            "type": "object",
            "properties": {
                "quote": {
                    "type": ["string", "null"]
                },
                "elaboration": {
                    "type": ["string", "null"]
                }
            },
            "required": ["quote", "elaboration"],
            "additionalProperties": False
        }
        for document in documents
    }

    # Updating 'required' field for 'quotes' to include all document names
    schema["properties"]["quotes"]["required"] = documents

    return schema


async def process_topics(topic):
    try:
        response = await aclient.chat.completions.create(
                        model='gpt-4o-mini',
                        response_format={
                            "type": "json_schema",
                            "json_schema": {
                                "name": "create_identify_quotes_for_topic",
                                "strict": True,
                                "schema": create_identify_quotes_for_topic_json_schema(documents, topic.get('final_topic',None), topic.get('final_description',None)),
                            },
                        },
                        messages=[
                            {"role": "system", "content": f'''Identify quotes related to "{topic.get('final_topic')}" and elaborate on those quotes, in order to answer "{theme}". To do so, generate a JSON. For each document, identify any quotes related to {topic.get('final_topic')} from the analyses of the documents and include them in the "quote" field; if no relevant quotes are found, set this field to `null`. Then, provide an elaboration related to the topic in the "elaboration" field for each document; if there's no elaboration, set this field to `null`.'''},
                            {
                                "role": "user",
                                "content":  f"""# Analyses of the documents

    {contexts}

    ###

    # JSON Output:"""
                        },
                    ],
                )

        response= json.loads(response.choices[0].message.content)

        #Abhay to implement retry mechanism. If not valid JSON, then retry the OpenAI call
        try:
            validate(instance=response, schema=create_identify_quotes_for_topic_json_schema(documents, topic['final_topic'], topic['final_description']))
        except Exception as e:
            print(f"Valiation failed as error '{e}'" )
            await asyncio.sleep(2)
            return await process_topics(topic)
            
        return response
    except Exception as e:
        print(f"processing topics requets fail as error '{e}")
        return None

async def main():
    tasks = [process_topics(topic) for topic in topics]
    results = await asyncio.gather(*tasks)
    return results

result = asyncio.run(main())


def remove_none_quotes(result):
    new_result={}
    # Iterate over each topic in the dictionary
    for topics in result:
        # Filter out documents where the quote is None
        filtered_quotes = {doc: details for doc, details in topics['quotes'].items() if details['quote'] is not None}

        # Update the topic's quotes with the filtered ones
        new_result[topics['topic']]=topics
        new_result[topics['topic']]['quotes']=filtered_quotes
    return result

result=remove_none_quotes(result)


generate_synthesis_schema = {
    "type": "object",
    "properties": {
        "synthesis": {
            "type": "object",
            "description": "A synthesis of all the topics, summarizing shared and unique viewpoints across the documents.",
            "strict": True,
            "properties": {
                "introduction": {
                    "type": "string",
                    "description": "A single-paragraph overview of the content of all documents in relation to the topics, mentioning each document and its relevance. This should be 4-6 sentences long."
                },
                "shared_viewpoints": {
                    "type": "array",
                    "description": "An array of paragraphs elaborating on viewpoints common across most documents, with specific document references and verbatim quotes. This section should contain at least 30 sentences in total.",
                    "items": {
                        "type": "string",
                        "description": "Each string should be a detailed paragraph of about 10 sentences long explaining one shared viewpoint with references and quotes from the documents."
                    }
                },
                "unique_viewpoints": {
                    "type": "array",
                    "description": "An array of paragraphs elaborating on unique or differing viewpoints found in the documents, with specific document references and verbatim quotes. This section should contain at least 30 sentences in total.",
                    "items": {
                        "type": "string",
                        "description": "Each string should be a detailed paragraph of about 10 sentences long explaining one unique or differing viewpoint with references and quotes from the documents."
                    }
                },
                "conclusion": {
                    "type": "string",
                    "description": "A summary of the overall synthesis, bringing together the shared and unique viewpoints. This should be 4-6 sentences long."
                }
            },
            "required": ["introduction", "shared_viewpoints", "unique_viewpoints", "conclusion"],
            "additionalProperties": False
        }
    },
    "required": ["synthesis"],
    "additionalProperties": False
}



generate_synthesis_instructions = f'''Based on the analyses of the documents and key topics & quotes, generate a synthesis of multiple documents on the topic "{theme}". To do so, generate a JSON:
- **Introduction (`introduction`):** Write a single-paragraph overview (4-6 sentences) summarizing the content of all documents in relation to the topic. Mention each document by name and briefly describe its relevance or stance on the topic.
- **Shared Viewpoints (`shared_viewpoints`):** Elaborate on viewpoints that are common across most documents. For each shared viewpoint, specify which documents hold this viewpoint. Write at least 30 sentences, integrating verbatim quotes from the documents and providing a detailed analysis of how these quotes contribute to the shared viewpoint.
- **Unique Viewpoints (`unique_viewpoints`):** Describe unique or differing viewpoints found in the documents. Write at least 30 sentences, using verbatim quotes from the documents to support your analysis. Clearly specify which document each unique viewpoint comes from.
- **Conclusion (`conclusion`):** Summarize the overall synthesis in 4-6 sentences, bringing together the shared and unique viewpoints (e.g., Overall, ...). Provide a cohesive overview that integrates the different perspectives discussed.

Note:
- **Document References:** Always specify the document associated with each quote and viewpoint. Avoid vague terms like "majority" or "some"; instead, be precise in attributing ideas to specific documents.
- **Verbatim Quotes:** Include at least one verbatim quote from a document to substantiate each point you make. Ensure that these quotes are integrated smoothly into your synthesis, so the output is coherent on its own.
- **No Bullet Points:** Write in full paragraphs, constructing a proper essay format throughout the JSON content. Bullet points or numbered lists should be avoided.'''



response = client.chat.completions.create(
                model='gpt-4o-mini',
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "generate_synthesis",
                        "strict": True,
                        "schema": generate_synthesis_schema,
                    },
                },
                messages=[
                    {"role": "system", "content": generate_synthesis_instructions},
                    {
                        "role": "user",
                        "content":  f"""# Analyses of the documents

{contexts}

###

# Key Topics and Quotes

{result}

###

# JSON Output:"""
                },
            ],
        )

synthesis = json.loads(response.choices[0].message.content)


validate(instance=synthesis, schema=generate_synthesis_schema)  