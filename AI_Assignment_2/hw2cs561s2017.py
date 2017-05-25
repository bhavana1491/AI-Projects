model = {}
symbols = set()
global clauses
clauses = []

def getSymbols():
    for cl in clauses:
        for i in cl.returnLiteralVariables():
            symbols.add(i)
    return symbols


def intersection(pos, neg):
   i_l =[]
   for i in pos:
       for j in neg:
           if i == j:
            i_l.append(i)
   return i_l


class Clause:
    literals =[]
    def __init__(self,literals):
        self.literals = literals
        self.positiveLiterals = []
        self.negativeLiterals = []
        self.literalNames =[]
        self.literalVariables =[]
        self.positiveSet()
        self.negativeSet()
        self.LiteralNamesSet()
        self.LiteralVariablesSet()

    def returnPositive(self):
        return self.positiveLiterals

    def returnNegative(self):
        return self.negativeLiterals

    def positiveSet(self):
        for cl in self.literals:
            if(cl.sign == '+'):
                self.positiveLiterals.append(cl.name)

    def negativeSet(self):
        for cl in self.literals:
            if(cl.sign == '~'):
                self.negativeLiterals.append(cl.name)

    def returnLiterals(self):
        return self.literals

    def returnLiteralNames(self):
        return self.literalNames

    def returnLiteralVariables(self):
        return self.literalVariables

    def LiteralNamesSet(self):
        for cl in self.literals:
            self.literalNames.append(cl.sign+cl.name)

    def LiteralVariablesSet(self):
        for cl in self.literals:
            self.literalVariables.append(cl.name)

    def isTautology(self):
        li = intersection(self.returnPositive(), self.returnNegative())
        if (len(li) > 0):
            return True
        else:
            return False

    def isEmpty(self):
        if len(self.literals) == 0:
            return True
        else:
            return False

    def getSingleLit(self):
        result = set()
        unique = []
        for item in self.returnLiterals():
            if item.sign+item.name not in result:
                result.add(item.sign+item.name)
                unique.append(item)
        return unique

class Lit:

    def __init__(self,guest,table,sign):
        self.var = 'X'
        self.guest = guest
        self.table = table
        self.name = self.var + "_"+ str(self.guest) + "_" + str(self.table)
        self.sign = sign

    def display(self):
        return self.sign + self.name + " "


def to_cnf():
    for i in range(0,n_g):
        cl =[]
        for j in range(1,(n_t+1)):
            l = Lit(str(i+1),str(j),'+')
            cl.append(l)
        c = Clause(cl)
        clauses.append(c)

    for i in range(0, n_g):
        for j in range(1, (n_t+1)):
            for k in range(j+1,(n_t+1)):
                cl = []
                cl.append(Lit(str(i + 1), str(j), '~'))
                cl.append(Lit(str(i + 1), str(k), '~'))
                c = Clause(cl)
                clauses.append(c)



    for i in range(0,len(fr)):
        a = fr[i][1]
        b = fr[i][2]
        for j in range(1,(n_t+1)):
            cl = []
            cl.append(Lit(a,str(j),'~'))
            cl.append(Lit(b, str(j),'+'))
            c = Clause(cl)
            clauses.append(c)
            cl = []
            cl.append(Lit(a, str(j), '+'))
            cl.append(Lit(b, str(j), '~'))
            c = Clause(cl)
            clauses.append(c)

    for i in range(0,len(en)):
        a = en[i][1]
        b = en[i][2]
        for j in range(1,(n_t+1)):
            cl = []
            cl.append(Lit(a, str(j), '~'))
            cl.append(Lit(b, str(j), '~'))
            c = Clause(cl)
            clauses.append(c)

def dpllSatisfiable():
    symbols = getSymbols()
    return dpll(clauses,symbols,model)

def dpll(clauses,symbols,model):

    if everyClauseTrue(clauses,model):
        return True

    if someClauseFalse(clauses,model):
        return False

    P, value = f_p_s(symbols,clauses,model)
    if P:
        return dpll(clauses, removeP(symbols, P), M_union(model, P, value))

    P, value = f_u_c(clauses, model)
    if P:
        return dpll(clauses, removeP(symbols, P), M_union(model, P, value))

    if not symbols:
        return True

    tempList = list(symbols)
    P, rest_symbols = tempList[0], tempList[1:]
    return (dpll(clauses, rest_symbols, M_union(model, P, True)) or
            dpll(clauses, rest_symbols, M_union(model, P, False)))

def everyClauseTrue(clauses,model):
    for c in clauses:
        if not determineVal(c):
            return False
    return True

def someClauseFalse(clauses,model):
    for c in clauses:
        if determineVal(c) == False:
            return True
    return False

def determineVal(cl):
    result = None

    if cl.isTautology():
        result = True
    elif cl.isEmpty():
        result = False
    else:
        unassigned = False
        val = None
        for i in cl.returnPositive():
            val = model.get(i)
            if val != None:
                if val == True:
                    result = True
                    break
            else:
                unassigned = True

        if result == None:
            for i in cl.returnNegative():
                val = model.get(i)
                if val != None:
                    if val == False:
                        result = True
                        break
                else:
                    unassigned = True

            if result == None:

                if not unassigned:
                    result = False
    return result



def removeP(symbols,P):
    while P in symbols:
        symbols.remove(P)
    return symbols

def M_union(model,P,value):
    model.update({P:value})
    return model

def f_p_s(symbols,clauses,model):
    purePositive = set()
    pureNegative = set()
    #print validSymbols

    for cl in clauses:

        if determineVal(cl) == True:
            continue

        for p in cl.returnPositive():
            if p in symbols:
                purePositive.add(p)

        for n in cl.returnNegative():
            if n in symbols:
                pureNegative.add(n)


    for s in symbols:
        if(s in purePositive and s in pureNegative):
            purePositive.remove(s)
            pureNegative.remove(s)

    if len(purePositive) > 0:
        return purePositive.pop(),True
    elif len(pureNegative) > 0:
        return pureNegative.pop(),False
    else:
        return None,None

def f_u_c(cl,model):
    for l in cl:
        if determineVal(l) == None:
            unassigned = None
            if len(l.returnLiterals()) == 1:
                unassigned = l.returnLiterals()[0]
            else:
                for i in l.returnLiterals():
                    v = model.get(i.name)
                    if v == None:
                        if unassigned == None:
                            unassigned = i
                        else:
                            unassigned = None
                            break

            if unassigned != None:
                name = unassigned.name

                if unassigned.sign == '+':
                    val = True
                else:
                    val = False
                return name,val
    return None,None

def main():
    file = open('input.txt', 'r')
    contents = file.read().splitlines()
    content = contents[0].split(' ')

    global n_g,n_t,fr,en
    n_g = int(content[0])
    n_t = int(content[1])
    fr = []
    en = []
    for i in range(1,len(contents)):
        content = contents[i].split(' ')
        if content[2] == 'F':
            fr.append([content[2],content[0],content[1]])
        else:
            en.append([content[2],content[0],content[1]])
    o_file = open("output.txt",'a')
    if (n_t <= 0 or n_g <= 0):
        print >> o_file,"no"
    else:
        to_cnf()
        result = dpllSatisfiable()
        if result == True:
            print >> o_file,"yes"
            res_dict ={}
            for i in model.iterkeys():
                if model.get(i) == True:
                    str = i.split("_")
                    res_dict.update({str[1]:str[2]})

            for j in sorted(res_dict.iterkeys(), key=lambda s: int(s[0:])):
                print >> o_file, j + " " + res_dict.get(j)

        else:
            print >> o_file,"no"

    file.close()
    o_file.close()


main()