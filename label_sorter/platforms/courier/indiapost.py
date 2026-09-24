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
        """
            header text is different on single and mixed items

        Returns:
            dict: _description_
        """
        # Shipping Label
        if self.get_pagetype() == self.PAGE_TYPES[0]:
            self.tracking_id = self.extract_id("tracking")
            header_pattern = 'Product name'
            #self.label_page_table = self.label_page_table[3]
            
            # loop through all nested lists 
            for data in self.page_table:
                # check the first element, it can be either a string or another list
                if header_pattern in data[0]:
                    data = data[1:]
                    for prodlist in data:
                        self.label_items.append({
                            "name" : prodlist[0], "qty" : prodlist[1]
                        })
            return self.label_items