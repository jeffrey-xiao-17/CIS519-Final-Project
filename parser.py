import re
import os
import subprocess
# from sklearn.metrics import accuracy_score

def load_and_parse_tokens(file_path):
    """
    Loads and separates tokens into entities and nonentities
    """
    entities = []
    nonentities = []
    with open(file_path, 'r') as f:
        for line in f:
            split = re.split(r'\t+', line)
            if (len(split) >= 6 and split[0] != 'O'):
                entities.append(split[5])
            elif (len(split) >= 6):
                nonentities.append(split[5])
    return entities, nonentities

def load_and_parse_tokens_compiled(file_path):
    """
    Loads and separates tokens into one compiled array
    """
    tokens = []
    with open(file_path, 'r') as f:
        for line in f:
            split = re.split(r'\t+', line)
            if (len(split) >= 6):
                tokens.append(split[5])
    return tokens

def create_clm_file(file_path, tokens):
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

def get_labels(file_path, out_file):
    """
    Reads and writes labels to all tokens

    Parameters
    ----------
    file_path : str
        The location of the original unedited file
    out_file : str
        The location of the file to write to (with the labels)
    """
    wf = open(out_file, "w")
    with open(file_path, 'r') as f:
        for line in f:
            split = re.split(r'\t+', line)
            if (len(split) >= 6 and split[0] != 'O'):
                wf.write("1\n")
            elif (len(split) >= 6):
                wf.write("0\n")
    wf.close()

# Creating CLM and parsed files
def create_CLM_and_parse_files():
    """
    Function to create all parsed .txt files (entities, nonentities, and tokens)
    """
    entities, nonentities = load_and_parse_tokens("./6_gold_labels/train_6_gold_labels.txt")
    create_clm_file("./parsed_character_files/train_6_gold_labels_entities.txt", entities)
    create_clm_file("./parsed_character_files/train_6_gold_labels_nonentities.txt", nonentities)
    create_clm_file("./parsed_character_files/train_6_gold_labels_tokens.txt", entities + nonentities)


def classify_all_tokens(entity_lm_file, nonentity_lm_file, tokens_file, out_file):
    """
    Classifies all tokens based on training data

    Parameters
    ----------
    entity_lm_file : str
        The location of the entity learning model
    nonentity_lm_file : str
        The location of the nonentity learning model
    tokens_file : str
        The location of the file with all tokens to be classified
    out_file : str
        The location of the output actual labels
    """
    wr = open(out_file, "w")
    wr.close()
    with open(tokens_file, 'r') as f:
        for line in f:
            wf = open("sample.txt", "w")
            wf.write(line.strip('\n'))
            wf.close()
            classify_one_token(entity_lm_file, nonentity_lm_file, "sample.txt", out_file)

def classify_one_token(entity_lm_file, nonentity_lm_file, txt_file, out_file):
    """
    Classify one token based on given learning models

    Parameters
    ----------
    entity_lm_file : str
        The location of the entity learning model
    nonentity_lm_file : str
        The location of the nonentity learning model
    txt_file : str
        The location of the temporary file for each word
    out_file : str
        The location of the output actual labels
    """
    subprocess2 = subprocess.Popen("srilm-1.7.3/bin/macosx/ngram -lm {lm} -ppl {token} ".format(lm=entity_lm_file, token=txt_file), shell=True, stdout=subprocess.PIPE)
    subprocess_return = subprocess2.stdout.read()
    entity_ppl = float(subprocess_return[subprocess_return.index("ppl= ") + 5:subprocess_return.index("ppl1= ")])
    subprocess2 = subprocess.Popen("srilm-1.7.3/bin/macosx/ngram -lm {lm} -ppl {token} ".format(lm=nonentity_lm_file, token=txt_file), shell=True, stdout=subprocess.PIPE)
    subprocess_return = subprocess2.stdout.read()
    nonentity_ppl = float(subprocess_return[subprocess_return.index("ppl= ") + 5:subprocess_return.index("ppl1= ")])
    f = open(out_file, "a")
    f.write("1\n" if entity_ppl < nonentity_ppl else "0\n")
    f.close()

tokens = load_and_parse_tokens_compiled("./12_gold_labels/dev_12_gold_labels.txt")
create_clm_file("./parsed_character_files/dev_12_gold_labels_tokens.txt", tokens)
get_labels("./12_gold_labels/dev_12_gold_labels.txt", "./NEI_labels/dev_12_expected_labels.txt")
classify_all_tokens("/Users/jeffreyxiao/Documents/GitHub/CIS519-Final-Project/CLM/train_6_gold_labels_entities.lm", 
"/Users/jeffreyxiao/Documents/GitHub/CIS519-Final-Project/CLM/train_6_gold_labels_nonentities.lm",
"/Users/jeffreyxiao/Documents/GitHub/CIS519-Final-Project/parsed_character_files/dev_12_gold_labels_tokens.txt",
"/Users/jeffreyxiao/Documents/GitHub/CIS519-Final-Project/NEI_labels/dev_12_actual_labels.txt")

def file_to_list(file_path):
    arr = []
    with open(file_path, 'r') as f:
        for line in f:
            arr.append(line.strip('\n'))
    return arr

# print(accuracy_score(file_to_list("/Users/jeffreyxiao/Documents/GitHub/CIS519-Final-Project/NEI_labels/dev_6_actual_labels.txt"),
# file_to_list("/Users/jeffreyxiao/Documents/GitHub/CIS519-Final-Project/NEI_labels/dev_6_expected_labels.txt")))