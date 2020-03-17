print("The parameters needed for unigram model predication are each word so i, look, forward, to, hearing, your , reply , and . " )


sentence_to_predict = "I look forward to hearing your reply ."
sentence_to_predict = sentence_to_predict.lower()
sentence_tokenized = sentence_to_predict.split()
uni_probability=1
calculations=""
parameters_0 = []
##log probability for unigram model
for word in sentence_tokenized:
    if unigram_model.get(word) != None:
        uni_probability*=unigram_model[word]
        calculations+=str(unigram_model[word]) + ' * '
    else:
        parameters_0.append(word)
print(calculations + ' = log(' +str(uni_probability) + ")")
print("the log probabilty based on the unigram model is: " + str(math.log(uni_probability,2)))
print("the parameters with 0 probability are below:")
print(parameters_0)