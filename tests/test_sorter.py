import sys, os, pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tests.test_filepaths import *
from label_sorter.sorter import LabelSorter

class Test_LabelSorter:
    sorter_inst = LabelSorter(pdf_path=amazon_pdf)
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
        sorted_summary = self.sorter_inst.create_sorting_summary()
        print(sorted_summary)
        assert sorted_summary.keys

    def test_sanitize_filename(self):
        sanitized = self.sorter_inst.sanitize_filename(unsanitized_name)
        assert sanitized == sanitized_name

    def test_create_sorted_pdf_files(self):
        """
        find the pdf filename, and search for the folder in its name.
        
        """
        summary_keys = self.sorter_inst.create_sorting_summary()
        created_files = os.listdir(self.sorter_inst.output_folder)
        
        assert summary_keys
        
