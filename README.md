# CIS519 Final Project (NEI/NER)

Cindy Hao, Jeffrey Xiao

## Overview of Code Base

### `parser.py`

#### Breakdown of relevant files/folders

```
.
├── X_gold_labels   # contains train, dev, and test files for X labels (X={0,6,12,18})
├── CLM
│   └── .lm learning models for all entity/nonentity and training files (6,12,18)
├── NEI_labels
│   ├── expected
│   │   └── .txt files of expected labels for each dev/test file
│   ├── train_12
│   │   └── .txt files of actual labels for each dev/test file trained on 12
│   ├── train_18
│   │   └── .txt files of actual labels for each dev/test file trained on 18
│   └── train_6
│       └── .txt files of actual labels for each dev/test file trained on 6
├── parsed_character_files
│   ├── tokens
│   │   └── .txt files of all tokens in each dev/test file
│   └── .txt files of all entities/nonentities (separated) for training data
├── srilm-1.7.3
│   └── SRILM library for creating N-gram CLM models
└── parser.py   # main .py file run for NEI portion
```

This file was used primarily for the Named Entity Identification (NEI) portion of this project. In essence, `parser.py` contains methods for each step of the training and prediction process, as shown in the diagram below.

![parser-process](images/parser-process.png)

The end of this file contains code (commented out since this was run on Google Collab) for retrieving the accuracy scores for each trained/predicted file.

Overall, this identification process took a while due to having to parse and load many files, but the results of the training and prediction processes were relatively successful.

### `pickler.py`

#### Breakdown of relevant files

```
.
├── sent_example.pickle   # contains pickle data regarding entities and uses (NOT included in repo due to large size)
├── filtered_pickles.json   # json mapping keys to number of occurrences (instead of complete sentences)
└── pickler.py   # main .py file run for generating pickle data
```

This file was used to filter out the keys from the pickle data. The original pickle data (which was taken from the Wikilinks database) mapped keys to complete sentences/phrases. This caused the file to be massive and wouldn't open on our local computers. To get around this, we chose to create a new file with all of the keys mapped to the number of occurrences in an effort to create a more readable file. This was successful, as seen in `filtered_pickles.json`. The output would then be used in the NER portion to choose entities for each of the 18 labels.

### `labler.py`

This file was used to load all of the labels from the dataset and write just the labels to a file. We mapped each of the 18 labels to an integer, 1-18 (with 0 being non-entities). The labels were written such that they were all ints. The output of this file is in the `NER_labels` folder. 

### `project_main.py`

This file used the output of the files above to perform various computations. First, we computed the accuracy scores for NEI of the various datasets from the files created in the other files explained above. 

The majority of the NER task was also completed here. We used the filtered pickle file (`filtered_pickels.json`) to pull out examples of each of the 18 labels. We created the RoBERTa model with the token classification head to create embeddings for each of the labels. This was done through finding the embedding for each of the sentences that corresponded to a label and taking an average of those. The embedding for each word itself relied on us knowing the token, the sentence the token appeared in, and the position of the token in the sentence (this was an integer between 0 and the length of the sentence -1). After finding each of the embedding averages, we wrote them to a file (`./NER_LABELS/label_vectors.json`). 

We repeated the same process for each of the words in the test file. We found its position in the sentence and computed its embedding as well. This laid the groundword for classification.

Some relevant functions here include:
*   `tokens = load_and_parse_tokens_compiled(filepath)` where filepath is the path to the given test file. this will return a list of tokens from the filepath
*   `tuple_list = get_sentence_position(tokens)` will return a tupe of (word, sentence, index) from a list of tokens
* `nei_labels = file_to_list(path_to_test_nei)` to load the NEI labels 
* `predictions = get_labels_from_tuple_list_and_write(tuple_list, nei_labels, file_name)` returns a list of the predicted labels and writes them to a file (in `./NER_labels`). The tuple list is a list of `(word, sentence, position)`. This function also uses `label_mappings` (map of label to integer code, 0-18) and `get_vector_from_sentence(word, sentence, index)` which creates the embedding using the RoBERTa model. 
