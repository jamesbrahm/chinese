#!/usr/bin/env python3

import unicodedata
import csv
import collections
import re

HSK_LEVEL=1
TTL=1
VOCAB = collections.deque()

def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn')

def get_hsk_data():
    hsk_data = []
    with open('data/hsk_3.0_vocab.csv', 'r') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=';')
        for row in csvreader:
            row['Pinyin'] = row['Pinyin'].replace("\xa0", "")
            row['Ascii'] = strip_accents(row['Pinyin'])
            row['HSK Set'] = int(row['HSK Set'])
            row['TTL'] = TTL
            if row['HSK Set'] <= HSK_LEVEL:
                hsk_data.append(row)
    return hsk_data

def proc_ans(ans):
    ans = ans.split("｜")[0]
    ans = re.sub(r'\W+', '', ans)
    return ans.replace(" ", "")

def ask_q(vocab):
    result = 0
    print()
    print(vocab['Character'])
    user_in = proc_ans(input("Pinyin: "))

    if user_in == proc_ans(vocab['Ascii']):
        print("Correct!")
        result = 1
    else:
        print("Nope. {}".format(vocab['Ascii']))
    
    print("{} -- {}".format(vocab['Pinyin'], vocab['Meaning']))
    return result

def srp():
   while len(VOCAB) > 0:
        word = VOCAB.popleft()
        result = ask_q(word) 
        if result: # correct
            # Decrement the TTL
            word['TTL'] = word['TTL']-1
        else: # incorrect
            while not ask_q(word):
                ()
            VOCAB.insert(5, word) 
        if word['TTL'] > 0:
            VOCAB.append(word)

def main():
    hsk_data = get_hsk_data()
    VOCAB.extend(hsk_data)
    srp()

if __name__ == '__main__':
    main()
