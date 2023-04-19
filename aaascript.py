import os
import io
import re

def getsubj(sentence):
    for line in sentence:#split the sentence into individual lines
        if ("nsubj" in line or "csubj" in line): #check if the line contains nsubj or csubj
            return int(line.split('\t')[0]) #if it does return the line number as an integer
    return 0 #there are no lines found with a subject in them, return 0

def getobj(sentence):
    for line in sentence.splitlines(): #same process as getsubj but looks for "obj" instead
        if ("obj" in line):
            return int(line.split('\t')[0])
    return 0

def getrootverb(sentence):
    rootverbposition = 0
    for line in sentence.splitlines():
        if ("VERB" in line and "root" in line):
            rootverbposition = int(line.split('\t')[0])
    for line in sentence.splitlines():
        #if the aux verb is dependent on the root verb and comes before the root verb
        if ("aux" in line and rootverbposition < int(line.split('\t')[0]) and rootverbposition == int(line.split('\t')[6])):
            return int(line.split('\t')[0])
    return rootverbposition

def getadv(sentence="", rootval=0):
    for line in sentence.splitlines(): #same process as getsubj but looks for "adv" instead
        if ("ADV" in line and rootval == int(line.split('\t')[6])): #also checks to see if it is dependant on the root verb
            return int(line.split('\t')[0]) 
    return 0 #note, this function only gets the FIRST adverb that is dependant on the root verb, not any others.



#The Meat And/Or Potatoes
path_to_folder = "/home/reevesbenjamind/LING475/LING475Project/datafiles" #the folder where we keep our files
filenames = os.listdir(path_to_folder) #making a list of all the files in the folder

for filename in filenames:
    with io.open(path_to_folder + "/" + filename, "r", encoding="utf-8") as file: #file wizardry ;)
        lines = file.read() #open file into variable 'lines'

    lines = re.sub(r'^.*#.*\n?', '', lines, flags=re.MULTILINE) #remove all lines that start with #
    sentences = lines.split("\n\n") #split the file into segments based on if they have \n\n (blank line)
    for sentence in sentences: #run through all the sentences
        sentence = sentence.strip() #get rid of any blank lines (there shouldn't be any but UD can be weird)

    #s = subject, v = verb, o = object, adva = adverb after verb, advb = adverb before verb
    countssvo = {"s":0, "v":0, "o":0, "sv":0, "vs":0, "so":0, "os":0, "sov":0, "osv":0, "ovs":0, "svo":0, "vso":0, "vos":0, "null":0}
    countsadv = {"advb":0, "adva":0}
    sentencescount = 0 #counts the number of sentences

    for sentence in sentences:
        s = getsubj(sentence)
        o = getobj(sentence)
        v = getrootverb(sentence)
        adv = getadv(sentence, v)

        #All of the following if statements can be reordered in any way and it should not affect the output
        #because the functions return 0 if the POS is not in the sentence, the if statements won't run unless it has each required POS for the given count
        if (not s and not o and not v): 
            countssvo["null"]+=1 #sentences that don't have a subject, object, or verb
            #uncomment the next sentence to print out the sentences that are null (most of them make sense as to why they are null)
            #print(sentence)
        if (s and not o and not v): 
            countssvo["s"]+=1 #we count every time ONLY the subject is found
            #print(sentence)
        if (not s and o and not v): countssvo["o"]+=1
        if (not s and not o and v): countssvo["v"]+=1
        if (s and v and not o and s < v): countssvo["sv"]+=1 #every time there is ONLY a subject and verb IN THIS ORDER
        if (s and v and not o and v < s): countssvo["vs"]+=1
        if (s and o and not v and s < o): countssvo["so"]+=1
        if (s and o and not v and o < s): countssvo["os"]+=1
        #I know the if statements are kind of hard to read but I blame python for that
        #each one checks to see if there is a subject, an object, and a verb, and then checks their position
        if (s and v and o and s<o and o<v): 
            countssvo["sov"]+=1
            #print(sentence)
        if (s and v and o and s<v and v<o): countssvo["svo"]+=1
        if (s and v and o and o<s and s<v): countssvo["osv"]+=1
        if (s and v and o and o<v and v<s): countssvo["ovs"]+=1
        if (s and v and o and v<s and s<o): countssvo["vso"]+=1
        if (s and v and o and v<o and o<s): countssvo["vos"]+=1
        if (adv and v<adv): countsadv["adva"]+=1
        if (adv and adv<v): countsadv["advb"]+=1
        sentencescount+=1

    print(filename)
    print(sum(countssvo.values())) #prints the number of sentences that were counted via countssvo
    print(sentencescount) #the actual number of sentences
    #compare the number of sentences to the number of svo marked sentences, should be mostly similar
    #if they aren't that means that the program isn't accounting for every everything that could be considered a "subject" or an "object"
    #this can probably be explained by sentences where there is exclusively o or exclusively v
    #it is also possible that the root isn't a verb, which makes looking for dependant subjects, objects, and adverbs much harder
    print(countssvo)
    print(countsadv)
