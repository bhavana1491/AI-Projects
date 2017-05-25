from collections import OrderedDict
from itertools import product
import re
import math
import time

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

class Variables:
    def __init__(self,name,sign):
        self.name = name
        self.sign = sign

def createObj(var):
   if(len(var) == 2 and var[1] == 'decision'):
       node = Node(var[0],[], {})
       bn.update({var[0]: node})
   else:

       s = var[0]
       n = s.split(" |")
       if n[0] != 'utility':
        topo_order.append(n[0])
       p=[]
       if (len(n) >1):
        p = n[1].split(" ")
       prob = {}
       for i in range(1,len(var)):
           str = ""
           pr = var[i].split(" ")
           v = pr[0]
           for j in range(1,len(pr)):
            str += pr[j]
           prob.update({str:v})
       node = Node(n[0],p[1:],prob)
       bn.update({n[0] : node})

def createQ(q_v):
    n = q_v[0]
    print n
    if(len(q_v)>1):
        x = str(q_v[1])
        s = x[0]
        v = Variables(n,s)
        return v

def createE(e_v):
    n = e_v[0]
    s = e_v[1]
    return n,s

def getTopology(Q_l,E_l):
    q_a=[]
    e_a =[]
    m_l=[]
    tp_o =[]
    id_a=[]
    for q in Q_l:
        p_m = bn.get(q.name).getProb()
        if len(p_m) != 0:
            q_a.append(q.name)
    for e,v in E_l.items():
        e_p_m = bn.get(e).getProb()
        if len(e_p_m)!=0:
            e_a.append(e)
    m_l = list(set(q_a + e_a))
    tp_o = list(topo_order)
    #print topo_order
    #print m_l
    for i in m_l:
        id_a.append(tp_o.index(i))
    if len(id_a)!= 0:
        m_id = max(id_a)
        tp_o_f = tp_o[:m_id+1]
        return tp_o_f
    return tp_o

def enumerateAsk(q, e,to):

    global bn
    prob_dist= [0]*2**len(q)
    ob_el = OrderedDict()
    prob_table = list(product(['+', '-'], repeat=len(q)))
    ob_el = dict(e)
    for i in range(0,2**len(q)):
        varbs = list(to)
        for j in range(0,len(q)):
            ob_el.update({q[j].name : prob_table[i][j]})
        #start = time.time()
        prob_dist[i] = enumerateAll(varbs,ob_el)
        # print prob_dist
        #print ("====> %s time : " % (time.time() - start))
    return prob_dist

def enumerateAll(vars,ob_el):

    global bn
    sum = 0.0
    if(len(vars) == 0):
        return 1.0
    y = vars.pop(0)
    k = bn.get(y)
    parents = k.getParents()
    if y in ob_el.keys():
        p = prob(y, parents, ob_el)
        if p != 0:

            return float(p) * enumerateAll(vars,ob_el)
    ob = dict(ob_el)
    for i in ['+','-']:
        v = list(vars)
        ob.update({y: i})
        p = prob(y,parents,ob)
        #print p
        if p!=0:
            sum += float(p) * enumerateAll(v,ob)

    return sum

def prob(y,parents,ob_el):

    global bn
    st =''
    if(len(parents)>0):

        for i in parents:
            st += ob_el.get(i)
    prob_d = bn.get(y).getProb()
    if(ob_el.get(y) == '-'):
        val = 1 - float(prob_d.get(st))
        return val
    val = prob_d.get(st)
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
    if sum == 0:
        return 0
    final_val = float(prob_val/sum)
    return round(final_val,2)

def Ask(q_t,q_list,e_list):
    if q_t == 'P':
        l_up = OrderedDict()
        to = getTopology(q_list, e_list)
        prob_table = list(product(['+', '-'], repeat=len(q_list)))
        for i in range(0, len(prob_table)):
            s_k = "".join(list(prob_table[i]))
            l_up.update({s_k: i})
        prob_dist = enumerateAsk(q_list,e_list,to)
        prob_value = Normalize(prob_dist,q_list,l_up)
        return prob_value
    if q_t == 'EU':
        eu_sum = 0
        global bn
        query_l=[]
        u = bn.get('utility')
        qu_l = list(u.parents)
        r_p = ""
        for i in range(0, len(qu_l)):
            qi = Variables(qu_l[i], '+')
            query_l.append(qi)
        for i in query_l:
            r_p = i.name
            if r_p in e_list.keys():
                query_l.remove(i)
        to = getTopology(query_l,e_list)
        prob_dist = enumerateAsk(query_l,e_list,to)
        updated_prob_dist = NormalizeTable(prob_dist)
        for i in range(0,len(updated_prob_dist)):
            val_s = '{0:b}'.format(i).zfill(int(math.log(len(updated_prob_dist),2))) #int(math.log(len(updated_prob_dist)))
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
        return eu_sum

def NormalizeTable(prob_dist):
    p_sum = 0
    u_prob_dist =[0] * len(prob_dist)
    for i in range(0, len(prob_dist)):
        p_sum += prob_dist[i]
    for i in range(0, len(prob_dist)):
        u_prob_dist[i] = float(prob_dist[i]/p_sum)
    return u_prob_dist

def main():
    global bn
    queries = []
    var = []
    q_v =[]
    file = open('input.txt', 'r')
    contents = file.read().splitlines()

    for i in range(0, len(contents)-1):
        queries.append(contents[i])
        if(contents[i] == '******'):
            sp_count = i
            break

    for i in range(sp_count+1,len(contents)):

        if(contents[i] == '***'):
            createObj(var)
            var = []
            continue

        elif contents[i] == '******':
            createObj(var)
            var = []
            continue

        else:
            var.append(contents[i])

    if(len(var)):
        createObj(var)
        var =[]
    o_file = open("output.txt", 'a')
    queries = queries[:-1]
    for q in queries:
        evid_m = OrderedDict()
        query_l =[]
        match = re.match(r'(.*)\(', q)
        q_t = match.group(1)
        qu = q[len(q_t)+1:len(q)-1]
        qu = qu.split("|")

        if(len(qu)>1):
            e_s = qu[1].split(",")
            e_s = map(str.strip, e_s)
            for i in e_s:
                second = i.split()
                evid_m.update({second[0]:second[2]})
        qu_s = qu[0].split(",")
        qu_s = map(str.strip, qu_s)
        if q_t == 'P' or q_t == 'EU':
            for i in qu_s:
                first = i.split()
                q_o = Variables(first[0],first[2])
                query_l.append(q_o)
        if q_t == 'P':
            prob_val = Ask(q_t, query_l, evid_m)
            print >> o_file, "%.2f" % prob_val
        if q_t == 'EU':
            eu_evid = dict(evid_m)
            for i in query_l:
                eu_evid.update({i.name:i.sign})
            EU_val = Ask(q_t,qu,eu_evid)
            print >> o_file, int(round(EU_val))
        if q_t == 'MEU':
            meu_evid = dict(evid_m)
            meu_table = [0]* 2 ** len(qu_s)
            meu_q_l =[]
            meu_val = OrderedDict()
            si_l = list(product(['+', '-'], repeat=len(qu_s)))
            string_list = map(' '.join, si_l)
            new_s_l = [x.replace(" ", "") for x in string_list]
            for i in range(0,len(new_s_l)):
                for j in range(0,len(qu_s)):
                    meu_evid.update({qu_s[j]:new_s_l[i][j]})
                meu_table[i] = Ask('EU',meu_q_l,meu_evid)
                meu_val.update({string_list[i]:meu_table[i]})
            maximum = max(meu_val, key=meu_val.get)
            print >> o_file, maximum, int(round(meu_val[maximum]))
    file.close()
    o_file.close()
main()