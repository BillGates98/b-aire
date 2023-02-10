import matplotlib.pyplot as plt
import csv

size = []
us = []
spacy = []
hunflair = []
bern2 = []

with open('data_fmeasure.csv','r') as csvfile:
	lines = csv.reader(csvfile, delimiter='\t')
	i = 0
	for row in lines:
		if i == 1 :
			size.append(int(row[1]))
			us.append(float(row[2]))
			spacy.append(float(row[3]))
			hunflair.append(float(row[4]))
			bern2.append(float(row[5]))
		i = 1

plt.plot(size, hunflair, color = 'r', marker = 'o',label = "Hunflair")
plt.plot(size, bern2, color = 'purple', marker = 'o',label = "Bern2")
plt.plot(size, spacy, color = 'b', marker = 'o',label = "SciSpacy")
plt.plot(size, us, color = 'g', marker = 'o',label = "B-aire")


# plt.xticks(rotation = 25)
plt.xlabel('Sample size')
plt.ylabel('Percent')
plt.title('F-measure', fontsize = 20)
# plt.grid()
plt.legend()
plt.savefig('./fmeasure_comparing.png')
# plt.show()
