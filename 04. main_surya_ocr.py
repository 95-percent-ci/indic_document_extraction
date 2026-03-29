from src.ocr.surya_ocr_infer import SuryaOCR
from surya.foundation import FoundationPredictor
from src.ocr.utils import read_image, get_single_page_gt_jsons, get_single_page_doc_name, get_ocr_results_df, read_json
from src.evaluation.metrics import cer, wer
from pathlib import Path
import argparse
import pandas as pd
import os

def parse_args():
    parser = argparse.ArgumentParser(description='Process OCR for Indic languages using Surya OCR')
    parser.add_argument('--language', type=str, default='hindi',
                      help='Language to process (default: hindi)')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    # Initialize paths
    _PATH_SYNTH_DATA_ = Path("synth_data")
    _LANG_ = args.language
    _PATH_IMAGES_LANG_ = _PATH_SYNTH_DATA_.joinpath(_LANG_)
    
    _PATH_IMAGES_LIST_PNG_ = list(_PATH_IMAGES_LANG_.glob("images/*/*.png"))
    _PATH_JSON_LIST_GT_ = list(_PATH_IMAGES_LANG_.glob("gt/*.json"))

    _PATH_RESULTS_ = Path("results")
    _PATH_SERVICE_ = Path("surya_ocr")
    _PATH_RESULTS_LANGUAGE = _PATH_RESULTS_.joinpath(_PATH_SERVICE_).joinpath(_LANG_)

    if not os.path.exists(_PATH_RESULTS_LANGUAGE): os.makedirs(_PATH_RESULTS_LANGUAGE)
    # Get pdf images corresponding to single page
    fn_counts, path_images_single_pg = get_single_page_doc_name(_PATH_IMAGES_LIST_PNG_)
    path_gt_single_pg = get_single_page_gt_jsons(_PATH_JSON_LIST_GT_, fn_counts)

    _N_TRAILS_ = 2  ## for testing purpose, set to 2. For full eval, set to len(path_images_single_pg)
    path_images_single_pg = path_images_single_pg[0:_N_TRAILS_]
    path_gt_single_pg = path_gt_single_pg[0:_N_TRAILS_]

    ## reading images
    image_data_list = [read_image(img_path, resize=True) for img_path in path_images_single_pg]

    ## Initialize Surya OCR
    surya_ocr_obj = SuryaOCR(FoundationPredictor())
    predictions = surya_ocr_obj.predict(images_list=image_data_list, max_tokens=1024)
    predctions_flattened = surya_ocr_obj.post_process(predictions)

    ## creatig sample results df
    ocr_res_df = get_ocr_results_df(path_images_single_pg, predctions_flattened)
    ocr_res_df.to_clipboard(index=False)

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
    gt_df_ocr.to_csv(_PATH_RESULTS_LANGUAGE.joinpath("results.csv"), index=False)
