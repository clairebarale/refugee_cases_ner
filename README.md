# Refugee_cases

### Table of contents:


### My Project presentation

### Setup

#### Data:
The raw data is not published on this github. It is accessible upon request.

| Terminology/Gazetter  | |
| ------------- | ------------- |
| [patterns](https://github.com/clairebarale/Refugee_cases/tree/main/extract_items/data/patterns) | terminology per label of the main text 

| Static vectors  | |
| ------------- | ------------- |
| [static_vectors](https://github.com/clairebarale/Refugee_cases/tree/main/extract_items/data/static_vectors) | static vectors |


#### Models:

| Configuration files  | |
| ------------- | ------------- |
| Case cover  | |
| [baseline.cfg](https://github.com/clairebarale/Refugee_cases/blob/main/extract_items/configs/case_cover/baseline.cfg) | Baseline CNN |
| [CNN+random_static.cfg](extract_items/configs/case_cover/CNN+random_static.cfg) | CNN with random static vectors |
| [config_trf.cfg](extract_items/configs/case_cover/config_trf.cfg) | RoBERTa-based transformers |
| [config_trf_legalbert.cfg](extract_items/configs/case_cover/config_trf_legalbert.cfg) | LegalBERT based transformers |

| Trained models  | |
| ------------- | ------------- |

Models can be package using the "spacy package" command. 


#### Scripts:

