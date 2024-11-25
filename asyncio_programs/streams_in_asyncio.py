import openai 
# Batch_client = openai.AzureOpenAI(
Azure_client=""
response = Azure_client.chat.completions.create(
    model="gpt-4o-mini",
    messages = [{
        "role":"user","content":"what is python"
    }]
)
print(response)