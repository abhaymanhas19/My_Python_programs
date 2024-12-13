import google.generativeai as genai
import os
import asyncio
genai.configure(api_key="AIzaSyDhqaE4zkfhbX0HFlXy4NNuvZOp7hIIBoY")
# AIzaSyBTlYapM8F_WuS43w_34H7IWo11mzxyr04
model = genai.GenerativeModel(model_name="gemini-1.5-flash")


async def test():
    text = await model.generate_content_async("what is your name")
    print(text.text)
    
    
async def main():
    tasks = [asyncio.create_task(test()) for _ in range(1)]
    await asyncio.gather(*tasks)
    
asyncio.run(main())