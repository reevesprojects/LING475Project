import os
from conllu import parse_incr

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

path_to_folder = "/home/reevesbenjamind/LING486/datafiles" #the folder where we keep our files
filenames = os.listdir(path_to_folder) #making a list of all the files in the folder

apoorlynamedstring = ""
sfound=False
vfound=False
ofound=False
rootpos=127
rootverbpos = 127
countssvo = {"sv":0, "vs":0, "so":0, "os":0, "ov":0, "vo":0, "sov":0, "osv":0, "ovs":0, "svo":0, "vso":0, "vos":0}

for filename in filenames:
    if not filename.startswith("output_"):

        with open(path_to_folder + "/" + filename, "r", encoding="utf-8") as file: #file wizardry ;)
            try:
                sentence_generator = parse_incr(file) #parse the file using conllu library, this just breaks it into sentences and tokens we can use
            except:
                print(filename)
            for sentence in sentence_generator: #sentence_generator is just a more efficient version of having all the strings in a single array
                apoorlynamedstring = "" #reset all the variables
                sfound=False
                vfound=False
                ofound=False
                rootverbpos = findRootVerb(sentence) #get the line number of the root verb
                rootpos = findRoot(sentence)

                for token in sentence: #each of the if statements have a _found variable so that they aren't repeated
                    #this has the downside of only allowing one per sentence, which may not be the case for things like adverbs
                    #the way this for loop works is that each token is checked to see if it is svoa
                    #if it is one of these, it adds the corresponding letter to a string
                    #because the tokens are ran through one at a time, the letters in the string should come in the same order as the sentence
                    #the string is then put into the file, one per sentence
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

                if apoorlynamedstring == "svo":countssvo["svo"]+=1
                if apoorlynamedstring == "sov":countssvo["sov"]+=1
                if apoorlynamedstring == "vos":countssvo["vos"]+=1
                if apoorlynamedstring == "vso":countssvo["vso"]+=1
                if apoorlynamedstring == "osv":countssvo["osv"]+=1
                if apoorlynamedstring == "ovs":countssvo["ovs"]+=1
                if apoorlynamedstring == "sv":countssvo["sv"]+=1
                if apoorlynamedstring == "vs":countssvo["vs"]+=1
                if apoorlynamedstring == "os":countssvo["os"]+=1
                if apoorlynamedstring == "so":countssvo["so"]+=1
                if apoorlynamedstring == "vo":countssvo["vo"]+=1
                if apoorlynamedstring == "ov":countssvo["ov"]+=1

            print(filename + "\t" + str(countssvo["svo"])+ "\t" + str(countssvo["sov"])+ "\t" + str(countssvo["vso"])+ "\t" + str(countssvo["vos"])+ "\t" + str(countssvo["osv"])+ "\t" + str(countssvo["ovs"])+ "\t" + str(countssvo["sv"])+ "\t" + str(countssvo["vs"])+ "\t" + str(countssvo["os"])+ "\t" + str(countssvo["so"])+ "\t" + str(countssvo["vo"])+ "\t" + str(countssvo["ov"]))