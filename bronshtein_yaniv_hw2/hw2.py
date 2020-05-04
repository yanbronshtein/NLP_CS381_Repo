import gensim
import bz2
import logging
from pathlib import Path

# H.W 2 by Yaniv Bronshtein
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

#Set up path to get news.crawl.bz2
path = input("Please enter the file path to the directory containing the file 'news.crawl.bz2.'\n")
data_folder = Path(path)
input_file = data_folder / "news.crawl.bz2"

document = [] #Contains processed content of news.crawl.bz2
#This function decompresses the bz2 file in read binary mode, parses each line and
#outputs the log with every 10000 lines read
def read_input(input_file):
    logging.info("reading file {0}...this may take a while".format(input_file))
    with bz2.open(input_file, 'rb') as file:
        for line in file:
            document.append(gensim.utils.simple_preprocess(line))
            if len(document) % 10000 == 0:
                logging.info("read " + str(len(document)) + " reviews")
    file.close()


read_input(input_file)

# build vocabulary and train model for questions 1 and 2
first_model = gensim.models.Word2Vec(
    document,
    size=150,
    window=5,
    min_count=2,
    iter=10)


#Build and train model for question 2
second_model = gensim.models.Word2Vec(
    document,
    size=50,
    window=2,
    min_count=2,
    iter=10)

print(
    "Question 1. Report similarity scores for the following pairs: (dirty, clean), (big, dirty),(big, large) ,(big,small)\n")
print("Similarity (dirty,clean) {0}\n".format(first_model.wv.similarity(w1="dirty", w2="clean")))
print("Similarity (big,dirty) {0}\n".format(first_model.wv.similarity(w1="big", w2="dirty")))
print("Similarity (big,large) {0}\n".format(first_model.wv.similarity(w1="big", w2="large")))
print("Similarity (big,small) {0}\n".format(first_model.wv.similarity(w1="big", w2="small")))

print("Question 2. Report 5 most similar items and the scores to 'polite','orange'\n")
print("Most similar to 'polite' {0}".format(first_model.wv.most_similar(["polite"], topn=5)))
print("Most similar to 'orange' {0}".format(first_model.wv.most_similar(["orange"], topn=5)))



print("Question 3. Now change the parameters of your model, as follows: window=2, size=50.\n"
      "Answer the 2 questions above for this new model.")
print("Question 1 V2. Report similarity scores for the following pairs: (dirty, clean), (big, dirty),(big, large) ,"
      "(big,small)\n")
print("Similarity (dirty,clean) {0}\n".format(second_model.wv.similarity(w1="dirty", w2="clean")))
print("Similarity (big,dirty) {0}\n".format(second_model.wv.similarity(w1="big", w2="dirty")))
print("Similarity (big,large) {0}\n".format(second_model.wv.similarity(w1="big", w2="large")))
print("Similarity (big,small) {0}\n".format(second_model.wv.similarity(w1="big", w2="small")))

print("Question 2 V2. Report 5 most similar items and the scores to 'polite','orange'\n")
print("Most similar to 'polite' {0}".format(second_model.wv.most_similar(["polite"], topn=5)))
print("Most similar to 'orange' {0}".format(second_model.wv.most_similar(["orange"], topn=5)))
