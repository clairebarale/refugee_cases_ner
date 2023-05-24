# Refugee_cases

### Table of contents:
1. Presentation
2. Setup
3. Data
4. Configuration files
5. Scripts

### My Project presentation
We introduce an end-to-end pipeline for retrieving, processing, and extracting targeted information from legal cases. This repository contains the code presented in our paper accepted for publication at ACL Findings 2023.
We perform information extraction based on state-of-the-art neural named-entity recognition (NER).
We test different architectures including two transformer models (RoBERTa and LegalBERT), using contextual and non-contextual embeddings, and compare general purpose versus domain-specific pre-training.
The workflow is explained in more details in the 2 yml: [project_case_cover_NER.yml](extract_items/project_case_cover_NER.yml) and [project_maintext_NER.yml](extract_items/project.yml).

### Setup
The NER models are trained using Spacy Entity Recognizer (see configuration files below)

Requirements: [requirements.txt](requirements.txt)

#### Data:
[CanLII](https://www.canlii.org/en/ca/irb/#search/type=decision&ccId=cisr&text=EXACT%20(Refugee)&origType=decision&origCcId=cisr) provides a dataset of 59,112 refugee cases associated with the Immigration and Refugee Board of Canada. The data is provided online in HTML and can be downloaded as PDF.

The raw data is not published on this github. It is accessible upon request.

| Terminology/Gazetter  | |
| ------------- | ------------- |
| [patterns](https://github.com/clairebarale/Refugee_cases/tree/main/extract_items/data/patterns) | terminology per label of the main text 

| Static vectors  | |
| ------------- | ------------- |
| [static_vectors](https://github.com/clairebarale/Refugee_cases/tree/main/extract_items/data/static_vectors) | static vectors |

The script [prodigy_explanation.sh](extract_items/data/prodigy_explanation.sh) contains explanations and instructions on the collection of annotated samples using prodigy semi-automatic annotation tool. 

#### Models:

| Configuration files  | |
| ------------- | ------------- |
| Case cover  | |
| [baseline.cfg](https://github.com/clairebarale/Refugee_cases/blob/main/extract_items/configs/case_cover/baseline.cfg) | Baseline CNN |
| [CNN+random_static.cfg](extract_items/configs/case_cover/CNN+random_static.cfg) | CNN with random static vectors |
| [config_trf.cfg](extract_items/configs/case_cover/config_trf.cfg) | RoBERTa-based transformers |
| [config_trf_legalbert.cfg](extract_items/configs/case_cover/config_trf_legalbert.cfg) | LegalBERT based transformers |

| Configuration files  | |
| ------------- | ------------- |
| Main text (1st set of categories: pretrained) | |
| [baseline.cfg](https://github.com/clairebarale/Refugee_cases/blob/main/extract_items/configs/pretrained/baseline.cfg) | Baseline CNN |
| [CNN+random_static.cfg](https://github.com/clairebarale/Refugee_cases/blob/main/extract_items/configs/pretrained/CNN%2Brandom_static.cfg) | CNN with random static vectors|
| [CNN+static_vectors.cfg](extract_items/configs/pretrained/CNN+static_vectors.cfg) | CNN with fine-tuned static vectors |
| [CNN+pretraining+random.cfg](extract_items/configs/pretrained/CNN+pretraining+random.cfg) | CNN with pretraining and random static vectors |
| [CNN+pretraining+myvectors.cfg](extract_items/configs/pretrained/CNN+pretraining+myvectors.cfg) | CNN with pretraining and fine-tuned static vectors |
| [config_trf.cfg](extract_items/configs/pretrained/preprocess.pyconfig_trf.cfg) | RoBERTa-based transformers |
| [config_trf_legalbert.cfg](extract_items/configs/pretrained/config_trf_legalbert.cfg) | LegalBERT based transformers |

| Configuration files  | |
| ------------- | ------------- |
| Main text (2nd set of categories: created from scratch)  | |
| [baseline.cfg](extract_items/configs/scratch/baseline.cfg) | Baseline CNN |
| [CNN+random_static.cfg](extract_items/configs/scratch/CNN+random_static.cfg) | CNN with random static vectors|
| [CNN+static_vectors.cfg](extract_items/configs/scratch/CNN+static_vectors.cfg) | CNN with fine-tuned static vectors |
| [CNN+pretraining+random.cfg](extract_items/configs/scratch/CNN+pretraining+random.cfg) | CNN with pretraining and random static vectors |
| [CNN+pretraining+myvectors.cfg](extract_items/configs/scratch/CNN+pretraining+myvectors.cfg) | CNN with pretraining and fine-tuned static vectors |
| [config_trf.cfg](extract_items/configs/scratch/config_trf.cfg) | RoBERTa-based transformers |
| [config_trf_legalbert.cfg](extract_items/configs/scratch/config_trf_legalbert.cfg) | LegalBERT based transformers |

The bash script [run.sh](extract_items/run.sh) contains an example on how to train the models using configuration files using Spacy.

Models can be packaged using the "spacy package" command. 


#### Scripts:
[preprocessing_scripts](extract_items/preprocessing_scripts) holds necessary script to curate the training data. 
[preprocess.py](extract_items/preprocessing_scripts/preprocess.py) converts the annotations from jsonl to spacy format. 

[utils](utils) contains a few scripts to help curate the text of the documents, count the number of annotations collected, or separate labels from each other. 
