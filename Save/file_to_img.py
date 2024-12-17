import os
from PIL import Image
import fitz  # PyMuPDF

def convert_pdf_to_image(pdf_path, output_dir="images", output_file_name="first_page.png"):

    # 저장 디렉토리 생성
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_file_name)

    # PDF 열기 및 첫 페이지 가져오기
    pdf_document = fitz.open(pdf_path)
    first_page = pdf_document[0]

    # 첫 페이지를 Pixmap으로 변환
    pix = first_page.get_pixmap(dpi=600)  # 해상도 설정
    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    # 이미지를 PNG로 저장
    image.save(output_path, "PNG")

    # PDF 닫기
    pdf_document.close()

    return output_path
