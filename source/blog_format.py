"""
This script is used to convert the jupyter notebook to a PDF file.
Code is from https://nbconvert.readthedocs.io/en/latest/removing_cells.html
but uses PDFExporter instead of HTMLExporter.
"""
from traitlets.config import Config
import nbformat as nbf
from nbconvert.exporters import PDFExporter
from nbconvert.preprocessors import TagRemovePreprocessor

# Setup config
c = Config()

# Tag cells with "remove_cell", "remove_output", "remove_input"
c.TagRemovePreprocessor.remove_cell_tags = ("remove_cell",)
c.TagRemovePreprocessor.remove_all_outputs_tags = ("remove_output",)
c.TagRemovePreprocessor.remove_input_tags = ("remove_input",)
c.TagRemovePreprocessor.enabled = True

# Configure and run out exporter
c.PDFExporter.preprocessors = ["nbconvert.preprocessors.TagRemovePreprocessor"]

# Remove date and added title instead of "blog"
c.LatexPreprocessor.date = ""
c.LatexPreprocessor.title = "Analysing the UK Analyst Role: What Do Employers Want?"

exporter = PDFExporter(config=c)
exporter.register_preprocessor(TagRemovePreprocessor(config=c), True)

# Configure and run exporter
output = PDFExporter(config=c).from_filename("blog.ipynb")

# Write to output pdf file
with open("blog.pdf", "wb") as f:
    f.write(output[0])