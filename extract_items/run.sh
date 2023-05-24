#!/bin/bash

#spacy train ./extract_items/configs/scratch/baseline.cfg  --output ./training/baseline/
#spacy train ./extract_items/configs/scratch/CNN+pretraining+myvectors.cfg  --output ./training/CNN+pretraining+myvectors/
#spacy train ./extract_items/configs/scratch/CNN+pretraining+random.cfg  --output ./training/CNN+pretraining+random/
#spacy train ./extract_items/configs/scratch/CNN+random_static.cfg  --output ./training/CNN+random_static/
#spacy train ./extract_items/configs/scratch/CNN+static_vectors.cfg  --output ./training/CNN+static_vectors/ # this is the best to use
#spacy train ./extract_items/configs/scratch/config_trf.cfg  --output ./training/config_trf_pretrained/
#spacy train ./extract_items/configs/scratch/config_trf_legalbert.cfg  --output ./training/config_trf_legalbert/

spacy evaluate ./training/baseline/model-last ./extract_items/data/main_text/categories_from_scratch/test_set_scratch.spacy
spacy evaluate ./training/CNN+pretraining+myvectors/model-last ./extract_items/data/main_text/categories_from_scratch/test_set_scratch.spacy
spacy evaluate ./training/CNN+pretraining+random/model-last ./extract_items/data/main_text/categories_from_scratch/test_set_scratch.spacy
spacy evaluate ./training/CNN+random_static/model-last ./extract_items/data/main_text/categories_from_scratch/test_set_scratch.spacy
spacy evaluate ./training/CNN+static_vectors/model-last ./extract_items/data/main_text/categories_from_scratch/test_set_scratch.spacy