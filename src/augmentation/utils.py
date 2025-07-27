import os
import fitz

def pdf_to_images(pdf_path, doc_id, output_dir):
    """
    Converts each page of a PDF to individual image file(png format)
    """
    pdf_document = fitz.open(pdf_path)

    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap(dpi = 300)
        image_path = os.path.join(output_dir, f"{doc_id}_{str(page_num + 1)}.png")
        pix.save(image_path)
    pdf_document.close()