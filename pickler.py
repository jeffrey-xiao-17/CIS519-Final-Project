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
                # json.dump(pickle.load(openfile), out)
                # pickle.dump(pickle.load(openfile), out)
            except EOFError:
                break
print(len(dictionary))
# with open(out_path) as f:
#     dictionary = json.load(f)
count = 0
filtered_dictionary = {}
with open("filtered_pickles.json", "w") as outfile:
    for k in sorted(dictionary, key=lambda k: len(dictionary[k]), reverse=True):
        # if (500 <= count < 1000):
            # print("{key} =========== {lenv}".format(key=k, lenv=len(dictionary[k])))
        filtered_dictionary[k] = len(dictionary[k])
        # count += 1
    json.dump(filtered_dictionary, outfile)