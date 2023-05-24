# script to transform the data_first_page to the spacy format
# input is the data_first_page downloaded from prodigy using db-out

from pathlib import Path
import spacy
import srsly
import typer
from spacy.tokens import Doc, DocBin
from spacy.util import get_words_and_spaces

def main(
    input_path: Path = typer.Argument(..., exists=True, dir_okay=False),
    output_path: Path = typer.Argument(..., dir_okay=False),
):
    """Preprocess JSON files into the .spacy filetype
    input_path (Path): path to the JSON file
    output_path (Path): xxx path once saved to the spaCy format
    """
    nlp = spacy.blank("en")
    doc_bin = DocBin(attrs=["ENT_IOB", "ENT_TYPE"])  # we're just concerned with NER

    for eg in srsly.read_jsonl(input_path):
            if eg["answer"] != "accept":
                continue
            tokens = [token["text"] for token in eg["tokens"]]
            words, spaces = get_words_and_spaces(tokens, eg["text"])
            doc = Doc(nlp.vocab, words=words, spaces=spaces)
            doc.ents = [
                doc.char_span(int(s["start"]), int(s["end"]), label=s["label"])
                for s in eg.get("spans", [])
            ]
            doc_bin.add(doc)
    doc_bin.to_disk(output_path)
    print(f"Processed {len(doc_bin)} documents: {output_path.name}")

if __name__ == "__main__":
    typer.run(main)