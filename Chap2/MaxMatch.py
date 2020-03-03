# function maxMatch(string, dictionary) returns list of tokens TypeError
#     if string is empty
#         return emptyList
#     for i = length(sentence) downto 1
#         firstword = first i chars of sentence
#         remainder = rest of sentence
#         if InDictionary(firstword, dictionary)
#             return list(firstword, MaxMatch(remainder, dictionary))
#
