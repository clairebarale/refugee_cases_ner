import pandas as pd
from fuzzywuzzy import fuzz
import re
from datasets import load_dataset
import multiprocessing

n_cores = multiprocessing.cpu_count()
print(f"We are running the program on {n_cores} CPU cores")
file = {"cleaned_sentences_decisionID.csv"}
dataset = load_dataset("clairebarale/Refugee_cases_allparagraphs_caseID", usecols=['Unnamed: 0',"decisionID", "Text"], data_files=file, sep=";", num_proc=n_cores, split="train")
print(dataset)


file_path = "./list_idx.txt" # 'Unnamed: 0' columns values
with open(file_path) as f:
    list_idx = f.readlines() # each line is a list item
f.close()

# removing the \n character
list_idx_rows_to_remove = []
for s in list_idx:
    list_idx_rows_to_remove.append(re.sub('\n', '', s))

print(list_idx_rows_to_remove)
print(f"We retrieve {len(list_idx)} annotated sentences")
print(type(dataset))
list_idx = dataset['Unnamed: 0']
print(len(list_idx))
#dataset_1 = dataset.select(lambda example: example['Unnamed: 0'] not in list_idx_rows_to_remove)
#print(dataset_1)
