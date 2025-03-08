
import openai
import asyncio


OPENAI_ASYNC_CLIENT=openai.AsyncOpenAI(api_key="")
from openai import OpenAI,AsyncOpenAI


Additional_instruction = "Return only a valid JSON object without any explanation, code blocks, or formatting. The response should be directly parseable by JSON.parse() or json.loads()." 
system_message = '''# Instructions

        Analyze the provided document and generate a JSON response to the question.

        ## Steps

        ### **Step 1: Understanding the Question**
        - Identify the key focus of the question.
        - Determine what kind of information would constitute an adequate response (e.g., causes, effects, statistics, or qualitative analysis).

        ---

        ### **Step 2: Extracting Relevant Quotes**
        - Review the given quotes and assess their relevance to the question.
        - Consider whether each quote provides direct evidence or only partial/contextual information.

        ---

        ### **Step 3: Structuring Each Paragraph**
        For each quote, you must construct a well-structured paragraph that follows this specific format:

        #### **1. Quote Introduction**
        - Start with a sentence introducing the key point from the document.
        - Directly quote the relevant passage from the document in quotation marks.

        #### **2. Elaborating on the Quote**
        - Explain what the quote means in context.
        - If necessary, expand on any implicit details that could clarify its significance.

        #### **3. Assessing Relevance to the Question**
        - Determine whether the quote directly addresses the question.
        - Identify any missing details that are needed to fully answer the question.

        #### **4. Evaluating Explicitness of the Information**
        - Assess whether the quote contains explicit information or if it only provides partial insight.
        - If it is vague or lacks supporting data, highlight these limitations.

        #### **5. Conclusion**
        - Summarize whether the quote sufficiently answers the question.
        - If the document provides a clear answer, state it explicitly.
        - If the document lacks enough detail, conclude that there is insufficient information.

        **Format the conclusion in bold double asterisks (`**`) to clearly indicate the final assessment.**

        ---

        ### **Step 4: Organizing the Response**
        - Each theme should be presented in a separate paragraph, ensuring clarity and organization.
        - If multiple quotes contribute to the same theme, combine them into a single paragraph with logical flow.
        - If different themes emerge, create separate paragraphs for each theme.

        ---

        ### **Step 5: Annotating Quotes**
        - Each paragraph must be linked to the corresponding quote(s) using the `"annotations"` field.
        - If a paragraph is derived from multiple quotes, include all relevant annotations.

        ---

        # Examples

        ## Example 1
        ```json
        {
        "question": "What were the key challenges faced during the project implementation?",
        "quotes": {
            "quote_1": {
            "quote": "One major challenge was the lack of stakeholder alignment, which led to repeated revisions and delays.",
            "filename": "project_report.pdf"
            },
            "quote_2": {
            "quote": "Resource constraints, particularly in terms of skilled personnel, created bottlenecks in execution.",
            "filename": "project_report.pdf"
            }
        },
        "answer": [
            {
            "theme": "Stakeholder Misalignment",
            "paragraph": "The report stated, 'One major challenge was the lack of stakeholder alignment, which led to repeated revisions and delays.' The document further elaborated that this issue arose due to differing priorities and expectations among key stakeholders, leading to multiple revisions throughout the project. These continuous adjustments significantly impacted the project's timelines and workload, forcing the team to rework deliverables and modify project plans frequently. The misalignment created inefficiencies and made it difficult to maintain a steady pace toward project milestones. **Thus, stakeholder misalignment was a key challenge that caused repeated delays and increased project complexity.**",
            "annotations": ["quote_1"]
            },
            {
            "theme": "Resource Constraints",
            "paragraph": "The document noted, 'Resource constraints, particularly in terms of skilled personnel, created bottlenecks in execution.' The document further explained that the shortage of experienced personnel in critical roles slowed down key phases of the project, making it difficult to maintain momentum and adhere to the planned schedule. This limitation led to frequent adjustments in resource allocation strategies and necessitated additional training efforts, further straining the available resources. **As a result, resource constraints were a significant challenge that contributed to execution bottlenecks and project inefficiencies.**",
            "annotations": ["quote_2"]
            }
        ]
        }
        ```

        ## Example 2
        ```json
        {
        "question": "What were the economic impacts of the policy changes on local businesses?",
        "quotes": {
            "quote_1": {
            "quote": "The policy changes primarily influenced investment patterns.",
            "filename": "economic_policy_report.pdf"
            }
        },
        "answer": [
            {
            "theme": "Policy Changes and Business Impact",
            "paragraph": "The report mentions that 'the policy changes primarily influenced investment patterns.' However, it does not specify whether these investment patterns affected local businesses or how they were impacted. The discussion appears to focus on investment trends broadly and primarily concern foreign businesses or large-scale investments. Since the document lacks explicit details on the economic effects of policy changes on local businesses, **it does not provide a direct answer to the question.**",
            "annotations": ["quote_1"]
            }
        ]
        }
        ```

        ## Example 3
        ```json
        {
        "question": "What were the effects of the Clean Air Act on urban air pollution levels in the United States?",
        "quotes": {
            "quote_1": {
            "quote": "The Clean Air Act introduced several regulatory measures aimed at reducing industrial emissions and promoting air quality monitoring.",
            "filename": "clean_air_act_analysis.pdf"
            }
        },
        "answer": [
            {
            "theme": "Clean Air Act and Air Pollution Reduction",
            "paragraph": "The document states, 'The Clean Air Act introduced several regulatory measures aimed at reducing industrial emissions and promoting air quality monitoring.' While this describes the intended goals of the Act, it does not provide specific data or analysis on how urban air pollution levels in the United States were affected. The passage lacks direct evidence, such as measured reductions in air pollutants, trends in air quality indices, or case studies of urban centers. Since it does not explicitly discuss the impact of the Clean Air Act on urban air pollution levels, **it does not directly answer the question.**",
            "annotations": [
                "quote_1"
            ]
            }
        ]
        }
        ```

        ## Reminder

        1. If analyzing interview transcripts, do not quote the moderator and only quote the interviewee. The goal is to analyze the interviewee responses, not the moderator responses.
        2. Only extract quotes from the document. Only make assessments based on what the quotes explicitly say. Make narrow strict interpretations of the quotes.

    '''
    
message = "<question>\n            **Question**:\n            What does the file say about 'what are the challenges'?\n            </question>\n            \n            ######\n\n            <document>\n\n            <Participant_2.docx>\n\n# Participant_2.docx\n\nAI Interviewer:\xa0Hi! I'm an AI voice interviewer developed by AILYZE and hired by HEKS. Thank you for joining us today. Let's start. How long have you been working at HEKS and what is your role in MEAL?\n\nParticipant:\xa0I’ve been with HEKS for about 8 years now. I work as a program consultant, focusing on Monitoring, Evaluation, Accountability, and Learning—or MEAL. My role primarily involves ensuring that our projects meet their goals and deliver measurable outcomes.\n\nAI Interviewer:\xa0I see. Can you tell me about a recent MEAL project that went well?\n\nParticipant:\xa0Sure. One project that went particularly well involved hiring an external evaluator to analyze the data we collected from a community program. Their insights were thorough, and the process went smoothly.\n\nAI Interviewer:\xa0What do you think made that project successful?\n\nParticipant:\xa0A big part of the success was due to clear communication and setting expectations early on. The external evaluator was highly experienced, and we worked closely with the local teams to ensure the data collection process was robust.\n\nAI Interviewer:\xa0Interesting. Can you give an example of a problem you've encountered with our MEAL processes?\n\nParticipant:\xa0One challenge has been a lack of mutual understanding between implementers and evaluators regarding the methodology used for data collection. This sometimes leads to inconsistent results or delays.\n\nAI Interviewer:\xa0Thank you for sharing. How did you or the team approach addressing this challenge?\n\nParticipant:\xa0We addressed it by implementing close follow-ups and conducting training sessions to build the capacity of the local teams involved in data collection. It helped bridge the gap between expectations and execution.\n\nAI Interviewer:\xa0I see. On a scale of 1 to 10, where 1 is very ineffective and 10 is highly effective, how would you rate the overall effectiveness of our current MEAL processes?\n\nParticipant:\xa0I’d say about a 7.5. There’s definitely room for improvement, but we’ve made significant progress.\n\nAI Interviewer:\xa0Thank you. Is there a specific resource you wish you had for MEAL work?\n\nParticipant:\xa0I think more access to appropriate tools and comprehensive training mechanisms would be very helpful.\n\nAI Interviewer:\xa0Do you think we need any new tools to make our MEAL processes better?\n\nParticipant:\xa0Yes, I believe having tools that simplify data visualization and reporting could make a big difference.\n\nAI Interviewer:\xa0Are you familiar with other organizations' MEAL practices?\n\nParticipant:\xa0Not really. I haven’t had much exposure to how other organizations handle MEAL.\n\nAI Interviewer:\xa0Where do you think we could learn from them?\n\nParticipant:\xa0I’d imagine that online case studies or shared resources could provide valuable insights.\n\nAI Interviewer:\xa0What emerging trends or considerations do you think might influence our MEAL processes in the future?\n\nParticipant:\xa0Chatbots could play a role in formalizing data collection and analysis processes. They might also improve response rates from participants.\n\nAI Interviewer:\xa0Are there any tools you've seen that you think could benefit us?\n\nParticipant:\xa0I’ve heard of advanced survey platforms that integrate AI for real-time analysis. Something like that could be useful.\n\nAI Interviewer:\xa0How would you describe your experience answering these questions from an AI interviewer?\n\nParticipant:\xa0Honestly, it feels a bit mechanical and somewhat creepy. It would be nice to have a more human-like interaction, and maybe some pauses for reflection.\n\nAI Interviewer:\xa0Do you see potential for integrating AI-driven interviews like this into our MEAL processes? If so, where do you think it could be most beneficial?\n\nParticipant:\xa0Yes, I think it could be useful for initial data collection or for conducting follow-ups where consistency is key. However, it would need to feel less robotic.\n\nAI Interviewer:\xa0Do you have any final thoughts?\n\nParticipant:\xa0Just that it’s an interesting approach, but there’s a lot of room for making it more engaging and natural.\n\nAI Interviewer:\xa0Thank you for sharing your insights. This concludes our interview. You may now close the page.\n\n</Participant_2.docx>\n\n</document>"



async def asyncopenrouter(system_message,user_message,json_schema=None):
  request_parameter = {
    "model": 'google/gemini-2.0-pro-exp-02-05:free',
    "extra_body":{"models":["google/gemini-exp-1206:free", "google/gemini-2.0-flash-001", "openai/gpt-4o-mini"]},
    "temperature":0.1,
  }
  
  if json_schema:
    if json_schema['type']=="json_object":
      response_structure = json_schema
    else:
        response_structure = {
            "type":"json_schema",
            "json_schema":json_schema,
            "strict":True
          }
    system_message = Additional_instruction +  system_message
    request_parameter.update({"messages" : [{"role": "system","content": system_message},{"role": "user","content": user_message}]})                              
    request_parameter.update({"response_format":response_structure})
    
  response = await asyncopenrouter_client.chat.completions.create(**request_parameter)
  return response

    

response = asyncio.run(asyncopenrouter(system_message=system_message,user_message=message,json_schema={'type':"json_object"}))
print(response)