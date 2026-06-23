import sys, os, pytest, re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tests.test_filepaths import *
from label_sorter.sorter import LabelSorter

class Test_LabelSorter:
    sorter_inst = LabelSorter(pdf_path=amazon_pdf)
    sorting_summary = sorter_inst.create_sorting_summary()
    
    files = {
        "Shopify" : shopify_pdf,
        "Amazon" : amazon_pdf
    }
        
    def test_find_platfrom(self):
        for platform,filename in self.files.items():
            if filename.endswith('.pdf') and os.path.exists(filename):
                inst = LabelSorter(pdf_path=filename)
                assert platform == inst.find_platform()

    def test_create_sorted_summary(self):
        print(self.sorting_summary)
        assert self.sorting_summary.keys
        

    def test_sanitize_filename(self):
        sanitized_name = self.sorter_inst.sanitize_filename(unsanitized_name)
        assert sanitized_name == static_sanitized_name

    def test_create_sorted_pdf_files(self):
        """
        sort the file, and make sure the output folder and its files exists.
        find the order counts from the .pdf filenames, and find the total count.
        """
        assert self.sorting_summary
        self.sorter_inst.create_sorted_pdf_files()
        assert self.sorter_inst.output_folder
        
    def test_check_output(self):
        assert self.sorter_inst.check_output() == True