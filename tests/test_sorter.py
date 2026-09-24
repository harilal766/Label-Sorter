import sys, os, pytest, re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tests.test_filepaths import *
from label_sorter.sorter import LabelSorter

class Test_LabelSorter:    
    platforms = {
        #"Amazon" : amazon_pdf
        "Indiapost" : indiapost_pdf
    }
    
    def test_find_platfrom(self):
        for platform,file in self.platforms.items():
            sorter_inst = LabelSorter(pdf_path=file)
            
            tested_platform = sorter_inst.find_platform()
            assert tested_platform == platform

    def test_create_sorting_summary(self):
        for platform,file in self.platforms.items():
            sorter_inst = LabelSorter(pdf_path=file)
            summary = sorter_inst.create_sorting_summary()
            assert len(summary.keys()) > 0

"""
    def test_create_sorted_pdf_files(self):
        for platform,file in self.platforms.items():
            sorter_inst = LabelSorter(pdf_path=file)
            sorter_inst.create_sorted_pdf_files()
"""