# https://github.com/explosion/sense2vec#recipe-sense2vecteach
# using sense2vec from explosion
# trained on reddit 2019
import glob
from pathlib import Path
from sense2vec import Sense2VecComponent, Sense2Vec
import spacy
import pandas as pd
import glob
from pathlib import Path



path_reddit_vectors = "/s2v_reddit_2019_lg"
s2v = Sense2Vec().from_disk(path_reddit_vectors)
#path_pretrained_vectors_cluster = "/home/s2113351/NER_decisions/s2v_reddit_2019_lg"
#s2v = Sense2Vec().from_disk(path_pretrained_vectors_cluster)

#nlp = spacy.load("en_core_web_lg")
#s2v = nlp.add_pipe("sense2vec")
#s2v.from_disk(path_reddit_vectors)

#read data_first_page with glob
def read_txt_files(source_folder):
    source_folder = Path(source_folder).expanduser()
    txt_files = glob.glob(f"{source_folder}/*.txt")
    return txt_files

def set_keywords_from_canlii_csv(csv_keywords_path):
    ####### here we create a list of unique words from canlii keywords
    ####### in order to gather keywords to be used in our patterns
    ####### then we will need to separate by label
    ####### we downloaded keywords together with the links of the files in .csv

    # create a list of unique keywords, i.e. we delete keywords that are found multiple times
    set_keywords = []

    # transform the csv to a dataframe
    mydf = pd.read_csv(csv_keywords_path, sep=';', usecols=['keywords'])
    print(mydf.head())

    # transform col of the df into a list of keywords
    list_keywords = mydf.keywords.values.tolist() #this is a list of strings

    keywords = []
    for s in list_keywords:
        s = s.split(' — ')
        for word in s:
            print(word)
            keywords.append(word)


    # using the set function to create list
    set_keywords = set(keywords)
    type(set_keywords)
    print(len(set_keywords)) # we get 3020 different keywords
    print( "The distinct keywords for all decisions are: " + str(set_keywords))

    return set_keywords

def get_correlations(phrase):
    """
    :param phrase: phrase/keyword(s) as a string
    :return: tuples containing most similar strings, depending on the defined parameters of similarity
    output looks like this:
    ('machine learning', 'NOUN'), 0.8986967)
    ((word, sense), score) where sense is the POS tag
    """

    nlp = spacy.load('en_core_web_lg')

    # path = Path(__file__).parent.joinpath("s2v_old")
    path = Path(__file__).parent.joinpath("s2v_reddit_2019_lg") #too large in memory for PyCharm
    s2v = Sense2VecComponent(nlp.vocab).from_disk(path)
    nlp.add_pipe(s2v)

    doc = nlp(phrase)

    assert doc[:].text == phrase # searching for my input keyword in the pretrained text

    # frequencies of the keys in the table, in descending order
    freq = doc[:]._.s2v_freq # frequency of the given key

    vector = doc[:]._.s2v_vec # vector of the given key

    #using try/except in case the keyword is not found at all in word2vec
    try:
       # finding the first 10 correlated words
       # semantic similarity estimate of two keys or two sets of keys.
       # The default estimate is cosine similarity using an average of static_vectors
       closest_words = doc[:]._.s2v_most_similar(10) # returns a list
       print(closest_words)

    except ValueError:
       print('Nothing found in sense2vec.')
       return ([])

    # similarity score for correlation btw words is set to 70%
    similar_words = [w[0][0] for w in closest_words if w[1] > 0.70]

    return similar_words

def clean_vocab_files(txt_file_folder):
    """
    :param txt_file_folder: path ot the folder containing the vocab.txt files
    :return: returns a string of terms, cleaned, removing newlines and spaces
    """

    txt_files = read_txt_files(txt_file_folder) #gets list of the files paths in the folder

    for file in txt_files:

        with open(file, 'r') as f:
            print(f"----------------{file} ------------------------ ")
            txt = Path(file).read_text() #get a string for each text file
            txt = txt.lower()
            txt = txt.strip() #removes end and start whitespaces
            txt = txt.replace('\n', ', ') #removing newlines

        print(txt)


def merge_patterns_jsonl (path_file1, path_file2, output_file_path = " "):

    file1 = glob.glob(path_file1)
    file2 = glob.glob(path_file2) # output is a list
    file_list = file1 + file2

    with open(f"{output_file_path}.jsonl", "w") as outfile:
        outfile.write('{}'.format(''.join([open(f, "r").read() for f in file_list])))








if __name__ == "__main__":


    # csv_keywords_path = "/home/clairebarale/PycharmProjects/refugee_cases_analysis/cases-collected_2022-10-24-13-26-00.csv"
    # we want to take only the column called "keywords"

    # prints a list of unique keywords from Canlii (from the download)
    #set_keywords_from_canlii_csv(csv_keywords_path)

    # directory containing one .txt per labels with examples
    #vocab_base_directory = "/home/clairebarale/PycharmProjects/NER/vocab_txt"

    #get_correlations("fear of persecution") # TODO: does not work, investigate. Not needed for now

    #clean_vocab_files("/home/clairebarale/PycharmProjects/NER/vocab_txt")

    path_alleged_facts1 = "/pattern_files/alleged_facts1.jsonl"
    path_alleged_facts2 = "/pattern_files/alleged_facts_patterns.jsonl"

    path_citations = "/pattern_files/citations.jsonl"

    path_claimant_event1 = "/pattern_files/claimant_event_patterns.jsonl"

    path_claimant_info1 = "/pattern_files/claimant_info1.jsonl"
    path_claimant_info2 = "/pattern_files/claimant_info_patterns.jsonl"

    path_credib_allegations1 = "/pattern_files/credib_allegations1.jsonl"
    path_credib_allegations2 = "/pattern_files/credib_allegations_patterns.jsonl"

    path_credib_doubt1 = "/pattern_files/credib_doubt1.jsonl"
    path_credib_doubt2 = "/pattern_files/credib_doubt_patterns.jsonl"

    path_credib_evidence1 = "/pattern_files/credib_evidence1.jsonl"
    path_credib_evidence2 = "/pattern_files/credib_evidence__patterns.jsonl"

    path_credib_inconsistency = "/pattern_files/credib_inconsistency_patterns.jsonl"

    path_determination = "/pattern_files/determination.jsonl"

    path_doc_evidence1 = "/pattern_files/doc_evidence1.jsonl"
    path_doc_evidence2 = "/pattern_files/doc_evidence_patterns.jsonl"

    path_explanation1 = "/pattern_files/explanation1.jsonl"
    path_explanation2 = "/pattern_files/explanation_patterns.jsonl"

    path_legal_ground1 = "/pattern_files/legal_ground_1.jsonl"
    path_legal_ground2 = "/pattern_files/legal_ground_patterns.jsonl"

    path_procedure1 = "/pattern_files/procedure1.jsonl"
    path_procedure2 = "/pattern_files/procedure_patterns.jsonl"

    #merge_patterns_jsonl(path_procedure1, path_procedure2, output_file_path="./final_patterns/procedure")
    #merge_patterns_jsonl(path_legal_ground2, path_legal_ground1, output_file_path="./final_patterns/legal_ground")
    #merge_patterns_jsonl(path_explanation2, path_explanation1, output_file_path="./final_patterns/explanation")
    #merge_patterns_jsonl(path_doc_evidence1, path_doc_evidence2, output_file_path="./final_patterns/doc_evidence")
    #merge_patterns_jsonl(path_credib_evidence1, path_credib_evidence2, output_file_path="./final_patterns/credib_evidence")
    #merge_patterns_jsonl(path_credib_doubt1, path_credib_doubt2, output_file_path="./final_patterns/credib_doubt")
    #merge_patterns_jsonl(path_credib_allegations1, path_credib_allegations2, output_file_path="./final_patterns/credib_allegations")
    #merge_patterns_jsonl(path_claimant_info1, path_claimant_info2, output_file_path="./final_patterns/claimant_info")
    #merge_patterns_jsonl(path_alleged_facts1, path_alleged_facts2, output_file_path="./final_patterns/alleged_facts")

    # creating one pattern file for all credibility labels DATASET 1

    path_credib1 = "/final_patterns/credib_allegations.jsonl"
    path_credib2 = "/final_patterns/credib_doubt.jsonl"
    path_credib3 = "/final_patterns/credib_evidence.jsonl"
    path_credib4 = "/final_patterns/credib_inconsistency_patterns.jsonl"
    #merge_patterns_jsonl(path_credib1, path_credib2, output_file_path= "./pattern_files/temp_credib1")
    #merge_patterns_jsonl(path_credib3, path_credib4, output_file_path="./pattern_files/temp_credib2")
    path_file1 = "/pattern_files/temp_credib1.jsonl"
    path_file2 = "/pattern_files/temp_credib2.jsonl"
    #merge_patterns_jsonl(path_file1, path_file2, output_file_path="./final_patterns/credibility_label_patterns.jsonl")

    # creating one pattern file for all 9 remaining labels DATASET 2

    path1 = "./final_patterns/alleged_facts.jsonl"
    path2 = "./final_patterns/citations.jsonl"
    path3 = "./final_patterns/claimant_event_patterns.jsonl"
    path4 = "./NER/final_patterns/claimant_info.jsonl"
    path5 = "./NER/final_patterns/determination.jsonl"
    path6 = "./NER/final_patterns/doc_evidence.jsonl"
    path7 = "./NER/final_patterns/explanation.jsonl"
    path8 = "./NER/final_patterns/legal_ground.jsonl"

    path9 = "./NER/final_patterns/procedure.jsonl"

    #merge_patterns_jsonl(path1, path2, output_file_path= "./pattern_files/temp_output1")
    #merge_patterns_jsonl(path3, path4, output_file_path= "./pattern_files/temp_output2")
    #merge_patterns_jsonl(path5, path6, output_file_path= "./pattern_files/temp_output3")
    #merge_patterns_jsonl(path7, path8, output_file_path= "./pattern_files/temp_output4")

    path_output1 = "../pattern_files/temp_output1.jsonl"
    path_output2 = "../pattern_files/temp_output2.jsonl"
    path_output3 = "../pattern_files/temp_output3.jsonl"
    path_output4 = "../pattern_files/temp_output4.jsonl"

    #merge_patterns_jsonl(path_output4, path_output3, output_file_path= "./pattern_files/temp_output11")
    #merge_patterns_jsonl(path_output2, path_output1, output_file_path= "./pattern_files/temp_output12")

    path_output11 = "../pattern_files/temp_output11.jsonl"
    path_output12 = "../pattern_files/temp_output12.jsonl"
    #merge_patterns_jsonl(path_output11, path_output12, output_file_path= "./pattern_files/temp_output_111")

    path_output_111 = "../pattern_files/temp_output_111.jsonl"

    merge_patterns_jsonl(path_output_111, path9, output_file_path="./final_patterns/9labels_patterns")
