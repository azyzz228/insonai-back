from together import Together
from django.conf import settings


client = Together(api_key=settings.TOGETHER_KEY)


def client_speech_text_to_llm(messages):    
    response = client.chat.completions.create(
        model="NousResearch/Hermes-3-Llama-3.1-405B-Turbo",
        messages=messages,
        max_tokens=252,
        temperature=0.5,
        top_p=0.7,
        top_k=30,
        repetition_penalty=1.2,
        stop=["<|eot_id|>"],
        stream=False
    )
    return response.choices[0].message.content