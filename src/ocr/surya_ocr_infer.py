from surya.foundation import FoundationPredictor
from surya.recognition import RecognitionPredictor
from surya.detection import DetectionPredictor
from pathlib import Path
from PIL import Image

class SuryaOCR:
    """Class to Handle Surya OCR Outputs"""
    def __init__(self, foundation_predictor: FoundationPredictor):
        self.foundation_predictor = foundation_predictor
        self.recognition_predictor = RecognitionPredictor(foundation_predictor)
        self.detection_predictor = DetectionPredictor()

        self.img_paths = []
        self.img_ocr_result_dict = {}
    
    def post_processor(self, ocr_result):
        """Post Process OCR Result to get flattend string"""
        ocr_str_flattened = ""
        special_style_tags = ["br","<u>", "</u>", "<b>", "</b>", "<i>", "</i>"]
        replacement_strings = [" ","", "", "", "", "", ""]  
        style_replacements = dict(zip(special_style_tags, replacement_strings))

        for text_line in ocr_result.text_lines:
            ## replace line break <br> with space
            text = text_line.text.replace("<br>", " ")
            for style, str_replace in style_replacements.items():
                ## replace special style tags with empty string
                text = text.replace(style, str_replace)
            ocr_str_flattened += text + " "
        
        return ocr_str_flattened.strip()
  
    def predict(self, images_list: list[Image], max_tokens=1024):
        ocr_result_obj = self.recognition_predictor(images_list, 
                                                    det_predictor=self.detection_predictor, 
                                                    max_tokens=max_tokens,
                                                    recognition_batch_size=512,
                                                    detection_batch_size=36)
        return ocr_result_obj
    
    def post_process(self, ocr_result_obj: list):
        """Post Process results to remove html tags"""
        results_flattened = []
        for ocr_result in ocr_result_obj:
            results_flattened.append(self.post_processor(ocr_result))
        return results_flattened