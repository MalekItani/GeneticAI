import random
def generateNumber(max):
    return (max-1)*random.random()

def generateDistinctPair(max):
    n1 = generateNumber(max)
    n2 = generateNumber(max)
    while n2 == n1:
        n2 = generateNumber(max)
    return int(n1), int(n2)

def generateChar():
    randomChar = int(random.random() * 90 + 32)
    return chr(randomChar)

def generateCharSequence(length):
    c = ""
    for i in range(length):
        c += generateChar()
    return c

class textGenome:
    def __init__(self, length, l = None, mutationRate = 0.01):
        self.length = length
        self.mutationRate = mutationRate
        if l is None:
            self.chromosome = generateCharSequence(length)
        else:
            self.chromosome = l
        self.mutate()
    def checkFitness(self, target):
        nTrue = 0
        for i in range(self.length):
            if target[i] == self.chromosome[i]:
                nTrue += 1
        return nTrue/self.length
    def mutate(self):
        for i in range(self.length):
            if generateNumber(100) <= self.mutationRate*100:
                temp = list(self.chromosome)
                temp[i] = generateChar()
                self.chromosome = ''.join(temp)

def cross(chrom1, chrom2, target):
    l = ""
    f1 = chrom1.checkFitness(target)
    f2 = chrom1.checkFitness(target)
    try:
        norm1 = f1/(f1+f2)*100
    except ZeroDivisionError:
        return textGenome(len(target))
    for i in range(chrom1.length):
        b = random.randint(0, 100)
        if b < norm1:
            l += chrom1.chromosome[i]
        else:
            l += chrom2.chromosome[i]
    return textGenome(chrom1.length, l);

