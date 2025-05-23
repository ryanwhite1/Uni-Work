import math
import random
import pylab

# Time[i][j] gives the time to press key j after pressing key i
Time = [[53,66,66,66,66,53,53,53,53,53,73,53,53,53,66,53,53,53,53,85,73,73,73,73,53,53],
[66,53,66,66,66,53,53,53,53,53,53,73,53,53,66,53,53,53,53,73,85,73,73,73,53,53],
[66,66,53,66,66,53,53,53,53,53,53,53,73,53,66,53,53,53,53,73,73,85,73,73,53,53],
[66,66,66,53,66,53,53,53,53,53,53,53,53,73,73,53,53,53,53,73,73,73,85,85,53,53],
[66,66,66,66,53,53,53,53,53,53,53,53,53,53,73,53,53,53,53,73,73,73,85,85,53,53],
[53,53,53,53,53,53,66,66,66,66,53,53,53,53,53,73,73,53,53,53,53,53,53,53,85,85],
[53,53,53,53,53,66,53,66,66,66,53,53,53,53,53,73,73,53,53,53,53,53,53,53,85,85],
[53,53,53,53,53,66,66,53,66,66,53,53,53,53,53,66,53,73,53,53,53,53,53,53,73,73],
[53,53,53,53,53,66,66,66,53,66,53,53,53,53,53,66,53,53,73,53,53,53,53,53,73,73],
[53,53,53,53,53,66,66,66,66,53,53,53,53,53,53,66,53,53,53,53,53,53,53,53,73,73],
[66,66,66,66,66,53,53,53,53,53,53,53,53,53,66,53,53,53,53,73,73,73,73,73,53,53],
[66,66,66,66,66,53,53,53,53,53,53,53,53,53,66,53,53,53,53,73,73,73,73,73,53,53],
[66,66,66,66,66,53,53,53,53,53,53,53,53,53,66,53,53,53,53,73,73,73,73,73,53,53],
[66,66,66,66,66,53,53,53,53,53,53,53,53,53,66,53,53,53,53,73,73,73,73,73,53,53],
[66,66,66,66,66,53,53,53,53,53,53,53,53,66,53,53,53,53,53,73,73,73,73,73,53,53],
[53,53,53,53,53,66,66,66,66,66,53,53,53,53,53,53,66,53,53,53,53,53,53,53,73,73],
[53,53,53,53,53,66,66,66,66,66,53,53,53,53,53,66,53,53,53,53,53,53,53,53,73,73],
[53,53,53,53,53,66,66,66,66,66,53,53,53,53,53,66,53,53,53,53,53,53,53,53,73,73],
[53,53,53,53,53,66,66,66,66,66,53,53,53,53,53,66,53,53,53,53,53,53,53,53,73,73],
[85,66,66,66,66,53,53,53,53,53,66,53,53,53,66,53,53,53,53,53,73,73,73,73,53,53],
[66,85,66,66,66,53,53,53,53,53,53,66,53,53,66,53,53,53,53,73,53,73,73,73,53,53],
[66,66,85,66,66,53,53,53,53,53,53,53,66,53,66,53,53,53,53,73,73,53,73,73,53,53],
[66,66,66,85,85,53,53,53,53,53,53,53,53,66,66,53,53,53,53,73,73,73,53,66,53,53],
[66,66,66,85,85,53,53,53,53,53,53,53,53,66,66,53,53,53,53,73,73,73,66,53,53,53],
[53,53,53,53,53,85,85,66,66,66,53,53,53,53,53,66,66,53,53,53,53,53,53,53,53,66],
[53,53,53,53,53,85,85,66,66,66,53,53,53,53,53,66,66,53,53,53,53,53,53,53,66,53]]

# Freq[a][b] gives the frequency that the pair of letters ab occurs in 100,000 pairs from a sample of English
Freq = [[4,224,348,391,18,92,240,18,453,9,138,1035,314,1767,10,191,0,1058,897,1362,143,241,80,11,299,10],
[161,20,11,0,599,0,0,0,87,10,0,226,2,0,248,0,0,161,41,9,237,9,0,0,194,0],
[426,4,79,4,643,3,0,565,261,2,127,164,1,0,901,0,1,156,12,375,106,0,0,1,45,0],
[222,2,7,61,758,4,23,2,380,3,0,42,22,10,195,1,0,88,74,4,137,24,11,0,38,0],
[717,32,542,1148,410,194,119,26,166,11,28,506,373,1388,62,180,34,2123,1306,367,36,253,140,194,147,3],
[154,0,0,0,203,185,0,1,331,3,0,63,1,0,530,0,0,224,7,98,91,0,0,0,3,0],
[182,5,0,8,393,2,46,230,140,0,1,62,2,69,175,1,0,194,27,10,75,0,2,0,11,0],
[1040,2,2,11,3026,1,1,6,653,0,0,13,12,24,502,1,0,81,17,134,59,1,4,0,24,0],
[263,85,678,348,341,133,233,8,7,1,48,532,266,2407,728,88,7,299,1208,1109,13,256,1,22,5,40],
[31,0,0,0,41,0,0,0,3,0,0,1,0,0,59,0,0,0,0,0,53,0,0,0,1,0],
[13,3,1,3,247,2,2,1,118,0,1,24,1,24,3,1,0,3,42,1,5,0,1,0,4,0],
[587,6,15,325,876,46,26,2,615,2,16,657,21,6,321,18,0,13,143,108,109,30,15,1,470,2],
[561,102,2,4,779,0,2,0,371,0,3,11,115,15,344,269,0,125,98,0,108,1,0,0,42,0],
[330,10,395,1156,656,71,993,21,353,7,42,70,62,90,473,5,10,6,467,1056,84,46,10,6,104,1],
[102,83,106,153,25,1058,57,24,98,6,67,365,566,1818,196,220,1,1253,243,411,931,238,304,11,75,4],
[330,4,0,0,537,3,0,31,126,0,0,259,13,0,361,150,0,512,50,74,98,0,0,0,7,0],
[0,0,3,0,1,0,0,0,1,0,0,0,0,0,2,0,0,0,0,0,107,0,1,0,1,0],
[679,19,82,242,1835,29,93,22,796,1,90,103,231,183,741,46,0,129,450,383,105,64,23,0,258,0],
[282,7,115,9,828,13,1,366,527,0,32,72,66,21,374,198,4,23,408,1134,278,2,27,0,33,0],
[507,11,58,2,1233,11,2,3556,1074,1,0,114,47,17,1186,6,3,488,321,192,186,1,83,0,192,9],
[109,90,169,53,154,15,133,1,83,4,2,352,106,455,14,141,0,502,359,469,3,2,2,8,11,5],
[95,0,0,0,842,0,0,2,286,0,0,0,0,0,63,0,0,3,1,0,1,0,0,0,13,0],
[436,7,2,7,343,1,0,370,452,0,1,28,7,75,259,0,2,26,36,3,0,1,1,1,7,0],
[20,0,20,0,25,0,0,3,31,0,0,0,1,0,2,67,0,0,0,49,3,0,0,0,1,0],
[11,4,27,15,189,2,0,7,48,0,2,10,47,17,62,11,0,4,73,11,1,0,5,0,0,0],
[17,1,0,0,39,0,0,1,9,0,0,2,0,1,5,0,0,1,1,0,5,0,0,0,2,4]]

A = range(26)

# Show the keyboard layout corresponding to permutation p
def ShowKeyboard(p):
	print (' '.join(chr(65+x) for x in p[0:10]))
	print ("",' '.join(chr(65+x) for x in p[10:19]))
	print (" ",' '.join(chr(65+x) for x in p[19:26]))
	print (TotalTime(p),'\n')
	
# Calculate the total time required by permutation p
def TotalTime(p):
	return sum([Time[i][j]*Freq[p[i]][p[j]] for i in A for j in A])

def ChooseTwo(p):
    i, j = random.sample(A, 2)
    c1 = TotalTime(p)
    p[i], p[j] = p[j], p[i]
    c2 = TotalTime(p)
    p[i], p[j] = p[j], p[i]
    return c2 - c1, (i, j)

def MoveTwo(p, neighbour):
    i, j = neighbour
    p[i], p[j] = p[j], p[i]
    return 


def RunSA(Solution,Cost,ChooseNeigh,MoveToNeigh,T,N,alpha):
    E = Cost(Solution)
    Best = E
    CostArr = [E]
    BestArr = [Best]
    BestSol = list(Solution)
    for i in range(N):
        delta,neighbour = ChooseNeigh(Solution)
        if delta < 0 or math.exp(-delta/T) > random.random():
            MoveToNeigh(Solution,neighbour)
            E += delta
            if E < Best:
                Best = E
                BestSol = list(Solution)
        CostArr.append(E)
        BestArr.append(Best)
        T *= alpha
    print (Best, T)
    pylab.plot(range(N+1),CostArr)
    pylab.plot(range(N+1),BestArr)
    pylab.show()
    return BestSol


# Sample calculation
# Qwerty keyboard
qwerty = ['Q','W','E','R','T','Y','U','I','O','P','A','S','D','F','G','H','J','K','L','Z','X','C','V','B','N','M']
startp = [ord(l)-65 for l in qwerty]
ShowKeyboard(startp)

RunSA(startp, TotalTime, ChooseTwo, MoveTwo, 100000, 10000, 0.999)
ShowKeyboard(startp)


