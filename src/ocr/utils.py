import json
from pathlib import Path
import pandas as pd

def read_json(path: str) -> dict:
    """Reads JSON and properly decodes Indic text"""
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        if 'header' in data:
            data['header'] = data['header'].encode('utf-8').decode('utf-8')
        if 'full_text' in data:
            data['full_text'] = data['full_text'].encode('utf-8').decode('utf-8')
        return data

def get_ocr_results_df(image_paths, results):
    """Convert OCR results to DataFrame"""
    ocr_results_list_dict = []
    for idx, img_path in enumerate(image_paths):
        degradation_level = img_path.parent.name
        gt_file_name = img_path.name.split("_n_pages_")[0]
        ocr_results_list_dict.append({
            "file_id": gt_file_name, 
            "degradation_level": degradation_level.split("_")[0][0].upper() + "_" + degradation_level.split("_")[1],
            "ocr_output_raw": results[idx].text.replace("\n", " ")
        })

    df_result = pd.DataFrame(ocr_results_list_dict)
    pivoted_df = df_result.pivot(
        index='file_id',
        columns='degradation_level', 
        values='ocr_output_raw'
    ).reset_index()

    pivoted_df.columns.name = None
    renamed_columns = {
        col: f'ocr_output_{col}' if col != 'file_id' else col 
        for col in pivoted_df.columns
    }
    return pivoted_df.rename(columns=renamed_columns)