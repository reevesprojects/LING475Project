import os
import io
from conllu import parse_incr

def findRootVerb(sentence):
    for token in sentence:
        if token['deprel'] == 'root' and token['upos'] == 'VERB':
            return token['id']
    return 127 #arbitrarily high number

path_to_folder = "/home/reevesbenjamind/LING475/LING475Project/datafiles" #the folder where we keep our files
filenames = os.listdir(path_to_folder) #making a list of all the files in the folder

apoorlynamedstring = ""
sfound=False
vfound=False
ofound=False
advfound=False
rootverbpos = 127
for filename in filenames:
    with open(path_to_folder + "/" + filename, "r", encoding="utf-8") as file: #file wizardry ;)
        output_filename = path_to_folder + "/" + filename + "_output"
        output = open(output_filename, "w", encoding="utf-8")
        sentence_generator = parse_incr(file)

        for sentence in sentence_generator:
            apoorlynamedstring = ""
            sfound=False
            vfound=False
            ofound=False
            advfound=False
            rootverbpos = findRootVerb(sentence)

            for token in sentence:
                if token['deprel'] == ('nsubj' or 'csubj') and not sfound:
                    apoorlynamedstring += "s"
                    sfound = True
                elif token['deprel'] == 'aux' and token['id'] < rootverbpos and token['head'] == rootverbpos and not vfound:
                    apoorlynamedstring += "v"
                    vfound = True
                elif token['deprel'] == 'obj' and token['head'] == rootverbpos:
                    apoorlynamedstring += "o"
                    ofound = True
                elif token['id'] == rootverbpos and not vfound:
                    apoorlynamedstring += "v"
                    vfound = True
                elif token['deprel'] == 'advmod' and token['head'] == rootverbpos and not advfound:
                    apoorlynamedstring += "a"
                    advfound=True
            if apoorlynamedstring == '': 
                apoorlynamedstring = "null"
            output.write(apoorlynamedstring + "\n")
        
        output.close()