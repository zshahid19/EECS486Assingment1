#!/usr/bin/env python3
import os
import re

"""
Module Docstring
"""

#Input: folder_path (path towards the folder with the dataset)
#Output: List containing all the files from the input folder_path
#Purpose: to turn the folder_path and give the user an actual manipultable data
def list_files_in_folder(folder_path):
    #Empty file_path list
    file_paths = []
    
    if not os.path.isdir(folder_path):
        print(f"Path does not exist")
        return file_paths

    #Iterating thorugh folder
    for entry in os.listdir(folder_path):
        full_path = os.path.join(folder_path, entry)
        # If good add it to the list
        if os.path.isfile(full_path):
            file_paths.append(full_path)

    return file_paths

#Input: A string containing the text from a file
#Output: the string with all the SGML tags removed
#Purpose: remove all the SGML tags from the input string
def removeSGML(file_text):
    #removed all SGML tags
    clean_text = re.sub(r'<.*?>', '', file_text)
    # print(clean_text)
    return clean_text


def main():
    folder_path = "test1/"
    file_paths = list_files_in_folder(folder_path)
    
    #opening each file
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            content = file.read()
            #Sending each file to removeSGML
            cleaned_content = removeSGML(content)
            print(f"Revmoed SGL on file: {file_path}")


def open_file(file_name):
    input_file = open(file_name, 'r')
    return input_file



if __name__ == "__main__":
    import sys
    main()
