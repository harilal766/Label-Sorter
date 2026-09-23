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
            
            prodtext = 'Product name Qty\n'
            #self.label_page_table = self.label_page_table[3]
            for row in self.label_page_table:
                if prodtext in row[0]:
                    self.label_page_table = row[0].replace(prodtext,'')
                    products = re.findall(r'.*\s\d{1,2}$',self.label_page_table)
                    for product in products:
                        self.label_items.append({
                            "name" : ' '.join(product.split(' ')[:-1]), "qty" : product.split(' ')[-1]
                        })
            print(self.label_items)
            return self.label_items