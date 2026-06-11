import re
from ..base_label import BaseLabel

class AmazonLabel(BaseLabel):
    ORDER_ID_PATTERN = r'\d{3}-\d{7}-\d{7}'
    TRACKING_ID_PATTERN = r'AWB#*\s\d{12}'
    
    def __init__(self, page_text, page_table,page_num):
        super().__init__(page_text, page_table,page_num)
        #self.amazon_product_name_pattern = r'\|\s[A-Z\d]+\s\(\s[A-Z\d-]+\s\)(\s|\n)Shipping Charges'
        self.product_name_pattern = r'\|\s[A-Z\d]+\s\(\s[A-Z\d-]+\s\)(\s|\n)'
        self.ship_date_pattern = r'\d{2}\.\d{2}\.\d{4}'
            
    def find_amazon_page_type(self):
        type = None
        try:
            if re.findall(self.order_id_pattern,self.page_text):
                type = "Invoice"
            else:
                if re.findall(r'^Tax Invoice/Bill of Supply/Cash Memo',self.page_text):
                    type = "Overlap"
                else:
                    type = "Shipping Label"
        except Exception as e:
            print(e)
        else:
            return type
    
    def analyze_page(self) -> dict:
        page_dict = {}
        try:
            # start of amazon function in the future
            # Ensuring invoice pages
            order_id_match = re.findall(self.order_id_pattern,self.page_text)
            ship_date_match = re.findall(self.ship_date_pattern,self.page_text)
            
            if self.find_amazon_page_type() == "Invoice":
                self.order_id = order_id_match[0]
                #self.page_debrief_dict["ship_date"] = ship_date_match[0]
                
                # Update product rows based on overlapped and normal invoice pages
                product_table = self.page_table[0]
                product_rows = product_table[1:-3]
                if not re.search(r'Whether tax is',self.page_text):
                    product_rows = product_table[1:-1]
                    print(product_rows)
                for row in product_rows:
                    prod_name = row[1]; prod_qty = row[3]
                    page_dict = {"item_name" : prod_name, "qty" : prod_qty}

                    if page_dict["item_name"] != None:
                        self.items.append(page_dict)
        except Exception as e:
            print(e)
        else:
            return self.page_debrief_dict