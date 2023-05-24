import glob
import re
from pathlib import Path
import json
import PyPDF2
from PyPDF2 import PdfFileReader
from PyPDF2.errors import EmptyFileError
import spacy


hyphenspace = re.compile(r'-\s')
nls = re.compile(r'(?<![\r\n])(\r?\n|\n?\r)(?![\r\n])')
spaces = re.compile(r'\s+')

def clean_text(text):
    """
    :rtype: object
    :param text: str
    :return: str
    """
    #clean = re.sub('\n ', '', str(text))
    #clean = re.sub('\s', ' ', str(text))
    #clean = re.sub('\W', ' ', text)
    #clean = re.sub('\s', ' ', text)
    # removing apostrophes and \n
    clean = re.sub("[^a-zA-Z0-9 -]", ' ', text) # TODO: ne pas enlever les char avec accent
    # removing hyphens
    #clean = hyphenspace.sub('', clean)
    # Remove multiple consecutive spaces
    clean = spaces.sub(' ', clean)
    # Remove random newlines
    clean = nls.sub(' ', clean)
    #remove stopwords
    #stopw = set(stopwords.words('english'))  # build-in list of stop words
    #clean = "".join([w for w in clean if w not in stopw])
    # Other random cleaning - noise removal
    #clean = cleantext.clean(clean)
    #print(clean)
    return clean

def get_pdf_handle(file_path):
    return PyPDF2.PdfFileReader(file_path)

#read data_first_page with glob
def read_txt_files(source_folder):
    source_folder = Path(source_folder).expanduser()
    txt_files = glob.glob(f"{source_folder}/*.txt")
    return txt_files

def txt_to_csv(clean_txt):
    #split_pretrained and returs a list
    list_text_separated_by_full_stop = clean_txt.split(".") #splitlines()


    # iterate over list
    for sentence in list_text_separated_by_full_stop:
        sentences.append({'text': sentence})

def txt_to_json_clean(clean_txt):
    #split_pretrained and returs a list
    list_text_separated_by_full_stop = clean_txt.split(".") #splitlines()

    sentences = []
    # iterate over list
    for sentence in list_text_separated_by_full_stop:
        sentences.append({'text': sentence})

    # indent=None adds no indentation to the file (no new lines per "text" - important for prodigy)
    # indent=4 does not work either! (we need no spaces for "text" with prodigy)
    json_lines = [json.dumps(l, ensure_ascii=False, indent=None) for l in sentences]
    json_data = '\n'.join(json_lines)

    #with open('data0001.jsonl', 'w') as f:
    #        f.write(json_data)

def get_all_pages_str_from_pdf(pypdf2_pdf):
    return pypdf2_pdf.extractText()

def get_last_page_str_from_pdf(file_path):
    pdf = get_pdf_handle(file_path)
    n_pages = pdf.getNumPages()
    last_page = pdf.getPage(n_pages-1)
    return last_page.extractText()

faulty_empty_pdfs = 0
def get_pdf_first_page_text(pdf_file):
    try:
        mypdf = PyPDF2.PdfFileReader(pdf_file) # read the PDFs
        #numpages = mypdf.getNumPages()
        first_page = mypdf.getPage(0)
        return first_page.extractText()
    except EmptyFileError:
        global faulty_empty_pdfs
        faulty_empty_pdfs += 1
        return False

def create_data_to_dict(base_path_root):
    """
    :param base_path_root: base path of the PDF files folders
    :return: a dict, key is the number of a decision, value is the raw text of the first page
    """

    data = {}

    # analysis/run statistics
    n_files = 0


    # gets path for pdf
    source_folder_pdf = Path(base_path_root).expanduser()

    # get all files in the folder as a list of paths
    files_list_pdf = glob.glob(f"{source_folder_pdf}/*.pdf")
    print(f"-- Folder {base_path_root} holds {len(files_list_pdf)} .pdf files")

    # loop: per decision file
    for decision_file_path in files_list_pdf:
        #print(decision_file_path)
        first_page = get_pdf_first_page_text(decision_file_path)

        n_files += 1

        # 2002canlii52643.pdf -- get the decision Id as key to the created dict
        with open(decision_file_path, "r", encoding='utf8') as fileid:
            decision_id = re.search('(?<=canlii)\d{1,5}(?=\.pdf)', decision_file_path)
            if decision_id:
                decision_id = decision_id[0]
            else:
                decision_id = "no_match_filename"
            # add new item to dictionary per decision, iteratively
            # key is the decisionID, value is the text string of first page
            data[decision_id] = str(first_page)

    print(f"Files processed: %d" % n_files)
    print(f"----------------------------------------------------")

    return data

def process_by_row (df):
    """
    :param df: input is a df with index is the decision id and second col is the raw text
    loops through every row of the df, ie it processed one decision at a time
    :return: updates the dataframe with the column with the NER results
    """
    list_to_df = []
    for idx, row in df.iterrows():
        # each row into a list
        list_row = list(row)

        # basic text cleaning using clean_raw_text function
        # row_ner is the full pre-processed text of the first page of a decision
        mylist_clean_row = []
        for str in list_row:
            clean_string = clean_raw_text(str)
            mylist_clean_row.append(clean_string)
        row_ner = [ner(text) for text in mylist_clean_row]
        row_ner = list(ner.pipe(mylist_clean_row))

        # applying NER pipeline to row_ner, ie to one decision at a time
        my_ner_output =[]
        for item in row_ner:
            for ent in item.ents:
                output = [ent.text, ent.start_char, ent.end_char, ent.label_]
                my_ner_output.append(output)

        # my_ner_output: this returns a list of list, containing all entities for one decision
        list_to_df.append(my_ner_output) # is a list of lists of lists (oops)

    # write my_ner_output to dataframe
    df["pretrained_spacy_en_core_web_md"] = list_to_df
    # print(df.head())
    return list_to_df

def clean_raw_text(raw_text):
    spaces = re.compile(r'\s+')
    clean_text = spaces.sub(' ', raw_text)
    clean_text = clean_text.lower()
    return clean_text

ner = spacy.load("en_core_web_md", disable=["tagger", "parser", "attribute_ruler", "lemmatizer"])
def process_all_cells(df):
    """
    :param df: input is a dataframe
    :return: creates a list of strings out of the dataframe, and converts the list to a spacy nlp object.
    creates data_first_page that is in the right format to be used with spacy models
    """
    # transform cells of the df to a list of strings, each string in the list corresponding to one case
    # mylist = ["This is a text",
    #         "These are lots of texts",
    #        "..]
    list_all_first_page_text = list(df[0])

    #basic text cleaning using clean_raw_text funtion
    list_all_first_page_text_clean = []
    for str in list_all_first_page_text:
        clean_str = clean_raw_text(str)
        list_all_first_page_text_clean.append(clean_str)

    all_cases = [ner(text) for text in list_all_first_page_text_clean]
    all_cases = list(ner.pipe(list_all_first_page_text_clean))
    return all_cases

def creates_df_for_annotation (df):
    """
    :param df: input is a df with index is the decision id and second col is the raw text
    loops through every row of the df, ie it processed one decision at a time
    :return: returns a json
    """
    list_to_df = []
    for idx, row in df.iterrows():
        # each row into a list
        list_row = list(row)

        # basic text cleaning using clean_raw_text function
        mylist_clean_row = []
        for txt in list_row:
            clean_string = clean_raw_text(txt)
            mylist_clean_row.append(clean_string)
        all_decisions = list(mylist_clean_row)
        # this returns a list of list
        list_to_df.append(all_decisions) # is a list of lists of lists (oops)

    # write my_ner_output to dataframe
    df["clean_text"] = list_to_df
    df['text'] = [','.join(map(str, l)) for l in df['clean_text']]
    df = df.drop('text_first_page', axis=1)
    df = df.drop('clean_text', axis=1)
    #json_clean_txt = df.to_json(orient="records")
    #json_clean_txt = json.dumps(df)
    #dicts=df.to_dict('records')
    #df = df.reset_index(drop=True)
    return df

def df_to_jsonfile(df):
    json_clean_txt = df.to_json(orient="records")
    jsonFile = open("data_for_annotation.json", "w")
    jsonFile.write(json_clean_txt)
    jsonFile.close()
    return jsonFile

if __name__ == '__main__':
    # here we have the base path, later we add the trailing digits in a for loop
    base_path_root_all_pdfs = "/home/clairebarale/PycharmProjects/refugee_cases_analysis/pdf_tar/PDF-inputfile-cases-collected_2022-10-24-13-26-00.csv-nowis2022-10-28-16-45-40"

    data_dict = create_data_to_dict(base_path_root_all_pdfs)
    # data_first_page is a dict

    # create a pandas dataframe from a python dictionary
    mydf = pd.DataFrame.from_dict(data_dict, orient='index')
    mydf.columns = ["text_first_page"]

    # clean the dataframe by removing rows which contain "False" for the 1st page
    mydf = mydf[mydf.iloc[:, 0] != 'False']

    ############### creating data_first_page ready to be annotated on Prodigy ##############################
    df_clean = creates_df_for_annotation(mydf)
    # print(df_clean.head())

    # creates .csv file with one column only called text (required input format)
    df_clean.to_csv("data_for_prodigy.csv", encoding='utf-8', sep=";", index=False, header=True)

    # creates jsonfile ready to be annotated with prodigy
    # file is called: data_for_annotation.json
    df_to_jsonfile(df_clean)

    #############################################################################################

    # creates a CSV file from the df
    # use a seperator that is not used in the text of the first page
    # first column is the case number, second column is the raw text of the first page
    # mydf.to_csv("first_page_all_cases.csv", encoding='utf-8', sep=";", index=True, header=True)

    # loading pipeline

    #############################################################################################
    # Use this if you want to have all entities in one, not structured by decision
    # transforming the df to a list of strings
    # this is the format of input data_first_page required by spacy to operate their model
    # (the .tolist would create a list of lists instead which is why we dont use it)

    # mydata = process_all_cells(mydf)
    #############################################################################################

    # searching for entities at the document level, ie per each decision as one string of text
    # we add a column to the initial dataframe mydf and we add it to the CSV file
    # we add a header corresponding to the architecture used / model used

    mydata = process_by_row(mydf)  # mydata is a list

    # write the csv -- this overwrites and writes a whole new csv file
    # mydf.to_csv("first_page_all_cases.csv", encoding='utf-8', sep=";", index=True, header=True)

    # update the existing csv with a new column, not overwriting the columns stored before, just adds a new col
    newdf = pd.read_csv('first_page_all_cases.csv', encoding='utf-8', sep=";")
    newdf["model_prodigy_update_50annotations"] = mydata
    newdf.to_csv('first_page_all_cases.csv', encoding='utf-8', sep=";", index=True, header=True)



