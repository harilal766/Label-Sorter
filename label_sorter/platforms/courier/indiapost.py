from label_sorter.platforms.base_label import BaseLabel

import re


class IndiapostLabel(BaseLabel):
    TRACKING_ID_PATTERN = r'EY\d{9}IN'
    
    def __init__(self, page_text, page_table = None, page_num = None):
        super().__init__(page_text, page_table, page_num)
    
    
    def get_pagetype(self):
        type = None
        if re.findall(self.TRACKING_ID_PATTERN,self.label_page_text):
            type = self.PAGE_TYPES[0]
        return type
    
    def get_page_summary(self) -> dict:
        # Shipping Label
        if self.get_pagetype() == self.PAGE_TYPES[0]:
            self.tracking_id = self.extract_id("tracking")
            
            self.label_page_table = self.label_page_table[3]
            
            for row in self.label_page_table:
                row = re.sub(r'Product name Qty\n','',row)
                product = row.split(' ')
                self.label_items.append({
                    "name" : ' '.join(product[:-1]), "qty" : product[-1]
                })
            return self.label_items