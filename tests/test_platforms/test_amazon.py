from tests.test_sorter import Test_LabelSorter

from label_sorter.platforms.base_label import BaseLabel
from label_sorter.platforms.ecommerce.amazon import AmazonLabel
from tests.test_sorter import Test_LabelSorter
from tests.test_filepaths import amazon_pdf
from tests.test_platforms.test_baselabel import TestBaseLabel
import pdfplumber, pytest


from pprint import pprint


class TestAmazon(TestBaseLabel):
    pdf = pdfplumber.open(amazon_pdf)
    pages = pdf.pages
    
    testing_index = 1 ; test_page = pages[testing_index]
    am_inst = AmazonLabel(
        page_text= test_page.extract_text(), page_table=test_page.extract_table(),
        page_num= testing_index+1
    )
    def test_pages(self):
        assert type(self.pages) == list
        assert self.pages[0]

    def test_get_page_type(self):
        assert self.am_inst.get_pagetype() == self.am_inst.PAGE_TYPES[1]
        
    def test_get_page_summary(self):
        self.am_inst.get_page_summary()
        assert self.am_inst.order_id
        print(self.am_inst.items)
        assert len(self.am_inst.items) > 0