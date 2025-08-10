import warnings
warnings.filterwarnings("ignore", category=UserWarning)
from pathlib import Path
import pandas as pd
import os
import argparse
from src.data_generation.pdf_generation import GeneratePDF

def parse_args():
    parser = argparse.ArgumentParser(description='Generate Synthetic PDF for Indic Languages')
    parser.add_argument('--code', type=str, default='hn',
                      help='Language code to generate (default: hn)')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    _FONTS_FOLDER_ = Path("fonts/")
    _SYTN_FOLDER_ = Path("synth_data/")
    langcode = args.code

    _N_SAMPLES_ = 30
    _N_WORDS_ = 300
    _PDF_FOLDER_ = "pdfs"
    _GT_FOLDER_ = "gt"

    ## lang_code_interested ##
    lang_codes = ["as", "bn", "en", "gu", "hi", "kn", "gom", "ne", "pa", "sa", "sd", "ta", "te"]
    writing_system = ["Bengali", "Bengali", "Latin", "Gujarati" ,"Devanagari", "Kannada", "Devanagari", "Devanagari", "Gurmukhi", "Devanagari",  "Arabic", "tamil", "telugu"]
    lang_script = dict(zip(lang_codes, writing_system))

    language_dict = {'as': 'assamese','bn': 'bengali','brx': 'bodo','doi': 'dogri','en': 'english','gu': 'gujarati','hi': 'hindi','kn': 'kannada',
                     'ks': 'kashmiri','gom': 'konkani','mai': 'maithili','ml': 'malayalam','mni': 'manipuri','mr': 'marathi','ne': 'nepali',
                     'or': 'odia','pa': 'punjabi','sa': 'sanskrit','sat': 'santali','sd': 'sindhi','ta': 'tamil','te': 'telugu','ur': 'urdu'}

    _LANGUAGE_ = language_dict[langcode]
    script = lang_script[langcode]
    lang_data_folder = os.path.join(_SYTN_FOLDER_, _LANGUAGE_)
    lang_pdf_folder = os.path.join(lang_data_folder, _PDF_FOLDER_)
    lang_gt_folder = os.path.join(lang_data_folder, _GT_FOLDER_)

    if not os.path.exists(lang_data_folder):
        os.makedirs(lang_data_folder)
    if not os.path.exists(lang_pdf_folder):
        os.makedirs(lang_pdf_folder)
    if not os.path.exists(lang_gt_folder):
        os.makedirs(lang_gt_folder)

    
    ## reading ground truth source
    _PATH_WIKI_SAMPLE = Path("raw_data/sample_wiki/combined_languages.parquet")
    df_wiki_sample = pd.read_parquet(_PATH_WIKI_SAMPLE)

    ## getiing lang code and word length
    df_wiki_sample['lang_code'] = df_wiki_sample['source_file'].apply(lambda x: x.split('.')[0])
    df_wiki_sample['word_length'] = df_wiki_sample['text'].apply(lambda x: len(x.split()))
    df_wiki_sample = df_wiki_sample[df_wiki_sample['word_length'] > 30]
    wiki_df = df_wiki_sample.loc[df_wiki_sample['lang_code'] == langcode].sort_values(by='word_length', ascending=False).head(_N_SAMPLES_).reset_index()


    for i, row in wiki_df.iterrows():
        text_hn = " ".join(wiki_df.iloc[i]['text'].split(" ")[0:_N_WORDS_])
        generator_obj = GeneratePDF(language=_LANGUAGE_, fonts_folder=_FONTS_FOLDER_)
        generator_obj.generate_pdf(text=text_hn, writing_system=script)
        generator_obj.write_pdf(lang_pdf_folder, file_idx=i+1)
        generator_obj.write_text(lang_gt_folder, file_idx=i+1)
