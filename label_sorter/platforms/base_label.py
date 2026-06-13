from abc import ABC, abstractmethod
import re


class BaseLabel:
    ORDER_ID_PATTERN : str | None = None
    TRACKING_ID_PATTERN : str | None = None
    
    PAGE_TYPES : tuple | None = None
    
    def __init__(self, page_text : str, page_table : list = None, page_num: int = None):
        """
        This is where all the common characteristics of a label should start.
        
        Common characteristics
        1. order id
        2. tracking id
        3. page text
        4. page table
        5. page number

        Args:
            page_text (str): texts in a page
            page_table (_type_): Tables in a page
            page_num (int, optional): Page number. Defaults to None.
        """
        self.page_text = page_text
        self.page_table = page_table
        self.page_number = page_num
        
        self.order_id: str | None = None
        self.tracking_id: str | None = None
        self.items: list = []
        
    def extract_id(self,pattern_type:str):
        pattern_types = {
            "order" : self.ORDER_ID_PATTERN,
            "tracking" : self.TRACKING_ID_PATTERN
        }
        selected_pattern = pattern_types[pattern_type]
        try:
            if not selected_pattern:
                raise NotImplementedError("Setup the subclass before doing this.")
            id_match = re.findall(selected_pattern,self.page_text)
            
            if id_match:
                return id_match[-1]
            else:
                return None
        except KeyError:
            raise KeyError("The pattern type provided is not available")
        
    def get_pagetype(self):
        pass
        
    def get_page_summary(self):
        pass
        basic_page_summary = {
            "page_number" : self.page_number,
            "page_text" : self.page_text,
            "page_table" : self.page_table,
            
            "order_id" : self.order_id,
            "items" : self.items
        }