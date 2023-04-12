import random

import plotly.graph_objects as go

import networkx as nx
import matplotlib.pyplot as plt

def liste_individu(n, p) :
   # Création de la liste
    I =[]
    for j in range (n+2) :
        prob = random.random()
        if prob<p:
            ethnie = 0
        else:
            ethnie = 1
        I.append(ethnie)
    return I

def calcul_SUM_P(P) :
    # Crée une liste SUM_P de tel sorte que SUM_P = [p1,p1+p2,p1+p2+p3 ..., p1+...+pn]
    # Cette liste sert à calculer des probabilités avec la fonction random
    SUM_P=[0]
    sum_P = 0
    for k in range(len(P)) :
        sum_P = sum_P + P[k]
        SUM_P.append(sum_P)
    return SUM_P

def calcul_sum_deg(G) :
    #Calcul la somme des connexions de chaque sommet (si 1 est lié à 0 et 0 est lié à 1 on a sum_deg = 2)
    sum_deg=0
    for k in range(len(G)) :
        sum_deg = sum_deg + len(G[k][1])
    return sum_deg


def ville(n,h, proportion):
    # Une ville est une agglomération d'individus
    # G  : liste des sommets Si du graphes
    # S  = [continent population 1 ou non (1 si population 1 et 0 sinon), [liste des connexions avec d'autres sommets]]
    # I : liste de des individus caractérisé par leur origine (population 1 ou population 2) à répartir dans les différentes villes
    # P  = [p1, ..., pn] avec pi la probabilité qu'un individu s'attache au sommet i
    # sum_deg : somme des degrés (connexions) du graph
    # sommet_choisi : sommet sur lequel va se fixer le nouvel individu
    # a : sommet potentiellement choisi par l'individu
    # h : homophilie
    # proportion : proportion de la population 1 dans la ville

    I = liste_individu(n, proportion)
    G = [[I[0],[1]],[I[1],[0]]]
    P =[1/2,1/2]
    SUM_P = calcul_SUM_P(P)
    a = 0
    



    # Création du graph grâce à un "algorithme de décisionnel"
    for i in range(len(I)-2) :
        while len(G) != i+3 :
        # tant que l'individu I n'a pas choisi de se fixer sur un sommet du graph, on continue l'algorithme de prise de décision suivant
            r = random.random()
            SUM_P = calcul_SUM_P(P)
            for k in range(len(SUM_P)) :
                if SUM_P[k] <= r and r <= SUM_P[k+1] :
                # L'individu va d'abord choisir le sommet auquel il s'intéresse. Cette probabilité est calculée grâce à la fonction random qui renvoie un chiffre entre 0 et 1. On compare ce chiffre au élément de la liste SUM_P pour trouver le sommet a été choisi. Le sommet k a été choisi.

                    if I[i+2] == G[k][0] :
                    # Si l'individu i+2 (+2 car individu0 et individu1 déjà sur la carte) est de la même nationnalité que l'individu du sommet k a alors le lien est établi
                        G[k][1].append(i+2)
                        #print("A la {} itération de l'algo : Le sommet {} a été choisi du premier coup. On a i+2 = {}, G = {} et G[{}][1] ={}".format(i,k, i+2, G,k,G[k][1]))
                        # dans ce cas on ajoute alors i+2 à la liste des connexions de l'individu k
                        G.append([I[i],[k]])
                        # on ajoute un sommet au graph
                        for j in range(len(P)):
                            P[j] = (len(G[j][1]))/calcul_sum_deg(G)
                        # puis on calcule ensuite la nouvelle probabilité de venir se fixer à chaque sommet
                        #print("On a ensuite ajouté un nouveau sommet, on a G= {} et modifier l'ancienne liste des probas avec P={}".format(G,P))
                        P.append(1/calcul_sum_deg(G))
                        # on ajoute la probabilité de choisir le sommet i+2 (l'individu i+2) à la liste des probabilités
                        #print("Finalement on se retrouve avec P={} à la {} itération".format(P,i))
                        break



                    else :
                    # Si l'individu i+2 n'est pas de la même nationnalité que l'individu du sommet
                        if random.random() < h :
                        # Il va décider de se fixer à ce sommet avec la probabilité p ( dépend de son homophilie ) et si il décide de rester :
                            G[k][1].append(i+2)
                            # on ajoute alors i+2 à la liste des connexions de l'individu k
                            #print("A la {} itération de l'algo : Le sommet {} a été choisi après réfléxion. On a i+2 = {}, G = {} et G[{}][1]={}".format(i,k, i+2, G, k,G[k][1]))
                            G.append([I[i],[k]])
                            # on ajoute un sommet au graph
                            for j in range(len(P)):
                                P[j] = (len(G[j][1]))/calcul_sum_deg(G)
                            # puis on calcule ensuite la nouvelle probabilité de venir se fixer à chaque sommet
                            #print("On a ensuite ajouté un nouveau sommet, on a G= {} et modifier l'ancienne liste des probas avec P={}".format(G,P))
                            P.append(1/calcul_sum_deg(G))
                            # on ajoute la probabilité de choisir le sommet i+2 (l'individu i+2) à la liste des probabilités
                            #print("Finalement on se retrouve avec P={} a la {} itération".format(P,i))
                            break

    return G

def compter_connexions(liste):
    sum1 = 0
    sum2 = 0
    for k in range(len(liste)):
        if liste[k][0] == 0:
            sum1 += len(liste[k][1])
        else:
            sum2 += len(liste[k][1])
    print("Nombre de connexions pour la population 1 : ", sum1)
    print("Nombre de connexions pour la population 2 : ", sum2)

nb_individus = int(input("Entrez le nombre d'individus : "))
homophilie = float(input("Entrez l'homophilie : "))
while homophilie > 1 or homophilie < 0:
    print("L'homophilie doit être comprise entre 0 et 1")
    homophilie = float(input("Entrez l'homophilie : "))
proportion = float(input("Entrez la proportion de la population 1 : "))
while proportion > 1 or proportion < 0:
    print("La proportion doit être comprise entre 0 et 1")
    proportion = float(input("Entrez la proportion de la population 2 : "))
    
liste = ville(nb_individus, homophilie, proportion)
compter_connexions(liste)


color_map = []
Graph = nx.Graph()
for i in range(len(liste)):
    Graph.add_node(i)
    for j in range(len(liste[i][1])):
        Graph.add_edge(i, liste[i][1][j])
for node in Graph:
    if liste[node][0] == 0:
        color_map.append('red')
    else:
        color_map.append('blue')
pos = nx.spring_layout(Graph, k=0.15, iterations=100, scale=2)
nx.draw(Graph, pos = pos, node_color=color_map, with_labels=False)
plt.show()
