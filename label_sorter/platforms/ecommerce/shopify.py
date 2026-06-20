import re
from ..base_label import BaseLabel

class ShopifyLabel(BaseLabel):
    ORDER_ID_PATTERN = r'Order\s.(\d{4,5})'
    PAGE_TYPES = BaseLabel.PAGE_TYPES + ["Invoice"]
    
    LABEL_PROD_PATTERN = r'ITEMS QUANTITY\s*(.*?)\s*Thank you for shopping with us!'
    LABEL_QTY_PATTERN = r'\d+\sof\s\d+'
    
    def __init__(self, page_text, page_table,page_num):
        super().__init__(page_text, page_table,page_num)
        
    def get_pagetype(self):
        """Since shopify labels can be modified, the input pdf can come with only shipping labels 
        or invoices next to it. Right now only the first one is analyzed

        Returns:
            _type_: _description_
        """
        page_type = None
        order_id_match = re.findall(self.ORDER_ID_PATTERN,self.label_page_text)
        if order_id_match:
            page_type = self.PAGE_TYPES[0]
        return page_type
    
    def get_page_summary(self):
        """get the product details
        find the prodname, qty and variation with the help of regex patterns

        Returns:
            _type_: _description_
        """
        try:
            if self.get_pagetype() == self.PAGE_TYPES[0]:
                items =  re.search(self.LABEL_PROD_PATTERN, self.label_page_text, re.DOTALL)
                if items:
                    prod_details = items.group(1)
                    print(prod_details)
                return items
        except Exception as e:
            print(e)
    