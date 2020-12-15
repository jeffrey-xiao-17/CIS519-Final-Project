import re
import os
import subprocess

def load_and_parse_entity_labels(file_path):
    """
    Loads and separates tokens into entities and nonentities
    """
    all_labels = []
    with open(file_path, 'r') as f:
        for line in f:
            split = re.split(r'\t+', line)
            if (len(split) >= 6 ):
            	all_labels.append(split[0])
    return all_labels

all_labels = load_and_parse_entity_labels("./18_gold_labels/test_18_gold_labels.txt")
# print(entities_labels)

def write_array_to_file(file_path, tokens):
    """
    Creates and writes all tokens in input array to new file

    Parameters
    ----------
    file_path : str
        The location of the output file
    tokens : list (string)
    """
    f = open(file_path, "w")
    for index in range(len(tokens)):
        if index != 0:
            f.write("\n")
        token = tokens[index]
        for char_index in range(len(token)):
            if char_index != 0:
                f.write(" ")
            f.write(token[char_index])
    f.close()

path_test_18_actual = "./NER_labels/test_18/test_18_actual.txt"
write_array_to_file(path_test_18_actual, all_labels)