class BaseLabel:
    def __init__(self, page_text, page_table, page_num = None):
        """
        Handles the common characteristics of an Ecommerce label, which are :

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
    