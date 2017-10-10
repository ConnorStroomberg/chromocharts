import pprint
"""
This file parses the UCSC cytoband.txt file per chromosome and converts it to chromocharts format
Example input file called chr.txt:
chrY	0	2500000	p11.32	gneg
chrY	2500000	3000000	p11.31	gpos50
chrY	3000000	11600000	p11.2	gneg
chrY	11600000	12500000	p11.1	acen
chrY	12500000	13400000	q11.1	acen
chrY	13400000	15100000	q11.21	gneg
chrY	15100000	19800000	q11.221	gpos50
chrY	19800000	22100000	q11.222	gneg
chrY	22100000	26200000	q11.223	gpos50
chrY	26200000	28800000	q11.23	gneg
chrY	28800000	59373566	q12	gvar

output:
[[0, 2500000, 'p11.32'], [2500000, 3000000, 'p11.31'], [3000000, 11600000, 'p11.2'], [11600000, 12500000, 'p11.1'], [12500000, 13400000, 'q11.1'], [13400000, 15100000, 'q11.21'], [15100000, 19800000, 'q11.221'], [19800000, 22100000, 'q11.222'], [22100000, 26200000, 'q11.223'], [26200000, 28800000, 'q11.23'], [28800000, 59373566, 'q12']]
"""
class CytobandParser:
    def __init__(self, filename):
        self.parseChromosome(filename)
    def parseChromosome(self, filename):
        output = []
        for line in open(filename):
            line = line.split('\t')
            output.append([int(line[1]), int(line[2]), line[3].strip('\n')])
        print(output)

def main():
    cp = CytobandParser('chr.txt')

if __name__ == '__main__':
    main()
