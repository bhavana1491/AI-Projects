from collections import OrderedDict
from itertools import product
import re
from copy import deepcopy
import math

sp_count = 0
l_count =0
bn = OrderedDict()
topo_order =[]



class Node:

    def __init__(self,name,parents,prob):
        self.name = name
        self.parents = parents
        self.prob = prob

    def getParents(self):
        return self.parents

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
   if(len(var) == 2 and var[1] == 'decision'):
       node = Node(var[0],[], {})
       bn.update({var[0]: node})
   else:

       s = var[0]

       #print s
       n = s.split(" |")
       #print n
       #print n[0]
       if n[0] != 'utility':
        topo_order.append(n[0])
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
    #print q
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
        ob_el = deepcopy(e)
        varbs = deepcopy(topo_order)
        #print "Topological:",varbs
            #print varbs
            #ob_el= OrderedDict()
        for j in range(0,len(q)):
            ob_el.update({q[j].name + prob_table[i][j]})
                #print ob_el
            #print ob_el
        prob_dist[i] = enumerateAll(varbs,ob_el)
        #print prob_dist
    return prob_dist




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
            v = deepcopy(vars)
            #print "Vars",v
            ob = deepcopy(ob_el)
            #print "Vars: ",v
            ob.update({y: i})
            #print "Updated evidence:",ob
            sum+= float(prob(y,parents,ob)) * enumerateAll(v,ob)
        #print sum
        return sum

def prob(y,parents,ob_el):
    st =''
    #print "Evidence: ",ob_el
    #print y
    #print parents
    #print ob_el
    if(len(parents)):
        for i in range(0,len(parents)):
            #print parents[i]
            #print "Ob_e Parents dict value:",ob_el.get(parents[i])
            st += ob_el.get(parents[i])
    prob_d = bn.get(y).getProb()
    #print prob_d
    #print str
    if(ob_el.get(y) == '-'):
        val = 1 - float(prob_d.get(st))
        #print "prob val :",val
        return val
    val = prob_d.get(st)
    #print "prob val of:", y, " :",val
    return val

def Normalize(prob_dist,q,l_up):
    sum = 0
    str=''
    for i in prob_dist:
        #print i
        sum+=i
    for i in range(0,len(q)):
        str+=q[i].sign #get sign from query
    prob_val = prob_dist[l_up.get(str)]
    #print "query prob val :",prob_val
    #print "Sum:",sum
    final_val = float(prob_val/sum)
    return round(final_val,2)

def Ask(q_t,q_list,e_list):
    if q_t == 'P':
        l_up = OrderedDict()
        prob_table = list(product(['+', '-'], repeat=len(q_list)))
        for i in range(0, len(prob_table)):
            s_k = "".join(list(prob_table[i]))
            #print s_k
            l_up.update({s_k: i})
        prob_dist = enumerateAsk(q_list,e_list)
        prob_value = Normalize(prob_dist,q_list,l_up)
        return prob_value
    if q_t == 'EU':
        eu_sum = 0
        query_l = []
        evid_m = {}
        ql = []
        u = bn.get('utility')
        qu_l = deepcopy(u.parents)
        r_p = ""
        for i in range(0, len(qu_l)):
            qi = Variables(qu_l[i], '+')
            query_l.append(qi)
        if '|' in q_list:
            # print q_list
            j = q_list.index('|')
            for k in range(0, j):
                ql.extend(q_list[k])
            for l in range(j + 1, len(q_list)):
                ql.extend(q_list[l])
            ql = filter(lambda x: x != '=', ql)
            if ',' in ql:
                ql = filter(lambda x: x != ',', ql)
                evid_m = {ql[i]: ql[i + 1] for i in range(0, len(ql), 2)}
                # print evid_m
            else:
                evid_m = {ql[i]: ql[i + 1] for i in range(0, len(ql), 2)}
                # print evid_m
        elif ',' in q_list:
            q_list = filter(lambda x: x != '=', q_list)
            # print q_list
            q_list = filter(lambda x: x != ',', q_list)
            evid_m = {q_list[i]: q_list[i + 1] for i in range(0, len(q_list), 2)}
            # print evid_m
        else:
            if len(q_list) == 3:
                evid_m.update({q_list[0]: q_list[2]})
        # print evid_m
        # print "QueryList",query_l
        for i in query_l:
            r_p = i.name
            if r_p in evid_m.keys():
                query_l.remove(i)
        # print "QueryList", query_l
        prob_dist = enumerateAsk(query_l, evid_m)
        # print prob_dist
        updated_prob_dist = NormalizeTable(prob_dist)
        # print updated_prob_dist
        # prob_table = list(product(['+', '-'], repeat=len(qu_l)))
        # print prob_table
        # print "prob_table",prob_table[3]
        # print len(qu_l)
        # print 2**len(qu_l)
        for i in range(0, len(updated_prob_dist)):
            val_s = '{0:b}'.format(i).zfill(
                int(math.log(len(updated_prob_dist), 2)))  # int(math.log(len(updated_prob_dist)))
            # print val_s
            val_st = val_s.replace('0', '+')
            val_st = val_st.replace('1', '-')
            if (len(val_st) < len(qu_l)):
                a_s = evid_m.get(r_p)
                val_st += a_s
                prob_t = bn.get('utility').getProb()
                eu_sum += updated_prob_dist[i] * float(prob_t.get(val_st))
            else:
                prob_t = bn.get('utility').getProb()
                eu_sum += updated_prob_dist[i] * float(prob_t.get(val_st))
                # print val_st
        return int(round(eu_sum))
        '''eu_sum = 0
        u = bn.get('utility')
        qu_l = u.parents
        for i in q_list:
            r_p = i.name
            if r_p in e_list.keys():
                q_list.remove(i)
        #print "QueryList", query_l
        prob_dist = enumerateAsk(q_list,e_list)
        #print prob_dist
        updated_prob_dist = NormalizeTable(prob_dist)
        #print updated_prob_dist
        #prob_table = list(product(['+', '-'], repeat=len(qu_l)))
        #print prob_table
        #print "prob_table",prob_table[3]
        #print len(qu_l)
        #print 2**len(qu_l)
        for i in range(0,len(updated_prob_dist)):
            val_s = '{0:b}'.format(i).zfill(int(math.log(len(updated_prob_dist),2))) #int(math.log(len(updated_prob_dist)))
            #print val_s
            val_st = val_s.replace('0','+')
            val_st = val_st.replace('1','-')
            if(len(val_st)< len(qu_l)):
                a_s = e_list.get(r_p)
                val_st += a_s
                prob_t = bn.get('utility').getProb()
                eu_sum += updated_prob_dist[i] * float(prob_t.get(val_st))
            else:
                prob_t = bn.get('utility').getProb()
                eu_sum += updated_prob_dist[i] * float(prob_t.get(val_st))
            #print val_st
        return int(round(eu_sum))'''
    if q_t == 'MEU':
        q_l =[]
        el=[]
        eu_list =[]
        if '|' in q_list:
            j = q_list.index('|')
            for k in range(0, j):
                q_l.extend(q_list[k])
            if ',' in q_l:
                q_l = filter(lambda x: x != ',', q_l)
            for l in range(j+1,len(q_list)):
                el.extend(q_list[l])
            print el
            print q_l
            #for i in range(0,2 ** len(q_l)):




        '''elif ',' in q_list:
            q_l= filter(lambda x: x != ',', q_list)'''







def NormalizeTable(prob_dist):
    #print prob_dist
    p_sum = 0;
    u_prob_dist =[0] * len(prob_dist)
    #print len(prob_dist)
    for i in range(0, len(prob_dist)):
        p_sum += prob_dist[i]
    #print p_sum
    for i in range(0, len(prob_dist)):
        #print prob_dist[i]
        u_prob_dist[i] = float(prob_dist[i]/p_sum)
        #print u_prob_dist[i]
    return u_prob_dist




def main():
    global bn
    queries = []
    var = []
    q_v =[]
    file = open('input02.txt', 'r')
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
            #print "utility:"
            #print var
            createObj(var)
            var = []
            continue

        else:
            var.append(contents[i])
            #print var

    if(len(var)):
        #print var
        createObj(var)
        var =[]

    queries = queries[:-1]
    #print queries

    for q in queries:
        qu=[]
        queries_list = []
        evidences = OrderedDict()
        evid_m = OrderedDict()
        query_l =[]
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
        if q_t == 'P':
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
                # print ql
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
                    #for i in queries_list:
                        #print i.name, i.sign

                #q_s = ''.join(ql)
                #print q_s
            #print len(queries_list)
            #printQuery(q_t, queries_list, evidences)

            prob_val = Ask(q_t,queries_list, evidences) #see the highest alphabet in both evidence and query and create new topological order deleting all variables afterhighest alphabet
            print "%.2f" %prob_val
        elif q_t == 'EU':
            #print qu
            query_l = []
            evid_m = {}
            ql = []
            u = bn.get('utility')
            qu_l = deepcopy(u.parents)
            r_p = ""
            for i in range(0, len(qu_l)):
                qi = Variables(qu_l[i], '+')
                query_l.append(qi)
            if '|' in qu:
                # print q_list
                j = qu.index('|')
                for k in range(0, j):
                    ql.extend(qu[k])
                for l in range(j + 1, len(qu)):
                    ql.extend(qu[l])
                ql = filter(lambda x: x != '=', ql)
                if ',' in ql:
                    ql = filter(lambda x: x != ',', ql)
                    evid_m = {ql[i]: ql[i + 1] for i in range(0, len(ql), 2)}
                    # print evid_m
                else:
                    evid_m = {ql[i]: ql[i + 1] for i in range(0, len(ql), 2)}
                    # print evid_m
            elif ',' in qu:
                qu = filter(lambda x: x != '=', qu)
                # print q_list
                qu = filter(lambda x: x != ',', qu)
                evid_m = {qu[i]: qu[i + 1] for i in range(0, len(qu), 2)}
                # print evid_m
            else:
                if len(qu) == 3:
                    evid_m.update({qu[0]: qu[2]})
            # print evid_m
            # print "QueryList",query_l
            EU_val = Ask(q_t,query_l,evid_m)
            print EU_val
        else:
            print q_t
            print qu
            str_l=[0]*2**len(qu)
            if ',' in qu:
                qu = filter(lambda x: x != ',', qu)
                print qu
                sign_l = list(product(['+', '-'], repeat=len(qu)))
                #print sign_l
                string_list = map(' '.join, sign_l)
                print 2**len(qu)
                for i in range(0,2**len(qu)):
                    str_l[i] = string_list[i].split(' ')
                    print str_l[i]





            meu_val = Ask(q_t,qu,evidences)



    '''for k in bn.iterkeys():
        print "Network"
        #print k
        n = bn.get(k)
        n.display()'''
    #print topo_order

main()