from label_sorter.sorter import LabelSorter
from tests.test_filepaths import *


sorter = LabelSorter(
    pdf_path = input("Enter filepath : ")
    #pdf_path = amazon_pdf
)
sorter.create_sorted_pdf_files()

