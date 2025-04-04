from groq import Groq

client = Groq(api_key="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")

response = client.chat.completions.create(
    model="llama3-70b-8192",
    messages=[
        {"role": "user", "content": "type 'a'."}
    ]
)

# Print response
print(response.choices[0].message.content)

# Check token usage
print(f"Input tokens: {response.usage.prompt_tokens}")
print(f"Output tokens: {response.usage.completion_tokens}")
print(f"Total tokens: {response.usage.total_tokens}")