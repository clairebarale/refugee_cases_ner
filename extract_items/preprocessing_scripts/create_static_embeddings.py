# Using GloVe
import numpy as np
from nltk.corpus import stopwords
import pandas as pd
import string
import csv
from collections import Counter
from mittens import Mittens
from sklearn.feature_extraction.text import CountVectorizer
import pickle

# Download GloVe vocabulary from: https://nlp.stanford.edu/projects/glove/

# convert my data from json to a list
def json_to_list(file_path = " "):
    mydf = pd.read_json(file_path)
    mylist = mydf.values.tolist()
    mylist = [item for sublist in mylist for item in sublist]
    return mylist

def clean_list(list):
    # is already all lower case
    # remove punctuation
    list = [line.translate(str.maketrans('', '', string.punctuation)) for line in list]
    list= [line.rstrip('“') for line in list]
    list = [line.rstrip('\'') for line in list]
    list = [line.rstrip('”') for line in list]

    # remove stopwords
    sw = stopwords.words('english')
    list = [w for w in list if w not in sw]
    return list

def glove2dict(glove_path=""):
    with open(f"{glove_path}") as f:
        reader = csv.reader(f, delimiter=' ', quoting=csv.QUOTE_NONE)
        embed = {line[0]: np.array(list(map(float, line[1:])))
                    for line in reader}
    return embed

def get_rareoov(xdict, val):
    return [k for (k,v) in Counter(xdict).items() if v<=val]

if __name__ == '__main__':

    # we need a co-occurence matrix and the associate vocabulary for our data
    # the we cam update Glove with it

    # input needs to be here a list of tokenized sentences

    print("Getting my data as a json file and preprocess it...")
    # file ="./data_maintext_final/cleaned_maintext__for_annotation_html.json"
    # file = "./NER_decisions/text_tokenized_by_sentences.json"
    # file = "/data_maintext_final/old_and_backups/cleaned_maintext__for_annotation_html.json"

    file = "/home/s2113351/NER_decisions/text_tokenized_by_sentences.json"
    # file ="./data_maintext_final/cleaned_maintext__for_annotation_html.json"


    #file = "./data_maintext_final/test.json"
    raw_text = json_to_list(file) #returns a flat list
    cleaned_sentences = clean_list(raw_text) # a list of sentences
    #print(len(cleaned_sentences))
    # result with all decisions: 2 391 630
    my_sentences= cleaned_sentences[:10000]

    print("Done! we have a clean list of sentences of length 15 000")
    print(len(my_sentences))


    # Common Crawl (840B tokens, 2.2M vocab, cased, 300d static_vectors, 2.03 GB download)
    # glove_path = "./glove.840B.300d.txt"
    # glove_path = "./glove.6B.300d.txt"

    # Wikipedia 2014 + Gigaword 5 (6B tokens, 400K vocab, uncased, 50d, 100d, 200d, & 300d static_vectors, 822 MB downloa
    small_glove_path = "./glove.6B.50d.txt"
    print("Load small glove embeddings")


    # load pretrained model and store static_vectors in a dict
    # static_vectors should be stored in a dict
    # key is the token and the value is the vector
    print("collecting glove static_vectors and storing them in a dict")
    pretrained_glove = glove2dict(glove_path=small_glove_path)
    print("Glove static_vectors collected")

    ########### VOCAB
    # building the vocab that is not present in pretrained Glove
    oov = [token for token in my_sentences if token not in pretrained_glove.keys()]

    # filter to keep only rare oov words has to be filtered out to save space
    # this step is optional
    oov_rare = get_rareoov(oov, 1)
    corp_vocab = list(set(oov) - set(oov_rare))

    # now remove rare oovs
    my_tokens = [token for token in my_sentences if token not in oov_rare]
    my_doc = [' '.join(my_tokens)]
    corp_vocab = list(set(oov)) # this is the vocabulary
    print("Data set vocabulary created")


    ############ MATRIX: Build the co-occurence matrix
    # Using CountVectorizer
    cv = CountVectorizer(ngram_range=(1, 1), vocabulary=corp_vocab)
    X = cv.fit_transform(my_doc)
    Xc = (X.T * X)
    Xc.setdiag(0)
    coocc_ar = Xc.toarray() # this it the co-occurence matrix, as an np array
    print("Co-occurence matrix created")

    ######## MITTENS MODEL TRAINING
    # Load the Mittens model
    mittens_model = Mittens(n=50, max_iter=1000) # 50 is the embedding dimension
    # Note: n must match the original embedding dimension
    print("Training step...")

    # Load cooccurrence matrix and vocab
    # Load the orgininal pretrained embeddings
    # Training step
    # new_embedding is a numpy array
    new_embeddings = mittens_model.fit(
        coocc_ar,
        vocab=corp_vocab,
        initial_embedding_dict=pretrained_glove)

    #new_embeddings = new_embeddings.flatten('C')
    print(new_embeddings)
    print(new_embeddings.shape)

    new_glove = dict(zip(corp_vocab, new_embeddings))
    #print(new_glove)

    # save file in a .txt, .zip or .tar format
    # first row contains the dimensions of the static_vectors
    # followed by a space-separated Word2Vec table
    f = open("./TESTS/repo_glove.pkl", "wb")
    pickle.dump(new_glove, f)
    f.close()

    np.savetxt("myfile_small_10000.txt", new_embeddings,delimiter=' ')
    print("Vectors saved to file!")











