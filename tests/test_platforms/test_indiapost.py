from tests.test_platforms.test_baselabel import TestBaseLabel
from tests.test_filepaths import indiapost_pdf
from label_sorter.platforms.courier.indiapost import IndiapostLabel

import pdfplumber

class TestIndiapost(TestBaseLabel):
    pdf = pdfplumber.open(indiapost_pdf)
    pages = pdf.pages
    
    testing_index = 1; test_page = pages[testing_index]
    in_inst = IndiapostLabel(
        page_text=test_page.extract_text(), page_table=test_page.extract_table(),
        page_num=1
    )
    
    def test_pages(self):
        assert type(self.pages) == list

    def test_extract_id(self):
        id = self.in_inst.extract_id(pattern_type="tracking")
        assert id
        
    def test_get_pagetype(self):
        page_type = self.in_inst.get_pagetype()
        assert page_type == self.in_inst.PAGE_TYPES[0]

    def test_get_pagesummary(self):
        page_summary = self.in_inst.get_page_summary()
        print(page_summary)
        assert len(page_summary) > 0





