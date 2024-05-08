# Assume openai>=1.0.0
from openai import OpenAI

# Create an OpenAI client with your deepinfra token and endpoint
openai = OpenAI(
    api_key="CSkQPUjHWOykiIvLHMfmfwUFv9tYE2aN",
    base_url="https://api.deepinfra.com/v1/openai",
)

chat_completion = openai.chat.completions.create(
    model = "mistralai/Mistral-7B-Instruct-v0.2",
    # model="mistralai/Mixtral-8x22B-Instruct-v0.1",
    # model="google/gemma-1.1-7b-it",
    # model="cognitivecomputations/dolphin-2.6-mixtral-8x7b",
    messages=[
        {
            "role": "system",
            "content": "You are a Computer Scicene Engineer having completed a doctorate in Computer Vision and Machine Learning. You are not allowed to go beyond the topics of Computer Science, or subtopics in the scope of computer science. You have to provide only accurate and relevant information to the topic."
        },
        {
            "role": "user", 
            "content": "Write an article on the topic Databases' Data Modeling."
        }
    ],
)

print(chat_completion.choices[0].message.content)
