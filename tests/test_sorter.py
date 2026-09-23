import sys, os, pytest, re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tests.test_filepaths import *
from label_sorter.sorter import LabelSorter

class Test_LabelSorter:
    sorter_inst = LabelSorter(pdf_path=indiapost_pdf)
    platform = sorter_inst.find_platform()
    sorting_summary = sorter_inst.create_sorting_summary()

    
    def test_find_platfrom(self):
        print(self.platform)
        self.platform == "Indiapost"

    def test_create_sorted_summary(self):
        assert self.sorting_summary
        

    def test_sanitize_filename(self):
        sanitized_name = self.sorter_inst.sanitize_filename(unsanitized_name)
        
        character_matches = re.search(
            rf"{self.sorter_inst.product_codes_pattern}|{self.sorter_inst.reserved_characters_pattern}|{self.sorter_inst.remaining_words_pattern}", 
            sanitized_name
        )
        assert sanitized_name

    def test_create_sorted_pdf_files(self):
        assert self.sorting_summary
        self.sorter_inst.create_sorted_pdf_files()
        assert self.sorter_inst.output_folder
        
    def test_check_output(self):
        assert self.sorter_inst.check_output() == True
        
