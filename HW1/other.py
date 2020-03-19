txt = ""
f = open('train.txt', 'r',encoding='utf-8-sig')
x = f.readline()
before_unk_uni_gramMap = {}
after_unk_uni_gramMap = {}
bi_gramMap={}
after_unk_uni_gramMap["<unk>"] = 0
wTrain = 0
# read file ,lower case all word, add <s> </s>
while x:
    y = x.split(" ")
    txt += "<s> "
    for z in y:
        txt += z.lower() + " "
        wTrain += 1
    txt += "</s> "
    x = f.readline()
newText = txt.split()
# create dictionary
for a in newText:
    if a not in before_unk_uni_gramMap:
        before_unk_uni_gramMap[a] = 1
    else:
        before_unk_uni_gramMap[a] = before_unk_uni_gramMap[a] + 1
# replace low frequency word
postProcess = ""
for a in newText:
    if before_unk_uni_gramMap[a] > 1:
        postProcess += a + " "
        after_unk_uni_gramMap[a] = before_unk_uni_gramMap[a]
    else:
        after_unk_uni_gramMap["<unk>"]+=1
        postProcess += "<unk> "
database = postProcess.split()
f.close()
# end pre-processing
# create bi-gram type
for i in range(len(database)-1):
    twoWords = database[i]+" "+database[i+1]
    if twoWords in bi_gramMap:
        bi_gramMap[twoWords] += 1
    else:
        bi_gramMap[twoWords] = 0
# Question 1
print("question1")
answer1 = len(after_unk_uni_gramMap)
print(answer1)
# Question 2
print("question2")
answer2 = 0
for x in after_unk_uni_gramMap:
    answer2 += after_unk_uni_gramMap[x]
print(answer2)
#Question 3
print("question 3")
#a read test
answer3a = 0
test3aMap = {}
wordType3aIn = {}
wordTokens3a = 0
test3a = open("brown-test.txt", "r",encoding='utf-8-sig')
x = test3a.readline()
while x:
    y = x.split()
    for z in y:
        z=z.lower()
        wordTokens3a += 1
        if z not in before_unk_uni_gramMap:
            answer3a += 1
            test3aMap[z.lower()] = 0
            wordType3aIn[z.lower()] = 0
        else:
            wordType3aIn[z.lower()] = 0
    wordTokens3a += 2 #<s> and </s>
    x = test3a.readline()

print("brown percent of missing token : "+str(answer3a / wordTokens3a))
print("brown percent of missing type : "+ str(len(test3aMap) / (len(wordType3aIn)+2)))
#b
answer3b = 0
test3bMap = {}
wordType3bIn = {}
wordTokens3b = 0
test3b = open("learner-test.txt", "r",encoding='utf-8-sig')
x = test3b.readline()
while x:
    y = x.split()
    for z in y:
        z=z.lower()
        wordTokens3b += 1
        if z not in before_unk_uni_gramMap:
            answer3b += 1
            test3bMap[z.lower()] = 0
            wordType3bIn[z.lower()] = 0
        else:
            wordType3bIn[z.lower()] = 0
    wordTokens3b +=2
    x = test3b.readline()
print("learner percent of missing token : "+str(answer3b / wordTokens3b))
print("learner percent of missing type : "+ str(len(test3bMap) / (len(wordType3bIn)+2)))
#Qunestion 4
print("question 4")
#count bigram

#a
Q4atxt=""
TokensNumber4a = 0
MissingToken4a=0
All4aMap = {}
Missing4aMap = {}
wordTokens4a = 0
test4a = open("brown-test.txt", "r")
x = test4a.readline()
while x:
    y = x.split()
    Q4atxt += "<s> "
    for z in y:
        if z.lower() in after_unk_uni_gramMap:
            Q4atxt += z.lower()+" "
        else:
            Q4atxt += "<unk> "
    Q4atxt += "</s> "
    x = test4a.readline()
data1=Q4atxt.split()
for i in range(len(data1)-1):
    TokensNumber4a += 1
    bi_token = data1[i]+" "+data1[i+1]
    All4aMap[bi_token]=0
    if bi_token not in bi_gramMap:
        MissingToken4a += 1
        Missing4aMap[bi_token]=0

print("brown percent of missing token : "+str(MissingToken4a / TokensNumber4a))
print("brwon percent of missing type : "+ str(len(Missing4aMap) / len(All4aMap)))
#B
Q4btxt=""
TokensNumber4b = 0
MissingToken4b=0
All4bMap = {}
Missing4bMap = {}
wordTokens4b = 0
test4b = open("learner-test.txt", "r")
x = test4b.readline()
while x:
    y = x.split()
    Q4btxt += "<s> "
    for z in y:
        if z.lower() in after_unk_uni_gramMap:
            Q4btxt += z.lower()+" "
        else:
            Q4btxt += "<unk> "
    Q4btxt += "</s> "
    x = test4b.readline()
data2=Q4btxt.split()
for i in range(len(data2)-1):
    TokensNumber4b += 1
    bi_token = data2[i]+" "+data2[i+1]
    All4bMap[bi_token]=0
    if bi_token not in bi_gramMap:
        MissingToken4b += 1
        Missing4bMap[bi_token]=0


print("learner percent of missing token : "+str(MissingToken4b / TokensNumber4b))
print("learner percent of missing type : "+ str(len(Missing4bMap) / len(All4bMap)))

