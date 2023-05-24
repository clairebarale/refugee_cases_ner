import json
import glob

result = []
for f in glob.glob("/new_jsonl_annotations_may2023/scratch/*.jsonl"):
    with open(f) as infile:
        for line in infile.readlines():
            try:
                result.append(json.loads(line)) # read each line of the file
            except ValueError:
                print(f)

# This would output jsonl
with open('./new_jsonl_annotations_may2023/scratch/merged_all_new_scratch.jsonl', 'w') as outfile:
    #json.dump(result, outfile)
    #write each line as a json
    outfile.write("\n".join(map(json.dumps, result)))
