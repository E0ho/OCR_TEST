import requests
import os

def call_azure_openai(prompt: str, category: str) -> str:
    """
    Azure OpenAI GPT 모델을 호출하여 입력된 프롬프트에 대한 응답을 반환합니다.
    """
    # Azure OpenAI 설정
    url = "https://bbcho-m4qo41ze-eastus2.cognitiveservices.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview"
    azure_api_key = os.environ.get("azure_api_key")

    # 헤더 설정
    headers = {
        "Content-Type": "application/json",
        "api-key": azure_api_key
    }

    target = ''
    if category == '전자지급 보증서':
        target = "{ 보증인: , 보증 금액: , 보증 기간 (시작일): , 보증 기간 (기한일): , 채무자: , 보증서 발급 일자: }"
    
    elif category == '물품대금 보증보험':
        target = "{ 보험 계약자: , 보험 가입 금액: , 보험 기간 (시작일): , 보험 기간 (기한일): , 증권 발급 지점: , 증권 발급 일자: , 증권 발급 기업: }"
    
    elif category == '신용 보증서 (변경)':
        target = "{ 채권자: , 피보증인(기업체) : , 피보증인(대표자) : , 보증 내용 일자 : , 변경된 보증 기한 : , 금액 :  , 발급일 : }"
    else:
        target = "{ 보증처 : , 채무자: ,  보증금 : , 보증 기일 (기한일) :  , 발급일 : }"
    
    prompt = "참조 문장 : " + prompt + "\n" + "타겟 : " + target + "\n" + "타겟의 각 Key에 해당하는 값을 참조 문장에서 찾아서 정재해 (target만 리턴, 다른 말 X)"


    # 요청 데이터
    payload = {
        "messages": [
            # {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.0,
        "top_p" : 0.05,
        "max_tokens": 200
    }

    try:
        # API 호출
        response = requests.post(url, headers=headers, json=payload, verify=False)

        # 응답 처리
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            return f"Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":

    # 테스트용 프롬프트
    user_prompt = "Explain the benefits of using Azure OpenAI."

    # Azure OpenAI API 호출
    response = call_azure_openai(user_prompt)
    print("Azure OpenAI 응답:", response)
