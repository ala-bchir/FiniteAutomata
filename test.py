# -*- coding: utf-8 -*-
"""
Code modifiable.
"""

from automate import Automate
from state import State
from transition import Transition
from myparser import *


#automate = Automate.creationAutomate("exempleAutomate.txt")
#automate.show("exempleAutomate")


#2.1
#1
s0=State(0,True,False)
s1= State(1, False, False)
s2= State(2, False, True)

t1=Transition(s0,"a",s0)
t2=Transition(s0,'b',s1)
t3=Transition(s1,'a',s2)
t4=Transition(s1,'b',s2)
t5=Transition(s2,'a',s0)
t6=Transition(s2,'b',s1)
t7=Transition(s0,'b',s0)
t8= Transition(s0,'a',s1)
t9=Transition(s2,'b',s2)
t10=Transition(s2,'a',s2)
t11=Transition(s1,'a',s1)




#----------------- Création de l'automate test ( l'automate A2 vu en td5 exercice 4 (ni complete ni deterministe)----------------------------------------
a=Automate([t7,t8,t11,t4,t9,t10])


auto = Automate([t1,t7,t8,t4,t9,t10])
#print("automate origine\n")
#print(auto)

#_________________________ tests sur l'automate ________________________

#print("teste sur l'automate \n")

if Automate.accepte(auto,"aaa") : 
    print("le mot 'aaa' est accepté ")
else:
    print("Le mot 'aaa' n'est pas accepté")

if Automate.accepte(auto,"baba") : 
    print("le mot 'baba' est accepté ")
else:
    print("Le mot 'baba' n'est pas accepté")

if Automate.estComplet(auto,"ab"):
    print("l'automate est complet ")
else:
    print("l'automate n'est pas complete")

if Automate.estDeterministe(auto):
    print("l'automate est determinitse")
else:
    print("l'automate n'est pas deterministe")


#----------- Opération sur l'automate --------------------

#auto = Automate.completeAutomate(auto,"ab")
#print("automate apres completion:\n")
#print(auto)

if Automate.estComplet(auto,"ab"):
    print("l'automate est complet ")
else:
    print("l'automate n'est pas complet")


auto = Automate.determinisation(auto)
print("apres determinisation")
print(auto)
print("__________________________________________")
print(a)
a = Automate.complementaire(a,"ab")
print(a)

print("__________________________________________")
s0=State(1,True,False)
s1=State(2,False,False)
s2=State(3,False,True)
auto1=Automate([Transition(s0,'a',s1),Transition(s1,'b',s2),Transition(s2,'a',s2),Transition(s2,'b',s2)])

s3=State('A',True,False)
s4=State('B',False,False)
s5=State('C',False,True)
auto2=Automate([Transition(s3,'a',s3),Transition(s3,'b',s3),Transition(s3,'b',s4),Transition(s4,'a',s5)])





li=Automate.intersection(auto1,auto2)
#print(li)

lu=Automate.union(auto1,auto2)
#print(lu)
print(auto1)
print(auto2)


con = Automate.concatenation(auto1,auto2)
print(con)
print(auto2)

et = Automate.etoile(auto2)
print(et)



