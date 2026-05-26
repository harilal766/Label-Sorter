.. Label Sorter documentation master file, created by
   sphinx-quickstart on Mon May 25 18:51:17 2026.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Label Sorter 
=============
A python library to sort and organize shipping label pdf files.
Currently supports Amazon and Shopify.

Installation
-------------
.. code-block:: console
   
   $ pip install label-sorter

Usage
------
.. code-block:: python

   from label_sorter import LabelSorter

   # create an instance of the LabelSorter class
   sorter = LabelSorter(pdf_path="path/to/input/file")

   # call the method to create sorted pdf files
   sorter.create_sorted_pdf_files()





.. toctree::
   :maxdepth: 2
   :caption: Table Of Contents:
   
   label_sorter
   base_label