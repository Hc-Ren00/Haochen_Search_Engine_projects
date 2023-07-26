import json
import re

def Findmorefrequency(word1, word2):
    posting1 = Inlist[word1]
    dict1 = {}
    for doc in posting1:
        dict1[doc[0]] = len(doc[1])
    posting2 = Inlist[word2]
    dict2 = {}
    for doc in posting2:
        dict2[doc[0]] = len(doc[1])
    result = []
    for i in dict1:
        if i in dict2:
            if dict1[i] > dict2[i]:
                result.append(i)
        if i not in dict2:
            result.append(i)
    return result

def FilesContainWord(word):
    posting = Inlist[word]
    result = set()
    for doc in posting:
        result.add(doc[0])
    return result

def getPositions(docid, word):
    posting = Inlist[word]
    for doc in posting:
        if doc[0] == docid:
            return doc[1]
    return []

def FileContainPhrase(docid, phrase):
    dict = {}
    for s in phrase:
        dict[s] = getPositions(docid, s)
    for p in dict[phrase[0]]:
        i = 1
        while i < len(phrase):
            p = p + 1
            if p not in dict[phrase[i]]:
                break
            i += 1
        if i == len(phrase):
            return True
    return False

def FilesContainPhrase(phrase):
    files = set()
    for s in phrase:
        w1 = FilesContainWord(s)
        for w in w1:
            files.add(w)
    result = set()
    for f in files:
        if FileContainPhrase(f, phrase):
            result.add(f)
    return result

def phrase2(phrase):
    return FilesContainPhrase(phrase)

def phrase1(phrase):
    return FilesContainPhrase(phrase)

def phrase0(phrase):
    return FilesContainPhrase(phrase)

def term3(word):
    return FilesContainWord(word)

def term2(word):
    return FilesContainWord(word)

def term1(word1, word2, word3):
    set1 = FilesContainWord(word1)
    set2 = FilesContainWord(word2)
    set3 = FilesContainWord(word3)
    result = set()
    for i in set1:
        result.add(i)
    for j in set2:
        result.add(j)
    for k in set3:
        result.add(k)
    return result

def term0(word1, word2, word3):
    lst1 = Findmorefrequency(word1, word3)
    lst2 = Findmorefrequency(word2, word3)
    resultset = set()
    for i in lst1:
        resultset.add(i)
    for j in lst2:
        resultset.add(j)
    return resultset

def writeFile(output, filename, type):
    Output = set()
    for id in output:
        if type == 'scene':
            Output.add(sceneId[id])
        else:
            Output.add(playId[id])
    Output0 = sorted(Output)
    with open(filename, 'w') as f:
        for element in Output0:
            f.write(element + '\n')
    f.close()

with open('shakespeare-scenes.json') as file:
    data = json.load(file)
file.close()

docid = 0
Inlist = {}
playId = {}
sceneId = {}
for doc in list(data.values())[0]:
    docid += 1
    tokens = re.split(" +", doc["text"])
    pos = 0
    positions = {}
    for tok in tokens:
        if tok not in positions:
            positions[tok] = []
        pos += 1
        if tok not in Inlist:
            Inlist[tok] = []
        positions[tok].append(pos)

    for e in positions:
        Inlist[e].append((docid, positions[e]))
    playId[docid] = doc['playId']
    sceneId[docid] = doc['sceneId']

#terms0
term0result = term0('thee', 'thou', 'you')
writeFile(term0result, 'terms0.txt', 'scene')

#terms1
term1result = term1('venice', 'rome', 'denmark')
writeFile(term1result, 'terms1.txt', 'scene')

#terms2
term2result = term2('goneril')
writeFile(term2result, 'terms2.txt', 'play')

#terms3
term3result = term3('soldier')
writeFile(term3result, 'terms3.txt', 'play')

#phrase0
phrase0result = phrase0(['poor', 'yorick'])
writeFile(phrase0result, 'phrase0.txt', 'scene')

#phrase1
phrase1result = phrase1(['wherefore', 'art', 'thou', 'romeo'])
writeFile(phrase1result, 'phrase1.txt', 'scene')

#phrase2
phrase2result = phrase2(['let', 'slip'])
writeFile(phrase2result, 'phrase2.txt', 'scene')

def getTextScenes():
    total = 0
    for doc in list(data.values())[0]:
        tokens = re.split(" +", doc["text"])
        total += len(tokens) - 1
    return total

def AvgScene():
    return getTextScenes() / len(sceneId.keys())

#AvgScene
print(AvgScene())


def getTextS(doc):
    tokens = re.split(" +", doc["text"])
    return len(tokens) - 1

def ShortestScene():
    shortest = getTextS(list(data.values())[0][0])
    shortscene = list(data.values())[0][0]["sceneId"]
    for doc in list(data.values())[0]:
        if getTextS(doc) < shortest:
            shortest = getTextS(doc)
            shortscene = doc['sceneId']
    return (shortest, shortscene)

#ShortestScene
print(ShortestScene())

def LongestScene():
    longest = getTextS(list(data.values())[0][0])
    longscene = list(data.values())[0][0]["sceneId"]
    for doc in list(data.values())[0]:
        if getTextS(doc) > longest:
            longest = getTextS(doc)
            longscene = doc['sceneId']
    return (longest, longscene)

#LongestScene
print(LongestScene())

def getTextPlay(playname):
    result = 0
    for doc in list(data.values())[0]:
        if doc['playId'] == playname:
            result += getTextS(doc)
    return result

def ShortestPlay():
    shortest = getTextPlay(playId[1])
    shortestPlay = playId[1]
    for p in playId:
        if getTextPlay(playId[p]) < shortest:
            shortest = getTextPlay(playId[p])
            shortestPlay = playId[p]
    return (shortest, shortestPlay)

#ShortestPlay
print(ShortestPlay())

def LongestPlay():
    longest = getTextPlay(playId[1])
    longestPlay = playId[1]
    for p in playId:
        if getTextPlay(playId[p]) > longest:
            longest = getTextPlay(playId[p])
            longestPlay = playId[p]
    return (longest, longestPlay)

#LongestPlay
print(LongestPlay())

def CountAll(word):
    lst = Inlist[word]
    newdict = {}
    for pair in lst:
        newdict[pair[0]] = len(pair[1])
    return newdict

#plot
ploty1 = CountAll('thee')
ploty2 = CountAll('thou')
ploty = {}
plotx = {}
for keys in sceneId:
    ploty[keys] = 0
    plotx[keys] = 0
for key in ploty:
    num1 = 0
    num2 = 0
    if key in ploty1:
        num1 = ploty1[key]
    if key in ploty2:
        num2 = ploty2[key]
    ploty[key] = num1 + num2
plotx1 = CountAll('you')
for key in plotx1:
    plotx[key] += plotx1[key]
plotdic = {}
for key in ploty:
    plotdic[key] = (plotx[key], ploty[key])
with open('plotx.txt', 'w') as pfile:
    for element in plotdic:
        pfile.write(str(plotdic[element][0]) + '\n')
pfile.close()

with open('ploty.txt', 'w') as pfile2:
    for element in plotdic:
        pfile2.write(str(plotdic[element][1]) + '\n')
pfile2.close()

