import requests
import os

def analyze_text(prompt: str, category: str) -> str:

    # OpenAI API 정보
    gpt_api_key = os.environ.get("gpt_api_key")
    url = "https://api.openai.com/v1/chat/completions"

    target = ''
    if category == '전자지급 보증서':
        target = "{ 보증인: / 보증 금액: / 보증 기간 (시작일): / 보증 기간 (기한일): / 채무자: / 보증서 발급 일자: }"
    
    elif category == '물품대금 보증보험':
        target = "{ 보험 계약자: / 보험 가입 금액: / 보험 기간 (시작일): / 보험 기간 (기한일): / 증권 발급 지점: / 증권 발급 일자: / 증권 발급 기업: }"
    
    elif category == '신용 보증서 (변경)':
        target = "{ 채권자: / 피보증인(기업체) : / 피보증인(대표자) : / 보증 내용 일자 : / 변경된 보증 기한 : / 금액 :  / 발급일 : }"
    else:
        target = "{ 보증처 : / 채무자: /  보증금 : / 보증 기일 (기한일) :  / 발급일 : }"

    prompt = "참조 문장 : " + prompt + "\n" + "타겟 : " + target + "\n" + "타겟의 각 Key에 해당하는 값을 참조 문장에서 찾아서 정재해 (target만 리턴, 다른 말 X)"

    # 요청 데이터
    data = {
        "model": "gpt-4o",
        "messages": [
            {"role": "user", "content": prompt}
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