from label_sorter.sorter import LabelSorter
from tests.test_filepaths import amazon_pdf


sorter = LabelSorter(
    pdf_path = input("Enter filepath : ")
)


platform = sorter.find_platform()
print(sorter.input_filepath,platform)

sorter.create_sorted_pdf_files()

