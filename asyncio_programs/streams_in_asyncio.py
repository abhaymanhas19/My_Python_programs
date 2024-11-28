import openai 



Azure_client=openai.AzureOpenAI(api_key=AZURE_OPENAI_KEY_2,azure_endpoint=AZURE_OPENAI_KEY_2_ENDPOINT,api_version=AZURE_API_VERSION)
response = Azure_client.chat.completions.create(
    model="gpt-4o-mini",
    messages = [{
        "role":"user","content":"what is python"
    }]
)
print(response)