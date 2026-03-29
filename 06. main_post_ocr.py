import pandas as pd
from pathlib import Path
from indicnlp.normalize.indic_normalize import IndicNormalizerFactory

from src.evaluation.metrics import cer, wer
from src.common.utils import normalize_text, get_samples_high_err
from src.post_ocr_corr.prompts import OCR_CORRECTOR_PROMPT_TEMPLATE_1, OCR_CORRECTOR_PROMPT_TEMPLATE_2
from src.post_ocr_corr.post_ocr_inference import postCorrectorLLM
import argparse
import os
import tqdm

def parse_args():
    parser = argparse.ArgumentParser(description='Perform ICL Post Correction using LLMs')
    parser.add_argument('--language', type=str, default='hindi',
                      help='Surya OCR Language results to do POST OCR Correction')
    parser.add_argument('--model', type=str, default='google/gemma-3-1b-it',
                      help='LLM to do post OCR. Other models like sarvamai/sarvam-1b, meta/llama-3.2')
    return parser.parse_args()

def add_err_to_table(results_df: pd.DataFrame) -> pd.DataFrame:
    """Adds CER and WER to result table

    :param results_df: Table containing GT and OCR Output
    :type results_df: pd.DataFrame
    """
    # computing cer & wer
    results_df = results_df.copy()
    gt_col = 'ground_truth'
    ocr_output_cols = ['ocr_output_L_0', 'ocr_output_L_1', 'ocr_output_L_2', 'ocr_output_L_3']
    cols_create_cer = ['cer_l0', 'cer_l1', 'cer_l2', 'cer_l3']
    cols_create_wer = ['wer_l0', 'wer_l1', 'wer_l2', 'wer_l3']
    
    for ocr_output_lvl, col_crt_cer in dict(zip(ocr_output_cols, cols_create_cer)).items():
        results_df[col_crt_cer] = results_df[[gt_col, ocr_output_lvl]].apply(lambda x: cer(x[gt_col], x[ocr_output_lvl]), axis=1)
    for ocr_output_lvl, col_crt_wer in dict(zip(ocr_output_cols, cols_create_wer)).items():
        results_df[col_crt_wer] = results_df[[gt_col, ocr_output_lvl]].apply(lambda x: wer(x[gt_col], x[ocr_output_lvl]), axis=1)

    col_ord = ['file_id' ,'ground_truth', 'ocr_output_L_0', 'ocr_output_L_1',
               'ocr_output_L_2', 'ocr_output_L_3', 'cer_l0', 'cer_l1', 'cer_l2',
               'cer_l3', 'wer_l0', 'wer_l1', 'wer_l2', 'wer_l3' ]
    
    results_df = results_df[col_ord]
    ## upper casing column names
    results_df.columns = results_df.columns.str.upper()
    
    return results_df


if __name__ == "__main__":
    args = parse_args()
    
    # Initialize paths
    _PATH_RESULTS_SURYA = Path("results/surya_ocr")
    _LANG_ = args.language
    model_id = args.model
    _RESULT_FL_NAME_ = "results.csv"
    _PATH_RESULT_LANG_ = _PATH_RESULTS_SURYA.joinpath(_LANG_).joinpath(_RESULT_FL_NAME_)
    
    # load_results #
    results_lang = pd.read_csv(_PATH_RESULT_LANG_)

    # normalize strings
    norm_factory = IndicNormalizerFactory()
    cols_to_norm = ['ground_truth', 'ocr_output_L_0', 'ocr_output_L_1', 'ocr_output_L_2', 'ocr_output_L_3']
    for col in cols_to_norm:
        results_lang[col] = results_lang.apply(lambda x: normalize_text(x[col], _LANG_, norm_factory), axis=1)

    # adding cer and wer cols
    results_lang = add_err_to_table(results_df=results_lang)
    
    ## Getting Samples with error rates >= 0.1
    results_high_err = get_samples_high_err(results_lang, threshold=0.1).reset_index()

    ## Initialsing LLM 
    post_ocr_llm = postCorrectorLLM(model_id=model_id)
    GenerationConfig = {"top_p": 0.9, "temperature": 0.0, "do_sample": False}
    resp_list = []

    for i in tqdm.tqdm(range(len(results_high_err))):
        row = results_high_err.iloc[i]
        OCR_OUTPUT = row['OCR_OUTPUT']
        CONTEXT = OCR_CORRECTOR_PROMPT_TEMPLATE_2.replace("{ocr_output}", OCR_OUTPUT)
        resp_list.append(post_ocr_llm(CONTEXT , kwargs=GenerationConfig))

    results_high_err['POST_OCR'] = resp_list
    # writing results
    _PATH_RESULTS_WRITE_ = Path("post_ocr_results/surya_ocr").joinpath(_LANG_).joinpath(model_id.split("/")[-1])
    if not os.path.exists(_PATH_RESULTS_WRITE_): os.makedirs(_PATH_RESULTS_WRITE_)
    results_high_err.to_csv(_PATH_RESULTS_WRITE_.joinpath("results_threshold_0.1_template_2.csv"), index=False)