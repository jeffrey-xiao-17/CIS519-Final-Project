import re

def load_and_parse_tokens(file_path):
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

def create_clm_file(file_path, tokens):
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

entities, nonentities = load_and_parse_tokens("./6_gold_labels/train_6_gold_labels.txt")
create_clm_file("./6_gold_labels/train_6_gold_labels_entities.txt", entities)
create_clm_file("./6_gold_labels/train_6_gold_labels_nonentities.txt", nonentities)
