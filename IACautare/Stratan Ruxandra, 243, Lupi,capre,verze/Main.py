

#Citire de la tastatura
print("Introduceti numele fisierului de intrare:")
fileName = input()
print("Introduceti numarul de solutii dorite:")
nSol=int(input())

#Prelucrarea datelor din fisier
f=open("C:/Users/ruxan/PycharmProjects/Lupi,capre,verze/venv/"+fileName,"r")
linii=f.readlines()

#Prima linie: nr de verze, capre si lupi de pe malul de est
l1 = linii[0].strip().split()
verze_init = int(l1[0])
capre_init = int(l1[2])
lupi_init = int(l1[4])

#A doua linie: capacitatea compartimentelor A si B si a magaziei
l2 = linii[1].strip().split()
K1 = int(l2[0])
K2 = int(l2[1])
M = int(l2[2])

#A treia linie: cat se mananca
l3 = linii[2].strip().split()
lup_lup = int(l3[1])
lup_capra = int(l3[3])
capra_varza = int(l3[5])

#Ultima linie: nr minim de verze, capre si lupi pt o stare finala
l4 = linii[3].strip().split()
verze_FINAL = int(l4[2])
capre_FINAL = int(l4[4])
lupi_FINAL = int(l4[6])

# print(verze_init,capre_init,lupi_init)
# print(K1, K2, M)
# print(lup_lup, lup_capra, capra_varza)
# print(verze_FINAL,capre_FINAL,lupi_FINAL)


#Verificare:

#0. Nu sunt numere negative printre datele de intrare
if(capre_init<0 or verze_init<0 or lupi_init<0 or verze_FINAL<0 or\
        capre_FINAL<0 or lupi_FINAL<0 or K1<0 or K2<0 or M<0):
    print("Input invalid")
    exit(True)

#1. Starea initiala este si finala
if(verze_FINAL+capre_FINAL+lupi_FINAL+verze_init+capre_init+lupi_init)==0:
    print("Starea initiala este deja si stare finala")
    exit(True)

#2. Nu se poate ajunge din starea initiala intr-o stare finala
if(verze_init< verze_FINAL or capre_init<capre_FINAL or lupi_init<lupi_FINAL):
    print("Problema nu are solutii")
    exit(True)


#O "stare" este de forma unei liste cu trei elemente - tot liste
#ex: [[1],[6,0,2],[7,2,0,5,2]]
#Primul element indica unde se afla taranul: [0] pt malul de est si [1]
#pentru cel de vest
#Al doilea indica numarul de verze, capre si lupi de pe malul de est (malul initial)
#Al treilea indica numarul de verze, capre si lupi de pe malul de vest, numarul
#de elemente aflate in magazie, precum si ce se afla in magazie - 1 pt verze,
#2 pt capre, 3 pt lupi, 0 pt nimic

#Astfel, starea [[1],[6,0,2],[7,2,0,5,2]] reprezinta:
# - taranul se afla pe malul de vest
# - pe malul de est sunt 6 verze, 0 capre si 2 lupi
# - pe malul de vest sunt 7 verze, 2 capre, 0 lupi + 5 capre in magazie

#Observatie: o stare este considerata dupa ce toate animalele s-au hranit
#odata cu plecarea taranului. Starea intermediara este "simplificata"
#in cadrul generarii succesorilor inainte de adaugarea in lista_succesori
#prin functia mananca() - prezentata mai jos

#Astfel, dupa citirea din fisier, starea initiala va fi:
start = [[0],[verze_init,capre_init,lupi_init],[0,0,0,0,0]]

#Exemplu de succesiune de stari:
st1=[[0],[21,10,2],[0,0,0,0,0]]
st2=[[1],[15,1,2],[0,7,0,0,0]]
st3=[[0],[15,1,2],[0,7,0,0,0]]
st4=[[1],[6,0,2],[7,2,0,5,2]]
st5=[[0],[6,2,2],[7,0,0,5,2]]
st6=[[1],[2,0,1],[11,2,0,5,2]]
st7=[[0],[2,2,1],[11,0,0,5,2]]
st8=[[1],[0,2,0],[13,0,1,5,2]]
st9=[[0],[0,2,0],[13,0,1,5,2]]
st10=[[1],[0,0,0],[13,2,1,5,2]] #final

#Functia de testare scop => nu au mai ramas verze, capre sau lupi pe malul de est
#iar pe malul de vest sunt indeplinite conditiile minime din fisier
def testeaza_scop(nodInfo):
  global verze_FINAL, capre_FINAL, lupi_FINAL
  if(nodInfo[1][0]+nodInfo[1][1]+nodInfo[1][2])!=0:
    return False
  v,c,l = 0,0,0
  #Adun eventuale elemente din magazie
  if(nodInfo[2][4]==1): v+=nodInfo[2][3]
  if(nodInfo[2][4]==2): c+=nodInfo[2][3]
  if(nodInfo[2][4]==3): l+=nodInfo[2][3]
  v+=nodInfo[2][0]
  c+=nodInfo[2][1]
  l+=nodInfo[2][2]
  if(v<verze_FINAL or c<capre_FINAL or l<lupi_FINAL):
    return False
  return True

#print(testeaza_scop([[1],[0,0,0],[13,2,1,5,2]])) #=> True


#Euristica
import math
def calculeaza_h(infoNod, tip_euristica="euristica banala"):
    global K1,K2, verze_FINAL,capre_FINAL,lupi_FINAL
    if tip_euristica=="euristica banala":
        if testeaza_scop(infoNod)==False:
            return 1
        return 0
    elif tip_euristica == "euristica admisibila 1": #daca sunt mai mult de 3 tipuri de elemente
      h = 0                                         #pe malul de est si starile finale trebuie sa
      nr = 0                                        #aiba un nr nenul din fiecare element pe malul de vest,
      if(infoNod[1][0]!=0): nr+=1                   #barca va face cel putin 2 drumuri de la est la vest pt ca nu se pot
      if(infoNod[1][1]!=0): nr+=1                   #transporta decat maxim 2 tipuri de elemente odata
      if(infoNod[1][2]!=0): nr+=1
      if(nr == 3 and verze_FINAL!=0 and capre_FINAL!=0 and lupi_FINAL!=0): h = 2
      elif(nr > 0): h = 1
      return h
    elif tip_euristica == "euristica admisibila 2":    #nr total de elemente ramase pe malul de est
      total = K1 + K2                                  #impartit la nr de locuri disponibile in barca
      vcl = infoNod[1][0]+infoNod[1][1]+infoNod[1][2]
      h = math.ceil(vcl/total)
      return h
    elif tip_euristica == "euristica neadmisibila":    #fiecare element este transportat separat
      h = infoNod[1][0]+infoNod[1][1]+infoNod[1][2]
      return h

# print(calculeaza_h([[1],[16,3,2],[2,4,1,0,0]],"euristica banala")) #=>1
# print(calculeaza_h([[1],[16,3,2],[2,4,1,0,0]],"euristica admisibila 1")) #=>2
# print(calculeaza_h([[1],[16,3,2],[2,4,1,0,0]],"euristica admisibila 2"))  #=>3
# print(calculeaza_h([[1],[16,3,2],[2,4,1,0,0]],"euristica neadmisibila"))  #=>21


#Functia auxiliara mananca folosita pt "simplificarea" unei stari noi in cadrul
#functiei de generare a succesorilor, care returneaza aceeasi configuratie minus
#verzele/caprele/lupii care dispar de pe malul unde nu este taranul -> sunt mancate/mancati
#de capre/lupi
def mananca(stare):
    global lup_capra, lup_lup, capra_varza
    if (stare[0][0] == 0):  # taranul e pe malul de est => mananca cele din vest
        v, c, l = stare[2][0], stare[2][1], stare[2][2]
    else:  # taranul e pe malul de vest => mananca cele din est
        v, c, l = stare[1][0], stare[1][1], stare[1][2]
    # print(v,c,l)

    if (c != 0):  # exista capre
        v -= c * capra_varza  # capre mananca verze
        if (v < 0): v = 0
        c -= l * lup_capra  # lupi mananca capre
        if (c < 0): c = 0
    else:  # lupi manaca lupi pt ca nu exista capre pe acel mal
        if (l > 1): l -= lup_lup
        if (l < 0): l = 0

    if (stare[0][0] == 0):
        stare[2][0], stare[2][1], stare[2][2] = v, c, l
    else:
        stare[1][0], stare[1][1], stare[1][2] = v, c, l

    return stare

#print(mananca([[1],[21,3,2],[0,7,0,0,0]]))  #=> [[1], [15, 1, 2], [0, 7, 0, 0, 0]]



#Idee/Prototip pt functia de generare a succesorilor
def genereaza_succesori(stCrt, tip_euristica="euristica banala"):
    lista_succesori = []
    global K1, K2, M

    if (stCrt[0][0] == 0):  # Taranul este pe malul de est, succesorii vor fi pe malul de vest

        for i in range(3):

            if (i == 0):  # mut verze in compartimentul A
                if (stCrt[1][0] == 0): continue  # nu am verze
                for j in range(4):
                    if (j == 0):  # nu mut nimic in compartimentul B
                        # mut doar verze in compartimentul A
                        #j==1: verze in A si in B
                        #j==2: verze in A si capre in B
                        #j==3: verze in A si lupi in B
                        v, c, l = stCrt[1][0], stCrt[1][1], stCrt[1][2]
                        v_op, c_op, l_op = stCrt[2][0], stCrt[2][1], stCrt[2][2]
                        v_mal_op, c_mal_op, l_mal_op = stCrt[2][0], stCrt[2][1], stCrt[2][2]
                        v_max_mut = min(K1, v)
                        k = 1
                        while (k <= v_max_mut):
                            v_mal_init = v - k
                            v_mal_op = v_op + k
                            mag = stCrt[2][3]
                            mag2 = stCrt[2][4]

                            # Var1: nu se umbla la magazie
                            stare_noua = [[1], [v_mal_init, c, l], [v_mal_op, c_op, l_op, mag, mag2]]
                            lista_succesori.append(mananca(stare_noua))

                            # Var2: e ceva in magazie si se scoate (totul, nu pe bucati)
                            if (mag != 0):
                                if (mag2 == 1):  # in magazie sunt verze
                                    v_mal_op += mag
                                elif (mag2 == 2):  # in magazie sunt capre
                                    c_mal_op = c_op + mag
                                else:  # in magazie sunt lupi
                                    l_mal_op = l_op + mag

                                stare_noua = [[1], [v_mal_init, c, l], [v_mal_op, c_mal_op, l_mal_op, 0, 0]]
                                lista_succesori.append(mananca(stare_noua))

                            # Var3: nu e nimic in magazie si pun
                            if (mag == 0):
                                if (v_mal_op > 0):  # pun verze in magazie
                                    mag = min(M, v_mal_op)
                                    mag2 = 1
                                    v_mal_op -= min(M, v_mal_op)
                                    stare_noua = [[1], [v_mal_init, c, l], [v_mal_op, c_mal_op, l_mal_op, mag, mag2]]
                                    lista_succesori.append(mananca(stare_noua))
                                if (c_mal_op > 0):  # pun capre in magazie
                                    mag = min(M, c_mal_op)
                                    mag2 = 2
                                    c_mal_op -= min(M, c_mal_op)
                                    stare_noua = [[1], [v_mal_init, c, l], [v_mal_op, c_mal_op, l_mal_op, mag, mag2]]
                                    lista_succesori.append(mananca(stare_noua))
                                if (l_mal_op > 0):  # pun lupi in magazie
                                    mag = min(M, l_mal_op)
                                    mag2 = 3
                                    l_mal_op -= min(M, l_mal_op)
                                    stare_noua = [[1], [v_mal_init, c, l], [v_mal_op, c_mal_op, l_mal_op, mag, mag2]]
                                    lista_succesori.append(mananca(stare_noua))

                            k += 1

            if (i == 1):  # mut capre in compartimentul A
                if (stCrt[1][1] == 0): continue  # nu am capre

            if (i == 2):  # mut lupi in compartimentul A
                if (stCrt[1][2] == 0): continue  # nu am lupi

    else:
        pass
        # Analog mal est, doar ca adaug posibilitatea ca barca sa se intoarca goala
        # si se elimina magazia

    return lista_succesori
