import pandas as pd
from pandas.io.json import json_normalize
from pprint import pprint
import json
from pathlib import Path
import typer

def obj_dict(obj):
    return obj.__dict__

def main(
    label_to_search = typer.Argument(...),
    output_path: Path = typer.Argument(..., dir_okay=False),
):
    #"label":"LAW"
    #jsonfile = "annotations_main_label_scratch_COPY.jsonl"
    jsonfile = "/home/clairebarale/PycharmProjects/Refugee_cases/new_annotations.jsonl"
    df = pd.read_json(jsonfile, lines=True)

    mycollection = []
    for index, row in df.iterrows():
        for myobj in row["spans"]:
            if 'label' in myobj:
                if myobj["label"] == label_to_search:
                    mycollection.append(row)

    #pprint(mycollection)
    df_new = pd.DataFrame(mycollection)
    df_new2 = df_new.copy()

    #for index, row in df_new.iterrows():
    #    mylist = []
    #    for myobj in row["spans"]:
    #        if myobj["label"] == 'PROCEDURE':
    #            mylist.append(myobj)
    #    df_new2.at[index, "spans"] = mylist

    #df_new = df_new.drop("index", axis=1)
    #print(df_new.head(10))
    #print(df_new.columns.values)
    json_string = df_new2.to_json(orient="records", lines=True)
    #print(json.dumps(json_string, indent=4))
   # #pprint(mycollection)
   # print("Converting list to JSON.. ", end="", flush=True)
   # json_string = json.dumps(mycollection, default=obj_dict)
   # print("Done.")
    with open(output_path, 'w', encoding='utf-8') as f:
        print("Writing JSON to file.. ", end="", flush=True)
        f.write(json_string)
        #json.dump(json_string, f) #, ensure_ascii=False, indent=4)
        print("Done.")

if __name__ == "__main__":
    typer.run(main)

#Counter({'DATE': 247, 'GPE': 186, 'ORG': 135, 'CLAIMANT_EVENT': 57, 'PERSON': 49, 'LAW': 47,
# 'DOC_EVIDENCE': 35, 'EXPLANATION': 34, 'CREDIBILITY': 34, 'PROCEDURE': 25, 'NORP': 24, 'CLAIMANT_INFO': 17,
# 'DETERMINATION': 4, 'LEGAL_GROUND': 3, 'LAW_REPORT': 2, 'LAW_CASE': 1})
