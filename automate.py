# -*- coding: utf-8 -*-

from transition import *
from state import *
import os
import copy
from sp import *
from itertools import product
from automateBase import AutomateBase
import itertools



class Automate(AutomateBase):
        
    def succElem(self, state, lettre):
        """State x str -> list[State]
        rend la liste des états accessibles à partir d'un état
        state par l'étiquette lettre
        """
        successeurs = []
        # t: Transitions
        for t in self.getListTransitionsFrom(state):
            if t.etiquette == lettre and t.stateDest not in successeurs:
                successeurs.append(t.stateDest)
        return successeurs


    def succ (self, listStates, lettre):
        """list[State] x str -> list[State]
        rend la liste des états accessibles à partir de la liste d'états
        listStates par l'étiquette lettre
        """
        liste_res = []
        for s in listStates:
            liste_res+=self.succElem(s,lettre)
        liste =set(liste_res)
            
        return list(liste)




    """ Définition d'une fonction déterminant si un mot est accepté par un automate.
    Exemple :
            a=Automate.creationAutomate("monAutomate.txt")
            if Automate.accepte(a,"abc"):
                print "L'automate accepte le mot abc"
            else:
                print "L'automate n'accepte pas le mot abc"
    """
    @staticmethod
    def accepte(auto,mot) :

        liste = auto.succ(auto.getListInitialStates(),mot[0])#liste contient les etats accessibles a patir des etats intiaux de auto par la premiere lettre de mot
        for l in mot[1:]:
            liste = auto.succ(liste,l)
        if State.isFinalIn(liste): #on test si la liste contient une etat finale 
            return True 
        return False 
            


        
        
      


    @staticmethod
    def estComplet(auto,alphabet) :
        liste = auto.listStates # liste de tout les etats de l'automate
        for s in liste: 
            for a in alphabet:
                if auto.succElem(s,a)==[] : #on test si l'etat s possede une transition d'etiquette a vers une autre etat si la liste contient 0 etat cad l'automate n'est pas complete
                    return False
        return True 

        
        


        
    @staticmethod
    def estDeterministe(auto) :

        #verifier que l'automate possede une seule état initial 
        if len(auto.getListInitialStates()) != 1 : 
            return False
        
        liste = auto.listStates #liste de tout les états de l'automate 
        for s in liste:
            liste_t = auto.getListTransitionsFrom(s) #liste qui contient toutes les transition de s vers une autre etat
            liste_eti = [] # liste qui contient tout les étiquette de la transition t 
            for t in liste_t:
                liste_eti.append(t.etiquette) 
            if len(liste_eti) != len(list(set(liste_eti))) : # on test si la liste des étiquette ne contient pas des doublons ( si elle contient des doublons cad l'automate est deterministe )
                return False
        return True
        
        

       
    @staticmethod
    def completeAutomate(auto,alphabet) :
        if (Automate.estComplet(auto,alphabet)):
            print("l'automate est déja complete:")
            return auto
        else:
            auto_res = copy.deepcopy(auto) #création dun nouvelle automate complete
            p = State("puits",False,False,) #creation de l'etat puis
            for e in alphabet:
                auto_res.addTransition(Transition(p,e,p)) #ajouter les transtion avec chaque etiquettes de l'alphabet a l'etat puits

            for s in auto.listStates:#on parcours tout les états de l'automate 
                liste =[] # la liste va stocker tout les étiquette de chauqe transition sortante de l'état "s" 
                
                for t in auto.getListTransitionsFrom(s):
                    liste.append(t.etiquette)
                
                
                for c in alphabet: #on parcours chauqe caracteres de l'alphabet
                    if c not in liste: #si c n'existe pas dans la liste on ajoute une nouvelle transition d'etiquette c de s vers p 
                        auto_res.addTransition(Transition(s,c,p))

            return auto_res
        
        



        

        
        

       

    @staticmethod
    def determinisation(auto) :
        """ Automate  -> Automate
        rend l'automate déterminisé d'auto
        """
        if (Automate.estDeterministe(auto)): #si l'automate est deterministe on return auto 
            return auto 
        Lstates=[State(set(auto.getListInitialStates()),True,False)] #on cree Lstates qui est la liste d'etats d'automate deterministe, 
        #elle contient d'abord l'etat initial du nouvel automate, qui a pour id l'ensemble d'etats initiaux d'auto 
        
	#pour l'affichage de l'etat initial d'automate derministe on se sert d'une chaine de caractere saff 
        saff='{'
        for s in set(auto.getListInitialStates()): #saff est la chaine de caractere qui represente l'ensemble des etats initiaux d'auto 
            saff=saff+str(s.id)+','
        saff=saff[:-1]+'}'

        Lsaffiche=[State(0,True,False,label=saff)] #on cree Lsaffiche qui sert pour l'affichage des etats d'automate deterministe, 
        #elle contient d'abord l'etat initial d'automate deterministe d'id 0 et de label saff

        Ltransition=[] #on cree Lstransition qui va stocker les transitions d'automate deterministe

        alphabet=auto.getAlphabetFromTransitions() #alphabet est la liste d'etiquettes de tous les transitions d'auto

        i=0
        while(i<len(Lstates)): #on fait une boucle qui parcours la liste des etats d'automate deterministe 
            #depart:State
            depart = Lstates[i] #depart represente l'etat de depart et elle est donc au debut l'etat initial d'automate deterministe(Lstates[0]) et 
            #change a chaque fois a l'etat suivant dans la liste
            #departaffiche:State
            departaffiche = Lsaffiche[i] #departaffiche represente l'etat de depart(avec le format d'affichage) et 
            #elle est donc au debut l'etat initial d'automate deterministe(Laffiche[0]) et change a chaque fois a l'etat suivant dans la liste
        
            for l in alphabet: 
                #de:set[State]
                de=set() #de est l'ensemble d'etats qui va stocker les etats successeurs des etats de depart par l,et il va representer l'id d'etat d'automate deterministe
                #deaffiche:str
                deaffiche='{' #deaffiche va etre le label de chaque etat de l'automate deterministe
    
                for s in depart.id: #on parcours l'ensemble d'etats qui est le id de l'etat depart
                    for t in auto.getListTransitionsFrom(s): #pour chaque transition partante de s:
                        if l==t.etiquette: #si l'etiquette de t est egale a l alors:
                            de.add(t.stateDest) #on ajoute a de l'etat de destination de cette transition
                            deaffiche=deaffiche+str(t.stateDest.id)+',' #on ajoute a deafiiche le id de l'etat de destination de cette transition
                    #a la fin du boucle qui parcours les transitions, on obtient 'de' qui est l'ensemble des etats successeurs de s par la lettre l 
                    
                    #des:State , des represente l'etat successeur de l'etat depart par la lettre l 
                    #desaffiche:State ,desaffiche represente l'etat successeur de l'etat departaffiche par la lettre l
    
                    if de==Lstates[0].id: # si de est le meme que l'id de l'etat initial de l'automate deterministe alors:
                        
                        desaffiche=Lsaffiche[0] 
                    #sinon:	
                    else: 
                        for ss in de: #
                            if ss.fin==True: #si l'ensemble de contient un etat final alors:
                                des=State(de,False,True) #l'etat destination ayant pour id l'ensemble 'de' va etre final
                                if des not in Lstates: #si des n'est pas deja presente dans Lstates, on l'ajoute
                                    Lstates.append(des)
                                desaffiche=State(Lstates.index(des),False,True,label=deaffiche[:-1]+'}') #l'etat de destination desaffiche prend pour id l'indexe de l'etat des dans Lstates, 
                                #pour label la chaine de caractere deaffiche et il est final 
                                break #il suffit qu'on trouve un etat final on sort du boucle
                            
                            else: #si 'de' ne contient aucun etat final alors:
                                des=State(de,False,False) #l'etat destination ayant pour id l'ensemble 'de' va etre ni final ni initial
                                if des not in Lstates: #si des n'est pas deja presente dans Lstates, on l'ajoute
                                    Lstates.append(des)
                                desaffiche=State(Lstates.index(des),False,False,label=deaffiche[:-1]+'}')#l'etat de destination desaffiche prend pour id l'indexe de 
                                #l'etat des dans Lstates,  pour label la chaine de caractere deaffiche et il est ni final ni initial 
                        
                                
                    if desaffiche not in Lsaffiche: #si l'etat desaffiche n'est pas dans la liste Lsaffiche on l'ajoute
                        Lsaffiche.append(desaffiche)
                Ltransition.append(Transition(departaffiche,l,desaffiche))

            i=i+1
            
        return  Automate(Ltransition)
                        


                
                    






        

       
        
    @staticmethod
    def complementaire(auto,alphabet):
        """ Automate -> Automate
        rend  l'automate acceptant pour langage le complémentaire du langage de a
        """
        if  not Automate.estDeterministe(auto):
            auto = Automate.determinisation(auto)
        if not Automate.estComplet(auto,alphabet):
            auto = Automate.completeAutomate(auto,alphabet)
        
        for s in auto.listStates:# pour chaque etat :
            if s.fin:           #si l'etat est final alors in le rend normal
                s.fin = False 
            else:             #sinon  il devient final 
                s.fin = True 
        
        return auto 

    


    

              
   
    @staticmethod
    def intersection (auto0, auto1):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage l'intersection des langages des deux automates
        """
        L0=auto0.listStates
        L1=auto1.listStates
        #on cree L qui contient la liste des etats de l'automate intersection (pas tous les etats sont L vont etre dans l'automate resultat)
        L=list(itertools.product(L0,L1))
        #print(L)
        
        #Ltransitions:list()
        Ltransitions=[] #c'est la liste des transitions de l'automate resultat
        #Lstates:list()
        Lstates=[] #c'est la liste des etats de l'automate resultat
        #Ls:list()
        Ls=[] #c'est la liste des etats de l'automate resultat mais avec un format d'affichage (label qui represente les couples)
        
        for (s0,s1) in L: #d'abord, on cherche l'etat initial de l'automate resultat:
            if (s0.init==True and s1.init==True): #c'est l'etat ou il ya les etats initiaux de auto1 et auto2
                sini=(s0,s1)
                si=State(0,True,False,label="("+str(s0.id)+","+str(s1.id)+")") #on cree l'etat si qui sert pour l'affichage de l'automate
                Lstates.append(sini) #on ajoute l'etat initial a la liste des etats 
                Ls.append(si) 
        i=0
        while (i<len(Ls)): #on parcours la liste d'etats de l'automate resultat
            (s0,s1)=Lstates[i] #(s0,s1) est l'etat qu'on va partir de lui,donc au debut il est l'etat initial qui est deja dans Lstates, 
            #apres il change a l'etat suivant  
            Lt0=auto0.getListTransitionsFrom(s0) #liste des transitions partantes de s0
            Lt1=auto1.getListTransitionsFrom(s1) #liste des transitions partantes de s1
            for t0 in Lt0:
                for t1 in Lt1:
                    if t0.etiquette==t1.etiquette: #si on trouve une transition avec la meme etiquette alors:
                    
                        if((t0.stateDest).init==True & (t1.stateDest).init==True): #on verifie.si.les.etats.successeurs de chaque etat s0 et s1 
                            #par cette transition sont initiaux, si c'est le cas:
                            if (t0.stateDest,t1.stateDest) not in Lstates: #si l'etat successeur de (s0,s1) n'est pas deja present dans Lstates,on l'ajoute
                                Lstates.append((t0.stateDest,t1.stateDest))
                            sd=State(Lstates.index((t0.stateDest,t1.stateDest)),True,False,label="("+str(t0.stateDest.id)+","+str(t1.stateDest.id)+")")#on cree sd: l'etat suivant de l'automate resultat qui est initial 
                            
                        elif((t0.stateDest).fin==True & (t1.stateDest).fin==True):#on verifie si les etats successeurs de chaque etat s0 et s1 par cette transition sont finaux, si c'est le cas:
                            if (t0.stateDest,t1.stateDest) not in Lstates:#si l'etat successeur de (s0,s1) n'est pas deja present dans Lstates,on l'ajoute
                                Lstates.append((t0.stateDest,t1.stateDest))
                            sd=State(Lstates.index((t0.stateDest,t1.stateDest)),False,True,label="("+str(t0.stateDest.id)+","+str(t1.stateDest.id)+")") #on cree sd: l'etat suivant de l'automate resultat qui est final 
                            
                        else: #si les etats successeurs de chaque etat s0 et s1 ne sont ni initiaux ni finaux alors: 
                            if (t0.stateDest,t1.stateDest) not in Lstates: #si l'etat successeur de (s0,s1) n'est pas deja present dans Lstates,on l'ajoute
                                Lstates.append((t0.stateDest,t1.stateDest))
                            sd=State(Lstates.index((t0.stateDest,t1.stateDest)),False,False,label="("+str(t0.stateDest.id)+","+str(t1.stateDest.id)+")") #on cree sd: l'etat suivant de l'automate resultat qui est ni final ni initial
                            
                        
                        if sd not in Ls: #si sd n'est pas deja present dans Ls, on l'ajoute sinon non
                            Ls.append(sd)
                                
                Ltransitions.append(Transition(Ls[i],t1.etiquette,sd)) #on ajoute a la liste de transitions de l'automate resultat la transition partante de Ls[i] vers sd	
            i=i+1			
                        
        return Automate(Ltransitions)
        

    @staticmethod
    def union (auto0, auto1):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage l'union des langages des deux automates
        """
        L0=auto0.listStates
        L1=auto1.listStates
        #on cree L qui contient la liste des etats de l'automate intersection (pas tous les etats sont L vont etre dans l'automate resultat)
        L=list(itertools.product(L0,L1))
        #print(L)
        
        #Ltransitions:list()
        Ltransitions=[] #c'est la liste des transitions de l'automate resultat
        #Lstates:list()
        Lstates=[] #c'est la liste des etats de l'automate resultat
        #Ls:list()
        Ls=[] #c'est la liste des etats de l'automate resultat mais avec un format d'affichage (label qui represente les couples)
        
        for (s0,s1) in L: #d'abord, on cherche l'etat initial de l'automate resultat:
            if (s0.init==True and s1.init==True): #c'est l'etat ou il ya les etats initiaux de auto1 et auto2
                sini=(s0,s1)
                si=State(0,True,False,label="("+str(s0.id)+","+str(s1.id)+")") #on cree l'etat si qui sert pour l'affichage de l'automate
                Lstates.append(sini) #on ajoute l'etat initial a la liste des etats 
                Ls.append(si) 
        i=0
        while (i<len(Ls)): #on parcours la liste d'etats de l'automate resultat
            (s0,s1)=Lstates[i] #(s0,s1) est l'etat qu'on va partir de lui,donc au debut il est l'etat initial qui est deja dans Lstates, apres il change a l'etat suivant  
            Lt0=auto0.getListTransitionsFrom(s0) #liste des transitions partantes de s0
            Lt1=auto1.getListTransitionsFrom(s1) #liste des transitions partantes de s1
            for t0 in Lt0:
                for t1 in Lt1:
                    if t0.etiquette==t1.etiquette: #si on trouve une transition avec la meme etiquette alors:
                    
                        if((t0.stateDest).init==True or (t1.stateDest).init==True): #on verifie si l'un des  etats successeurs de chaque etat s0 et s1 par cette transition sont initiaux, si c'est le cas:
                            if (t0.stateDest,t1.stateDest) not in Lstates: #si l'etat successeur de (s0,s1) n'est pas deja present dans Lstates,on l'ajoute
                                Lstates.append((t0.stateDest,t1.stateDest))
                            sd=State(Lstates.index((t0.stateDest,t1.stateDest)),True,False,label="("+str(t0.stateDest.id)+","+str(t1.stateDest.id)+")")#on cree sd: l'etat suivant de l'automate resultat qui est initial 
                            
                        elif((t0.stateDest).fin==True or (t1.stateDest).fin==True):#on verifie si l'un des  etats successeurs de chaque etat s0 et s1 par cette transition sont finaux, si c'est le cas:
                            if (t0.stateDest,t1.stateDest) not in Lstates:#si l'etat successeur de (s0,s1) n'est pas deja present dans Lstates,on l'ajoute
                                Lstates.append((t0.stateDest,t1.stateDest))
                            sd=State(Lstates.index((t0.stateDest,t1.stateDest)),False,True,label="("+str(t0.stateDest.id)+","+str(t1.stateDest.id)+")") #on cree sd: l'etat suivant de l'automate resultat qui est final 
                            
                        else: #si les etats successeurs de chaque etat s0 et s1 ne sont ni initiaux ni finaux alors: 
                            if (t0.stateDest,t1.stateDest) not in Lstates: #si l'etat successeur de (s0,s1) n'est pas deja present dans Lstates,on l'ajoute
                                Lstates.append((t0.stateDest,t1.stateDest))
                            sd=State(Lstates.index((t0.stateDest,t1.stateDest)),False,False,label="("+str(t0.stateDest.id)+","+str(t1.stateDest.id)+")") #on cree sd: l'etat suivant de l'automate resultat qui est ni final ni initial
                            
                        
                        if sd not in Ls: #si sd n'est pas deja present dans Ls, on l'ajoute sinon non
                            Ls.append(sd)
                                
                Ltransitions.append(Transition(Ls[i],t1.etiquette,sd)) #on ajoute a la liste de transitions de l'automate resulta lat transition partante de Ls[i] vers sd	
            i=i+1			
                        
        return Automate(Ltransitions)

   
       

    @staticmethod
    def concatenation (auto1, auto2):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage la concaténation des langages des deux automates
        """
        Lstates=[] #liste d'etats d'automate resultat
	
        Ltransitions=[] #liste de transitions d'automate resultat
        
        for i1 in auto1.getListInitialStates():
            #on verifie au debut si les états finaux et initiaux d'auto1 sont distinctes ou non pour determiner les etats initiaux de l'automate resultat

            if i1 in auto1.getListFinalStates(): #si l'intersection de I1 et F1 n'est pas vide alors les etats initiaux de l'automate resultat sont celles de auto1 et celles de auto2:
                Lstates=auto1.listStates+auto2.listStates #la liste d'etats de l'automate resultat est composee d'etats de auto1 et d'etats d'auto2				
                Ltransitions=auto1.listTransitions+auto2.listTransitions #la liste de transitions de l'automate resultat est composee des transitions de auto1 et des transitions d'auto2				
                break #des qu'en trouve un element commun on sort de la boucle
            else: #si l'intersection de I1 et F1 est l'ensemble vide alors:
                nouvelauto2=copy.deepcopy(auto2) #on cree nouvelauto2 qui est une copie de auto2
                for s in nouvelauto2.getListInitialStates(): #pour chaque etat initial de nouvelauto2:
                        s.init=False #il n'est plus initial
                        

                Lstates=auto1.listStates+nouvelauto2.listStates	#la liste d'etats de l'automate resultat est donc composee d'etats de auto1 et d'etats de nouvelauto2			
                Ltransitions=auto1.listTransitions+nouvelauto2.listTransitions #la liste de transitions de l'automate resultat est composee des transitions de auto1 et des transitions de nouvelauto2				
        
        #on obtient alors la liste d'etats et la liste de transitions de l'automate resultat,on fait maintenant la concatenation:
                
        for t in auto1.listTransitions:
            if t.stateDest in auto1.getListFinalStates(): #pour chaque transition t d'auto1 si l'etat destination de t est final alors:
                for s in auto2.getListInitialStates():
                    Ltransitions.append(Transition(t.stateSrc,t.etiquette,s)) #on ajoute une transition partante de l'etat source de t par l'etiquette de t vers chaque etat initial d'auto2
        for s in Lstates: 
            if s in auto1.getListFinalStates(): #les etats finaux d'auto1 ne sont plus finaux dans l'automate resultat:
                s.fin=False			
            
        return Automate(Ltransitions,Lstates)
    
    @staticmethod
    def etoile (auto):
        """ Automate  -> Automate
        rend l'automate acceptant pour langage l'étoile du langage de a
        """
        sFinal = auto.getListFinalStates() #liste des etats finaux d'auto 
        Liste_t = [] # liste des transition 
        for t in auto.listTransitions :
            if t.stateDest in sFinal : # si la transition arrive vers un etat final on l'ajoute à la liste 
                Liste_t.append(t)

        sInitial = auto.getListInitialStates() #liste des etats initials d'auto 
        for t in Liste_t :
            for s in sInitial :
                nt = Transition(t.stateSrc, t.etiquette, s) #on cree une nouvelle transition qui va de l'etat source de la transition vers les etats initiales
                auto.addTransition(nt) # on ajoute la transition a auto 

        return auto
        




