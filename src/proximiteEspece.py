


def freq(Fpredite1,Fpredite2,NbFamilleTotal):
    N = NbFamilleTotal
    freq1, freq2 = [0 for k in range(NbFamilleTotal)], [0 for k in range(NbFamilleTotal)]
    #print(len(freq2),len(Fpredite2))
    for k in range(len(Fpredite1)):
        famille1 = Fpredite1[k]
        famille2 = Fpredite2[k]
        freq1[famille1] += 1
        freq2[famille2] += 1
    return freq1,freq2

def proximite_local_pondere(Fpredite1,Fpredite2,NbFamilleTotal):
    freq1, freq2 = freq(Fpredite1,Fpredite2,NbFamilleTotal)
    #print("freq1 : ", freq1)
    #print("freq2 : ", freq2)
    prox_local_pondere = [0 for k in range(len(freq1))]
    for k in range(len(freq1)):
        totalApparition = freq1[k] + freq2[k]
        if totalApparition == 0 :
            prox_local_pondere[k]=0
        else :
            proportionF1 = freq1[k]/totalApparition
            proportionF2 = freq2[k] / totalApparition
            #print(k,proportionF1,proportionF2)
            prox_local = abs(proportionF1-proportionF2)
            prox_local_pondere[k] = prox_local * totalApparition
    return prox_local_pondere

def proximite_global(Fpredite1,Fpredite2,NbFamilleTotal):
    print(Fpredite2)
    NbSequence = len(Fpredite1) + len(Fpredite2)
    prox_local_pondere = proximite_local_pondere(Fpredite1,Fpredite2,NbFamilleTotal)
    moyenne_pondere = sum(prox_local_pondere) / NbSequence
    return 1-moyenne_pondere

def test():
    proximite_global([0,0,0,0,0,1],[1,1,1,1,1,0],2)

if __name__=="__main__":
    test()
