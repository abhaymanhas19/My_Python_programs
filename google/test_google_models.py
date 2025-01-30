import google.generativeai as genai
import os
import asyncio
import pathlib
genai.configure(api_key="")

model = genai.GenerativeModel(model_name="gemini-exp-1206")


# FILE UPLOAD TESTING GOOGLE GEMINI
prompt = "please provide the transcript of the speech from 9:"

# FIRST WAY
# file=genai.upload_file(path=pathlib.Path("google/Hindi - Audio.mp3"),mime_type="audio/mp3")
# response = model.generate_content([prompt, file])

# SECOND WAY
# response = model.generate_content([prompt,   {
#         "mime_type": "audio/mp3",
#         "data": pathlib.Path("google/Hindi - Audio.mp3").read_bytes()
#     }])


# THIRD WAY
file = open("google/Hindi - Audio.mp3","rb")
binary_data = file.read()

chat= model.start_chat()

response = asyncio.run(chat.send_message_async(content=["what is the length of file in milisecond",{
    "mime_type":"audio/mpeg",
    "data":binary_data
}]))
print(response.text)


# ASYNC TESTING GOOGLE GEMINI
# async def test():
#     text = await model.generate_content_async("what is your name")
#     print(text.text)

# async def main():
#     tasks = [asyncio.create_task(test()) for _ in range(1)]
#     await asyncio.gather(*tasks)
    
# asyncio.run(main())