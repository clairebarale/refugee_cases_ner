import jsonlines
import pandas as pd

def df_to_jsonfile(df):
    json_lines = df.to_json(orient='records', lines=True)
    jsonFile = open("data_maintext_final/old_and_backups/sentences_lines.jsonl", "w")
    jsonFile.write(json_lines)
    jsonFile.close()
    return jsonFile


if __name__ == "__main__":
    jsonfile = "./data_maintext_final/old_and_backups/text_tokenized_by_sentences.json"

    mydf = pd.read_json(jsonfile)
    print(mydf.head())
    print(len(mydf.index))
    df_to_jsonfile(mydf)
