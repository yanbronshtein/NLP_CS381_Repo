import copy

# Source paths of train.txt and test.txt

path = "/Users/yanivbronshtein/Coding/QueensCollege/NLP_CS381_Repo/HW1"

sources = [path + "/train.txt", path + "/test.txt"]  # todo: change back to original nigga


# sources = [path + "/train_small.txt", path + "/test_small.txt"]


# This function is used to tokenize and path data read from train.txt and test.txt
def pad_and_tokenize_file_data(file_path):
    tokenized_padded_data = []
    with open(file_path) as file:
        for line in file:
            line = line.strip()
            if line:
                line = line.lower()
                tokenized_line = line.split()
                tokenized_line.insert(0, '<s>')  # Prepend start symbol
                tokenized_line.insert(len(tokenized_line), '</s>')  # Append stop symbol
                tokenized_padded_data.append(tokenized_line)
    file.close()
    return tokenized_padded_data


train_data_dict = {}


def pre_process_train_data(file_path):
    tokenized_train_data = pad_and_tokenize_file_data(file_path)

    for line in tokenized_train_data:
        for word in line:
            train_data_dict[word] = 1 if word not in train_data_dict else train_data_dict[word] + 1

    rare_words_dict = {key: value for (key, value) in train_data_dict.items() if
                       value == 1 and value != "<s>" and value !=
                       "</s>"}  # rare_words_dict contains only those words that are not start or end symbols that 
    # appear only once in training
    # those words that appear once in training

    # Replace each word in tokenized_train_data with <unk> if it only appears once in rare_words_dict 
    for line in tokenized_train_data:
        for i in range(0, len(line)):
            if line[i] in rare_words_dict:
                line[i] = "<unk>"

    return tokenized_train_data


def pre_process_test_data(file_path):
    tokenized_test_data = pad_and_tokenize_file_data(file_path)

    # Replace each word in tokenized_test_data with "<unk>" if it does not appear in testing
    for line in tokenized_test_data:
        for i in range(0, len(line)):
            if line[i] not in train_data_dict:
                line[i] = "<unk>"

    return tokenized_test_data


processed_train_data = pre_process_train_data(sources[0])
processed_test_data = pre_process_test_data(sources[1])


def count_total_word_tokens(data):
    token_count = 0
    for line in data:
        token_count += len(line)
    return token_count


# bigram_model = {}
# total_number_of_bigrams = 0
# tokenized_training_unk_splitted = tokenized_training_unk.split()
# for i in range(len(tokenized_training_unk_splitted)-1):
#     bigram_key = tokenized_training_unk_splitted[i] + "," + tokenized_training_unk_splitted[i+1]
#     if bigram_model.get(bigram_key) == None:
#         bigram_model[bigram_key] = 1
#     else:
#         bigram_model[bigram_key] = bigram_model[bigram_key] + 1
#     total_number_of_bigrams+=1


unique_word_count_training = len(train_data_dict)
print("Q1: How many word types (unique words) are there in the training corpus?\n "
      "Please include the padding symbols and the unknown token.\n" + str(unique_word_count_training))

total_word_count_training = count_total_word_tokens(processed_train_data)
print("Q2: How many word tokens are there in the training corpus?\n" + str(total_word_count_training))


def train_unigram_mle():
    unigram_model = copy.deepcopy(train_data_dict)

    for word in unigram_model:
        unigram_model[word] = unigram_model[word] / total_word_count_training

    return unigram_model


unigram_model = train_unigram_mle()
print("")

sum = 0
for word in unigram_model:
    sum += unigram_model[word]

print(sum)