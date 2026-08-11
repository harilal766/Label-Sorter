import re
from pprint import pprint
from ..base_label import BaseLabel
import pandas as pd

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
            # Order Number:
            #if re.findall(self.ORDER_ID_PATTERN,self.label_page_text):
            if re.findall(r'Order Number:',self.label_page_text):
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
                # the whole table in the invoice page is made as a 2d array, it should be made into a dictionary or pandas df form
                
                table_df = pd.DataFrame(self.label_page_table[0][1:],columns=self.label_page_table[0][0])
                
                for index, row in table_df.iterrows():
                    #print(row['Sl.\nNo'], row['Description'], row['Qty'])
                    if row['Sl.\nNo'].isnumeric():
                        self.label_items.append(
                            {"name":row['Description'], "qty":row['Qty']}
                        )
        except AttributeError:
            raise AttributeError("Check type of the table column")