from collections import OrderedDict
from itertools import product
import re
import copy

sp_count = 0
l_count =0
bn = OrderedDict()
topo_order =[]



class Node:

    def __init__(self,name,parents,prob):
        self.name = name
        self.parents = parents
        self.prob = prob

    '''def setParent(self):
        for p in self.parents:
            self.parents.append(p)'''

    def getParents(self):
        return self.parents

    '''def setProb(self):
        for i in self.prob:
            self.prob.append(i)'''

    def getProb(self):
        return self.prob

    def display(self):
        print self.name
        print self.getParents()
        print self.getProb()

class Variables:
    def __init__(self,name,sign):
        self.name = name
        self.sign = sign

def createObj(var):

   #print var
   s = var[0]

   #print s
   n = s.split(" |")
   topo_order.append(n[0])
   #print n[0]
   p=[]
   if (len(n) >1):
    #print n[1]
    p = n[1].split(" ")
    #print p
   prob = {}
   for i in range(1,len(var)):
       str = ""
       pr = var[i].split(" ")
       #print pr
       v = pr[0]
       #print v
       for j in range(1,len(pr)):
        str += pr[j]
       #print str
       prob.update({str:v})



    #print prob
   node = Node(n[0],p[1:],prob)
   bn.update({n[0] : node})
   #print bn.keys()
   #print n

def createQ(q_v):
    n = q_v[0]
    if(len(q_v)>1):
        s = q_v[1]
        #print "Query Variables"
        #print n
        #print s
        v = Variables(n,s)
        return v

def createE(e_v):
    n = e_v[0]
    s = e_v[1]
    #print "Evidence Variables"
    #print n
    #print s

    return n,s


def printQuery(q_t,Q_l,E_l):
    print q_t
    for q in Q_l:
        print "Query Name"
        print q.name
    if(len(E_l)):
        for e,v in E_l.items():
            print "Evidence Name"
            print e ,v

def enumerateAsk(q, e):
    global bn
    prob_dist= [0]*2**len(q)
    #print e
    #print vars
    ob_el = OrderedDict()
    l_up = OrderedDict()
    prob_table = list(product(['+', '-'], repeat=len(q)))
    for i in range(0,len(prob_table)):
      s_k = "".join(list(prob_table[i]))
      l_up.update({s_k : i})
    '''for k in l_up.keys():
        print k,l_up.get(k)'''


    for i in range(0,2**len(q)):
        ob_el = copy.deepcopy(e)
        varbs = list(topo_order)
        #print varbs
        #ob_el= OrderedDict()
        for j in range(0,len(q)):
            ob_el.update({q[j].name + prob_table[i][j]})
            #print ob_el
        #print ob_el
        prob_dist[i] = enumerateAll(varbs,ob_el)
    #print prob_dist
    return Normalize(prob_dist,q,l_up)



def enumerateAll(vars,ob_el):
    #print len(vars)
    #print ob_el
    #print "New evidence ",ob_el
    sum = 0.0
    if(len(vars) == 0):
        return 1.0
    y = vars[0]
    #print "Y: ",y
    #print "Vars: ",vars
    #print "Evidence: ",ob_el
    vars.remove(y)
    #print "Y ",y

    if y in ob_el:
        #print y
        k = bn.get(y)
        parents = k.getParents()
        #print "parents ", parents
        return float(prob(y,parents,ob_el)) * enumerateAll(vars,ob_el)
    else:
        k = bn.get(y)
        parents = k.getParents()
        for i in ['+','-']:
            v = list(vars)
            ob = ob_el.copy()
            #print "Vars: ",v
            ob.update({y: i})
            #print "Updated evidence:",ob
            sum+= float(prob(y,parents,ob)) * enumerateAll(v,ob)
        #print sum
        return sum

def prob(y,parents,ob_el):
    str =''
    #print "Evidence: ",ob_el
    for i in range(0,len(parents)):
        str+=ob_el.get(parents[i])
    prob_d = bn.get(y).getProb()
    #print prob_d
    #print str
    if(ob_el.get(y) == '-'):
        val = 1 - float(prob_d.get(str))
        #print "prob val :",val
        return val
    val = prob_d.get(str)
    #print "prob val of:", y, " :",val
    return val

def Normalize(prob_dist,q,l_up):
    sum = 0
    str=''
    for i in prob_dist:
        #print i
        sum+=i
    for i in range(0,len(q)):
        str+=q[i].sign
    prob_val = prob_dist[l_up.get(str)]
    #print "query prob val :",prob_val
    #print "Sum:",sum
    final_val = float(prob_val/sum)
    print "Final :", round(final_val,2)


def main():
    global bn
    queries = []
    var = []
    q_v =[]
    file = open('input01.txt', 'r')
    contents = file.read().splitlines()
    #print contents

    for i in range(0, len(contents)-1):
        queries.append(contents[i])
        if(contents[i] == '******'):
            sp_count = i
            break



    for i in range(sp_count+1,len(contents)):

        if(contents[i] == '***'):
            #l_count = i
            createObj(var)
            var = []
            continue

        elif contents[i] == '******':
            l_count = i
            createObj(var)
            var = []
            break

        else:
            var.append(contents[i])

    if(len(var)):
        createObj(var)

    queries = queries[:-1]
    #print queries

    for q in queries:
        qu=[]
        queries_list = []
        evidences = OrderedDict()
        #print q
        match = re.match(r'(.*)\(', q)
        q_t = match.group(1) #query_type
        for i in range(len(q_t)+1,(len(q))):
            qu.extend(q[i].split(" "))
        qu = qu[:-1]
        qu = filter(None, qu)
        #print qu
        ql = []
        el = []
        q_v = []
        e_v=[]
        E_l=[]
        if '|' in qu:
            j = qu.index('|')
            for k in range(0,j):
                ql.extend(qu[k])
            #print ql
            ql = filter(lambda x: x != '=',ql)
            #print ql
            for n in range(0,len(ql)):
                Q_l=[]
                if ql[n] == ',':
                    q_o=createQ(q_v)
                    queries_list.append(q_o)
                    q_v = []
                    continue
                else:
                    q_v.append(ql[n])
            if(len(q_v)):
                q_o = createQ(q_v)
                queries_list.append(q_o)
            #q_s = ''.join(ql)
            #print q_s
            for l in range(j+1,len(qu)):
                el.extend(qu[l])
            #print el
            el = filter(lambda x: x != '=', el)
            #print el
            for x in range(0,len(el)):
                E_l=[]
                if el[x] == ',':
                    e,v=createE(e_v)
                    evidences.update({e:v})
                    e_v = []
                    continue
                else:
                    e_v.append(el[x])
            if(len(e_v)):
                e,v=createE(e_v)
                evidences.update({e:v})
            #e_s = ''.join(el)
            #print e_s

        else:
            ql.extend(qu)
            #print ql
            ql = filter(lambda x: x != '=', ql)
            #print ql
            for n in range(0,len(ql)):

                if ql[n] == ',':
                    q_o =createQ(q_v)
                    queries_list.append(q_o)
                    q_v = []
                    continue
                else:
                    q_v.append(ql[n])
            if (len(q_v)):
                q_o=createQ(q_v)
                queries_list.append(q_o)

            #q_s = ''.join(ql)
            #print q_s
        #print len(queries_list)
        #printQuery(q_t, queries_list, evidences)
        enumerateAsk(queries_list, evidences)
    '''for k in bn.iterkeys():
        print "Network"
        print k
        n = bn.get(k)
        n.display()'''
    #print topo_order

main()