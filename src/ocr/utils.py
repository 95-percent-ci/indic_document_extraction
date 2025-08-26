import json
from pathlib import Path
import pandas as pd
from PIL import Image


def read_json(path: str) -> dict:
    """Reads JSON and properly decodes Indic text"""
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data
    
def get_single_page_doc_name(path_pdf_images: list[Path]) -> list[str]:
    """Get names of document which have multiple pages. This helps in handling these files in downstream"""    
    # dictionary to store, file_name and it counts as they appear in image files. count >1 indicate, pdf contains 2 files
    file_name_img_counts = {} 
    path_pdf_img_single_pg = []
    for image_fp in path_pdf_images:
        image_fn = image_fp.name.split(".")[0]
        file_name, pdf_page_count = image_fn.split("_n_pages_")[0], int(image_fn.split("_n_pages_")[-1].split("_")[0])
        file_name_img_counts[file_name] = pdf_page_count
        if pdf_page_count == 1:
            path_pdf_img_single_pg.append(image_fp)

    return file_name_img_counts , path_pdf_img_single_pg

def get_single_page_gt_jsons(path_gt_jsons: list[Path], fn_page_count: dict[str, int]) -> list[Path]:
    """Gets GT Json file path for documents contained in 1 page"""
    
    fn_counts_single_page = [key for key, value in fn_page_count.items() if value == 1]
    path_gt_single_pg = []
    for gt_json_path in path_gt_jsons:
        gt_file_name = gt_json_path.name.split(".")[0]
        if gt_file_name in fn_counts_single_page:
            path_gt_single_pg.append(gt_json_path)
    return path_gt_single_pg

def get_ocr_results_df(image_paths, results):
    """Convert OCR results to DataFrame"""
    ocr_results_list_dict = []
    for idx, img_path in enumerate(image_paths):
        degradation_level = img_path.parent.name
        gt_file_name = img_path.name.split("_n_pages_")[0]
        ocr_output_raw = results[idx].replace("\n", " ")
        ocr_results_list_dict.append({
            "file_id": gt_file_name, 
            "degradation_level": degradation_level.split("_")[0][0].upper() + "_" + degradation_level.split("_")[1],
            "ocr_output_raw": ocr_output_raw
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

def read_image(image_path: Path) -> Image.Image:
        """Read image from a path. If Resize is True, it sets width to 2048 and adjusts height to maintain aspect ratio."""
        if isinstance(image_path, str):
                image_path = Path(image_path)
        if not image_path.exists():
            raise FileNotFoundError(f"Image file {image_path} does not exist.")
        img_load = Image.open(image_path)
        return img_load
