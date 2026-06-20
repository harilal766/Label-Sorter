from tests.test_platforms.test_baselabel import TestBaseLabel
from label_sorter.platforms.ecommerce.shopify import ShopifyLabel


from tests.test_filepaths import shopify_pdf

import pdfplumber


class TestShopifyLabel(TestBaseLabel):
    pdf = pdfplumber.open(shopify_pdf)
    pages = pdf.pages
    
    testing_index = 8 ; test_page = pages[testing_index]
    sh_inst = ShopifyLabel(
        page_text= test_page.extract_text(), page_table=test_page.extract_table(),
        page_num= testing_index+1
    )
    
    def test_get_pagetype(self):
        assert self.sh_inst.get_pagetype() == ShopifyLabel.PAGE_TYPES[0]
        
    def test_get_page_summary(self):
        assert self.sh_inst.get_page_summary()
    