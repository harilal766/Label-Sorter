from label_sorter.sorter import LabelSorter



sorter = LabelSorter(
    pdf_path = "/mnt/hdd/projects/Label-Sorter/test_labels/amazon.pdf"
)

platform = sorter.find_platform()
print(platform)