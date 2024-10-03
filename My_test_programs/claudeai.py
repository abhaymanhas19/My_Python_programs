# import anthropic
import time

# 
# # message = anthropic_client.messages.create(
# #     model="claude-3-5-sonnet-20240620",
# #     max_tokens=1000,
# #     temperature=0,
# #     system="you  are are a AI MODEL",
# #     messages = [
# #         {"role": "user", "content": "Hello there."},
# #         {"role": "assistant", "content": "Hi, I'm Claude. How can I help?"},
# #         {"role": "user", "content": "Can you explain Glycolysis to me?"},
# # ]
# # )

# with anthropic_client.messages.stream(
#     max_tokens=1024,
#     messages=[{"role": "user", "content": "Hello"}],
#     model="claude-3-5-sonnet-20240620",
#     ) as stream:
  

#     for text in stream.text_stream:
#         print(text, end="", flush=True)


# from openai import AzureOpenAI
#

# def transcript():
#     start_time=time.time()
#     transcription = client.chat.completions.create(
#     model="gpt-4o-mini", 
#     messages=[{"role":"user","content":"what is python"}]
#     )
#     print(time.time()-start_time)
#     return transcription


# print(transcript().choices[0].message.content)


#################################################3
# import fal_client
# import os
# import asyncio
# import aiofiles


# async def trancscript():
#     url= await fal_client.upload_async(await aiofiles.open("harvard.wav", "rb"),"audio/wav")
#     start_time=time.time()
#     handler = await fal_client.submit_async(
#         "fal-ai/wizper",
#         arguments={
#             "audio_url": url,
#         },
#     )
#     log_index = 0
#     async for event in handler.iter_events(with_logs=True):
#         if isinstance(event, fal_client.InProgress):
#             new_logs = event.logs[log_index:]
#             for log in new_logs:
#                 print(log["message"])
#             log_index = len(event.logs)

#     print(time.time()-start_time)
#     return await handler.get()

# # 
# print(asyncio.run(trancscript()))



# import asyncio 
# from openai import AsyncOpenAI

# async def translate_text(text, output_language):
#     response = await aclient.chat.completions.create(
#         model="gpt-3.5-turbo",
#         temperature=0.0,
#         messages=[
#                     {"role": "system", "content": f"Translate the user content to {output_language} language in desired format as they are."},
#                     {
#                         "role": "user",
#                         "content": f"Translate the text in {output_language} language , Don't add anything from you end . The text is '{text}'",
#                     },
                  
#                     ]
#         )
#     response = response.choices[0].message.content
#     return response
# asyncio.run(translate_text("Hi, can you introduce yourself?","Simplified Chinese"))



# from openai import OpenAI

# stream = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[{"role": "user", "content": "you are a research analyst.Your job is generate market analysis based on their capital"}],
#     stream=True,
# )
# for chunk in stream:
#     if chunk.choices[0].delta.content is not None:
#         print(chunk.choices[0].delta.content, end="")