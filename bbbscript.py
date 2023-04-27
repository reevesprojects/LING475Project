import os
from conllu import parse_incr
from conllu.models import TokenList

def findRootVerb(sentence):
    for token in sentence:
        if 'root' in token['deprel'] and token['upos'] == 'VERB':
            return token['id']
    return 127 #arbitrarily high number

def findRoot(sentence):
    for token in sentence:
        if 'root' in token['deprel']:
            return token['id']
    return 127 #arbitrarily high number


def findSubVerb(sentence, srootval):
    for token in sentence:
        if 'VERB' in token['upos'] and token['id'] == srootval:
            return token['id']
    return 127
           
path_to_folder = "/home/reevesbenjamind/LING475/LING475Project/datafiles" #the folder where we keep our files
filenames = os.listdir(path_to_folder) #making a list of all the files in the folder

sentencecount = 0
advbcount = 0
advacount = 0
for filename in filenames:
    if not filename.startswith("output_") and not filename.startswith("sub_"):

        with open(path_to_folder + "/" + filename, "r", encoding="utf-8") as file:
            output_filename = path_to_folder + "/" + "output_" + filename #make a new file for the output (we will run shell commands on it to get our data)
            sub_filename = path_to_folder + "/" + "sub_" + filename
            output = open(output_filename, "w", encoding="utf-8")
            sub = open(sub_filename, "w", encoding = "utf-8")
            sentence_generator = parse_incr(file) #parse the file using conllu library, this just breaks it into sentences and tokens we can use

            for sentence in sentence_generator: #sentence_generator is just a more efficient version of having all the strings in a single array
                sentencecount+=1
                apoorlynamedstring = "" #reset all the variables
                anotherstring=""
                sfound=False
                vfound=False
                ofound=False
                advfound=False
                ssfound=False #subordinating subject
                svfound=False
                sofound=False
                sadvfound=False
                inSCONJ=False
                srootpos=127
                srootverbpos=127
                rootverbpos = 127
                rootpos = 127
                rootverbpos = findRootVerb(sentence) #get the line number of the root verb
                rootpos = findRoot(sentence)

                for token in sentence: #each of the if statements have a _found variable so that they aren't repeated
                    #this has the downside of only allowing one per sentence, which may not be the case for things like adverbs
                    #the way this for loop works is that each token is checked to see if it is svoa
                    #if it is one of these, it adds the corresponding letter to a string
                    #because the tokens are ran through one at a time, the letters in the string should come in the same order as the sentence
                    #the string is then put into the file, one per sentence
                    if not inSCONJ:
                        if 'nsubj' in token['deprel'] and rootpos == token['head'] and not sfound:
                            apoorlynamedstring += "s"
                            sfound = True
                        elif 'csubj' in token['deprel'] and rootpos == token['head'] and not sfound:
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
                        elif 'obj' in token['deprel'] and token['head'] == rootpos and not ofound:
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
                        elif 'SCONJ' in token["upos"] and not inSCONJ: #we are marking subordinarting qlauses as 'q' for qlause
                            #apoorlynamedstring += "q" 
                            srootpos=token['head']
                            srootverbpos= findSubVerb(sentence, srootpos)
                            inSCONJ=True
                    else: #this runs if we are in a subordinating clause
                        if 'nsubj' in token['deprel'] and srootpos == token['head'] and not ssfound:
                            anotherstring+="s"
                            ssfound = True
                        elif 'csubj' in token['deprel'] and srootpos == token['head'] and not ssfound:
                            anotherstring += "s"
                            ssfound = True
                        elif srootpos == token['id'] and token['upos'] == 'NOUN' and not ssfound:
                            anotherstring += "s"
                            ssfound = True
                        elif srootpos == token['id'] and token['upos'] == 'PROPN' and not ssfound:
                            anotherstring += "s"
                            ssfound = True
                        elif 'aux' in token['deprel'] and token['id'] < srootverbpos and token['head'] == srootverbpos and not svfound:
                            anotherstring += "v"
                            svfound = True
                        elif 'obj' in token['deprel'] and token['head'] == srootpos and not sofound:
                            anotherstring += "o"
                            sofound = True
                        elif token['id'] == srootverbpos and not svfound:
                            anotherstring += "v"
                            svfound = True
                        elif 'advmod' in token['deprel'] and token['head'] == srootverbpos and not sadvfound:
                            anotherstring += "a"
                            sadvfound=True
                        if '.' in token['lemma'] or ',' in token['lemma'] or ';' in token['lemma'] or '!' in token['lemma'] or '?' in token['lemma']:
                            inSCONJ=False
                            ssfound=False
                            svfound=False
                            sofound=False
                            sadvfound=False
                            inSCONJ=False
                            srootpos=127
                            srootverbpos=127
                            if anotherstring=="":
                                anotherstring=="null"
                            sub.write(anotherstring+"\n")
                            anotherstring=""

                           

                if apoorlynamedstring == '': 
                    apoorlynamedstring = "null"
                #uncomment below and replace 'v' with any other letter to see why you may only be getting that letter (underrepresentation)
                #if apoorlynamedstring.startswith("v"):
                #    for token in sentence:
                #        print(token['id'], token['form'], token['lemma'], token['upos'], token['xpos'], token['feats'], token['head'], token['deprel'], token['deps'], token['misc'])
                output.write(apoorlynamedstring + "\n")
            print("adva: " + str(advacount))
            print("advb: " + str(advbcount))
            print("sentences: " + str(sentencecount))
            output.close()