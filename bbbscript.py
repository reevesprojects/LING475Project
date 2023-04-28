import os
from conllu import parse_incr

def findRoot(sentence):
    for token in sentence:
        if 'root' in token['deprel']:
            return token
    return -1

           
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
                roottoken = findRoot(sentence)

                for token in sentence: #each of the if statements have a _found variable so that they aren't repeated
                    #this has the downside of only allowing one per sentence, which may not be the case for things like adverbs
                    #the way this for loop works is that each token is checked to see if it is svoa
                    #if it is one of these, it adds the corresponding letter to a string
                    #because the tokens are ran through one at a time, the letters in the string should come in the same order as the sentence
                    #the string is then put into the file, one per sentence
                    if not inSCONJ:
                        if 'nsubj' in token['deprel'] and roottoken['id'] == token['head'] and not sfound:
                            apoorlynamedstring += "s"
                            sfound = True
                        elif 'csubj' in token['deprel'] and roottoken['id'] == token['head'] and not sfound:
                            apoorlynamedstring += "s"
                            sfound = True
                        elif 'aux' in token['deprel'] and 'VERB' in roottoken['upos'] and token['head'] == roottoken['id'] and not vfound:
                            apoorlynamedstring += "v"
                            vfound = True
                        elif 'obj' in token['deprel'] and token['head'] == roottoken['upos'] and not ofound:
                            apoorlynamedstring += "o"
                            ofound = True
                        # if copular and AUX and the token's head is a noun and the token's head noun's head is the root
                        elif 'cop' in token['deprel'] and 'AUX' in token['upos'] and 'NOUN' in sentence[token['head']-1]['upos'] and sentence[sentence[token['head']-1]['head']] == roottoken and not vfound:
                            apoorlynamedstring += "v"
                            vfound=True
                        elif token == roottoken and 'VERB' in roottoken['upos'] and not vfound:
                            apoorlynamedstring += "v"
                            vfound = True
                        elif 'advmod' in token['deprel'] and sentence[token['head']-1] == roottoken and not advfound:
                            apoorlynamedstring += "a"
                            advfound=True
                            if (token["id"] < roottoken['id']): advbcount+=1
                            else: advacount+=1
                        elif 'SCONJ' in token["upos"] and not inSCONJ: #we are marking subordinarting qlauses as 'q' for qlause
                            #apoorlynamedstring += "q" 
                            sroottoken=sentence[token['head']-1]
                            inSCONJ=True
                    else: #this runs if we are in a subordinating clause
                        if 'nsubj' in token['deprel'] and sroottoken == sentence[token['head']-1] and not ssfound:
                            anotherstring+="s"
                            ssfound = True
                        elif 'csubj' in token['deprel'] and sroottoken == sentence[token['head']-1] and not ssfound:
                            anotherstring += "s"
                            ssfound = True
                        elif 'aux' in token['deprel'] and sroottoken == sentence[token['head']-1] and 'VERB' in sentence[token['head']-1]['upos'] and not svfound:
                            anotherstring += "v"
                            svfound = True
                        elif 'cop' in token['deprel'] and 'AUX' in token['upos'] and 'NOUN' in sentence[token['head']-1]['upos'] and sentence[sentence[token['head']-1]['head']] == sroottoken and not vfound:
                            apoorlynamedstring += "v"
                            vfound=True
                        elif 'obj' in token['deprel'] and sroottoken == sentence[token['head']-1] and not sofound:
                            anotherstring += "o"
                            sofound = True
                        elif token == sroottoken and 'VERB' in token['upos'] and not svfound:
                            anotherstring += "v"
                            svfound = True
                        elif 'advmod' in token['deprel'] and sroottoken == sentence[token['head']-1] and 'VERB' in sentence[token['head']-1]['upos'] and not sadvfound:
                            anotherstring += "a"
                            sadvfound=True
                        if '.' in token['lemma'] or ',' in token['lemma'] or ';' in token['lemma'] or '!' in token['lemma'] or '?' in token['lemma']:
                            inSCONJ=False
                            ssfound=False
                            svfound=False
                            sofound=False
                            sadvfound=False
                            inSCONJ=False
                            if anotherstring=="":
                                anotherstring="null"
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