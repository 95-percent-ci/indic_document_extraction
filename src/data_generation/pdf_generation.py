import random
import warnings
from fpdf import FPDF
from fpdf.enums import Align

class PDF(FPDF):
    """Custom PDF Class to manage headers, body & footers"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.header_text = ""
        self.footer_text = ""
        self.add_header_flag = False
        self.add_footer_flag = False
        self.font_name = None

    def header(self):
        if self.add_header_flag:
            self.set_font(self.font_name, style="B", size=13)
            width = self.get_string_width(self.header_text) + 6
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

