from collections import OrderedDict
from itertools import product
from itertools import chain
import re
from copy import copy
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
    if(len(q_v)>1):
        s = q_v[1]
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
            q_a.extend(q.name)
    for e,v in E_l.items():
        e_p_m = bn.get(e).getProb()
        if len(e_p_m)!=0:
            e_a.extend(e)
    m_l = list(set(q_a + e_a))
    tp_o = list(topo_order)
    for i in m_l:
        id_a.append(tp_o.index(i))
    m_id = max(id_a)
    tp_o_f = tp_o[:m_id+1]
    return tp_o_f

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
    final_val = float(prob_val/sum)
    return round(final_val,2)

def Ask(q_t,q_list,e_list):
    for e in bn.keys():
        print "Node:",e
        print "Parents:",bn.get(e).parents
    if q_t == 'P':
        l_up = OrderedDict()
        to = getTopology(q_list, e_list)
        prob_table = list(product(['+', '-'], repeat=len(q_list)))
        for i in range(0, len(prob_table)):
            s_k = "".join(list(prob_table[i]))
            l_up.update({s_k: i})
        #prob_dist = enumerateAsk(q_list,e_list,to)
        prob_value = Normalize(prob_dist,q_list,l_up)
        return prob_value
    if q_t == 'EU':
        eu_sum = 0
        query_l =[]
        evid_m ={}
        ql=[]
        u = bn.get('utility')
        qu_l = list(u.parents)
        r_p = ""
        for i in range(0, len(qu_l)):
            qi = Variables(qu_l[i], '+')
            query_l.append(qi)
        if '|' in q_list:
            j = q_list.index('|')
            for k in range(0, j):
                ql.extend(q_list[k])
            for l in range(j+1,len(q_list)):
                ql.extend(q_list[l])
            ql = filter(lambda x: x != '=', ql)
            if ',' in ql:
                ql = filter(lambda x: x != ',', ql)
                evid_m = {ql[i]: ql[i + 1] for i in range(0, len(ql), 2)}
            else:
                evid_m = {ql[i]: ql[i + 1] for i in range(0, len(ql), 2)}
        elif ',' in q_list:
                q_list = filter(lambda x: x != '=', q_list)
                q_list = filter(lambda x: x != ',', q_list)
                evid_m = {q_list[i]: q_list[i + 1] for i in range(0, len(q_list), 2)}
        else:
            if len(q_list) == 3:
                evid_m.update({q_list[0]: q_list[2]})
        for i in query_l:
            r_p = i.name
            if r_p in evid_m.keys():
                query_l.remove(i)
        to = getTopology(query_l,evid_m)
        prob_dist = enumerateAsk(query_l,evid_m,to)
        updated_prob_dist = NormalizeTable(prob_dist)
        for i in range(0,len(updated_prob_dist)):
            val_s = '{0:b}'.format(i).zfill(int(math.log(len(updated_prob_dist),2))) #int(math.log(len(updated_prob_dist)))
            val_st = val_s.replace('0','+')
            val_st = val_st.replace('1','-')
            if(len(val_st)< len(qu_l)):
                a_s = evid_m.get(r_p)
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
    file = open('input12.txt', 'r')
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
        qu=[]
        queries_list = []
        evidences = OrderedDict()
        evid_m = OrderedDict()
        query_l =[]
        match = re.match(r'(.*)\(', q)
        q_t = match.group(1)
        for i in range(len(q_t)+1,(len(q))):
            qu.extend(q[i].split(" "))
        qu = qu[:-1]
        qu = filter(None, qu)
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
                ql = filter(lambda x: x != '=',ql)
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
                for l in range(j+1,len(qu)):
                    el.extend(qu[l])
                el = filter(lambda x: x != '=', el)
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

            else:
                ql.extend(qu)
                ql = filter(lambda x: x != '=', ql)
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
            prob_val = Ask(q_t,queries_list, evidences)
            print >> o_file,"%.2f" %prob_val
        elif q_t == 'EU':
            EU_val = Ask(q_t,qu,evidences)
            print >> o_file, int(round(EU_val))
        else:
            m_ql=[]
            e_m = {}
            if '|' in qu:
                a_c_l =[]
                e_c_m = OrderedDict()
                j = qu.index('|')
                for i in range(0,j):
                    ql.extend(qu[i])
                for k in range(j+1,len(qu)):
                    a_c_l.extend(qu[k])
                if ',' in ql:
                    meu_p_c = OrderedDict()
                    ql = filter(lambda x: x != ',', ql)
                    meu_table = [0] * 2 ** len(qu)
                    e_c_m = OrderedDict()
                    m_ql = list(ql)
                    si_l = list(product(['+', '-'], repeat=len(m_ql)))
                    string_list = map(' '.join, si_l)
                    meu_table =[0] * 2 ** len(m_ql)
                    for i in range(0, 2 ** len(m_ql)):
                        st_l = string_list[i].split(' ')
                        e_l = ['='] * len(m_ql)
                        c_l = [','] * len(m_ql)
                        mc_l = zip(m_ql, e_l, st_l, c_l)
                        m_l = list(chain.from_iterable(mc_l))
                        m_q_l = m_l[:-1]
                        m_q_l.extend("|")
                        m_q_l.extend(a_c_l)
                        meu_table[i] = Ask('EU',m_q_l,e_c_m)
                        meu_p_c.update({string_list[i]: meu_table[i]})
                    maximum = max(meu_p_c, key=meu_p_c.get)
                    print >> o_file,maximum, int(round(meu_p_c[maximum]))
                else:
                    m_ql = list(ql)
                    meu_pd = OrderedDict()
                    si_l = list(product(['+', '-'], repeat=len(m_ql)))
                    string_list = map(' '.join, si_l)
                    meu_table = [0] * 2 ** len(m_ql)
                    for i in range(0, 2 ** len(m_ql)):
                        st_l = string_list[i].split(' ')
                        e_l = ['='] * len(m_ql)
                        mc_l = zip(m_ql, e_l, st_l)
                        m_l = list(chain.from_iterable(mc_l))
                        m_l.extend("|")
                        m_l.extend(a_c_l)
                        meu_table[i] = Ask('EU', m_l, e_c_m)
                        meu_pd.update({string_list[i]: meu_table[i]})
                    maximum = max(meu_pd, key=meu_pd.get)
                    print >> o_file, maximum, int(round(meu_pd[maximum]))

            elif ',' in qu:
                qu = filter(lambda x: x != ',', qu)
                meu_table = [0] * 2 ** len(qu)
                e_c_m = OrderedDict()
                meu_c = OrderedDict()
                m_ql = list(qu)
                si_l= list(product(['+', '-'], repeat=len(m_ql)))
                string_list = map(' '.join, si_l)
                for i in range(0,2 ** len(m_ql)):
                    st_l = string_list[i].split(' ')
                    e_l = ['='] * len(m_ql)
                    c_l = [','] * len(m_ql)
                    mc_l = zip(m_ql,e_l,st_l,c_l)
                    m_l = list(chain.from_iterable(mc_l))
                    m_q_l = m_l[:-1]
                    meu_table[i] = Ask('EU',m_q_l,e_c_m)
                    meu_c.update({string_list[i]: meu_table[i]})
                maximum = max(meu_c, key=meu_c.get)
                print >> o_file,maximum, int(round(meu_c[maximum]))
            else:
                meu = OrderedDict()
                m_ql = list(qu)
                m_ql.extend("=")
                m_ql.extend("+")
                meu_p = Ask('EU',m_ql,e_m)
                meu.update({'+' : meu_p})
                qu.extend("=")
                qu.extend("-")
                meu_m = Ask('EU', qu, e_m)
                meu.update({'-': meu_m})
                maximum = max(meu, key=meu.get)
                print >> o_file, maximum, int(round(meu[maximum]))
main()