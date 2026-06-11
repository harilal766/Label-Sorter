from label_sorter.core import LabelSorter



sorter = LabelSorter(
    pdf_path = input("Enter filepath : ")
)

sorter.create_sorted_pdf_files()