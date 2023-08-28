
from random import randint
import matplotlib.pyplot as plt
import colorama
from random import seed


seed(125)

class cislo:
    vyherniCislo : int
    multiplier : float
    def __init__(self,vyherniCislo,multiplier) -> None:
        self.vyherniCislo = vyherniCislo
        self.multiplier = multiplier

class cisloGrafu:
    i : int
    vydelanePenize : int
    pocetHitu : int
    sazky : int
    def __init__(self,i,vydelanePenize,pocetHitu,sazky) -> None:
            self.i = i
            self.vydelanePenize = vydelanePenize
            self.pocetHitu = pocetHitu
            self.sazky = sazky


cervena = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
cerna = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
zelena = [0]

def pridejMultiplierKCislum(staryList : list, multiplier : float):
    newList = list()

    for vyherniCislo in staryList:
        newList.append(cislo(vyherniCislo, multiplier))

    return newList


nasobnaZelena = pridejMultiplierKCislum(zelena,35)
nasobnaCervena = pridejMultiplierKCislum(cervena,2)
nasobnaCerna = pridejMultiplierKCislum(cerna,2)


#Poupravit => má mi dávat jenom jestli se trefí nebo ne
def monte_Carlo(pocet_iteraci, vyherniCisla :list):
    postupList = list()  
    shots = dict()
    shotsMissed = dict()
    for i in range(pocet_iteraci):
        shot = randint(0,36)

        if shot in map(lambda x: x.vyherniCislo, vyherniCisla ):
            postupList.append((True, next((vyherniCislo for vyherniCislo in vyherniCisla if vyherniCislo.vyherniCislo == shot),2).multiplier))
            if shot in shots:
                shots[shot] += 1
            else:
                shots.update({shot:1})
        else:
            postupList.append((False, None))
            if shot in shotsMissed:
                shotsMissed[shot] += 1
            else:
                shotsMissed.update({shot:1})
    print(colorama.Fore.GREEN + str(shots))
    print(colorama.Fore.RED + str(shotsMissed))
    return postupList

'''
#Poupravit => má mi dávat jenom jestli se trefí nebo ne
def monte_Carlo(pocet_iteraci, vyherniCisla :list):
    postupList = list()
    
    vydelanePenize = 0
    pocetHitu = 0
    
    for i in range(pocet_iteraci):
        shot = randint(0,36)
        if shot in map(lambda x: x.vyherniCislo, vyherniCisla ):
            pocetHitu +=1
            yaa = filter( lambda x: x.vyherniCislo == shot,vyherniCisla)
            multiplier = 1
            for x in yaa:
                multiplier = x.multiplier                
                break
            vydelanePenize += (-1 ) + 1 *  multiplier
        else:
            vydelanePenize -= 1
        postupList.append(cisloGrafu(i,vydelanePenize,pocetHitu,1))

    return postupList
'''


seznam = list()
seznam.append(cislo(0,14))

def vyhodnotStrategii(vyherni_cisla):
    sazba = 50
    postupList = monte_Carlo(10000, vyherni_cisla)
    graf = list()
    vydelanePenize = 0
    i = 0
    pocetHitu = 0

    for (trefil,multiplier) in postupList:
        if trefil: 
            vydelanePenize += multiplier * sazba
            pocetHitu+=1
            
        vydelanePenize -= sazba 

        graf.append(cisloGrafu(i,vydelanePenize,pocetHitu,sazba))
        i += 1

    fig, ax = plt.subplots()


    textVyhernichCisel = "Výherní čísla: "+",".join(str(vyherni_cislo.vyherniCislo)for vyherni_cislo in vyherni_cisla)

    ax.plot( list(map(lambda x: x.i,graf)), list(map(lambda x: x.vydelanePenize,graf)), linewidth=2.0,color="Green")
    ax.set_title(f"{textVyhernichCisel}\nVydělané peníze při strategii sázení na čísla se sazbou 50$: " + str(graf[len(graf)-1].vydelanePenize))
    ax.set_xlabel("Počet pokusů")
    ax.set_ylabel("Profit")
    ax.yaxis.set_major_formatter(lambda x, y: "{:n}".format(x)+"$")
    print("Výherní šance je: " +str(pocetHitu / i * 100) + "%")
    plt.show()


vyhodnotStrategii(nasobnaZelena)
vyhodnotStrategii(nasobnaCervena)
vyhodnotStrategii(nasobnaCerna)