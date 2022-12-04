def comparePred(Fpredites, Fattendues):
    score = 0
    for i in range(len(Fpredites)):
        fp1,fa1 = Fpredites[i], Fattendues[i]
        list_seq_same_fpredict = []
        for j in range(i+1, len(Fpredites)): #liste des séquences ayant la même étiquette que la ième séquence
            fp2 = Fpredites[j]
            if fp2 == fp1 :
                list_seq_same_fpredict.append(j)
        for j in list_seq_same_fpredict:
            print(i,j)
            fp2,fa2 = Fpredites[j], Fattendues[j]
            if fp1 == fp2 and fa1 == fa2:
                score += 1
                print("Match", score)
                # les séquences i et j sont dans la même famille dans les prédictions et les attendus

            elif fp1 == fp2 and fa1 != fa2:
                score -= 1
                print("Missmatch", score)
                # les séquences i et j sont dans la même famille dans les prédictions mais pas dans les attendus

        list_seq_same_fpredict2 = []
        for j in range(1, len(Fpredites)):
            if j!=i:
                fp2 = Fpredites[j]
                if fp2 == fp1 :
                    list_seq_same_fpredict2.append(j)
        if len(list_seq_same_fpredict2) == 0: # Si séquence seule dans une famille, on veut vérifier qu'elle est aussi solo dans la vérif
            test = True
            for j in range(len(Fattendues)):
                fa2 = Fattendues[j]
                if fa1 == fa2 & i != j:
                    # Plusieurs éléments dans la famille attendues => score -1
                    test = False
            if test : score += 1
            else : score -= 1
            print("solo : ",i,", score : ", score)


    return score

def confusion(Fpredites, Fattendues):
    TruePositive,TrueNegative,FalsePositive,FalseNegative = 0,0,0,0
    for i in range(len(Fpredites)):
        fp1, fa1 = Fpredites[i], Fattendues[i]
        for j in range(i+1,len(Fpredites)):
            fp2, fa2 = Fpredites[j], Fattendues[j]
            # True positive
            if fp1 == fp2 and fa1==fa2 :
                TruePositive +=1
            # False positive
            elif fp1 == fp2 and fa1!=fa2 :
                FalsePositive += 1
            # True positive
            elif fp1 != fp2 and fa1!=fa2 :
                TrueNegative += 1
            # False negative
            else : FalseNegative += 1
    return TruePositive,TrueNegative,FalsePositive,FalseNegative


def test():
    Fpredites = [1, 1, 1, 4, 3, 3, 0, 2, 4, 4]
    Fattendues= [0, 0, 0, 1, 2, 2, 3, 4, 4, 4]
    print(confusion(Fpredites, Fattendues))
    #print(comparePred(Fpredites, Fattendues))
if __name__=="__main__":
    test()