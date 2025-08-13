from PIL import Image
from pathlib import Path
import pandas as pd
import os
from dotenv import load_dotenv, find_dotenv
from src.ocr.utils import read_json, get_ocr_results_df, get_single_page_doc_name, get_single_page_gt_jsons
from src.evaluation.metrics import cer, wer
from src.ocr.tesseract_infer import TesseractOCR, ocr_worker
import argparse
import tqdm
from multiprocessing import Pool, cpu_count

load_dotenv()
def parse_args():
    parser = argparse.ArgumentParser(description='Process OCR for Indic languages using tesseract')
    parser.add_argument('--language', type=str, default='hindi',
                      help='Language to process (default: hindi)')
    return parser.parse_args()


def main():
    args = parse_args()
    # Initialize paths
    _PATH_SYNTH_DATA_ = Path("synth_data")
    _LANG_ = args.language
    _PATH_IMAGES_LANG_ = _PATH_SYNTH_DATA_.joinpath(_LANG_)
    
    _PATH_IMAGES_LIST_PNG_ = list(_PATH_IMAGES_LANG_.glob("images/*/*.png"))
    _PATH_JSON_LIST_GT_ = list(_PATH_IMAGES_LANG_.glob("gt/*.json"))

    _PATH_RESULTS_ = Path("results")
    _PATH_SERVICE_ = Path("tesseract")
    _PATH_RESULTS_LANGUAGE = _PATH_RESULTS_.joinpath(_PATH_SERVICE_).joinpath(_LANG_)

    if not os.path.exists(_PATH_RESULTS_LANGUAGE): os.makedirs(_PATH_RESULTS_LANGUAGE)

    # Get pdf images corresponding to single page
    fn_counts, path_images_single_pg = get_single_page_doc_name(_PATH_IMAGES_LIST_PNG_)
    path_gt_single_pg = get_single_page_gt_jsons(_PATH_JSON_LIST_GT_, fn_counts)    

    tasks = [(img_path, _LANG_) for img_path in path_images_single_pg]

    with Pool(cpu_count()) as p:
        # Use imap to apply the ocr_worker to each task.
        # tqdm is used to display a progress bar.
        results = list(tqdm.tqdm(p.imap(ocr_worker, tasks), total=len(path_images_single_pg)))

    ocr_res_df = get_ocr_results_df(path_images_single_pg, results)

    # Process ground truth
    file_id_gt_dict = []
    for file_gt in path_gt_single_pg:
        file_nm = file_gt.name.split(".")[0]
        gt_json = read_json(file_gt)
        file_id_gt_dict.append({
            "file_id": file_nm, 
            "ground_truth": (gt_json['header'] + "\n" + gt_json['full_text']).replace("\n", " ")
        })
    
    gt_df = pd.DataFrame(file_id_gt_dict)

    # joining results with actual
    gt_df_ocr = pd.merge(gt_df, ocr_res_df, on='file_id')

    # computing cer & wer
    gt_col = 'ground_truth'
    ocr_output_cols = ['ocr_output_L_0', 'ocr_output_L_1', 'ocr_output_L_2', 'ocr_output_L_3']
    cols_create_cer = ['cer_l0', 'cer_l1', 'cer_l2', 'cer_l3']
    cols_create_wer = ['wer_l0', 'wer_l1', 'wer_l2', 'wer_l3']

    for ocr_output_lvl, col_crt_cer in dict(zip(ocr_output_cols, cols_create_cer)).items():
        gt_df_ocr[col_crt_cer] = gt_df_ocr[[gt_col, ocr_output_lvl]].apply(lambda x: cer(x[gt_col], x[ocr_output_lvl]), axis=1)

    for ocr_output_lvl, col_crt_wer in dict(zip(ocr_output_cols, cols_create_wer)).items():
        gt_df_ocr[col_crt_wer] = gt_df_ocr[[gt_col, ocr_output_lvl]].apply(lambda x: wer(x[gt_col], x[ocr_output_lvl]), axis=1)

    # writing results
    gt_df_ocr.to_csv(_PATH_RESULTS_LANGUAGE.joinpath("results.csv"), index=False)

if __name__ == "__main__":
    main() 