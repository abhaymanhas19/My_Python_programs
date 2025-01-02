import json
SYNC_MAIN_MODEL="gpt-4o-mini"
import openai
import os
import json


AZURE_OPENAI_KEY_1=""
AZURE_OPENAI_KEY_1_ENDPOINT=""
AZURE_API_VERSION_1 = "2024-02-01"

OPENAI_SECRET_KEY_0= ""
OPENAI_ASYNC_CLIENT=openai.AsyncOpenAI(api_key=OPENAI_SECRET_KEY_0)

aclient =  openai.AsyncAzureOpenAI( 
    api_key=AZURE_OPENAI_KEY_1,
    api_version=AZURE_OPENAI_KEY_1_ENDPOINT,
    azure_endpoint=AZURE_API_VERSION_1)

def generate_topics_json_schema():
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
    return generate_topics_json_schema
    
async def main(contexts):
    generate_topics_instructions = f"""Identify 2-6 topics that directly answer the question/ theme: "{"explain the file"}". 
                                To do so, generate a JSON. First, provide a list of preliminary topics under `"preliminary_topics"`, including a name and detailed description for each topic. Next, evaluate and describe whether the topics are mutually exclusive and if they collectively cover all relevant areas in the `"mutual_exclusivity_check"` and `"collective_exhaustiveness_check"` fields, respectively. Finally, offer any suggestions for refining the topics in the `"recommendations"` field and finalize the list of topics in `"final_topics"`, ensuring they are distinct and clearly defined."""
    
    function= {
                "name": "generate_summary_topics",
                "description": "The output should be according as  defined parameters.",
                "parameters": generate_topics_json_schema(),
            }
    
    response = await aclient.chat.completions.create(
        model=SYNC_MAIN_MODEL,
        temperature=0.2,
        messages=[
            {"role": "system", "content": generate_topics_instructions},
            {
                "role": "user",
                "content": f"""# Analyses of the documents

                {contexts}

                ###

                ### Output Instruction:
                Generate a JSON object based on the defined json schema. Do not include any explanations or additional text..""",
            },
        ],
        functions=[function],
        function_call={"name": "generate_summary_topics"}
        
    )
    function_args = response.choices[0].message.function_call.arguments
    topics_response = json.loads(function_args)
    return topics_response

import asyncio
text="Document BG_Advisor_meeting_3-14-24_AM_otter_ai.docx\n\nSo many graphic designers now work from home, and we're not going to send a kid some guy's garage for a mentorship. So how can we offer that experience on campus, or a lot of our students have the issue of transportation. I have a 16 year old girl that doesn't drive yet and her mom is not going to put her on a bus in San Diego to get her to go from San Ysidro to wherever she needs to be, because that's where she drives home every single day hurt, she gets dropped off here. So she doesn't have the transportation ability to receive a mentorship but she's really interested in hair braiding. So we got her a mannequin, and she's doing online YouTube tutorials and creating a portfolio. So that's where our X factors and LTI projects come into play is offering students the experiences for their specific pathways that they may not be able to receive off campus. Michael Crawford   In the sector's real quick, where did those come from? Um, it's something Holly BG advisor   that neural has taken on."
print(asyncio.run(main(text)))