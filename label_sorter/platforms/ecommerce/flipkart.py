import re
from ..base_label import BaseLabel

class FlipkartLabel(BaseLabel):
    def __init__(self, page_text, page_table, page_num):
        super().__init__(page_text, page_table, page_num)
        self.flipkart_order_id_pattern = r'OD\d{19}'
        
    def verify_page_is_not_cropped(self):
        try:
            pass
        except Exception as e:
            print(e)