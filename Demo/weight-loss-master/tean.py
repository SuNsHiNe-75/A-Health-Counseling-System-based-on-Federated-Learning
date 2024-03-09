import csv
ff=[]
with open('test.csv', 'r') as file1:
		reader= csv.reader(file1)
		for row in reader:
			ff.append(row)

print(ff[0][2])