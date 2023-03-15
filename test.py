import openai

# Set up the OpenAI API client
openai.api_key = "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"

# Set up the model and prompt
model_engine = "text-davinci-003"
prompt = "steps tocreate portfolio website"

# Generate a response
completion = openai.Completion.create(
    engine=model_engine,
    prompt=prompt,
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.5,
)

response = completion.choices[0].text
print(response)