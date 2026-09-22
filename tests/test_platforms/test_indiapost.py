from tests.test_platforms.test_baselabel import TestBaseLabel
from label_sorter.platforms.courier.indiapost import IndiapostLabel
from tests.test_filepaths import indiapost_pdf

import pdfplumber

class TestIndiapost(TestBaseLabel):
    pdf = pdfplumber.open(indiapost_pdf)
    pages = pdf.pages

    
    




