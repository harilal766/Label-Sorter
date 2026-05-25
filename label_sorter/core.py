import pdfplumber, re, os,sys, logging, json
from pypdf import PdfReader, PdfWriter
from pprint import pprint
from label_sorter.platforms.ecommerce.base_label import BaseLabel
from label_sorter.platforms.ecommerce.shopify import ShopifyLabel
from label_sorter.platforms.ecommerce.amazon import AmazonLabel

logging.getLogger('pdfminer').setLevel(logging.ERROR)


class LabelSorter:
    def __init__(self, pdf_path):
        self.input_filepath = pdf_path
        self.output_folder = self.input_filepath.replace(".pdf","")
        self.platform = self.find_platform()
        self.misc_filename = "Mixed"
        
        # regex patterns for filename sanitization which will als be needed for unit testing.
        self.reserved_characters_pattern = r"[,\/\\\:\*\?\"\<\>]"
        #self.product_codes_pattern = r"\|\s([A-Z]|\d)+\s\(\s((\d|[A-Z]){1,4}-*){1,3}\s\)|" # HSN30049011
        self.product_codes_pattern = r"B0.*|HSN.*|\s"
        self.another_pattern = r"\s{2}|\n|Shipping Charges|\/|:"
        
    def find_platform(self) -> str:
        """
        Finding the platform based on the characteristics of the input file.
        
        Raises:
            Raises if no such file exists.

        Returns:
            str: Capitalized platform name if found, else None.
        """
        platform = None
        if os.path.exists(self.input_filepath) == False:
            sys.exit("Input file does not exist....")
        try:
            with pdfplumber.open(self.input_filepath) as pdf_file:
                total_pages = 0; amazon_count = 0 
                
                shopify_order_id_count, amazon_order_id_count, flipkart_order_count = 0, 0, 0
                
                for page_index, page in enumerate(pdf_file.pages):
                    total_pages += 1
                    page_text = page.extract_text(); page_tables = page.extract_tables()
                    
                    # Shopify Initializations
                    sh = ShopifyLabel(page_text=page_text, page_table=page_tables,page_num=0)
                    am = AmazonLabel(page_text=page_text, page_table=page_tables,page_num=0)
                    
                    if re.findall(sh.shopify_order_id_pattern, page_text):
                        shopify_order_id_count += 1
                    elif re.findall(am.amazon_order_id_pattern, page_text):
                        amazon_order_id_count += 1
                    
                    platform_instances = {
                        "Amazon" : AmazonLabel(page_text=page_text, page_table=page_tables,page_num=0)
                    }    
                    
                if total_pages == shopify_order_id_count:
                    platform = "Shopify"
                # this condition is not complete, need to add overlap page detection
                elif amazon_order_id_count > 0:
                    platform = "Amazon"
                elif total_pages == 2*flipkart_order_count:
                    platform = "Flipkart"
            
        except FileNotFoundError:
            print(f"The file {self.input_filepath} does not exist.")
        except Exception as e:
            print(e)
        else:
            return platform

    def sanitize_filename(self,filename):
        """
        Removes Reserved characters and product codes from the filename to make it suitable for file naming.

        Args:
            filename (str): filename from the pdf page.

        Raises:
            TypeError: If the filename is not a string.

        Returns:
            str : filename with unwanted characters removed.
        """
        try:
            sanitization_patterns = (self.reserved_characters_pattern,self.product_codes_pattern, self.another_pattern)
            for pattern in sanitization_patterns:
                filename = re.sub(pattern,"",filename)
                
            return filename
        except TypeError as te:
            raise TypeError(f"Got {type(filename)} instead of string in sanitized filename")
            
    def create_sorted_summary(self):
        """
        Adds the product names, variations, the page numbers which consists of it in nested dictionary format. 
        
        Raises:
            AttributeError: _description_

        Returns:
            dict : dictionary that contains full summary of the input pdf file.
        """
        page_debrief = None; 
        # summary dictionaries
        summary_dict = {}; chosen_summary_dict = {}
        pages_list = None
        try:
            with pdfplumber.open(self.input_filepath) as pdf_file:
                for page_index, page in enumerate(pdf_file.pages):
                    page_text = page.extract_text(); page_table = page.extract_tables()
                    page_number = page_index+1
                    pages = [page_number-1, page_number] if self.platform == "Amazon" else [page_number]
                    debriefs = {
                        "Shopify" : ShopifyLabel(page_text=page_text, page_table=page_table,page_num=page_number).analyze_shpy_page(),
                        "Amazon" : AmazonLabel(page_text=page_text, page_table=page_table,page_num=page_number).analyze_amzn_page(),
                    }
                    
                    page_debrief = debriefs.get(self.platform,None)  
                    if page_debrief.get("order_id",None):
                        order_id = page_debrief.get("order_id",None)
                        items_list = page_debrief.get("items",None)
                        for item_dict in items_list:
                            item_count = len(items_list)
                            if item_count == 1:
                                chosen_summary_dict = summary_dict
                            elif item_count > 1:
                                if not self.misc_filename in summary_dict.keys():
                                    summary_dict[self.misc_filename] = {
                                        "pages" : [], "summary" : {}
                                    }
                                chosen_summary_dict = summary_dict[self.misc_filename]["summary"]
                                for mixed_page in pages:
                                    if not mixed_page in summary_dict[self.misc_filename]["pages"]: 
                                        summary_dict[self.misc_filename]["pages"].append(mixed_page)
                                        
                            item_name = item_dict.get("item_name",None)
                            # getting a clean item name
                            
                            item_name = self.sanitize_filename(filename=item_name)
                            print(item_name)
                            item_qty = item_dict["qty"]
                            # give dedicated dict for each item name.
                            if not item_name in chosen_summary_dict.keys():
                                chosen_summary_dict[item_name] = {}
                            # give empty list or 0 for item name, based on order items.
                            if not item_qty in chosen_summary_dict[item_name].keys():
                                chosen_summary_dict[item_name][item_qty] = [] if item_count == 1 else 0
                            # populate the page numbers or item variation count, based on the same criteria commented above 👆🏼.
                            chosen_summary_dict[item_name][item_qty] += pages if item_count == 1 else 1
        except AttributeError as ae:
            raise AttributeError(f"Attribute issues found at summary dictionary : \n {ae}")
        except Exception as e:
            print(e)
        else:
            return summary_dict
            
    def create_single_pdf_file(self, pdf_name, page_numbers):
        if page_numbers == None:
            sys.exit("Received Nonetype instead of page numbers")
        try:
            reader = PdfReader(self.input_filepath); writer = PdfWriter()
            #print(pdf_name, page_numbers)
            # adding pages to the writer
            for page in page_numbers:
                writer.add_page(reader.pages[page-1])
                
            page_count = len(page_numbers)
            order_count = int(page_count/2) if self.platform == "Amazon" else page_count
            
            sorted_pdf_file = f"{re.sub(r"[\|\.\/]*",r"",pdf_name)} - {order_count} order{"s" if order_count > 1 else ""}.pdf"
        except Exception as e:
            print(e)
        else:
            if writer:
                if sorted_pdf_file:
                    out_filepath = os.path.join(self.output_folder, sorted_pdf_file)
                    with open(out_filepath, "wb") as out_pdf:
                        writer.write(out_pdf)        
            
    def create_sorted_pdf_files(self):
        """Generates out pdf files by parsing the summary dictionary.
        """
        summary_dict = self.create_sorted_summary()
        
        #pprint(summary_dict.keys())
        
        if len(summary_dict.keys()) == 0:
            sys.exit("Cannot sort with empty summary...")
            
        #order_count = None; page_numbers = None
        output_file = None 
        # Create output folder if not created already.
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
            print(f"Created output folder : {self.output_folder}")

        output_count = 0
        try:
            print(f"Sorted Summary :")
            for sorting_key, value in summary_dict.items():
                # Assigning output file name and its pages according to order type
                # single item orders
                if sorting_key != self.misc_filename:
                    #print(f"Writing Single item order",end=", ")
                    for qty,page_list in value.items():
                        output_count += 1
                        #print(f"Detected more than one qty.")
                        self.create_single_pdf_file(
                            pdf_name = f"{output_count} - {sorting_key} - {qty}", page_numbers=page_list
                        )
                else:
                    output_count += 1
                    self.create_single_pdf_file(
                        pdf_name = f"{output_count} - {self.misc_filename}", page_numbers= value.get("pages",None)
                    )
        except Exception as e:
            print(f"Err : {e}")
