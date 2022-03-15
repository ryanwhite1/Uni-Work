def is_dna(string):
    valid = False
    while len(string)%3 == 0:
        for var in string:
            if var == 'A':
                valid = True
            elif var == 'C':
                valid = True
            elif var == 'G':
                valid = True
            elif var == 'T':
                valid = True
            else:
                valid = False
                break
        break
    return valid

def reverse_complement(dna):
    valid = is_dna(dna)
    
    if valid == False:
        return 'None'

    res = ''
    while valid == True:
        for var in dna:
            if var == 'A':
                res += 'T'
            elif var == 'T':
                res += 'A'
            elif var == 'G':
                res += 'C'
            elif var == 'C':
                res += 'G'
        break
    return res[::-1]

def print_codons(dna):
    valid = is_dna(dna)
    if valid == False:
        return
    x = 0
    y = 3
    while y <= len(dna):
        print(dna[x:y])
        x += 3
        y += 3
        
    
