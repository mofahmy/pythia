#!/usr/bin/python

from sys import argv
import re
import random

def read_file(file):
    f = open(file, 'r')
    content = f.read()
    f.close()
    return content

def append_to_file(file, content):
    f = open(file, 'a')
    f.write(content)
    f.write("\n\n")
    f.close()

def get_socrates_lines(text):
    lines = text.split("\n\n")
    lines = [re.sub("\n"," ",item) for item in lines]
    lines = [item.strip() for item in lines]
    
    
    soc_lines = [item for item in lines if (item.startswith("Soc.") or item.startswith("Socrates."))]
    soc_lines = [re.sub("Soc(?:rates)?\.",'',item) for item in soc_lines]
    soc_lines = [item.strip() for item in soc_lines]
    return soc_lines

def build_dictionary(depth, lines):
    dictionary = {}

    linecount = 0
    for l in lines:
        linecount = linecount + 1
        
        words = l.split()
        index = 0
        while index < len(words) - depth:
            begin = index
            end = index + depth

            state = words[index:end]
            key = ' '.join(state)
            
            value = words[index+depth]

            if key not in dictionary:
                dictionary[key] = []

            dictionary[key].append(value)

            index += 1
    return dictionary

def generate_wisdom(dictionary, depth, max_length):
    current_length = depth

    wisdom = 'a'

    while wisdom[0].islower():
        wisdom = random.choice(list(dictionary.keys()))

    current_key = wisdom
    
    while current_length < max_length:
        if current_key not in dictionary:
            break
        
        next_word = random.choice(dictionary[current_key])
        wisdom = wisdom + " " + next_word

        current_length += 1
        
        wisdom_split = wisdom.split(' ')
        begin = current_length - depth
        end = len(wisdom_split)

        current_key = ' '.join(wisdom_split[begin:end])
        
    return wisdom

if __name__ == '__main__':
    script, infile, outfile, depth, max_length = argv
    depth = int(depth)
    max_length = int(max_length)
    
    dialogues = read_file(infile).split("\n")
    dialogues = [item for item in dialogues if item]
    
    for d in dialogues:
        text = read_file(d)
        soc_lines = get_socrates_lines(text)
        for s in soc_lines:
            append_to_file(outfile, s)

    master_file = read_file(outfile)
    all_lines = master_file.split("\n\n")

    dictionary = build_dictionary(depth, all_lines)

    for x in range(1,10):
        wisdom = generate_wisdom(dictionary, depth, max_length)
        print(wisdom,"\n\n")
