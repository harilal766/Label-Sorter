import re
from ..base_label import BaseLabel

class AmazonLabel(BaseLabel):
    ORDER_ID_PATTERN = r'\d{3}-\d{7}-\d{7}'
    TRACKING_ID_PATTERN = r'AWB#*\s\d{12}'
    
    PAGE_TYPES = ("Shipping Label","Invoice", "Invoice Overlap")
    
    def __init__(self, page_text, page_table,page_num):
        super().__init__(page_text, page_table,page_num)
        #self.amazon_product_name_pattern = r'\|\s[A-Z\d]+\s\(\s[A-Z\d-]+\s\)(\s|\n)Shipping Charges'
        self.product_name_pattern = r'\|\s[A-Z\d]+\s\(\s[A-Z\d-]+\s\)(\s|\n)'
        self.ship_date_pattern = r'\d{2}\.\d{2}\.\d{4}'
            
    def get_pagetype(self):
        type = None
        try:
            if re.findall(self.ORDER_ID_PATTERN,self.page_text):
                type = self.PAGE_TYPES[1]
            else:
                if re.findall(r'^Tax Invoice/Bill of Supply/Cash Memo',self.page_text):
                    type = self.PAGE_TYPES[2]
                else:
                    type = self.PAGE_TYPES[0]
        except Exception as e:
            print(e)
        else:
            return type
    
    def get_page_summary(self) -> dict:
        try:
            # start of amazon function in the future
            # Ensuring invoice pages
            #order_id_match = re.findall(self.ORDER_ID_PATTERN,self.page_text)
            
            if self.get_pagetype() == self.PAGE_TYPES[1]:
                self.order_id = self.extract_id("order")
                # Update product rows based on overlapped and normal invoice pages
                
                for row in self.page_table[1:]:
                    serial_number_cell = str(row[0])
                    if serial_number_cell.isnumeric() == True:
                        prodname = row[1]; prod_qty = row[3]
                        self.items.append(
                            { "name" : prodname, "qty" : prod_qty }
                        )
        except AttributeError:
            raise AttributeError("Check type of the table column")
        