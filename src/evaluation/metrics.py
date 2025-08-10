import jiwer

def calculate_error_rates(ground_truth: str, ocr_text: str):
    """Calculate Character and Word Error Rates"""
    char_metrics = jiwer.process_characters(ground_truth, ocr_text)
    word_metrics = jiwer.process_words(ground_truth, ocr_text)
    
    return {
        'cer': char_metrics.cer,
        'wer': word_metrics.wer,
        'char_alignment': jiwer.visualize_alignment(char_metrics),
        'word_alignment': jiwer.visualize_alignment(word_metrics)
    }

def cer(ground_truth: str, ocr_text: str):
    """Calculate Character and Word Error Rates"""
    char_metrics = jiwer.process_characters(ground_truth, ocr_text)
    return char_metrics.cer

def wer(ground_truth: str, ocr_text: str):
    """Calculate Character and Word Error Rates"""
    word_metrics = jiwer.process_words(ground_truth, ocr_text)
    return word_metrics.wer



