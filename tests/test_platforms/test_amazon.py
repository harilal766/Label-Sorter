from tests.test_sorter import Test_LabelSorter

from label_sorter.platforms.base_label import BaseLabel
from label_sorter.platforms.ecommerce.amazon import AmazonLabel
from tests.test_sorter import Test_LabelSorter
from tests.test_filepaths import amazon_pdf
from tests.test_platforms.test_baselabel import TestBaseLabel
import pdfplumber, pytest





class TestAmazon(TestBaseLabel):
    pdf = pdfplumber.open(amazon_pdf)
    pages = pdf.pages
    
    test_page = pages[0]
    am_inst = AmazonLabel(
        page_text= test_page.extract_text(), page_table=test_page.extract_table(),page_num=33
    )
    def test_pages(self):
        assert type(self.pages) == list
        assert self.pages[0]
        """
    def test_find_amazon_page_type(self):
        assert self.am_inst.analyze_page() == self.am_inst.PAGE_TYPES[0]
    
    @pytest.mark.skip(reason="This test is currently failing due to changes in the PDF structure. Needs to be updated to reflect the new structure.")
    def test_analyze_page(self):
        assert self.am_inst.analyze_page()
        
        """