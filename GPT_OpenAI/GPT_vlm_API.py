import requests
import os
from langchain.embeddings import OpenAIEmbeddings                       # Word Embedding
from langchain.vectorstores import Chroma                               # Vector DB (Chroma DB)



def analyze_text(prompt: str, category: str) -> str:

    # OpenAI API 정보
    gpt_api_key = os.environ.get("gpt_api_key")
    url = "https://api.openai.com/v1/chat/completions"

    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=gpt_api_key)
    database = Chroma(persist_directory="./vector_db", embedding_function = embeddings )

    # Chroma에서 filter와 query를 조합하여 검색
    target = database.similarity_search_with_score(
        filter = filter_conditions, 
        k = 3
    )

    prompt = "참조 문장 : " + prompt

    # 요청 데이터
    data = {
        "model": "gpt-4o",
        "messages": [
            {"role": "user", "content": prompt + target[0][0].page_content}
        ],
        "temperature": 0.0,
        "top_p" : 0.05
    }

    # 요청 헤더
    headers = {
        "Authorization": f"Bearer {gpt_api_key}",
        "Content-Type": "application/json"
    }

    # OpenAI API 호출
    try:
        print(prompt)
        response = requests.post(url, headers=headers, json=data, verify=False)

        # GPT 응답 반환
        gpt_response = response.json()
        print(gpt_response)
        # return gpt_response
        return gpt_response["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        # 오류 처리
        return f"Error calling GPT API: {e}"