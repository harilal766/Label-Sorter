from abc import ABC, abstractmethod
class BaseLabel:
    
    ORDER_ID_PATTERN : str | None = None
    TRACKING_ID_PATTERN : str | None = None
    
    def __init__(self, page_text : str, page_table, page_num: int = None):
        """
        This is where all the common characteristics of a label should start.
        
        Common characteristics
        1. order id
        2. tracking id
        3. page text
        4. page table
        5. page number
        
        The 2 and 4 are usually common in all pdf files, so we need to find out what seperate them from a label pdf. 

        Args:
            page_text (str): texts in a page
            page_table (_type_): Tables in a page
            page_num (int, optional): Page number. Defaults to None.
        """
        self.page_debrief_dict = {
            "order_id" : None, "items" : []
        }
        self.page_text = page_text
        self.page_table = page_table
        self.page_number = page_num
    