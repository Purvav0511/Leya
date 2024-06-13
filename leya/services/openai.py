import os
import requests
import json

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
OPENAI_EMBEDDING_MODEL = 'text-embedding-ada-002'
CHATGPT_MODEL = 'gpt-3.5-turbo'

def get_embedding(chunk):
    url = 'https://api.openai.com/v1/embeddings'
    headers = {
      'content-type': 'application/json; charset=utf-8',
      'Authorization': f"Bearer {OPENAI_API_KEY}"
    }
    data = {
      'model': OPENAI_EMBEDDING_MODEL,
      'input': chunk
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_json = response.json()

    embedding = response_json["data"][0]["embedding"]
    return embedding

def get_llm_answer(prompt):
    """ Queries OpenAI's language model to generate an answer based on the given prompt. """
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {OPENAI_API_KEY}"
    }
    data = {
        'model': CHATGPT_MODEL,
        'messages': [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}],
        'temperature': 0.5,  # Adjust as needed for creativity
        'max_tokens': 4000   # Adjust based on how long responses you need
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_json = response.json()
    completion = response_json["choices"][0]["message"]["content"]

    return completion