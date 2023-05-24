import pandas as pd
from fuzzywuzzy import fuzz
import re
from tqdm import tqdm
from datasets import load_dataset, Features, Value
import multiprocessing

def get_text_in_list(df):
    my_texts = []
    for index, row in df.iterrows():
        for myobj in row["text"]:
            my_texts.append(row["text"])
    return my_texts

def ratio_levenshtein_similarity(str1, str2):
    #fuzz uses Levenshtein Distance
    # will return 100 if there is a word match
    similarity_ratio = fuzz.token_set_ratio(str1, str2)
    # print(similarity_ratio)
    return similarity_ratio

if __name__ == "__main__":

    ######### the files containing the annotations:
    source_jsonl_scratch = "./extract_items/data/main_text/category_from_scratch_may23/merged_all_new_scratch.jsonl"
    source_jsonl_pretrained = "./extract_items/data/main_text/category_pretrained_may23/merged_all_new_pretrained.jsonl"

    df1 = pd.read_json(source_jsonl_pretrained, lines=True)
    df2 = pd.read_json(source_jsonl_scratch, lines=True)
    my_texts1 = get_text_in_list(df1)
    my_texts2 = get_text_in_list(df2)
    my_text = my_texts1 + my_texts2 # my list containing all sentences that have been annotated
    print(f"Total number of sentences with annotations:  {len(my_text)}")  # 1,643,592 sentences annotated
    my_text = set(my_text)
    my_text = list(my_text)
    print(f"Total number of sentences with annotations:  {len(my_text)}") # 5,483 unique sentences annotated

    #################### the files containing the "DETERMINATION" sentences:
    # delete sentences containing determination bc they are too similar in btw cases
    determinations_sentences_file = "/home/clairebarale/PycharmProjects/legal_prediction/data/determinations_sentences/sentences+decision_label.csv"
    df_determination = pd.read_csv(determinations_sentences_file, usecols=["extracted_sentences_determination"], sep=";")
    df_determination["extracted_sentences_determination"] = df_determination["extracted_sentences_determination"].apply(lambda x: x.strip('[\'')).replace('')
    df_determination["extracted_sentences_determination"] = df_determination["extracted_sentences_determination"].apply(lambda x: x.strip('\']')).replace('')
    det_sentences = df_determination.values.tolist()
    list_det_sentences = [item for sublist in det_sentences for item in sublist]
    # print(len(list_det_sentences))
    list_det_sentences = set(list_det_sentences)
    list_det_sentences = list(list_det_sentences)
    # print(len(list_det_sentences))

    ########### Pre-processing:
    #TODO: uncomment the following loops
    sent_flagged = []
    for sentence in tqdm(list_det_sentences):
        for annotated_sent in my_text:
            if ratio_levenshtein_similarity(sentence, annotated_sent)>90:
                my_text.remove(annotated_sent)
                sent_flagged.append(annotated_sent)
    print(f"Total number of sentences flagged as being DETERMINATION (ie to be removed):  {len(sent_flagged)}")
    print(f"Total number of sentences to retrieve:  {len(my_text)}")

    print("removing sentences that are too short...")
    for sentence in tqdm(my_text):
        if len(sentence)>5:
            my_text.remove(sentence)
    print(f"Total number of sentences to retrieve:  {len(my_text)}")

    # now mytext is the list of sentences that I need to attribute
    # eg. we want to search the text of cases and find to which case each sentence belongs

    ################ loading the file containing all sentences (HF):
    # If the dataset is gated/private, make sure you have run huggingface-cli login
    # loading from huggingface private repo
    # 180456248 rows in the csv
    n_cores = multiprocessing.cpu_count()
    print(f"We are running the program on {n_cores} CPU cores")
    file = {"cleaned_sentences_decisionID.csv"}
    dataset = load_dataset("clairebarale/Refugee_cases_allparagraphs_caseID", usecols=['Unnamed: 0',"decisionID", "Text"], data_files=file, sep=";", num_proc=n_cores)
    print(dataset)

    def match_sentences(example):
        for sentence in my_text:
            try:
                if sentence==example["Text"]:
                    id_canlii = example["decisionID"]
                    index = example['Unnamed: 0']
                    with open("./flagged_canlii_ids.txt", "a") as f:
                        f.write(f"{id_canlii}\n")
                        f.write(f"{sentence}\n")
                    with open("./list_idx.txt", "a") as file:
                        file.write(f"{index}\n")
                    my_text.remove(sentence)
            except:
                pass

    dataset.map(match_sentences, num_proc=n_cores)


"""
    # from local
    file = "/home/clairebarale/PycharmProjects/Refugee_cases/extract_items/data/all_sentences_decisionID.csv"
    dataset = load_dataset('csv', data_files=file, sep=";", usecols=["decisionID", "Text"], use)
    print(dataset)
    exit()

    #df_sentences = pd.read_csv("/home/clairebarale/PycharmProjects/Refugee_cases/extract_items/data/all_sentences+decisionID.csv", sep=";", usecols=["decisionID", "Text"])
    #df.drop(" Unnamed: 0", inplace=True)
    df_sentences.set_index("decisionID", inplace=True)

    df_sentences = df_sentences[:100]
    print(len(df_sentences))
    exit()

    
    print(f"running in parallel on {n_cores} cores...")

    chunk_size = int(df_sentences.shape[0] / n_cores)
    chunks = [df_sentences.iloc[df_sentences.index[i:i + chunk_size]] for i in range(0, df_sentences.shape[0], chunk_size)]
    print(chunks)
    exit()

    files_list_html_chunks = np.array_split(files_list_html, n_cores)

    results = Parallel(n_jobs=n_cores)(delayed(process_chunk)(files_list_html_chunks[i]) for i in range(0, n_cores))

    def process_chunk_df(chunked_df):
        list_matches = []
        for idx, row in tqdm(df_sentences.iterrows()):
            #print(row["Text"])
            for sentence in my_text:
                try:
                    if sentence in row["Text"]:
                        #print("found a match")
                        print(idx)
                        list_matches.append(idx)
                        # saving the canlii ID to a file
                        with open("./flagged_canlii_ids.txt", "a") as f:
                            f.write(f"{idx}\n")
                except:
                    pass
        print(len(list_matches))


    exit()


    #and return the canlii number? check how many and delete them?
"""




def get_judge_col_cross_comparison(df):
    """
    input: the 2 columns of the dataframe
    we compare the 2 col and find the common name. This name in common is the name of the judge
    :return: a list of judge names
    """
    list_judges = []

    for extracted_person, ner_output in zip(result_df["extracted_persons"], result_df["NER_output"]):
        # print(type(extracted_person), type(ner_output)) # extracted person is a list, ner_output a str
        ner_output = str(ner_output) # there is one type integer
        ner_output_as_list = re.sub("'", "", ner_output)
        ner_output_as_list = ner_output_as_list.strip('][').split(', ')
            # ner_output_as_list = ner_output_as_list.strip('][').split(' ')
            # print(ner_output_as_list)
            # converting my string-type list to list
            # print(type(extracted_person), type(ner_output_as_list))
            # ner_output_as_list = ast.literal_eval(ner_output)
        matches = set(extracted_person).intersection(ner_output_as_list)  # matches is a set, not a list (can convert set to list)
            # print(f"extracted: {extracted_person}, ner: {ner_output}, matches: {matches}")

        if matches == set():
            for item in ner_output_as_list:
                similarity_ratio = ratio_levenshtein_similarity(extracted_person, ner_output)
                if similarity_ratio == 100:
                    matches = item
                        # print(matches)

        list_judges.append(matches)

        # print(list_judges)
    return list_judges