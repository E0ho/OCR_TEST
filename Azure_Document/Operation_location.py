import requests

def fetch_text(url: str, api_key: str) -> list:

    # Header 재정의
    headers = {
        "Ocp-Apim-Subscription-Key": api_key
    }

    # GET 요청
    response = requests.get(url, headers=headers, verify=False)

    # 응답 처리
    if response.status_code == 200:
        result = response.json()
        # return result
        text = result['analyzeResult']['content']
        
        # 텍스트 반환
        result = text.replace("\n", ",")
        print(result)
        return result
    
    else:
        # Error
        raise Exception(f"Error {response.status_code}: {response.text}")
