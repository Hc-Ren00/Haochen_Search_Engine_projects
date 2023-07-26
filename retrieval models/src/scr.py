import math
import re

#Assumption that L,R are given for a single query for Recall, P@k, AP.
def Recall_k(L, R, k):
    #Assumption that R is a list.
    numerator = 0
    for j in range(k):
        if j >= len(L):
            break
        if L[j] in R:
            numerator += 1
    result = numerator/len(R)
    return result


def precision_k(L, R, k):
    #k here is the number of top retrieved documents we need to check for precision.
    numerator = 0
    for i in range(k):
        if i >= len(L):
            break
        if L[i] in R:
            numerator += 1
    result = numerator/k
    return result


def NDCG_k(L, R, k, Dict_R):
    #k here is the number of top retrieved documents we need to check for precision.
    #Dict_R is the hashmap which contains the relevancy of each document.
    IDCG = 0
    sortedR = sorted(R, key = lambda x: Dict_R[x], reverse =True)
    #sort the relevant documents to calculate IDCG
    IDCG = int(Dict_R[sortedR[0]])
    for i in range(1, k):
        if i == len(R):
            break
        Rel = int(Dict_R[sortedR[i]])
        IDCG += Rel / math.log2(i + 1)
    rel = 0
    if len(L) > 0 and L[0] in R:
        rel = int(Dict_R[L[0]])
    for i in range(1,k):
        if i >= len(R) or i >= len(L):
            break
        elif L[i] in R:
            rel_i = int(Dict_R[L[i]])
            rel += rel_i / math.log2(i + 1)
    numerator = rel
    denominator = IDCG
    result = numerator/denominator
    return result

def RR(L, R):
    num = 0
    for i in L:
        if i in R:
            return 1/(num+1)
        num += 1
    return 0

def MRR (type, Q, ListQR):
    #ListQL - List of retrieved documents per query
    #ListRL - List of relevant documents per query
    score = 0
    for i in Q:
        if type == "bm25":
            L = bm25ListQL[i]
        elif type == "ql":
            L = qlListQL[i]
        elif type == "sdm":
            L = sdmListQL[i]
        elif type == "stress":
            L = stressListQL[i]
        R = ListQR[i]
        x = RR(L, R)
        score += x
        #print(str(x) + " " + type + "RR")
    return score/len(Q)

def F1_k(L, R, k):
    recall = Recall_k(L, R, k)
    precision = precision_k(L, R, k)
    if recall + precision == 0:
        return 0
    return (2 * recall * precision) / (recall + precision)

def AP(L,R):
    #since k is not given, we assume k = len(L)
    count = 0
    numerator = 0
    num = 0
    for key in L:
        if key in R:
            count += 1
            numerator += precision_k(L, R, num + 1)
        num += 1
    if count == 0:
        return 0
    result = numerator / count
    return result


def MAP(type, Q, ListQR):
    numerator = 0
    count = 0
    x = 0
    for key in Q:
        count += 1
        if type == "bm25":
            x = AP(bm25ListQL[key], ListQR[key])
        elif type == "ql":
            x = AP(qlListQL[key], ListQR[key])
        elif type == "sdm":
            x = AP(sdmListQL[key], ListQR[key])
        elif type == "stress":
            x = AP(stressListQL[key], ListQR[key])
        numerator += x
        #print(str(x) + " " + type + "AP")
    return numerator / count

Q = {} #keys: query id, values: query content
with open("queries") as f:
    for line in f:
        x = line.split("\t")
        Q[x[0]] = x[1].replace("\n", "")
f.close()

ListDict_R = {}
bm25ListQL = {}
qlListQL = {}
sdmListQL = {}
stressListQL = {}
ListQR = {}

for key in Q:
    ListQR[key] = {}
    bm25ListQL[key] = []
    qlListQL[key] = []
    sdmListQL[key] = []
    stressListQL[key] = []
    ListDict_R[key] = {}

with open("qrels") as f:
    for line in f:
        x = line.split(" ")
        ListDict_R[x[0]][x[2]] = x[3].replace("\n", "")
        if int(x[3]) > 0:
            ListQR[x[0]][x[2]] = x[3].replace("\n", "")
f.close()

with open("bm25.trecrun") as f:
    for line in f:
        x = line.split(" ")
        bm25ListQL[x[0]].append(x[2])
f.close()

with open("ql.trecrun") as f:
    for line in f:
        x = line.split(" ")
        qlListQL[x[0]].append(x[2])
f.close()

with open("sdm.trecrun") as f:
    for line in f:
        x = line.split(" ")
        sdmListQL[x[0]].append(x[2])
f.close()

dict = {}
for key in Q:
    dict[key] = []
with open("stress.trecrun") as f:
    for line in f:
        x = line.split(" ")
        x[len(x) - 1] = x[len(x) - 1].replace("\n", "")
        dict[x[0]].append(x)
    for key in dict:
        dict[key] = sorted(dict[key], key = lambda x: int(x[3]))
    for key in dict:
        for e in dict[key]:
            stressListQL[e[0]].append(e[2])
f.close()

def NDCGktrecrun(type, ListQR, k, ListDict_R):
    sum = 0
    for key in Q:
        if type == "bm25":
            curScore = NDCG_k(bm25ListQL[key], ListQR[key], k, ListDict_R[key])
        elif type == "ql":
            curScore = NDCG_k(qlListQL[key], ListQR[key], k, ListDict_R[key])
        elif type == "sdm":
            curScore = NDCG_k(sdmListQL[key], ListQR[key], k, ListDict_R[key])
        elif type == "stress":
            curScore = NDCG_k(stressListQL[key], ListQR[key], k, ListDict_R[key])
        sum += curScore
        #print(str(curScore) + " " + type + "NDCG")
    return sum / len(Q)

print(str(NDCGktrecrun("bm25", ListQR, 10, ListDict_R)) + " " + "ndcgkbm25")
print(str(NDCGktrecrun("ql", ListQR, 10, ListDict_R)) + " " + "ndcgkql")
print(str(NDCGktrecrun("sdm", ListQR, 10, ListDict_R)) + " " + "ndcgksdm")
print(str(NDCGktrecrun("stress", ListQR, 10, ListDict_R)) + " " + "ndcgkstress")

print(str(MRR("bm25", Q, ListQR)) + " " + "mrrbm25")
print(str(MRR("ql", Q, ListQR)) + " " + "mrrql")
print(str(MRR("sdm", Q, ListQR)) + " " + "mrrsdm")
print(str(MRR("stress", Q, ListQR)) + " " + "mrrstress")

def Pk(type, ListQR, k):
    sum = 0
    for key in Q:
        if type == "bm25":
            curScore = precision_k(bm25ListQL[key], ListQR[key], k)
        elif type == "ql":
            curScore = precision_k(qlListQL[key], ListQR[key], k)
        elif type == "sdm":
            curScore = precision_k(sdmListQL[key], ListQR[key], k)
        elif type == "stress":
            curScore = precision_k(stressListQL[key], ListQR[key], k)
        sum += curScore
        # print(str(curScore) + " " + type + "NDCG")
    return sum / len(Q)

print(str(Pk("bm25", ListQR, 5)) + " " + "Pkbm25-5")
print(str(Pk("ql", ListQR, 5)) + " " + "Pkql-5")
print(str(Pk("sdm", ListQR, 5)) + " " + "Pksdm-5")
print(str(Pk("stress", ListQR, 5)) + " " + "Pkstress-5")

print(str(Pk("bm25", ListQR, 20)) + " " + "Pkbm25-20")
print(str(Pk("ql", ListQR, 20)) + " " + "Pkql-20")
print(str(Pk("sdm", ListQR, 20)) + " " + "Pksdm-20")
print(str(Pk("stress", ListQR, 20)) + " " + "Pkstress-20")

def Recall(type, ListQR, k):
    sum = 0
    for key in Q:
        if type == "bm25":
            curScore = Recall_k(bm25ListQL[key], ListQR[key], k)
        elif type == "ql":
            curScore = Recall_k(qlListQL[key], ListQR[key], k)
        elif type == "sdm":
            curScore = Recall_k(sdmListQL[key], ListQR[key], k)
        elif type == "stress":
            curScore = Recall_k(stressListQL[key], ListQR[key], k)
        sum += curScore
        # print(str(curScore) + " " + type + "NDCG")
    return sum / len(Q)

print(str(Recall("bm25", ListQR, 20)) + " " + "recallbm25")
print(str(Recall("ql", ListQR, 20)) + " " + "recallql")
print(str(Recall("sdm", ListQR, 20)) + " " + "recallsdm")
print(str(Recall("stress", ListQR, 20)) + " " + "recallstress")

def F1(type, ListQR, k):
    sum = 0
    for key in Q:
        if type == "bm25":
            curScore = F1_k(bm25ListQL[key], ListQR[key], k)
        elif type == "ql":
            curScore = F1_k(qlListQL[key], ListQR[key], k)
        elif type == "sdm":
            curScore = F1_k(sdmListQL[key], ListQR[key], k)
        elif type == "stress":
            curScore = F1_k(stressListQL[key], ListQR[key], k)
        sum += curScore
        # print(str(curScore) + " " + type + "NDCG")
    return sum / len(Q)

print(str(F1("bm25", ListQR, 20)) + " " + "F1bm25")
print(str(F1("ql", ListQR, 20)) + " " + "F1ql")
print(str(F1("sdm", ListQR, 20)) + " " + "F1sdm")
print(str(F1("stress", ListQR, 20)) + " " + "F1stress")

print(str(MAP("bm25", Q, ListQR)) + " " + "mapbm25")
print(str(MAP("ql", Q, ListQR)) + " " + "mapql")
print(str(MAP("sdm", Q, ListQR)) + " " + "mapsdm")
print(str(MAP("stress", Q, ListQR)) + " " + "mapstress")

f = open("output.metrics", "w")
f.write("bm25.trecrun" + " " + "NDCG@10" + " " + str(NDCGktrecrun("bm25", ListQR, 10, ListDict_R)) + "\n")
f.write("ql.trecrun" + " " + "NDCG@10" + " " + str(NDCGktrecrun("ql", ListQR, 10, ListDict_R)) + "\n")
f.write("sdm.trecrun" + " " + "NDCG@10" + " " + str(NDCGktrecrun("sdm", ListQR, 10, ListDict_R)) + "\n")
f.write("stress.trecrun" + " " + "NDCG@10" + " " + str(NDCGktrecrun("stress", ListQR, 10, ListDict_R)) + "\n")

f.write("bm25.trecrun" + " " + "MRR" + " " + str(MRR("bm25", Q, ListQR)) + "\n")
f.write("ql.trecrun" + " " + "MRR" + " " + str(MRR("ql", Q, ListQR)) + "\n")
f.write("sdm.trecrun" + " " + "MRR" + " " + str(MRR("sdm", Q, ListQR)) + "\n")
f.write("stress.trecrun" + " " + "MRR" + " " + str(MRR("stress", Q, ListQR)) + "\n")

f.write("bm25.trecrun" + " " + "P@5" + " " + str(Pk("bm25", ListQR, 5)) + "\n")
f.write("ql.trecrun" + " " + "P@5" + " " + str(Pk("ql", ListQR, 5)) + "\n")
f.write("sdm.trecrun" + " " + "P@5" + " " + str(Pk("sdm", ListQR, 5)) + "\n")
f.write("stress.trecrun" + " " + "P@5" + " " + str(Pk("stress", ListQR, 5)) + "\n")

f.write("bm25.trecrun" + " " + "P@20" + " " + str(Pk("bm25", ListQR, 20)) + "\n")
f.write("ql.trecrun" + " " + "P@20" + " " + str(Pk("ql", ListQR, 20)) + "\n")
f.write("sdm.trecrun" + " " + "P@20" + " " + str(Pk("sdm", ListQR, 20)) + "\n")
f.write("stress.trecrun" + " " + "P@20" + " " + str(Pk("stress", ListQR, 20)) + "\n")

f.write("bm25.trecrun" + " " + "Recall@20" + " " + str(Recall("bm25", ListQR, 20)) + "\n")
f.write("ql.trecrun" + " " + "Recall@20" + " " + str(Recall("ql", ListQR, 20)) + "\n")
f.write("sdm.trecrun" + " " + "Recall@20" + " " + str(Recall("sdm", ListQR, 20)) + "\n")
f.write("stress.trecrun" + " " + "Recall@20" + " " + str(Recall("stress", ListQR, 20)) + "\n")

f.write("bm25.trecrun" + " " + "F1@20" + " " + str(F1("bm25", ListQR, 20)) + "\n")
f.write("ql.trecrun" + " " + "F1@20" + " " + str(F1("ql", ListQR, 20)) + "\n")
f.write("sdm.trecrun" + " " + "F1@20" + " " + str(F1("sdm", ListQR, 20)) + "\n")
f.write("stress.trecrun" + " " + "F1@20" + " " + str(F1("stress", ListQR, 20)) + "\n")

f.write("bm25.trecrun" + " " + "MAP" + " " + str(MAP("bm25", Q, ListQR)) + "\n")
f.write("ql.trecrun" + " " + "MAP" + " " + str(MAP("ql", Q, ListQR)) + "\n")
f.write("sdm.trecrun" + " " + "MAP" + " " + str(MAP("sdm", Q, ListQR)) + "\n")
f.write("stress.trecrun" + " " + "MAP" + " " + str(MAP("stress", Q, ListQR)) + "\n")

f.close()

a = open("qlploty.txt", "w")
b = open("qlplotx.txt", "w")
c = open("sdmploty.txt", "w")
d = open("sdmplotx.txt", "w")
e = open("bm25ploty.txt", "w")
f = open("bm25plotx.txt", "w")
for k in range(1, 100):
    A = Pk("ql", ListQR, k)
    B = Recall("ql", ListQR, k)
    C = Pk("sdm", ListQR, k)
    D = Recall("sdm", ListQR, k)
    E = Pk("bm25", ListQR, k)
    F = Recall("bm25", ListQR, k)
    a.write(str(A) + "\n")
    b.write(str(B) + "\n")
    c.write(str(C) + "\n")
    d.write(str(D) + "\n")
    e.write(str(E) + "\n")
    f.write(str(F) + "\n")
a.close()
b.close()
c.close()
d.close()
e.close()
f.close()




