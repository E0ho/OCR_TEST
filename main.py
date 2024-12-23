from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from Save.save_pdf import save_uploaded_file
from Azure_Document.Document_api import document_intelligence   # Azure Document Intelligence       # Azure Computer Vision
# from GPT_OpenAI.GPT_vlm_API import analyze_text                 # GPT
from Azure_OpenAI.Azure_OpenAI import call_azure_openai
# from OpenAI.HuggingFace import analyze_text                   # GPT


app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # 모든 도메인 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# FineTuniSng
@app.post("/text_inference/")
async def pdf_analyze(file: UploadFile = File(...), category: str = Form(...)):

    # PDF 파일 저장
    file_path = save_uploaded_file(file)

    # Azure OCR 함수 호출
    result = document_intelligence(file_path)
    # return result
    print(result)
    # result = call_azure_openai(result, category)
    
    result = analyze_text(result, category)
    print(result)
    # print(result)

    return result


from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

templates = Jinja2Templates(directory="templates")
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    print('Request for index page received')
    return templates.TemplateResponse('index.html', {"request": request})


import os
import uvicorn

# if __name__ == "__main__":
#     # PORT 환경 변수를 사용
#     port = int(os.environ.get("PORT", 8000))
#     uvicorn.run(app, host="0.0.0.0", port=port)