import pickle
import random
import json
path = "/Users/jeffreyxiao/Desktop/sent_example.pickle"
out_path = "/Users/jeffreyxiao/Documents/GitHub/CIS519-Final-Project/pickle_data.json"
dictionary = {}
with open(out_path, 'w') as out:
    with (open(path, "rb")) as openfile:
        while True:
            try:
                dictionary = pickle.load(openfile)
            except EOFError:
                break

filtered_dictionary = {}
with open("filtered_pickles.json", "w") as outfile:
    for k in sorted(dictionary, key=lambda k: len(dictionary[k]), reverse=True):
        filtered_dictionary[k] = len(dictionary[k])
    json.dump(filtered_dictionary, outfile)