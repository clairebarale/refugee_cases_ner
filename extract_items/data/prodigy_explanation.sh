#!/bin/bash

# Explanation to create a labeled data set with Prodigy

# upload and create a dataset in prodigy
prodigy db-in {dataset name} {path to jsonl file}

# download the labeled data
prodigy db-out {dataset name} > {path to jsonl file}


###### Creating labeled data for the case case_cover ######

## 1 creating prodigy dataset
# data set name: first_ner
# source data for the first page: data_for_annotation.json

# opening prodigy annotation tool
# data_for_annotation.json is the data to load in to the first_ner dataset
# 30sec per decision first page
# en_core_web_trf is a pretrained language model
# ner.correct is the recipe to use for semi-automatic annotation
# --unsegmented does not split the text but displays one case case_cover at a time
prodigy ner.correct {data set} en_core_web_trf {PATH}--label PERSON,ORG,DATE,GPE --unsegmented

#getting data_first_page out of prodigy
prodigy db-out {data set} > {chosen_output_file.jsonl}


###### Creating patterns for the main text ######

# create patterns using pre-trained word embeddings (relying on cosine sim)
# to run on a cluster because pretrained static_vectors is too big to run on local machine
# we create one dataset per label
# dataset in prodigy have the same name as the names of the txt files containing terminology created manually
# run the below command once per text file words, changing parameters:
prodigy sense2vec.teach {dataset_name} /home/s2113351/NER_decisions/s2v_reddit_2019_lg --seeds {list of comma separated words} --threshold 0.70 --n-similar 20

# create the actual pattern from the obtained list of words
# outputs a jsonf containing the patterns
prodigy sense2vec.to-patterns {dataset_name} en_core_web_lg {LABELS} --output-file {PATH}

# then complete the patterns with exact phrases, using terms.teach recipe, then terms.to-patterns
# have to create a new jsonl file because otherwise it overwrites the existing file
# using terms.teach recipe and then terms.to-pattern (without annotation)

prodigy terms.teach {dataset_name} en_core_web_lg --seeds {list of comma separated words}
prodigy terms.to-patterns {dataset_name} {PATH} --label {LABELS}

# merge files to create one jsonl file
# using the function in ./preprocessing_scripts/create_pattern_labels.py

# files are stored in the directory: ./data/patterns

###### Creating labeled data for the main text #######

# can't use bert.ner.manual because it does not accept patterns for now
# tokenized by sentences

## 1- Labels created from scratch
# using blank (no spacy pipeline)

prodigy ner.manual {main_dataset} blank:en {PATH} --label DOC_EVIDENCE,PROCEDURE,LAW_REPORT,PERSON,CLAIMANT_INFO,CREDIBILITY,DETERMINATION,CLAIMANT_EVENT,EXPLANATION,LAW_CASE --patterns {PATH}

## 1- Labels that have been pre-trained
# using an existing model for semi-automatic annotation
prodigy ner.correct main_ner en_core_web_trf {PATH} --label GPE,NORP,DATE,ORG,LAW
# one hour for 1000 sentences annotated.

