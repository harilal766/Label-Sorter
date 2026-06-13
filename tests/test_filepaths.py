import json, os, json
from pathlib import Path

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
test_and_root_join = os.path.join(TEST_DIR,"..")
Root = os.path.abspath(test_and_root_join)
test_label_dir = os.path.join(Root,"test_labels")

test_json_filename = "label_sorter.json"

test_json_content = {
    "before_sanitize" : "",
    "after_sanitize" : ""
}

files = os.listdir()

if not test_json_filename in files:
    json_str = json.dumps(test_json_content, indent=4)
    
    with open(test_json_filename,"w") as json_file:
        json_file.write(json_str)
        json_file.close()

with open(test_json_filename,"r") as json_file:
    credentials = json.load(json_file)
    
    amazon_pdf = os.path.join(test_label_dir, "amazon.pdf")
    shopify_pdf = os.path.join(test_label_dir, "shopify.pdf")
    
    unsanitized_name = credentials["before_sanitize"]
    sanitized_name = credentials["after_sanitize"]
    
    
    

    

