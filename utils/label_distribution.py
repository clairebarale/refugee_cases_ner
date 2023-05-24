from prodigy.components.db import connect
from collections import Counter

def label_distributions_first_ner(dataset_name = " "):
    # first_ner labels: PERSON,ORG,DATE,GPE

    db = connect()
    examples_first_ner = db.get_dataset_examples(f"{dataset_name}")

    # dict should look like this: {'DATE': 5, 'PERSON': 4, 'ORG': 1, 'GPE': 1}
    # containing all annotation
    dict = {'GPE': 0, 'DATE': 0, 'PERSON': 0, 'ORG': 0}

    for eg in examples_first_ner:

        labels = [span["label"] for span in eg.get("spans", [])]
        # print(labels)
        count = Counter(labels) # a dictionnary Counter({'GPE': 5, 'DATE': 3, 'PERSON': 3, 'ORG': 1})
        #print(count)

        dict = Counter(count) + Counter(dict)

    print(dict)
    print("total number of annotation in first_ner is: ", sum(dict.values()))

# decided not to use this dataset because the static_vectors are too close to each other and confusing.
# maybe worth give it a shot later on
def label_distribution_credibility_ner(dataset_name = " "):
    # labels: CREDIB_ALLEG,CREDIB_DOUBT,CREDIB_EVIDENCE,CREDIB_INCONS
    db = connect()
    examples_credibility_ner = db.get_dataset_examples(f"{dataset_name}")

    # dict should look like this: {'DATE': 5, 'PERSON': 4, 'ORG': 1, 'GPE': 1}
    # containing all annotation
    dict = {'CREDIB_ALLEG': 0, 'CREDIB_DOUBT': 0, 'CREDIB_EVIDENCE': 0, 'CREDIB_INCONS': 0, 'CREDIBLIITY': 0}

    for eg in examples_credibility_ner:
        labels = [span["label"] for span in eg.get("spans", [])]
        # print(labels)
        count = Counter(labels)  # a dictionnary Counter({'GPE': 5, 'DATE': 3, 'PERSON': 3, 'ORG': 1})
        # print(count)

        dict = Counter(count) + Counter(dict)

    print(dict)
    print("total number of annotation in credibility_ner is: ", sum(dict.values()))

def label_distribution_9labels_ner(dataset_name = " "):
    #labels: PROCEDURE,CITATION,ALLEGED_FACTS,CLAIMANT_INFO,CLAIMANT_EVENT,DOC_EVIDENCE,DETERMINATION,LEGAL_GROUND,EXPLANATION
    # plus adding: credibility label
    # adding CITATION_CASE
    # so now it is 11 labels actually

    db = connect()
    examples_9labels_ner = db.get_dataset_examples(f"{dataset_name}")

    # dict should look like this: {'DATE': 5, 'PERSON': 4, 'ORG': 1, 'GPE': 1}
    # containing all annotation

    dict = {'CREDIBILITY': 0, 'CITATION_CASE':0,'PROCEDURE': 0, 'CITATION': 0, 'ALLEGED_FACTS': 0, 'CLAIMANT_INFO': 0, 'CLAIMANT_EVENT': 0, 'DOC_EVIDENCE': 0, 'DETERMINATION': 0, 'LEGAL_GROUND': 0, 'EXPLANATION': 0}

    for eg in examples_9labels_ner:
        labels = [span["label"] for span in eg.get("spans", [])]
        # print(labels)
        count = Counter(labels)  # a dictionnary Counter({'GPE': 5, 'DATE': 3, 'PERSON': 3, 'ORG': 1})
        # print(count)

        dict = Counter(count) + Counter(dict)

    print(dict)
    print("total number of annotation in the dataset " f"{dataset_name}" " is: ", sum(dict.values()))

def label_distribution_pretrained_labels_ner(dataset_name = " "):
    # labels:

    db = connect()
    examples_pretrained_ner = db.get_dataset_examples(f"{dataset_name}")

    # dict should look like this: {'DATE': 5, 'PERSON': 4, 'ORG': 1, 'GPE': 1}
    # containing all annotation
    dict = {'GPE': 0, 'DATE': 0, 'PERSON': 0, 'ORG': 0, 'LAW': 0, 'NORP': 0, 'PERSON': 0, 'ORG': 0} #TODO: change label names here

    for eg in examples_pretrained_ner:
        labels = [span["label"] for span in eg.get("spans", [])]
        # print(labels)
        count = Counter(labels)  # a dictionnary Counter({'GPE': 5, 'DATE': 3, 'PERSON': 3, 'ORG': 1})
        # print(count)

        dict = Counter(count) + Counter(dict)

    print(dict)
    print("total number of annotation in pretrained_label_ner is: ", sum(dict.values()))


def label_label_distribution_pretrained_main_ner_cluster(dataset_name=""):
    # DATE,EVENT,FAC,GPE,LANGUAGE,LAW,LOC,MONEY,NORP,ORG,PERSON

    db = connect()
    examples_pretrained_ner = db.get_dataset_examples(f"{dataset_name}")

    # dict should look like this: {'DATE': 5, 'PERSON': 4, 'ORG': 1, 'GPE': 1}
    # containing all annotation
    dict = {'DATE': 0, 'EVENT': 0, 'FAC': 0, 'GPE': 0, 'LANGUAGE': 0, 'LAW': 0, 'LOC': 0, 'MONEY': 0, 'NORP': 0, 'ORG': 0, 'PERSON': 0}  # TODO: change label names here

    for eg in examples_pretrained_ner:
        labels = [span["label"] for span in eg.get("spans", [])]
        # print(labels)
        count = Counter(labels)  # a dictionnary Counter({'GPE': 5, 'DATE': 3, 'PERSON': 3, 'ORG': 1})
        # print(count)

        dict = Counter(count) + Counter(dict)

    print(dict)
    print(sum(dict.values()))

if __name__ == '__main__':

    #label_distributions_first_ner(dataset_name= "first_ner")
    # result : Counter({'DATE': 675, 'PERSON': 593, 'GPE': 503, 'ORG': 178})

    #label_distribution_credibility_ner(dataset_name= "new_credib") # this dataset shows only one credib label instead of 4

    # label_distribution_9labels_ner(dataset_name="9labels_ner") # all original annotation
    # label_distribution_9labels_ner(dataset_name="last_reviewed") # reviewed dataset
    label_distribution_9labels_ner(dataset_name="NEW_SCRATCH1") # -- use this one
    # label_distribution_9labels_ner(dataset_name="all_labels")  # -- use this one

    label_label_distribution_pretrained_main_ner_cluster(dataset_name="NEW_SCRATCH1")
    #label_label_distribution_pretrained_main_ner_cluster(dataset_name="main_pretrained")

