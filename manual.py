from label_sorter.sorter import LabelSorter



sorter = LabelSorter(
    pdf_path = "/mnt/hdd/projects/Label-Sorter/test_labels/shopify.pdf"
)


platform = sorter.find_platform()
print(sorter.input_filepath,platform)