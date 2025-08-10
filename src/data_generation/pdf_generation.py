import random
import warnings
from fpdf import FPDF
from fpdf.enums import Align
import json

class PDF(FPDF):
    """Custom PDF Class to manage headers, body & footers"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.header_text = ""
        self.footer_text = ""
        self.add_header_flag = False
        self.add_footer_flag = False
        self.font_name = None
        self.header_style = "B"

    def header(self):
        if self.add_header_flag:
            self.set_font(self.font_name, style=self.header_style, size=13)
            width = self.get_string_width(self.header_style) + 6
            self.set_x((210 - width) / 2)
            self.cell(width, 10, self.header_text, align="C", new_x="LMARGIN", new_y="NEXT")
            self.ln(10)

    def footer(self):
        if self.add_footer_flag:
            self.set_y(-15)
            self.cell(0, 10, self.footer_text, align="C", new_x="LMARGIN", new_y="NEXT")


class IndicPDFGenerator:
    """
    A utility class to generate multi-column, styled PDF documents in Indian languages using custom fonts.

    Attributes:
        font_name (str): The name of the font to use, must be present in font_file_map.
        font_size (int): Randomly chosen font size between 10 and 15.
        pdf (PDF): Instance of the custom PDF class for document creation.

    Methods:
        generate(text: str, output_filename: str):
            Generates a PDF from the given text and saves it to the specified filename.

    Internal Methods:
        _register_fonts():
            Registers the required fonts with the PDF instance based on font_name.

        _set_header_footer(text):
            Randomly sets header and footer text for the PDF, using phrases from the input text.

        _get_alignment():
            Randomly selects a text alignment (left, justify, center, right) for the document.

        _get_n_cols():
            Randomly decides the number of columns (1 or 2) for the document layout.

        _write_paragraphs(text, n_cols, doc_alignment_str):
            Writes the text into the PDF in paragraphs, with random styling and indentation.
    """
    def __init__(self, font_name: str, font_file_map: dict):
        self.font_name = font_name
        self.font_file_map = font_file_map
        self.font_size = random.randint(12, 15)
        self.pdf = PDF()
        self.pdf.font_name = self.font_name
        self._register_fonts()
        self.pdf.set_font(self.font_name, size=self.font_size)
        self.pdf.set_text_shaping(True)

    def _register_fonts(self):
        font_path_all = self.font_file_map.get(self.font_name)
        self.bold_avail = False
        self.italic_avail = False
        self.bold_italic_avail = False
        if isinstance(font_path_all, dict):
            font_path = font_path_all.get("normal", None)
            bold_font_path = font_path_all.get("B", None)
            italic_font_path = font_path_all.get("I", None)
            bold_italic_font_path = font_path_all.get("BI", None)
            self.pdf.add_font(self.font_name, "", font_path)
            if bold_font_path:
                self.pdf.add_font(self.font_name, "B", bold_font_path)
                self.bold_avail = True
            if italic_font_path:
                self.pdf.add_font(self.font_name, "I", italic_font_path)
                self.italic_avail = True
            if bold_italic_font_path:
                self.pdf.add_font(self.font_name, "BI", bold_italic_font_path)
                self.bold_italic_avail = True
        else:
            self.pdf.add_font(self.font_name, "", font_path_all)

    def _set_header_footer(self, text):
        # Header
        if random.random() < 1:
            self.pdf.add_header_flag = True
            if not self.bold_avail:
                self.pdf.header_style = ""
            self.pdf.header_text = " ".join(random.sample(text.split(), min(5, len(text.split()))))
        # Footer
        if random.random() < 0:
            self.pdf.add_footer_flag = True
            self.pdf.footer_text = " ".join(random.sample(text.split(), min(5, len(text.split()))))

    def _get_alignment(self):
        """ Gets a random alignment for the document text. """
        alignment_choices = [(Align.L, 0.65), (Align.J, 0.2), (Align.C, 0.1), (Align.R, 0.05)]
        alignments, probabilities = zip(*alignment_choices)
        doc_alignment_enum = random.choices(alignments, probabilities)[0]
        align_map = {Align.L: "left", Align.J: "justify", Align.C: "center", Align.R: "right"}
        return align_map[doc_alignment_enum]
    
    def _get_n_cols(self):
        """Randomly decide the number of columns for the text."""
        cols = 1
        if random.random() <+ 0: cols = 2
        return cols

    def _write_paragraphs(self, text, n_cols, doc_alignment_str):
        """Write the text into the PDF in paragraphs with random styling."""
        paragraphs = text.split("\n")
        with self.pdf.text_columns(ncols=n_cols) as cols:
            for para in paragraphs:
                if para.strip():
                    indent = self._get_random_indent()
                    with cols.paragraph(text_align=doc_alignment_str, first_line_indent=indent) as paragraph:
                        self._write_styled_words(paragraph, para)
                        paragraph.ln()
                        paragraph.ln()
    
    def _get_random_indent(self):
        """Randomly decide the first line indent for a paragraph."""
        return 15 if random.random() < 0.2 else 0
    
    def _get_random_style(self):
        """Randomly decide the style for a phrase (bold, italic, etc.)."""
        # styling compoents
        style_compo = ""
        if random.random() < 0.5:
            if self.bold_avail: 
                style_compo = "B"
        if random.random() < 0.5:
            if self.italic_avail: 
                style_compo = "I"
        if random.random() < 0.3:
            if self.bold_italic_avail: 
                style_compo = "BI"
        
        # underline and strike-through
        if random.random() < 0.3:
            style_compo += "U"
            return style_compo
        return style_compo
    def _write_styled_words(self, paragraph, para):
        """Write words to the paragraph with random styling."""
        words = para.split()
        i = 0
        while i < len(words):
            if random.random() < 0.1:
                phrase_length = random.randint(1, 6)
                start = i
                end = min(len(words), i + phrase_length)
                style = self._get_random_style()
                self.pdf.set_font(self.font_name, style=style, size=self.font_size)
                paragraph.write(" ".join(words[start:end]) + " ")
                i = end
            else:
                self.pdf.set_font(self.font_name, style="", size=self.font_size)
                paragraph.write(words[i] + " ")
                i += 1
    
    def generate(self, text: str):
        """
        Generates a PDF document from the provided text, applying random styling, headers, footers,
        alignment, and column layout. Saves the output to the specified filename.

        Args:
            text (str): The input text to render in the PDF.
        """
        self._set_header_footer(text)
        self.pdf.alias_nb_pages()
        self.pdf.add_page()
        doc_alignment_str = self._get_alignment()
        n_cols = self._get_n_cols()
        self._write_paragraphs(text, n_cols, doc_alignment_str)
        return self.pdf
    
class GeneratePDF:
    """Generate PDF files for different languages using IndicPDFGenerator."""
    
    language_to_writing_system_wiki_avail = {
        "marathi": ["Devanagari"], "hindi": ["Devanagari"], "sanskrit": ["Devanagari"],
        "tamil": ["tamil"], "telugu": ["telugu"], "kannada": ["Kannada"],"malayalam": ["Malayalam"],
        "bengali": ["Bengali"], "assamese": ["Bengali"],"manipuri": ["Bengali", "Meetei-mayek"],"nepali": ["Devanagari"],
        "gujarati": ["Gujarati"], "punjabi": ["Gurmukhi"], "konkani": ["Devanagari"],"oriya": ["Odia"],"kashmiri": ["Devanagari", "Arabic"], 
        "sindhi": ["Arabic", "Devanagari"], "urdu": ["Arabic"],"english": ["Latin"], "santali": ["Ol-chiki", "Devanagari"],
        }

    def __init__(self, language, fonts_folder):
        self.language = language # language name (eg: marathi, hindi, etc.)
        self.fonts_folder = fonts_folder # root folder for fonts
        self.writing_systems = self.language_to_writing_system_wiki_avail.get(language, []) # available writing systems for the language

    def check_writing_system(self, writing_system):
        """Check if the writing system is applicable for the language."""
        self.writing_system = writing_system
        if writing_system not in self.writing_systems:
            raise ValueError(f"Writing system '{writing_system}' is not applicable for language '{self.language}'.")
        
    def get_writing_system_fonts(self, writing_system):
        """Check if the fonts for the writing system exist."""
        fonts_writing_system = self.fonts_folder / writing_system
        if not fonts_writing_system.exists():
            raise FileNotFoundError(f"Fonts folder for writing system '{writing_system}' does not exist.")
        fonts_folder = [x for x in fonts_writing_system.rglob("*/") if x.is_dir()]
        return fonts_folder
    
    def select_font_randomly(self):
        """Select a random font from the available fonts for the writing system."""
        font_selected = random.choice(self.fonts_folder)
        return font_selected, font_selected.name
    
    def set_font_properties(self):
        """For given font, set font properties like regular, bold, italic, etc."""
        font_files = list(self.selected_font_path.glob("*.ttf"))
        font_prop_dict = self._get_font_properties(font_files)
        return {self.font_name: font_prop_dict}


    def _get_font_properties(self, font_files):
        """Get font properties for the selected font."""
        font_prop_dict = {}
        for font_file in font_files:
            fl_name = font_file.name.removesuffix(".ttf")
            identifer_str = fl_name.split("-")[-1]  # get the last part of the font name
            if identifer_str == "700": # bold 
                font_prop_dict["B"] = font_file 
            if identifer_str == "regular": # regular
                font_prop_dict["normal"] = font_file
            if identifer_str == "italic":
                font_prop_dict["I"] = font_file
            if identifer_str == "700-italic":
                font_prop_dict["BI"] = font_file
        return font_prop_dict 
        
    def generate_pdf(self, text: str, writing_system: str):
        """Generate a PDF file with the given text."""
        _REQ_PAGE_COUNT_ = 1
        self.check_writing_system(writing_system)

        # Get all available font folders for the writing system inside the fonts folder
        self.fonts_folder = self.get_writing_system_fonts(writing_system)

        # Select a random font path & corresponding font name from the available fonts
        self.selected_font_path, self.font_name = self.select_font_randomly()

        # Set font properties for the selected font
        font_properties = self.set_font_properties()

        # Generate PDF and ensure it has the required number of pages
        pdf_generator_obj = IndicPDFGenerator(self.font_name, font_properties)
        self.text = text
        self.generated_pdf = pdf_generator_obj.generate(text)

    def write_pdf(self, output_dir, file_idx):
        """Write pdf file for given file_idx & output dir"""
        self.generated_pdf.output(f"{output_dir}/{self.writing_system}_{self.font_name}_{file_idx}_n_pages_{self.generated_pdf.pages_count}.pdf")

    def write_text(self, output_dir, file_idx):
        """Write text file for given file_idx & output dir. This is used as ground truth later on"""
        file_name = f"{output_dir}/{self.writing_system}_{self.font_name}_{file_idx}.json"
        data = {
            "header": self.generated_pdf.header_text,
            "full_text": self.text
        }
        with open(file_name, 'w', encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

