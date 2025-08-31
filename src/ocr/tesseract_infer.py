import tesserocr
from PIL import Image
import os

class TesseractOCR():
    """Class to Handle Tessaract OCR Outputs"""
    # language name to tessarct model code map #
    name_map = {"assamese": "asm", "bengali": "ben", "english": "eng", "gujarati": "guj",
                "hindi": "hin", "kannada": "kan", "nepali": "nep", "marathi": "mar","malayalam": "mal","manipuri": "mni",
                "oriya": "ori", "punjabi": "pan","sanskrit": "san", "sindhi": "snd", "santali": "sat",
                "tamil": "tam", "telugu": "tel", "urdu": "urd"}
    
    def __init__(self, language_name: str):
        lang_id = self.name_map.get(language_name)
        self.tesseract_model = tesserocr.PyTessBaseAPI(path=os.getenv('TESSDATA_PREFIX') , lang=lang_id)

    def _read_image(self, img_path: str) -> bytes:
        """Read image file and return bytes content"""
        return Image.open(img_path)

    def perform_ocr(self, img_path: str):
        """Perform OCR using PyTesseract Engine"""
        img_data = self._read_image(img_path)
        self.tesseract_model.SetImage(img_data)
        ocred_text = self.tesseract_model.GetUTF8Text()
        return  ocred_text
    
def ocr_worker(img_path_lang_tuple):
    """
    A wrapper function to perform OCR on a single image.
    This is the function that the multiprocessing Pool will call.
    """
    img_path, language = img_path_lang_tuple
    # The TesseractOCR object is created within the worker process
    tesseract_obj = TesseractOCR(language_name=language)
    ocred_text = tesseract_obj.perform_ocr(img_path=img_path)
    return ocred_text

