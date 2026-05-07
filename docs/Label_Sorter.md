# LabelSorter Class
## Attributes
Sorting dictionary : to store the sorted data i.e; product name, quantity, and page numbers.
label filepath : path of the input pdf file
output folder : name of the folder to store sorted pdf files, created by replacing the `.pdf` extension with empty string
platform : platform of the pdf label eg : Amazon, Shopify etc...

# Technical Terms to Remember
Sorting key :
Platform : 

## Methods and their working logic
### Find platform
Accepts the pdf filepath as argument.
Loops through each page of the pdf file, counts order id occurences of each  platforms.
After the loop is exited, the total page count and counts of these orders ids are compared,
based on these conditions.
1. if shopify order ids are same as that of page counts, the pdf belongs to shopify.
2. if amazon order id is present, and the page numbers are more than or equal to the order id count, its amazon.

# Refine item name
Remove unwanted product codes from the item name.
## Amazon
Amazon labels typically use specific formats for their identifiers. Knowing what to look for allows you to filter out the descriptive text.

    ASINs (Amazon Standard Identification Numbers): These are 10-character alphanumeric strings starting with "B0" (e.g., B07XJ8C8F1).

    SKUs (Stock Keeping Units): These are merchant-defined, but often follow a consistent internal logic (e.g., DE-WHT-XL-01).

    FNSKUs: These usually start with "X0" (e.g., X002L9K6RB).

# Create sorted summary
1. Iterates through each page again and extracts the texts and tables in each page.
2. pages that contains the order id of the detected platform is analyzed to get the product name, variation and quantity.
    1. if more than one product is present in the page, its a miscellaneous order which have its own dedicated dictionary.
    2. the product variation and the pages where it appears are feeded to the dedicated dictionary based on how many items are present in each order.
    3. before adding to the dictionary, reserved characters are removed from the variation name to avoid issues while it's rendered as sorted pdf group later. 
3. after all pages are analyzed the miscellaneous dictionary is added to the "mixed" key of main dictionary.


### Create sorted pdf files
after the sorted summary dict is generated, this function will use a nested loop to analyze it and will generate the pdf file based on the page numbers list.    

### Create single pdf file
creates a single pdf file based on the output folder, product name and its sorted page nums,
this function will be used inside a loop to create sorted pdfs for all the details in the sorted dictionary.


# Potential bugs
while dealing with Delhivery, Bluedart etc, if their api integrations are done with shopify, these labels will have shopify order id, which will make the program think its handling with shopify and execute its algorithm.

amazon platform detection needs more tight logic in the future.