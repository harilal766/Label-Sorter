import re
from ..base_label import BaseLabel

class AmazonLabel(BaseLabel):
    ORDER_ID_PATTERN = r'\d{3}-\d{7}-\d{7}'
    TRACKING_ID_PATTERN = r'AWB#*\s\d{12}'
    
    PAGE_TYPES = BaseLabel.PAGE_TYPES + ["Invoice", "Invoice Overlap"]
    
    def __init__(self, page_text, page_table,page_num):
        super().__init__(page_text, page_table,page_num)
        #self.amazon_product_name_pattern = r'\|\s[A-Z\d]+\s\(\s[A-Z\d-]+\s\)(\s|\n)Shipping Charges'
        self.product_name_pattern = r'\|\s[A-Z\d]+\s\(\s[A-Z\d-]+\s\)(\s|\n)'
        self.ship_date_pattern = r'\d{2}\.\d{2}\.\d{4}'
            
    def get_pagetype(self):
        type = None
        try:
            if re.findall(self.ORDER_ID_PATTERN,self.label_page_text):
                type = self.PAGE_TYPES[1]
            else:
                if re.findall(r'^Tax Invoice/Bill of Supply/Cash Memo',self.label_page_text):
                    type = self.PAGE_TYPES[2]
                else:
                    type = self.PAGE_TYPES[0]
        except Exception as e:
            print(e)
        else:
            return type
    
    def get_page_summary(self) -> dict:
        """Reads the items table in the invoice page  

        Raises:
            AttributeError: _description_

        Returns:
            dict: _description_
        """
        try:
            # start of amazon function in the future
            # Ensuring invoice pages
            #order_id_match = re.findall(self.ORDER_ID_PATTERN,self.page_text)
            
            if self.get_pagetype() == self.PAGE_TYPES[1]:
                self.order_id = self.extract_id("order")
                # Update product rows based on overlapped and normal invoice pages
                for row in self.label_page_table[0]:
                    serial_number_cell = row[0]
                    if serial_number_cell.isnumeric():
                        self.label_items.append(
                            {"name":row[1], "qty":row[3]}
                        )
                
        except AttributeError:
            raise AttributeError("Check type of the table column")
        