import numpy as np 
import pandas as pd 
import re
import unicodedata
import tokenize_uk
import os

def get_path(path):
    """
    Get path to the file with texts.
    Check if the path exists.
    Get the absolute path to the file.
    """
    if not os.path.exists(path):
        return print("The path does not exist.")
    else:
        path = os.path.abspath(path)
        return path

def get_text(path):
    """
    Read the file with texts.
    If there are any empty cells in the "text" column, delete them.
    Return a list of texts.
    """
    df = pd.read_csv(path, sep=",", encoding="utf-8")
    if df["text"].isnull().values.any():
        df = df.dropna(subset=["text"])
        text = df.iloc["text"]
    else:
        text = df.iloc["text"]
    return text

def clean_text(line):
    replaced = re.sub('\n', '', line)
    right_quote = unicodedata.lookup('RIGHT DOUBLE QUOTATION MARK')
    left_quote = unicodedata.lookup('LEFT DOUBLE QUOTATION MARK')
    normalized = replaced.replace(right_quote, '\"').replace(left_quote, '\"')
    tokenized = ' '.join(tokenize_uk.tokenize_uk.tokenize_words(normalized))
    return tokenized



def write_to_file(data, path):
    """
    Write processed texts to file. 
    If a text consists of several sentences, each sentence is written on a new line.
    Create a list of lists, where each list contains a single processed text.
    """
    processed_texts = []
    for i in data:
        t = []
        line = clean_text(i)
        t.append(line)
        processed_texts.append(t)
    
    # Chech if the path exists
    if not os.path.exists(path):
        os.makedirs(path)

    # Write each text to a new file
    for text in enumerate(processed_texts):
        with open(path, + str(text[0]) + ".txt", "w", encoding="utf-8") as f:
            f.write("".join(text[1]))
            f.close
