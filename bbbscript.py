import os
from conllu import parse_incr

def findRootVerb(sentence):
    for token in sentence:
        if 'root' in token['deprel'] and token['upos'] == 'VERB':
            return token['id']
    return 127 #arbitrarily high number

path_to_folder = "/home/reevesbenjamind/LING475/LING475Project/datafiles" #the folder where we keep our files
filenames = os.listdir(path_to_folder) #making a list of all the files in the folder

sentencecount = 0
advbcount = 0
advacount = 0
apoorlynamedstring = ""
sfound=False
vfound=False
ofound=False
advfound=False
rootverbpos = 127
for filename in filenames:
    if not filename.startswith("output_"):

        with open(path_to_folder + "/" + filename, "r", encoding="utf-8") as file: #file wizardry ;)
            output_filename = path_to_folder + "/" + "output_" + filename #make a new file for the output (we will run shell commands on it to get our data)
            output = open(output_filename, "w", encoding="utf-8")
            try:
                sentence_generator = parse_incr(file) #parse the file using conllu library, this just breaks it into sentences and tokens we can use
            except:
                print(filename)
            for sentence in sentence_generator: #sentence_generator is just a more efficient version of having all the strings in a single array
                sentencecount+=1
                apoorlynamedstring = "" #reset all the variables
                sfound=False
                vfound=False
                ofound=False
                advfound=False
                rootverbpos = findRootVerb(sentence) #get the line number of the root verb

                for token in sentence: #each of the if statements have a _found variable so that they aren't repeated
                    #this has the downside of only allowing one per sentence, which may not be the case for things like adverbs
                    #the way this for loop works is that each token is checked to see if it is svoa
                    #if it is one of these, it adds the corresponding letter to a string
                    #because the tokens are ran through one at a time, the letters in the string should come in the same order as the sentence
                    #the string is then put into the file, one per sentence
                    if 'nsubj' in token['deprel'] and not sfound:
                        apoorlynamedstring += "s"
                        sfound = True
                    elif 'csubj' in token['deprel'] and not sfound:
                        apoorlynamedstring += "s"
                        sfound = True
                    elif 'root' in token['deprel'] and token['upos'] == 'NOUN' and not sfound:
                        apoorlynamedstring += "s"
                        sfound = True
                    elif 'root' in token['deprel'] and token['upos'] == 'PROPN' and not sfound:
                        apoorlynamedstring += "s"
                        sfound = True
                    elif 'aux' in token['deprel'] and token['id'] < rootverbpos and token['head'] == rootverbpos and not vfound:
                        apoorlynamedstring += "v"
                        vfound = True
                    elif 'obj' in token['deprel'] and token['head'] == rootverbpos and not ofound:
                        apoorlynamedstring += "o"
                        ofound = True
                    elif token['id'] == rootverbpos and not vfound:
                        apoorlynamedstring += "v"
                        vfound = True
                    elif 'advmod' in token['deprel'] and token['head'] == rootverbpos and not advfound:
                        apoorlynamedstring += "a"
                        advfound=True
                        if (token["id"] < rootverbpos): advbcount+=1
                        else: advacount+=1
                
                if apoorlynamedstring == '': 
                    apoorlynamedstring = "null"
                #uncomment below and replace 'v' with any other letter to see why you may only be getting that letter (underrepresentation)
                #if apoorlynamedstring == 'v':
                #    for token in sentence:
                #        print(token['id'], token['form'], token['lemma'], token['upos'], token['xpos'], token['feats'], token['head'], token['deprel'], token['deps'], token['misc'])
                output.write(apoorlynamedstring + "\n")
            print("adva: " + str(advacount))
            print("advb: " + str(advbcount))
            print("sentences: " + str(sentencecount))
            output.close()