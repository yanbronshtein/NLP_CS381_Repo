import gensim
import bz2


from pathlib import Path

path = input("Please enter the file path to the directory containing the file 'news.crawl.bz2.'\n")
data_folder = Path(path)
input_file = data_folder / "news.crawl.bz2"
tokenized_data = []

def read_input(input_file):
    with bz2.open(input_file, 'rb') as file:
        for line in file:
            tokenized_data.append(gensim.utils.simple_preprocess(line))
    file.close()

read_input(input_file)
