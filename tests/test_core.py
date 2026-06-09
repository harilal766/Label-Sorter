import sys, os, pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from filepaths import *
from label_sorter.core import LabelSorter


class Test_LabelSorter:
    label_inst = LabelSorter(pdf_path=amazon_pdf)
    files = {
        "Shopify" : shopify_pdf,
        "Amazon" : amazon_pdf
    }
    def test_find_platfrom(self):
        for platform,filename in self.files.items():
            if filename.endswith('.pdf') and os.path.exists(filename):
                inst = LabelSorter(pdf_path=filename)
                assert inst.find_platform() == platform
    
    def test_create_sorted_summary(self):
        assert type(self.label_inst.create_sorted_summary()) == dict

    def test_sanitize_filename(self):
        sanitized = self.label_inst.sanitize_filename(unsanitized_name)
        assert sanitized == sanitized_name

    def test_create_sorted_pdf_files(self):
        """
        Check output filenames and make sure the numbering is in correct order, mixed file have number as well.
        all the files except the summary.json should have .pdf extension
        """
        summary_keys = self.label_inst.create_sorted_summary()
        created_files = None
        
        assert summary_keys
        