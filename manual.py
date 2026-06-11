from label_sorter.sorter import LabelSorter



sorter = LabelSorter(
    pdf_path = input("Enter filepath : ")
)

sorter.create_sorted_pdf_files()