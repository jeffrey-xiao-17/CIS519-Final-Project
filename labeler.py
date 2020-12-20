import re
import os
import subprocess

def load_and_parse_entity_labels(file_path):
    """
    Loads all of the labels into an array
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

label_mappings = {
	"O": 0,
	"PER": 1,
	"NORP": 2,
	"FAC": 3,
	"ORG": 4,
	"GPE": 5,
	"LOC": 6,
	"PRODUCT": 7,
	"EVENT": 8,
	"WORK_OF_ART": 9,
	"LAW": 10,
	"LANGUAGE": 11,
	"DATE": 12,
	"TIME": 13,
	"PERCENT": 14,
	"MONEY": 15,
	"QUANTITY": 16,
	"ORDINAL": 17,
	"CARDINAL": 18
}
def write_array_to_file(file_path, tokens):
    """
    writes an array to a file, with each element of the array
    on a separate line

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
        label_code = 0
        if (token != "O"):
        	dash_index = token.index("-")
        	if (dash_index < -1):
        		continue
        	token = token[dash_index+1:]
        	label_code = 0
        	if token in label_mappings:
        		label_code = label_mappings[token]
        f.write(str(label_code))
    f.close()

path_test_18_actual = "./NER_labels/test_18/test_18_actual_codes.txt"
write_array_to_file(path_test_18_actual, all_labels)