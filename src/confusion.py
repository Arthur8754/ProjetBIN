import pandas as pd


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

def perf_confusion(TP,TN,FP,FN):
    N=TP+TN+FP+FN
    accuracy = (TP+TN)/N
    recall = TP/(TP+FN)
    precision = TP/(TP+TN)
    F1 = 2 * precision*recall/(precision+recall)
    return accuracy,recall,precision, F1

def confusion_print(TP, TN, FP, FN):
    array = [[TN, FN], [FP, TP]]
    df = pd.DataFrame(array, index=["Negative Prediction", "Positive Prediction"], columns=["Negative Reality", "Positive Reality"])
    print(df)