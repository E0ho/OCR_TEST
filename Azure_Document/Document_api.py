import requests
import time
from Azure_Document.Operation_location import fetch_text
import os

def document_intelligence(file_path):
    """
    Azure Form Recognizer API를 사용하여 문서에서 텍스트를 추출합니다.
    """
    # Azure API 설정
    endpoint = "https://wrnt-ocr.cognitiveservices.azure.com/"
    api_version = "2023-07-31"
    url = f"{endpoint}/formrecognizer/documentModels/prebuilt-read:analyze?api-version={api_version}"
    di_api_key = os.environ.get("di_api_key")
    
    # 헤더 설정
    headers = {
        "Content-Type": "application/octet-stream",
        "Ocp-Apim-Subscription-Key": di_api_key,
    }

    # 파일 업로드 및 API 호출
    with open(file_path, "rb") as f:
        response = requests.post(url, headers=headers, data=f, verify=False)

        # 요청 성공: 비동기 작업 URL 반환
        if response.status_code == 202:
            operation_location_url = response.headers["Operation-Location"] 
        else:
            # 오류 응답 반환
            return {"error": response.status_code, "error_message": response.text}

    # 결과 대기 및 가져오기
    for _ in range(3):
        time.sleep(5)  # 대기

        try:
            # 처리 완료: 텍스트 결과 반환
            text = fetch_text(operation_location_url, di_api_key)
            return text
        except Exception:
            pass  # 처리 중 예외 발생 시 계속 대기

    # 처리 지연 오류 반환
    return {"error": "PDF 파일 처리가 오래 걸립니다 (너무 무거움)"}



if __name__ == "__main__":
    # 테스트용 파일 경로
    test_file_path = "uploads/first_page.pdf"

    # 문서 분석 호출
    result = document_intelligence(test_file_path)

    # 결과 출력
    print("분석 결과:", result)
