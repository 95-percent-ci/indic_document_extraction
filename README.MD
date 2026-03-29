# Indic Document Extraction

This project contains scripts for document extraction in Indic languages, including synthetic data generation, image augmentation, OCR processing with multiple engines, and post-OCR correction.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/95-percent-ci/indic_document_extraction.git
   cd indic_document_extraction
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install system dependencies**:
   - For Tesseract OCR: Install Tesseract on your system (e.g., `brew install tesseract` on macOS, `apt install tesseract-ocr` on Ubuntu).
   - Ensure you have Python 3.8+ installed.

4. **Set up environment variables**:
   - Create a `.env` file in the root directory.
   - Add necessary API keys and credentials (e.g., for Google Document AI, Google Cloud credentials).

## Usage

Run the main scripts in the following order for a complete pipeline:

1. **Generate synthetic PDFs**:
   ```bash
   python 01. main_pdf_gen.py --code hi
   ```
   Replace `hi` with your desired language code (e.g., `bn` for Bengali, `ta` for Tamil).

2. **Augment images**:
   ```bash
   python 02. main_img_augment.py --language hindi
   ```
   This converts PDFs to images and adds noise at different degradation levels.

3. **Run OCR with different engines**:
   - Google Document AI: `python 03. main_google_ocr.py --language hindi`
   - Surya OCR: `python 04. main_surya_ocr.py --language hindi`
   - Tesseract: `python 05. main_tessarct_ocr.py --language hindi`

4. **Post-OCR correction**:
   ```bash
   python 06. main_post_ocr.py --language hindi --model google/gemma-3-1b-it
   ```
   Replace the model with available options like `sarvamai/sarvam-1b` or `meta/llama-3.2`.

## Project Structure

- `01. main_pdf_gen.py` to `06. main_post_ocr.py`: Main execution scripts.
- `fonts/`: Font files for different Indic scripts.
- `notebooks/`: Jupyter notebooks for evaluation, data generation, and experiments.
- `pdf_samples/`: Sample PDF files.
- `raw_data/`: Raw data including Indic language samples.
- `results/`: Output results from OCR processing.
- `sample_images/`: Sample images for testing.
- `requirements.txt`: Python dependencies.
- `src/`: Source code modules for data generation, OCR, evaluation, etc.

## Main Files

- **01. main_pdf_gen.py**: Generates synthetic PDFs for Indic languages using specified language codes.
- **02. main_img_augment.py**: Converts PDFs to images and adds various levels of noise/degradation to create augmented image datasets.
- **03. main_google_ocr.py**: Performs OCR on images using Google Document AI for Indic languages.
- **04. main_surya_ocr.py**: Performs OCR on images using Surya OCR for Indic languages.
- **05. main_tessarct_ocr.py**: Performs OCR on images using Tesseract for Indic languages, with multiprocessing.
- **06. main_post_ocr.py**: Applies post-OCR correction using LLMs and computes evaluation metrics like CER and WER.
