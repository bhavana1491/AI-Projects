import sys, getopt, collections
from itertools import product
from copy import copy
import math
import time

network = {}
completeQuestionList = []
topologicalOrdering = []
causalNodes = []
decisionNodes = []

class proposition:
    def __init__(self,name,sign):
        self.name = name
        self.sign = sign

    def getName(self):
        return self.name

    def getSign(self):
        return self.sign

    def display(self):
        return str(self.name) + str(self.sign)
#-------------------------------------- PROPOSITION -----------------------------------------

#----------------------------------------- NODE ----------------------------------------------
class Node:
    def __init__(self, name, parent, table):
        self.nodeName = name
        self.parent = parent
        self.table = table

    def getParents(self):
        return self.parent

    def getValueOf(self, givenValues):
        # print "parent = " + str(self.parent)
        sign = ""
        if len(self.parent) > 0:
            for eachNode in self.parent:
                sign = sign + givenValues[eachNode]
            # print "sign = " + sign
            return self.table[sign]
        else:
            return self.table["+"]

    def display(self):
        return "Current node => " + str(self.nodeName) + "\nParent => " + str(self.parent) + "\ntable => " + str(self.table)
# ----------------------------------------- NODE ----------------------------------------------

#------------------------------------------ begin creating each node  --------------------------------------------------
def createEachNode( eachNodeDetails ):
    print " ----------- each node details -------- "
    print eachNodeDetails
    nameOFNodes = (eachNodeDetails[0]).split()
    currentNodeName = nameOFNodes[0]
    if( len(nameOFNodes) > 0 ):
        parentNodes = nameOFNodes[2:]

    table = {}
    if( len(parentNodes)>0 ):
        for eachValue in eachNodeDetails[1:]:
            eachEntry = str(eachValue).split()
            key = ""
            for val in eachEntry[1:]:
                key = key + str(val)
            table.update({key:eachEntry[0]})

    else:
        table.update({"+": eachNodeDetails[1]})
    newNode = Node(currentNodeName,parentNodes,table)

    global topologicalOrdering
    topologicalOrdering.append(currentNodeName)
    global causalNodes
    if eachNodeDetails[1] != "decision" :
        if str(currentNodeName) != "utility":
            causalNodes.append(currentNodeName)
    else:
        decisionNodes.append(currentNodeName)

    global network
    network.update({currentNodeName:newNode})

#------------------------------------------ end creating each node ------------------------------------------------------

#----------------------------------------- PROBABLITY NODE ----------------------------------------------
def probablityType(questionName, questionQuery, questionEvidence):
    question = {"name": questionName,
                "query" : questionQuery,
                "evidence":questionEvidence}

    evidenceObject = []
    evidenceMap = {}
    if questionEvidence is not None:
        for eachEvidenceTerm in questionEvidence.split(","):
            one = eachEvidenceTerm.split()
            evidenceObject.append(proposition(one[0], one[2]))
            evidenceMap.update({one[0]: one[2]})
    question["evidenceObject"] = evidenceObject
    question["evidenceMap"] = evidenceMap

    if questionName == "MEU":
        question["queryList"] = [x.strip(' ') for x in questionQuery.split(",")]
    else:
        queryObject = []
        queryMap = {}
        for eachQueryTerm in questionQuery.split(","):
            one = eachQueryTerm.split()
            queryObject.append(proposition(one[0], one[2]))
            queryMap.update({one[0]: one[2]})
        question["queryObject"] =   queryObject
        question["queryMap"] = queryMap
        question["queryandEvidence"] = list(question["evidenceMap"].keys()) + list(question["queryMap"].keys())

    return question
#----------------------------------------- PROBABLITY NODE ----------------------------------------------


#------------------------------------------ begin creating each asked question  ----------------------------------------
def createEachQuery( questions ):

    file = open("output.txt", "w")
    print "---------- create each query details - all questions given -------"
    print questions

    deleteIndex = 0
    for eachQuestion in questions:

        deleteIndex = deleteIndex + 1
        print "\nFor query " + str(deleteIndex)

        questionType = eachQuestion.split("(") #use questionType[0] for the question type
        conditions = questionType[1].strip(")")
        print "Question type = " + questionType[0]
        print "conditions = " + conditions

        q = None
        query = conditions.split("|")
        if len(query) > 1:
            q = probablityType(questionType[0], query[0], query[1])
            print q
        else:
            q = probablityType(questionType[0], query[0], None)
            print q

        if q["name"] == "P":
            resultantTable = enumerationAsk(q)
            finalResult = normalise(resultantTable, q["queryObject"])
            print "Final result for P = " + ("%.2f" % finalResult)
            file.writelines(str("%.2f" % finalResult) + "\n")

        elif q["name"] == "EU":
            resultantTable, quest, retq = generateInputsForEU(q)
            finalResult = normaliseForEU(resultantTable, quest, retq, 0)
            print "EU print trying " + str(finalResult)
            file.writelines(str(finalResult) + "\n")

        elif q["name"] == "MEU":
            resultantTable = generateInputsForMEU(q)
            print "Max table = " + str(resultantTable)
            print "Max table = " + str(resultantTable)
            maxEU = max([(v, i) for i, v in enumerate(resultantTable)])
            len_createdTable = int(math.log(len(resultantTable), 2))
            val = maxEU[1]
            val = "{0:b}".format(val).zfill(len_createdTable)
            val = val.replace('0', '+')
            val = val.replace('1', '-')

            print str(val) + " " + str(maxEU[0])
            file.writelines(str(" ".join(list(val))) + " " + str(maxEU[0]) + "\n")

#------------------------------------------ end creating each asked question  ----------------------------------------

#--------------------------------  begin generate inputs for MEU -----------------------------------------------------
def generateInputsForMEU( eachQuestion ):
    EUResults = []
    print "----------- MEU clause generation ----------"
    for p in product(("+", "-"), repeat=len(eachQuestion["queryList"])):
        queryList = eachQuestion["queryList"]
        sl = []
        for i in range(len(queryList)):
            # print str(queryList[i]) + "" + str(p[i])
            sl.append(str(queryList[i]) + " = " + str(p[i]))
        query = ", ".join(sl)
        question = probablityType("EU", query, eachQuestion["evidence"])
        print
        print "one combination"
        print question

        questionCopy = copy(question)
        print generateInputsForEU(questionCopy)
        resultantTable, quest, q = generateInputsForEU(questionCopy)
        finalResult = normaliseForEU(resultantTable, quest, q, 1)
        EUResults.append(finalResult)
    print "MEU RESULT => " + str(EUResults)
    return EUResults
#--------------------------------  begin generate inputs for MEU -----------------------------------------------------

#--------------------------------  begin generate inputs for EU -----------------------------------------------------
def generateInputsForEU( eachQuestion ):
    global network, causalNodes
    print "----------- EU clause generation ----------"
    print "query = " + str(eachQuestion["queryMap"])
    print "evidence = " + str(eachQuestion["evidence"])
    print "evidence map = " + str(eachQuestion["evidenceMap"])
    print "utiltity node parents :" + str(network["utility"].parent)
    query = copy(network["utility"].parent)
    for i in query:
        if i in eachQuestion["queryMap"]:
            query.remove(i)
    q = " = +, ".join(query)
    print "query = " + str(query[0])
    print "q = " + str(q)
    if eachQuestion["evidence"] is not None:
        evidence = eachQuestion["evidence"] + ", " + eachQuestion["query"]
    else:
        evidence = eachQuestion["query"]
    print "evidence = " + str(evidence)

    question = probablityType("EU",q+" = +",evidence)

    return enumerationAsk(question), question, query
#--------------------------------  end generate inputs for EU -----------------------------------------------------


#---------------------------------- Enumeration ASK --------------------------------------------------------
def enumerationAsk( eachQuestion ):
    print "-------------- ENUMERATION ASK --------------"
    resultantTable = []
    observedEvidence = collections.OrderedDict(eachQuestion["evidenceMap"])
    print "observed evidence = " + str(observedEvidence)
    queryObjects = eachQuestion["queryObject"]
    newVars = generateNewVars( eachQuestion )

    # for each of the rows in the table TT - truth table
    obevidence = copy(observedEvidence)
    for p in product(("+", "-"), repeat=len(queryObjects)):
        for i in range(len(queryObjects)):
            obevidence.update({queryObjects[i].getName(): p[i]})
        tp = list(newVars)
        print "Call enumeration all"
        start = time.time()
        v = enumerateAll(tp, obevidence)
        print " --- %s ---" % (time.time() - start)
        print v
        resultantTable.append(v)
    return resultantTable
#---------------------------------- Enumeration ASK --------------------------------------------------------

#----------------------------------- Enumerate ALL --------------------------------------------------------
def enumerateAll( var, e ):
    # anothervar = list(var)
    # anothere = copy(e)
    if len(var)==0:
        return 1

    y = var.pop(0)
    global network
    p = network[y].getParents()

    if( y in e.keys() ):
        prob = float(probablity( y, p, e ))
        if prob > 0.0:
            return float(prob * enumerateAll( var, e ))

    sum = 0
    vars = list(var)
    es = copy(e)
    for eachDomain in ["+","-"]:
        var = list(vars)
        e = es
        e.update({y:eachDomain})
        prob = float(probablity(y, p, e))
        if prob > 0.0:
            sum += float( prob * enumerateAll(var, e) )
    return sum
#----------------------------------- Enumerate ALL --------------------------------------------------------

#---------------------------------- begin normalise for probablity -----------------------------------------------
def normalise( resultantTable, queryList ):
    print "Normalise the following : "
    print resultantTable
    binaryString = ""
    for eachQueyLiteral in queryList:
        if eachQueyLiteral.getSign() == "+":
            binaryString = binaryString+"0"
        else:
            binaryString = binaryString+"1"
    num = resultantTable[ int(binaryString,2) ] * (1/sum(resultantTable))
    return float(round(num,2))
#---------------------------------- end normalise for probablity -----------------------------------------------

#---------------------------------- begin normalise for expected utility -----------------------------------------------
def normaliseForEU( resultantTable, quest, q, callFrom ):
    global network
    resultantTable = map(lambda x: x*(1/sum(resultantTable)), resultantTable)
    print resultantTable
    print network["utility"].table
    table = network["utility"].table

    su = 0
    print "len of res = " + str(math.log(len(resultantTable),2))

    len_createdTable = int(math.log(len(resultantTable),2))
    len_givenTable = int(len(table.keys()[0]))
    for i in range(len(resultantTable)):
        #print str("{0:b}".format(i)).zfill(int(math.sqrt(len(resultantTable))))
        val = "{0:b}".format(i).zfill(len_createdTable)
        val = val.replace('0','+')
        val = val.replace('1','-')
        if len_createdTable == len_givenTable:
            su = su + (resultantTable[i] * float(table[val]))
        else:
            sign = ""
            for key in network["utility"].parent:
                if key in q:
                    sign = sign + val.split()[q.index(key)]
                else:
                    sign = sign + quest["evidenceMap"][key]
            print "search with sign = " + sign
            su = su + (resultantTable[i] * float(table[sign]))
    if callFrom == 0:
        return int(round(su))
    else:
        return su
#---------------------------------- end normalise for expected utility -----------------------------------------------

#---------------------------------------- generating new vars ---------------------------------------------
def generateNewVars( eachQuestion ):
    global topologicalOrdering, decisionNodes
    newSet = []
    largestIndex = 0
    for key in eachQuestion["queryandEvidence"]:
        if topologicalOrdering.index(key) > largestIndex:
            largestIndex = topologicalOrdering.index(key)
    copyCausalNode = list(topologicalOrdering)
    copyCausalNode = copyCausalNode[:largestIndex+1]

    return [item for item in copyCausalNode if item not in decisionNodes]
#---------------------------------------- generating new vars ---------------------------------------------

#---------------------------------- begin calculate probablity -----------------------------------------------
def probablity( currentNodeName, parentsList, signMap ):
    # print "---- *get value for* ----"
    # print "name = " + currentNodeName + currentSign
    # print "with conditions = " + str(getValueFor)
    getValueFor = {}
    if (len(parentsList)>0):
        for eachParent in parentsList:
            getValueFor.update({eachParent:signMap[eachParent]})

    global network
    if signMap[currentNodeName] == "+":
        return float(network[currentNodeName].getValueOf(getValueFor))
    else:
        value = float(network[currentNodeName].getValueOf(getValueFor))
        return float(1 - value)
#---------------------------------- end calculate probablity -----------------------------------------------

#------------------------------------------ begin get value for ------------------------------------------------------
def returnValueFor(currentNodeName, getValueFor, currentSign):
    # print "---- *get value for* ----"
    # print "name = " + currentNodeName + currentSign
    # print "with conditions = " + str(getValueFor)

    global network
    if currentSign == "+":
        return float(network[currentNodeName].getValueOf( getValueFor ))
    else:
        value = float(network[currentNodeName].getValueOf( getValueFor ))
        return 1 - value
#------------------------------------------ end get value for ------------------------------------------------------

#------------------------------------- get parent -------------------------------------------------------
def getParent( child ):
    global network
    toreturn = network[child].getParents()
    return toreturn
#------------------------------------- get parent -------------------------------------------------------

#------------------------------------------ begin read input data ------------------------------------------------------
def readInputs( filename ):
    print "-------read inputs-------"
    file = open(filename, "r").readlines()

    index = 0
    eachQuery = []
    for eachInput in file:
        index = index+1
        if eachInput.rstrip() == "******":
            break
        eachQuery.append(eachInput.rstrip())

    print "Queries = "
    print eachQuery

    eachNodeData = []
    for eachInput in file[index:]:
        index = index + 1
        if eachInput.rstrip() == "***":
            createEachNode( eachNodeData )
            eachNodeData = []
            continue
        elif eachInput.rstrip() == "******":
            createEachNode(eachNodeData)
            eachNodeData = []
            break
        else:
            eachNodeData.append(eachInput.rstrip())

    eachUtility = []
    for eachInput in file[index:]:
        index = index+1
        eachUtility.append(eachInput.rstrip())

    if( len(eachUtility) ):
        createEachNode( eachUtility )

    if (len(eachNodeData)>0):
        createEachNode(eachNodeData)

    createEachQuery( eachQuery )

#------------------------------------------ end read input data ------------------------------------------------------
def main():
    try:
        inputFilename = "input12.txt"
        readInputs( inputFilename )

    except getopt.GetoptError:
        #print 'input file name error'
        sys.exit(2)

start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time))