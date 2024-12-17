import os
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image

def save_uploaded_file(file, upload_dir="uploads", output_file_name="first_page"):
    """
    업로드된 파일을 저장하고, PDF의 첫 페이지 또는 이미지를 저장합니다.

    Args:
        file: 업로드된 파일 객체 (PDF 또는 이미지).
        upload_dir (str): 저장 디렉토리.
        output_file_name (str): 출력 파일 이름(확장자는 자동 추가).
    
    Returns:
        str: 저장된 파일 경로.
    """
    # 저장 경로 생성
    os.makedirs(upload_dir, exist_ok=True)
    
    # 파일 확장자 확인
    file_extension = os.path.splitext(file.filename)[-1].lower()
    file_path = os.path.join(upload_dir, f"{output_file_name}{file_extension}")
    
    # PDF 파일 처리
    if file_extension == ".pdf":
        reader = PdfReader(file.file)  # UploadFile 객체를 바로 읽음
        writer = PdfWriter()
        
        # 첫 페이지 추출
        writer.add_page(reader.pages[0])
        
        # PDF 저장
        with open(file_path, "wb") as output_file:
            writer.write(output_file)
    
    # 이미지 파일 처리
    elif file_extension in [".jpg", ".jpeg", ".png"]:
        image = Image.open(file.file)
        
        # 이미지를 첫 페이지만 저장 (여기서는 단일 이미지만 저장)
        image.save(file_path)
    
    else:
        raise ValueError("지원하지 않는 파일 형식입니다. PDF 또는 이미지 파일만 업로드하세요.")
    
    return file_path
