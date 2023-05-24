import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


def split_data(json_file, train_set_size, validation_set_size, output_train = "", output_dev = "", output_test = ""):
    """
    :param json_file: the json file downloaded from prodigy
    train set would usually be 0.8, validation 0.2
    validation is then divided in half between test and dev set
    :return: 3 json files. one for train, one for test, one for dev.
    you have to indicate the paths of the output files in the function
    """

    mydf = pd.read_json(json_file, lines=True)

    #cleaning the df from decisions without any annotations

    # converting col into strings (otherwise gives a NaN)
    #mydf["tokens"] = mydf["tokens"].astype(str)
    #mydf["spans"] = mydf["spans"].astype(str)
    #mydf["_is_binary"] = mydf["_is_binary"].astype(bool)
    #mydf["_timestamp"] = mydf["_timestamp"].astype(str)

    print(mydf.head())

    # split_pretrained between train and test set
    train, validation = train_test_split(mydf, test_size=validation_set_size, train_size=train_set_size, shuffle=True)
    # outputs 2 dataframe
    print(validation.head())
    print(train.head())

    # then we need to split_pretrained the validation set in half into dev and test for spacy
    # dev is used during training
    # test is used for evaluation after training
    dev, test = train_test_split(validation, test_size=0.5, train_size=0.5, shuffle=True)

    # print (train, dev, test)

    # then we convert it back to json format
    # from json it is easier to format for spacy encoding as a next step

    # create json for train set
    train_set = train.to_json(orient="records", lines = True)
    jsonFile_train = open(f"{output_train}", "w")
    jsonFile_train.write(train_set)
    jsonFile_train.close()

    # create json for test set
    test_set = test.to_json(orient="records", lines=True)
    jsonFile_test = open(f"{output_test}", "w")
    jsonFile_test.write(test_set)
    jsonFile_test.close()

    # create json for dev test
    dev_set = dev.to_json(orient="records", lines=True)
    jsonFile_dev = open(f"{output_dev}", "w")
    jsonFile_dev.write(dev_set)
    jsonFile_dev.close()

    return jsonFile_dev, jsonFile_test, jsonFile_train



if __name__ == '__main__':

    #for_first_page_split()

    #split_data("/home/clairebarale/PycharmProjects/NER/data_maintext_final/annotation_main_pretrained_labels_with_law.jsonl", train_set_size=0.8, validation_set_size=0.2,
               #output_train="/home/clairebarale/PycharmProjects/NER/data_maintext_final/split_pretrained/train_set_pretrained.jsonl",
               #output_dev="/home/clairebarale/PycharmProjects/NER/data_maintext_final/split_pretrained/dev_set_pretrained.jsonl",
               #output_test="/home/clairebarale/PycharmProjects/NER/data_maintext_final/split_pretrained/test_set_pretrained.jsonl")

    split_data("./extract_items/data/main_text/category_pretrained_may23/merged_all_new_pretrained.jsonl", train_set_size=0.8, validation_set_size=0.2,
               output_train="./extract_items/data/main_text/category_pretrained_may23/train_set_scratch.jsonl",
               output_dev="./extract_items/data/main_text/category_pretrained_may23/dev_set_scratch.jsonl",
               output_test="./extract_items/data/main_text/category_pretrained_may23/test_set_scratch.jsonl")

    #split_data("/home/clairebarale/PycharmProjects/NER/data_1stpage_final/346_first_ner_annotations.jsonl", train_set_size=0.8, validation_set_size=0.2,
    #           output_train="/home/clairebarale/PycharmProjects/NER/data_1stpage_final/train_set.jsonl",
    #           output_dev= "/home/clairebarale/PycharmProjects/NER/data_1stpage_final/dev_set.jsonl",
    #           output_test= "/home/clairebarale/PycharmProjects/NER/data_1stpage_final/test_set.jsonl")



