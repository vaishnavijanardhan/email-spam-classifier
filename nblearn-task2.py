import sys
import os
import json
import random

def learnModel(diction,data):
    for each_file in data:
            filest = open(each_file,"r",encoding="latin1")
            file_content = filest.read()
            tokens = file_content.split()
            for each_token in tokens:
                if(each_token in diction):
                    diction[each_token] = diction[each_token] + 1
                else:
                    diction[each_token] = 1
            filest.close()

HamData = []
SpamData = []

if len(sys.argv) < 2:
    print("Error: The input data path is NULL or empty\n")
    sys.exit(-1)

for drctry, drctry_name, file_name in os.walk(sys.argv[1]):
    for every_file in file_name:
        if ".txt" in every_file:
            if "ham" in every_file:
                HamData.append(os.path.join(drctry,every_file))
            else:
                 SpamData.append(os.path.join(drctry,every_file))

# Training the learner with only 10% of the data

folder_train = 0.1
random.seed(100)

total_files = len(HamData) + len(SpamData)
total_train_files = int(round(folder_train*total_files*0.5))
HamData = random.sample(HamData,total_train_files)
SpamData = random.sample(SpamData,total_train_files)

hamfiles_total=len(HamData)
spamfiles_total=len(SpamData)

dict_ham = {}
dict_spam = {}

learnModel(dict_ham,HamData)
learnModel(dict_spam,SpamData)

parameters_model = {
    "ham":dict_ham,
    "spam":dict_spam,
    "total_ham":hamfiles_total,
    "total_spam":spamfiles_total
    }

with open('nbmodel.txt','w') as writefile:
     json.dump(parameters_model,writefile)