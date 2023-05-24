from bs4 import BeautifulSoup
import re
import glob
from pathlib import Path
import pandas as pd
import numpy as np
from nltk.tokenize import sent_tokenize
from joblib import Parallel, delayed
import multiprocessing
from sklearn.utils import shuffle
import tqdm

# initialize for basic text cleaning
nls = re.compile(r'(?<![\r\n])(\r?\n|\n?\r)(?![\r\n])')
spaces = re.compile(r'\s+')
html_tags = re.compile(r'\xa0')
paragraph_brackets = re.compile(r'\[\d+]')


def clean_text_html_decision(list_paragraphs):
    """
    :param list_paragraphs: is the list of strings from one single decisions.
    :return: the list of strings cleaned, containing only the main text we want to keep
    """
    clean_list_paragraphs = []
    for item in list_paragraphs:
        # lowercase every strings
        item = item.lower()

        # Remove multiple consecutive spaces
        clean = spaces.sub(' ', item)

        #removing beginning of paragraph that have brackets and number in that formtt [XX]
        clean = paragraph_brackets.sub('', item)

        # Remove random newlines
        clean = nls.sub(' ', clean)
        clean_list_paragraphs.append(clean)

    clean_list_paragraphs = list(filter(None, clean_list_paragraphs))

    return clean_list_paragraphs

def clean_extract_main_paragraphs(mylist):
    """
    :param mylist: list in which the text is cleaned but still contains the first page
    :return: list that contains only the paragraphs of the main text
    We delete everything that has less than 10 words in the string, assuming that paragraphs of text are longer
    """
    mylist = ([item for item in mylist if len(item.split())>5 ])

    return mylist

def clean_extract_first_last_paragraphs(mylist):
    # get the first and last paragraphs only
    # remove the following if you want the whole text/ all paragraphs
    new_list = []

    # first_paragraphs = mylist[:2]
    last_paragraphs = mylist[-10:]

    #new_list = first_paragraphs+last_paragraphs
    new_list = last_paragraphs
    return new_list

def clean_list_footnotes(clean_list):

    clean_list = ([item for item in clean_list if "CISR" not in item])
    clean_list = ([item for item in clean_list if "Direction des services de révision" not in item])
    clean_list = ([item for item in clean_list if "344 Slater Street" not in item])
    clean_list = ([item for item in clean_list if "Under section 72" not in item])
    clean_list = ([item for item in clean_list if "Canlii" not in item])
    clean_list = ([item for item in clean_list if "exhibit" not in item])
    clean_list = ([item for item in clean_list if "judicial review" not in item])

    return clean_list

def paragraphs_to_list(html_doc_path):
    """
    :param path_html: path the the HTML file
    :return: list of paragraphs, all clean, ready to be used
    """

    # HTML parser, using BeautifulSoup
    f = open(html_doc_path, 'r', encoding="utf8")
    soup = BeautifulSoup(f, 'html.parser')

    # print(soup.prettify()) # displays whole file with indententation and html tags

    # print(len(soup.find_all("p"))) #gets the number of b tags in the whole html doc

    # loop to get all the b tags of the html
    #for b in soup.find_all("b"):
        #text = p.get_text()
        #print(text)

    # loop to get all the tags of the html
    text = []
    for p in soup.find_all("p"):
        # print(p)
        text.append(p.get_text(strip=True))

    #basic cleaning to get only the text of decision by paragraph
    clean_list = clean_text_html_decision(text)

    # now we want to remove the text of the first page and of the footnotes
    # the goal is to keep only the main text
    main_paragraphs = clean_extract_main_paragraphs(clean_list) # returns a list of main paragraphs
    main_paragraphs = clean_list_footnotes(main_paragraphs)

    return main_paragraphs

def sentences_to_list(html_doc_path):
    """
        :param path_html: path the the HTML file
        :return: list of sentences, all clean, ready to be used
        """

    # HTML parser, using BeautifulSoup
    f = open(html_doc_path, 'r', encoding="utf8")
    soup = BeautifulSoup(f, 'html.parser')
    # print(html_doc_path)

    #print(soup.prettify()) # displays whole file with indententation and html tags

    # print(len(soup.find_all("p"))) #gets the number of b tags in the whole html doc

    # loop to get all the b tags of the html
    # for b in soup.find_all("b"):
    # text = p.get_text()
    # print(text)


    # loop to get all the tags of the html
    text = []
    for p in soup.find_all("p"):
        text.append(p.get_text(strip=True))

    # basic cleaning to get only the text of decision by paragraph
    clean_list = clean_text_html_decision(text)

    # now we want to remove the text of the first page and of the footnotes
    # the goal is to keep only the main text
    main_paragraphs = clean_extract_main_paragraphs(clean_list)
    main_paragraphs = clean_list_footnotes(main_paragraphs) # is a list


    # get only last and first paragraphs -- remove the following commands if you want the whole text
    #main_paragraphs = clean_extract_first_last_paragraphs(main_paragraphs)

    main_text_sentences = []
    for paragraph in main_paragraphs:
        sentences = sent_tokenize(paragraph)
        main_text_sentences.append(sentences)

    # Tanawat tells me to write a comment that it's flattening the list of lists
    main_text_sentences = [item for sublist in main_text_sentences for item in sublist]
    f.close()
    return main_text_sentences

def html_directory_to_dict(base_path_root_html_folder):
    # this function creates a dict
    # key is the decision id
    # value is a list of paragraphs (for one single decision)

    # gets path for html files
    source_folder_html = Path(base_path_root_html_folder).expanduser()

    # get all files in the folder as a list of paths
    files_list_html = glob.glob(f"{source_folder_html}/*.html")
    print(f"-- Folder {base_path_root_html_folder} holds {len(files_list_html)} .html files")

    # creating the dict, key will be the decision id, then each value is a paragraph
    dict_main_text = {}

    # analysis/run statistics
    n_files = 0

    for path in tqdm.tqdm(files_list_html):
        # HTML parser, using BeautifulSoup
        f = open(path, 'r', encoding="utf8")

        n_files += 1

        # prints the text of the tile, e.g. 2004 CanLII 69483 (CA IRB) | Mohammed v. Canada (Citizenship and Immigration) | CanLII
        #fileid = soup.title.string

        # getting the key for the dictionary ie the decision id
        # 2004canlii69525.html -- get the decision Id as key to the created dict
        with open(path, "r", encoding='utf8') as fileid:
            decision_id = re.search('(?<=canlii)\d{1,6}(?=\.html)', path)

            if decision_id:
                decision_id = decision_id[0]
            else:
                decision_id = "no_match_filename"

        # create a list per decision, that is stored as value in the dict
        # add one entry to the list per paragraph in decision
        # key is the decisionID, value is a list of paragraphs as text strings
        dict_main_text[decision_id] = []

        # we get here a list of paragraphs as strings
        # each item of the list is a paragraph
        # this is for a single decision
        main_text = sentences_to_list(path) # a list of sentences per decision

        # if wanna use paragraphs
        #main_text = paragraphs_to_list(path)

        for item in main_text:
            dict_main_text[decision_id].append(item)

    print(f"{n_files} from the HTML folder have been processed")
    return dict_main_text

    print(f"----------------------------------------------------")
    print(f"Files processed: %d" % n_files)

def list_to_dataframe(mylist):
    """
    :param mylist: list of paragraphs for one single html file
    :return: a daframe for one single file, ie we get one dataframe per decision
    """
    mydf = pd.DataFrame (mylist, columns = ['text'])

    return mydf

def df_to_jsonfile(df, output_json = ""):
    json_clean_txt = df.to_json(orient="records")
    jsonFile = open(f"{output_json}", "w")
    jsonFile.write(json_clean_txt)
    jsonFile.close()
    return jsonFile

def process_chunk(files_list_html):
    list_all_decisions = []
    for path in files_list_html:

        # HTML parser, using BeautifulSoup
        f = open(path, 'r', encoding="utf8")
        soup = BeautifulSoup(f, 'html.parser')

        #n_files += 1

        # we get here a list of paragraphs as strings
        # each item of the list is a paragraph
        # this is for a single decision
        #main_text = paragraphs_to_list(path)

        # if you want a list of sentences:
        main_text = sentences_to_list(path)

        list_all_decisions = list_all_decisions + main_text
    return list_all_decisions

if __name__ == '__main__':

    print("starting script")

    #base_path_root_html_folder= "/home/clairebarale/PycharmProjects/refugee_cases_analysis/tar_html/HTML-inputfile-cases-collected_2022-10-24-13-26-00.csv-nowis2022-10-24-15-52-54"
    base_path_root_html_folder = "/home/s2113351/Refugee_cases/extract_items/data/HTML_files"
    #base_path_root_html_folder = "/home/clairebarale/PycharmProjects/NER/test_html" #test folder with 3 html decisions

    # gets path for html files
    source_folder_html = Path(base_path_root_html_folder).expanduser()

    # get all files in the folder as a list of paths
    files_list_html = glob.glob(f"{source_folder_html}/*.html")
    print(f"-- Folder {base_path_root_html_folder} holds {len(files_list_html)} .html files")

    # analysis/run statistics
    #n_files = 0

    #n_cores = multiprocessing.cpu_count()
    #print(f"running in parallel on {n_cores} cores...")
    #files_list_html_chunks = np.array_split(files_list_html, n_cores)

    #results = Parallel(n_jobs=n_cores)(delayed(process_chunk)(files_list_html_chunks[i]) for i in range(0, n_cores))

    # flatten a list of lists to a single list
    #list_all_decisions = [item for sublist in results for item in sublist]

    #mydf = list_to_dataframe(list_all_decisions) # creates a dataframe with all paragraphs, one per row

    print(f"----------------------------------------------------")
    #print(f"Files processed: %d" % n_files)

    ############################ using dict ####################################################
    # useful if I need to keep the decision IDs. I.e. not needed to create a json for annotation

    # process html folder, and get a dict containing one list of paragraphs per decision
    dict_main_text = html_directory_to_dict(base_path_root_html_folder)

    # write dict to a dataframe
    mydf = pd.DataFrame.from_dict(dict_main_text, orient='index')
    mydf.index.name = "decisionID"
    mydf.reset_index(inplace=True)
    print(mydf.head())
    value_list = [col for col in mydf.columns if col != "decisionID"]
    mydf = pd.melt(mydf, id_vars=["decisionID"], value_vars=value_list,
            value_name='Text').drop('variable', axis=1)
    print(mydf.head())

    #############################################################################################

    # clean the dataframe by removing rows which contain "False" for the 1st page
    #mydf = mydf[mydf.iloc[:, 0] != 'False']
    #mydf = shuffle(mydf) # using sklearn utils function
    #print(mydf.head())


    ############### creating data_first_page ready to be annotated on Prodigy ##############################
    #df_to_jsonfile(mydf, output_json="last_sentences.json")
    #print(mydf.head())
    #print(mydf.tail())

    #############################################################################################
    mydf.to_csv("/home/s2113351/Refugee_cases/extract_items/data/all_sentences+decisionID.csv", sep=';', header=True, index=True)
