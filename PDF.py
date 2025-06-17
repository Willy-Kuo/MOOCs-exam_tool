import img2pdf

def createPDF(images: list[str], output_path: str):
    pdf_bytes = img2pdf.convert(images)
    with open(output_path, "wb") as f:
        f.write(pdf_bytes)