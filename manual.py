from label_sorter.sorter import LabelSorter
from tests.test_filepaths import *


sorter = LabelSorter(
    pdf_path = amazon_pdf
)


platform = sorter.find_platform()
print(sorter.input_filepath,platform,sorter.create_sorting_summary())

sorter.create_sorted_pdf_files()

