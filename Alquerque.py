#Am folosit modelul de la laborator pt implementare

#Algoritmii min_mx/alpha_beta
def min_max(stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    stare.mutari_posibile = stare.mutari()

    mutariCuEstimare = [min_max(x) for x in
                        stare.mutari_posibile]

    if stare.j_curent == Joc.JMAX:
        stare.stare_aleasa = max(mutariCuEstimare, key=lambda x: x.estimare)
    else:
        stare.stare_aleasa = min(mutariCuEstimare, key=lambda x: x.estimare)

    stare.estimare = stare.stare_aleasa.estimare
    return stare


def alpha_beta(alpha, beta, stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    if alpha > beta:
        return stare

    stare.mutari_posibile = stare.mutari()

    if stare.j_curent == Joc.JMAX:
        estimare_curenta = float('-inf')

        for mutare in stare.mutari_posibile:
            stare_noua = alpha_beta(alpha, beta, mutare)

            if (estimare_curenta < stare_noua.estimare):
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare
            if (alpha < stare_noua.estimare):
                alpha = stare_noua.estimare
                if alpha >= beta:  # interval invalid
                    break

    elif stare.j_curent == Joc.JMIN:
        estimare_curenta = float('inf')
        for mutare in stare.mutari_posibile:
            stare_noua = alpha_beta(alpha, beta, mutare)

            if (estimare_curenta > stare_noua.estimare):
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare
            if (beta > stare_noua.estimare):
                beta = stare_noua.estimare
                if alpha >= beta:
                    break

    stare.estimare = stare.stare_aleasa.estimare

    return stare

import time
import copy

ADANCIME_MAX=6

#CLASA JOC CU METODELE SPECIFICE
class Joc:
    NR_COLOANE = 5
    JMIN = None
    JMAX = None
    GOL = '#'

    # stare initiala
    def __init__(self, tabla=None):  # Joc()
        self.matr = tabla or [['N', 'N', 'N', 'N', 'N'], ['N', 'N', 'N', 'N', 'N'], ['N', 'N', '#', 'A', 'A'],
                              ['A', 'A', 'A', 'A', 'A'], ['A', 'A', 'A', 'A', 'A']]

    @classmethod
    def jucator_opus(cls, jucator):
        return cls.JMAX if jucator == cls.JMIN else cls.JMIN

    # Configuratia tablei permite doar unor piese sa se deplaseze pe diagonala, raportat la pozitia lor
    # Astfel, piesa de indice [i][j] se poate deplasa pe diagonala doar daca suma i+j este para
    def diag(self, i, j):
        if ((i + j) % 2) == 0: return True
        return False

    #TESTARE STARE FINALA
    def final(self):
        stare = self.matr
        # 1. Nu mai sunt piese
        okn, oka = 0, 0
        for i in range(5):
            for j in range(5):
                if (stare[i][j] == 'A'):
                    oka = 1
                elif (stare[i][j] == 'N'):
                    okn = 1
        if (okn + oka) == 0: return 'remiza'
        if (okn + oka) == 1:
            if (okn == 0):
                return 'A'  # nu mai sunt piese negre => a castigat A
            else:
                return 'N'  # nu mai sunt piese albe => a castigat N

        # 2. Nu mai sunt mutari disponibile
        # diag(i,j) va verifica daca sunt posibile mutarile/salturile pe diagonale
        okn, oka = 0, 0
        for i in range(5):
            for j in range(5):
                # Pentru ALB
                if (stare[i][j] == 'A'):

                    # posibile mutari pe linia precedenta
                    if (i - 1) >= 0:
                        if (j - 1) >= 0 and self.diag(i, j):
                            # muta la i-1,j-1
                            if (stare[i - 1][j - 1] == '#'): oka = 1
                            # sare peste i-1,j-1 la i-2,j-2
                            if (stare[i - 1][j - 1] == 'N' and (i - 2) >= 0 and (j - 2) >= 0):
                                if (stare[i - 2][j - 2] == '#'): oka = 1
                        # muta la i-1,j
                        if (stare[i - 1][j] == '#'): oka = 1
                        # sare peste i-1,j la i-2,j
                        if (stare[i - 1][j] == 'N' and (i - 2) >= 0):
                            if (stare[i - 2][j] == '#'): oka = 0
                        if (j + 1) <= 4 and self.diag(i, j):
                            # muta la i-1,j+1
                            if (stare[i - 1][j + 1] == '#'): oka = 1
                            # sare peste i-1,j+1 la i-2,j+2
                            if (stare[i - 1][j + 1] == 'N' and (i - 2) >= 0 and (j + 2) <= 4):
                                if (stare[i - 2][j + 2] == '#'): oka = 1

                    # posibile mutari pe linia curenta
                    if (j - 1) >= 0:
                        # muta la i,j-1
                        if (stare[i][j - 1] == '#'): oka = 1
                        # sare peste i,j-1 la i,j-2
                        if (stare[i][j - 1] == 'N' and (j - 2) >= 0):
                            if (stare[i][j - 2] == '#'): oka = 1
                    if (j + 1) <= 4:
                        # muta la i,j+1
                        if (stare[i][j + 1] == '#'): oka = 1
                        # sare peste i,j+1 la i,j+2
                        if (stare[i][j + 1] == 'N' and (j + 2) <= 4):
                            if (stare[i][j + 2] == '#'): oka = 1

                    # posibile mutari pe linia urmatoare
                    if (i + 1) <= 4:
                        if (j - 1) >= 0 and self.diag(i, j):
                            # muta la i+1,j-1
                            if (stare[i + 1][j - 1] == '#'): oka = 1
                            # sare peste i+1,j-1 la i+2,j-2
                            if (stare[i + 1][j - 1] == 'N' and (i + 2) <= 4 and (j - 2) >= 0):
                                if (stare[i + 2][j - 2] == '#'): oka = 1
                        # muta la i+1,j
                        if (stare[i + 1][j] == '#'): oka = 1
                        # sare peste i+1,j la i+2,j
                        if (stare[i + 1][j] == 'N' and (i + 2) <= 4):
                            if (stare[i + 2][j] == '#'): oka = 1
                        if (j + 1) <= 4 and self.diag(i, j):
                            # muta la i+1,j+1
                            if (stare[i + 1][j + 1] == '#'): oka = 1
                            # sare peste i+1,j+1 la i+2,j+2
                            if (stare[i + 1][j + 1] == 'N' and (i + 2) <= 4 and (j + 2) <= 4):
                                if (stare[i + 2][j + 2] == '#'): oka = 1

                # Pentru NEGRU
                elif (stare[i][j] == 'N'):
                    # posibile mutari pe linia precedenta
                    if (i - 1) >= 0:
                        if (j - 1) >= 0 and self.diag(i, j):
                            # muta la i-1,j-1
                            if (stare[i - 1][j - 1] == '#'): okn = 1
                            # sare peste i-1,j-1 la i-2,j-2
                            if (stare[i - 1][j - 1] == 'A' and (i - 2) >= 0 and (j - 2) >= 0):
                                if (stare[i - 2][j - 2] == '#'): okn = 1
                        # muta la i-1,j
                        if (stare[i - 1][j] == '#'): okn = 1
                        # sare peste i-1,j la i-2,j
                        if (stare[i - 1][j] == 'A' and (i - 2) >= 0):
                            if (stare[i - 2][j] == '#'): okn = 0
                        if (j + 1) <= 4 and self.diag(i, j):
                            # muta la i-1,j+1
                            if (stare[i - 1][j + 1] == '#'): okn = 1
                            # sare peste i-1,j+1 la i-2,j+2
                            if (stare[i - 1][j + 1] == 'A' and (i - 2) >= 0 and (j + 2) <= 4):
                                if (stare[i - 2][j + 2] == '#'): okn = 1

                    # posibile mutari pe linia curenta
                    if (j - 1) >= 0:
                        # muta la i,j-1
                        if (stare[i][j - 1] == '#'): okn = 1
                        # sare peste i,j-1 la i,j-2
                        if (stare[i][j - 1] == 'A' and (j - 2) >= 0):
                            if (stare[i][j - 2] == '#'): okn = 1
                    if (j + 1) <= 4:
                        # muta la i,j+1
                        if (stare[i][j + 1] == '#'): okn = 1
                        # sare peste i,j+1 la i,j+2
                        if (stare[i][j + 1] == 'A' and (j + 2) <= 4):
                            if (stare[i][j + 2] == '#'): okn = 1

                    # posibile mutari pe linia urmatoare
                    if (i + 1) <= 4:
                        if (j - 1) >= 0 and self.diag(i, j):
                            # muta la i+1,j-1
                            if (stare[i + 1][j - 1] == '#'): okn = 1
                            # sare peste i+1,j-1 la i+2,j-2
                            if (stare[i + 1][j - 1] == 'A' and (i + 2) <= 4 and (j - 2) >= 0):
                                if (stare[i + 2][j - 2] == '#'): okn = 1
                        # muta la i+1,j
                        if (stare[i + 1][j] == '#'): okn = 1
                        # sare peste i+1,j la i+2,j
                        if (stare[i + 1][j] == 'A' and (i + 2) <= 4):
                            if (stare[i + 2][j] == '#'): okn = 1
                        if (j + 1) <= 4 and self.diag(i, j):
                            # muta la i+1,j+1
                            if (stare[i + 1][j + 1] == '#'): okn = 1
                            # sare peste i+1,j+1 la i+2,j+2
                            if (stare[i + 1][j + 1] == 'A' and (i + 2) <= 4 and (j + 2) <= 4):
                                if (stare[i + 2][j + 2] == '#'): okn = 1
        if (oka + okn) == 1:
            if (oka == 0):
                return 'N'
            else:
                return 'A'
        if (oka + okn) == 0:
            return 'Jucatorul curent'

        return False

    #GENERARE SUCCESORI => posibile mutari
    def mutari(self, jucator):  # jucator = simbolul jucatorului care muta
        l_mutari = []
        stare = self.matr
        if (jucator == 'A'):
            opus = 'N'
        else:
            opus = 'A'
        for i in range(5):
            for j in range(5):
                if (self.matr[i][j] == jucator):

                    # posibile mutari pe linia precedenta
                    if (i - 1) >= 0:
                        if (j - 1) >= 0 and self.diag(i, j):
                            # muta pe i-1,j-1
                            if (stare[i - 1][j - 1] == '#'):
                                copie_matr = copy.deepcopy(self.matr)
                                copie_matr[i - 1][j - 1] = jucator
                                copie_matr[i][j] = '#'
                                l_mutari.append(Joc(copie_matr))
                            # sare peste i-1,j-1 la i-2,j-2
                            if (stare[i - 1][j - 1] == opus and (i - 2) >= 0 and (j - 2) >= 0):
                                if (stare[i - 2][j - 2] == '#'):
                                    copie_matr = copy.deepcopy(self.matr)
                                    copie_matr[i - 2][j - 2] = jucator
                                    copie_matr[i][j] = '#'
                                    copie_matr[i - 1][j - 1] = '#'  # ia piesa adversarului peste care a sarit
                                    l_mutari.append(Joc(copie_matr))
                        # muta pe i-1, j
                        if (stare[i - 1][j] == '#'):
                            copie_matr = copy.deepcopy(self.matr)
                            copie_matr[i - 1][j] = jucator
                            copie_matr[i][j] = '#'
                            l_mutari.append(Joc(copie_matr))
                        # sare peste i-1,j la i-2,j
                        if (stare[i - 1][j] == 'N' and (i - 2) >= 0):
                            if (stare[i - 2][j] == '#'):
                                copie_matr = copy.deepcopy(self.matr)
                                copie_matr[i - 2][j] = jucator
                                copie_matr[i][j] = '#'
                                copie_matr[i - 1][j] = '#'
                                l_mutari.append(Joc(copie_matr))

                        if (j + 1) <= 4 and self.diag(i, j):
                            # muta la i-1,j+1
                            if (stare[i - 1][j + 1] == '#'):
                                copie_matr = copy.deepcopy(self.matr)
                                copie_matr[i - 1][j + 1] = jucator
                                copie_matr[i][j] = '#'
                                l_mutari.append(Joc(copie_matr))
                            # sare peste i-1,j+1 la i-2,j+2
                            if (stare[i - 1][j + 1] == 'N' and (i - 2) >= 0 and (j + 2) <= 4):
                                if (stare[i - 2][j + 2] == '#'):
                                    copie_matr = copy.deepcopy(self.matr)
                                    copie_matr[i - 2][j + 2] = jucator
                                    copie_matr[i][j] = '#'
                                    copie_matr[i - 1][j + 1] = '#'
                                    l_mutari.append(Joc(copie_matr))

                    # posibile mutari pe linia curenta
                    if (j - 1) >= 0:
                        # muta la i,j-1
                        if (stare[i][j - 1] == '#'):
                            copie_matr = copy.deepcopy(self.matr)
                            copie_matr[i][j - 1] = jucator
                            copie_matr[i][j] = '#'
                            l_mutari.append(Joc(copie_matr))
                        # sare peste i,j-1 la i,j-2
                        if (stare[i][j - 1] == 'N' and (j - 2) >= 0):
                            if (stare[i][j - 2] == '#'):
                                copie_matr = copy.deepcopy(self.matr)
                                copie_matr[i][j - 2] = jucator
                                copie_matr[i][j] = '#'
                                copie_matr[i][j - 1] = '#'
                                l_mutari.append(Joc(copie_matr))
                    if (j + 1) <= 4:
                        # muta la i,j+1
                        if (stare[i][j + 1] == '#'):
                            copie_matr = copy.deepcopy(self.matr)
                            copie_matr[i][j + 1] = jucator
                            copie_matr[i][j] = '#'
                            l_mutari.append(Joc(copie_matr))
                        # sare peste i,j+1 la i,j+2
                        if (stare[i][j + 1] == 'N' and (j + 2) <= 4):
                            if (stare[i][j + 2] == '#'):
                                copie_matr = copy.deepcopy(self.matr)
                                copie_matr[i][j + 2] = jucator
                                copie_matr[i][j] = '#'
                                copie_matr[i][j + 1] = '#'
                                l_mutari.append(Joc(copie_matr))

                    # posibile mutari pe linia urmatoare
                    if (i + 1) <= 4:
                        if (j - 1) >= 0 and self.diag(i, j):
                            # muta la i+1,j-1
                            if (stare[i + 1][j - 1] == '#'):
                                copie_matr = copy.deepcopy(self.matr)
                                copie_matr[i + 1][j - 1] = jucator
                                copie_matr[i][j] = '#'
                                l_mutari.append(Joc(copie_matr))
                            # sare peste i+1,j-1 la i+2,j-2
                            if (stare[i + 1][j - 1] == 'N' and (i + 2) <= 4 and (j - 2) >= 0):
                                if (stare[i + 2][j - 2] == '#'):
                                    copie_matr = copy.deepcopy(self.matr)
                                    copie_matr[i + 2][j - 2] = jucator
                                    copie_matr[i][j] = '#'
                                    copie_matr[i + 1][j - 1] = '#'
                                    l_mutari.append(Joc(copie_matr))
                        # muta la i+1,j
                        if (stare[i + 1][j] == '#'):
                            copie_matr = copy.deepcopy(self.matr)
                            copie_matr[i + 1][j] = jucator
                            copie_matr[i][j] = '#'
                            l_mutari.append(Joc(copie_matr))
                        # sare peste i+1,j la i+2,j
                        if (stare[i + 1][j] == 'N' and (i + 2) <= 4):
                            if (stare[i + 2][j] == '#'):
                                copie_matr = copy.deepcopy(self.matr)
                                copie_matr[i + 2][j] = jucator
                                copie_matr[i][j] = '#'
                                copie_matr[i + 1][j] = '#'
                                l_mutari.append(Joc(copie_matr))
                        if (j + 1) <= 4 and self.diag(i, j):
                            # muta la i+1,j+1
                            if (stare[i + 1][j + 1] == '#'):
                                copie_matr = copy.deepcopy(self.matr)
                                copie_matr[i + 1][j + 1] = jucator
                                copie_matr[i][j] = '#'
                                l_mutari.append(Joc(copie_matr))
                            # sare peste i+1,j+1 la i+2,j+2
                            if (stare[i + 1][j + 1] == 'N' and (i + 2) <= 4 and (j + 2) <= 4):
                                if (stare[i + 2][j + 2] == '#'):
                                    copie_matr = copy.deepcopy(self.matr)
                                    copie_matr[i + 2][j + 2] = jucator
                                    copie_matr[i][j] = '#'
                                    copie_matr[i + 1][j + 1] = '#'
                                    l_mutari.append(Joc(copie_matr))

        return l_mutari

    #VALIDAREA MUTARII UTLIZATORULUI
    def validare(self, l, c, lf, cf, st):
        valid = False
        valid_salt = False
        l_salt, c_salt = 0, 0
        rez = []

        # i-1,j - sus
        if lf == (l - 1) and cf == c: valid = True
        # i,j-1 - stanga
        if lf == l and cf == (c - 1): valid = True
        # i,j+1 - dreapta
        if lf == l and cf == (c + 1): valid = True
        # i+1,j - jos
        if lf == (l + 1) and cf == c: valid = True

        # diagonale
        if self.diag(l, c):
            # i-1,j-1 - stanga sus
            if lf == (l - 1) and cf == (c - 1): valid = True
            # i-1,j+1 - dreapta sus
            if lf == (l - 1) and cf == (c + 1): valid = True
            # i+1,j-1 - stanga jos
            if lf == (l + 1) and cf == (c - 1): valid = True
            # i+1,j+1 - dreapta jos
            if lf == (l + 1) and cf == (c + 1): valid = True

        if (st == 'A'):
            sop = 'N'
        else:
            sop = 'A'

        # Salturi
        # i-2,j - sus
        if lf == (l - 2) and cf == c and self.matr[l - 1][c] == sop:
            valid, valid_salt = True, True
            l_salt = l - 1
            c_salt = c
        # i, j-2 - stanga
        if lf == l and cf == (c - 2) and self.matr[l][c - 1] == sop:
            valid, valid_salt = True, True
            l_salt = l
            c_salt = c - 1
        # i, j+2 - dreapta
        if lf == l and cf == (c + 2) and self.matr[l][c + 1] == sop:
            valid, valid_salt = True, True
            l_salt = l
            c_salt = c + 1
        # i+2, j - jos
        if lf == (l + 2) and cf == c and self.matr[l + 1][c] == sop:
            valid, valid_salt = True, True
            l_salt = l + 1
            c_salt = c

        # Salturi pe diagonale
        if self.diag(l, c):
            # i-2,j-2 - stanga sus
            if lf == (l - 2) and cf == (c - 2) and self.matr[l - 1][c - 1] == sop:
                valid, valid_salt = True, True
                l_salt = l - 1
                c_salt = c - 1
            # i-2,j+2 - dreapta sus
            if lf == (l - 2) and cf == (c + 2) and self.matr[l - 1][c + 1] == sop:
                valid, valid_salt = True, True
                l_salt = l - 1
                c_salt = c + 1
            # i+2, j-2 - stanga jos
            if lf == (l + 2) and cf == (c - 2) and self.matr[l + 1][c - 1] == sop:
                valid, valid_salt = True, True
                l_salt = l + 1
                c_salt = c - 1
            # i+2, j+2 - dreapta jos
            if lf == (l + 2) and cf == (c + 2) and self.matr[l + 1][c + 1] == sop:
                valid, valid_salt = True, True
                l_salt = l + 1
                c_salt = c + 1

        #valid - mutarea e valida
        #valid_salt - mutarea e un salt valid
        #l_salt, c_salt => indicii piesei adversarului peste care se sare si care va fi eliminata
        rez = [valid, valid_salt, l_salt, c_salt]
        return rez

    # Calculeaza nr de piese ale jucatorului curent ramase pe tabla
    def nr_piese(self, jucator):
        nr = 0
        for i in range(5):
            for j in range(5):
                if self.matr[i][j] == jucator: nr += 1
        return nr

    # ESTIMARE in functie de cate piese ale jucatorului curent mai raman, comparativ cu
    # adversarul
    def estimeaza_scor(self, adancime):
        t_final = self.final()

        if t_final == self.__class__.JMAX:
            return (199 + adancime)
        elif t_final == self.__class__.JMIN:
            return (-199 - adancime)
        elif t_final == 'remiza':
            return 0
        else:
            return (self.nr_piese(self.__class__.JMAX) - self.nr_piese(self.__class__.JMIN))

    def sirAfisare(self):
        stare = self.matr
        print(stare[0][0] + stare[0][1] + stare[0][2] + stare[0][3] + stare[0][4])
        print(stare[1][0] + stare[1][1] + stare[1][2] + stare[1][3] + stare[1][4])
        print(stare[2][0] + stare[2][1] + stare[2][2] + stare[2][3] + stare[2][4])
        print(stare[3][0] + stare[3][1] + stare[3][2] + stare[3][3] + stare[3][4])
        print(stare[4][0] + stare[4][1] + stare[4][2] + stare[4][3] + stare[4][4])

    def __str__(self):
        # return self.sirAfisare()
        self.sirAfisare()
        return ""

    def __repr__(self):
        # return self.sirAfisare()
        self.sirAfisare()
        return ""

#STARE
class Stare:

    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, estimare=None):
        self.tabla_joc = tabla_joc
        self.j_curent = j_curent

        self.adancime = adancime

        self.estimare = estimare

        self.mutari_posibile = []

        self.stare_aleasa = None

    def mutari(self):
        l_mutari = self.tabla_joc.mutari(self.j_curent)  # lista de informatii din nodurile succesoare
        juc_opus = Joc.jucator_opus(self.j_curent)

        l_stari_mutari = [Stare(mutare, juc_opus, self.adancime - 1, parinte=self) for mutare in l_mutari]

        return l_stari_mutari

    def __str__(self):
        # sir= str(self.tabla_joc) + "(Juc curent:"+self.j_curent+")\n"
        str(self.tabla_joc)
        # self.tabla_joc.sirAfis()
        print("(Juc curent:" + self.j_curent + ")\n")
        return ""
        # return sir


def afis_daca_final(stare_curenta):
    final = stare_curenta.tabla_joc.final()
    if (final):
        if (final == "remiza"):
            print("Remiza!")
        else:
            print("A castigat " + final)

        return True

    return False

#Algoritmul ruleaza, dar nu este complet - nu implementeaza toate regulile jocului(ex:
#jucatorul nu are sa posibilitatea sa faca o mutare si un salt
#in aceeasi runda)
#si mai are niste scapari la verificarea conditiilor
def joaca():
    global ADANCIME_MAX;
    # initializare algoritm
    raspuns_valid = False
    while not raspuns_valid:
        nivel = input("Nivel joc? (raspundeti cu 1,2 sau 3)\n 1.Incepator\n 2.Mediu\n 3.Avansat\n ")
        if nivel in ['1', '2', '3']:
            raspuns_valid = True
        else:
            print("Nu ati ales o varianta corecta.")
    if (nivel == 1):
        ADANCIME_MAX = 2
    elif (nivel == 2):
        ADANCIME_MAX = 4
    raspuns_valid = False

    while not raspuns_valid:
        tip_algoritm = input("Algoritmul folosit? (raspundeti cu 1 sau 2)\n 1.Minimax\n 2.Alpha-beta\n ")
        if tip_algoritm in ['1', '2']:
            raspuns_valid = True
        else:
            print("Nu ati ales o varianta corecta.")
    # initializare jucatori
    raspuns_valid = False
    while not raspuns_valid:
        Joc.JMIN = input("Doriti sa jucati cu A sau cu N? ")
        if (Joc.JMIN in ['A', 'N']):
            raspuns_valid = True
        else:
            print("Raspunsul trebuie sa fie A sau N.")
    Joc.JMAX = 'A' if Joc.JMIN == 'N' else 'N'

    # initializare tabla
    tabla_curenta = Joc();  # apelam constructorul
    print("Tabla initiala")
    # print(str(tabla_curenta))
    str(tabla_curenta)
    # tabla_curenta.sirAfis()

    # creare stare initiala
    stare_curenta = Stare(tabla_curenta, 'A', ADANCIME_MAX)

    while True:
        if (stare_curenta.j_curent == Joc.JMIN):
            # muta jucatorul utilizator

            print("Acum muta utilizatorul cu simbolul", stare_curenta.j_curent)
            raspuns_valid = False
            raspuns_valid1 = False
            raspuns_valid2 = False
            print("Intrerupeti jocul? 0 - Nu / 1 - Da")
            nr = int(input())
            if (nr == 1): exit()
            while not raspuns_valid:
                try:
                    print("Selectati piesa pe care doriti sa o mutati")
                    linie = int(input("linie="))
                    coloana = int(input("coloana="))

                    if (linie in range(Joc.NR_COLOANE) and coloana in range(Joc.NR_COLOANE)):
                        if stare_curenta.tabla_joc.matr[linie][coloana] == Joc.JMIN:
                            raspuns_valid1 = True
                        else:
                            print("Trebuie sa selectati o piesa proprie")
                    else:
                        print("Linie sau coloana invalida (trebuie sa fie unul dintre numerele 0,1,2,3,4).")

                except ValueError:
                    print("Linia si coloana trebuie sa fie numere intregi")

                if (raspuns_valid1 == False): continue

                try:
                    print("Selectati unde doriti sa mutati piesa")
                    linie_f = int(input("linie="))
                    coloana_f = int(input("coloana="))

                    if (linie in range(Joc.NR_COLOANE) and coloana in range(Joc.NR_COLOANE)):
                        # print()
                        if stare_curenta.tabla_joc.matr[linie_f][coloana_f] != Joc.GOL:
                            print("Spatiul selectat trebuie sa fie liber")
                            continue
                        # validare mutare
                        rez = stare_curenta.tabla_joc.validare(linie, coloana, linie_f, coloana_f, Joc.JMIN)
                        if rez[0] == False:
                            print("Mutare invalida")
                            continue
                        else:
                            raspuns_valid2 = True
                    else:
                        print("Linie sau coloana invalida (trebuie sa fie unul dintre numerele 0,1,2,3,4).")

                except ValueError:
                    print("Linia si coloana trebuie sa fie numere intregi")
                if raspuns_valid1 and raspuns_valid2: raspuns_valid = True

            # dupa iesirea din while sigur am valide atat linia cat si coloana
            # deci pot modifica "tabla de joc"

            #piesa selectata se muta in noul loc
            stare_curenta.tabla_joc.matr[linie_f][coloana_f] = Joc.JMIN
            #locul vechi devine gol
            stare_curenta.tabla_joc.matr[linie][coloana] = Joc.GOL

            if rez[1] == True:  # salt => piesa peste care se sare (a adversarului) va fi eliminata
                stare_curenta.tabla_joc.matr[rez[2]][rez[3]] = Joc.GOL

            # afisarea starii jocului in urma mutarii utilizatorului
            print("\nTabla dupa mutarea jucatorului")
            print(str(stare_curenta))
            # TO DO 8a
            # testez daca jocul a ajuns intr-o stare finala
            # si afisez un mesaj corespunzator in caz ca da
            if (afis_daca_final(stare_curenta)):
                break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)

        # --------------------------------
        else:  # jucatorul e JMAX (calculatorul)
            # Mutare calculator

            print("Acum muta calculatorul cu simbolul", stare_curenta.j_curent)
            # preiau timpul in milisecunde de dinainte de mutare
            t_inainte = int(round(time.time() * 1000))

            # stare actualizata e starea mea curenta in care am setat stare_aleasa (mutarea urmatoare)
            if tip_algoritm == '1':
                stare_actualizata = min_max(stare_curenta)
            else:  # tip_algoritm==2
                stare_actualizata = alpha_beta(-500, 500, stare_curenta)
            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc  # aici se face de fapt mutarea !!!
            print("Tabla dupa mutarea calculatorului")
            print(str(stare_curenta))

            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")
            # TO DO 8b
            if (afis_daca_final(stare_curenta)):
                break

            # S-a realizat o mutare.  jucatorul cu cel opus
            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)

joaca()


