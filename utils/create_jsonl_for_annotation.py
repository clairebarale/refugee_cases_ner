import re

def clean_raw_text(raw_text):
    spaces = re.compile(r'\s+')
    clean_text = spaces.sub(' ', raw_text)
    clean_text = clean_text.lower()
    return clean_text

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



