from pathlib import Path
import sys
import os
import argparse

from src.augmentation.noise_addition import ImageNoiseAddition
from src.augmentation.utils import pdf_to_images

def parse_args():
    parser = argparse.ArgumentParser(description="""Generate Images from PDF at various degradation levels. 
                                     Assumes language partioned pdf are present in synth data foler as ROOT_SYNTH/LANGUAGE/pdfs""")
    parser.add_argument('--language', type=str, default='hindi',
                        help='Language Code to Load PDF files')
    return parser.parse_args()

if __name__ == "__main__":
    ARGS = parse_args()
    ROOT_SYNTH_FOLDER = Path("synth_data/")
    PDF_FOLDER = Path("pdfs")
    LANGUAGE = ARGS.language
    FOLDER_LANG = ROOT_SYNTH_FOLDER.joinpath(Path(LANGUAGE)).joinpath(Path(PDF_FOLDER))

    QUALITY_LEVELS = ["level_0", "level_1", "level_2", "level_3"]
    IMG_FOLDER_NAME = "images"
    
    ## first, simple pdf to png conversion is done (level 0 is cleaned pdf image)
    PATH_FOLDER_LEVEL = ROOT_SYNTH_FOLDER.joinpath(Path(LANGUAGE)).joinpath(IMG_FOLDER_NAME)

    quality_level = QUALITY_LEVELS[0]
    PATH_FOLDER_QUALITY_0 = PATH_FOLDER_LEVEL.joinpath(quality_level)
    if not os.path.exists(PATH_FOLDER_QUALITY_0): 
        os.makedirs(PATH_FOLDER_QUALITY_0)

    ## fetching all pdf ifles
    pdf_files = list(FOLDER_LANG.glob("*.pdf"))

    for pdf_file in pdf_files:
        file_nm = pdf_file.name.split(".")[0]
        pdf_to_images(pdf_file, file_nm, PATH_FOLDER_QUALITY_0)

    
    ## Adding Noise To Images
    DEGRADATION_LEVELS = ["level_1", "level_2", "level_3"]
    DEGRADATION_IMPACT = ["low", "medium", "high"]
    level_degrad_dict = dict(zip(DEGRADATION_LEVELS, DEGRADATION_IMPACT))

    for level in DEGRADATION_LEVELS:
        IMG_FOLDER_QUALITY_LEVEL = os.path.join(PATH_FOLDER_QUALITY_0.parent, level)
        if not os.path.exists(IMG_FOLDER_QUALITY_LEVEL):
            os.makedirs(IMG_FOLDER_QUALITY_LEVEL)
        
        ## get list of clean images
    image_files = list(PATH_FOLDER_QUALITY_0.glob("*.png"))

    ## degrade it across each degraadtion level
    for img_path in image_files:
        for quality_level, deg_impact in level_degrad_dict.items():
            noise_adder = ImageNoiseAddition(img_path=img_path, degradation_level=deg_impact)
            _FOLDER_TO_SAVE_ = os.path.join(PATH_FOLDER_QUALITY_0.parent, quality_level)
            noise_adder.save_transformed_image(output_folder=_FOLDER_TO_SAVE_)    
    
    