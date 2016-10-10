import sys
import os
import json
import math

def find_probability(class_probability,curr_dict,other_dict,sizOfVocab,num_words):

    filest = open(every_fl,"r",encoding="latin1")
    file_content = filest.read()

    tokens = file_content.split()

    value_tmp = [curr_dict[token] if token in curr_dict else 0 if token in other_dict else -1 for token in tokens]
    value_tmp = [each_value for each_value in value_tmp if each_value != -1]

    prob_tmp = [ math.log((each_value+1)/(num_words + sizOfVocab)) for each_value in value_tmp]
    prob_final = sum(prob_tmp) + math.log(class_probability)

    filest.close()
    return prob_final


with open('nbmodel.txt') as model_file:
     read_params = json.load(model_file)

total_ham = read_params["total_ham"]
total_spam = read_params["total_spam"]

dict_ham = read_params["ham"]
dict_spam = read_params["spam"]

total_words = list(dict_ham.keys()) + list(dict_spam.keys())
total_words = list(set(total_words))
sizOfVocab = len(total_words)

total_hamWords = sum(list(dict_ham.values()))
total_spamWords = sum(list(dict_spam.values()))

denom = total_ham + total_spam
prob_ham = total_ham / (denom)
prob_spam = total_spam / (denom)

dev_data = []
for drctry, drctry_name, file_name in os.walk(sys.argv[1]):
    for every_file in file_name:
        if ".txt" in every_file:
            dev_data.append(os.path.join(drctry,every_file))

find_label = []
for every_fl in dev_data:

    ham_probability = find_probability(prob_ham,dict_ham,dict_spam,sizOfVocab,total_hamWords)
    spam_probability = find_probability(prob_spam,dict_spam,dict_ham,sizOfVocab,total_spamWords)

    if ham_probability > spam_probability:
        find_label = find_label + ["ham"]
    else:
        find_label = find_label + ["spam"]


toOutput = ""
for result in zip(dev_data,find_label):
    toOutput = toOutput + "{0} {1}".format(result[1],result[0]) + "\n"
    outputfile = open("nboutput.txt","w")
    outputfile.write(toOutput)
    outputfile.close()
