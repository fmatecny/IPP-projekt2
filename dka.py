

#DKA:xmatec00
import argparse
import sys
import re

try:
#parsovanie argumentov
	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('--input=', dest='inFile', nargs=1,
					   help='vstupny subor')
	parser.add_argument('--output=', dest='outFile', nargs=1,
					   help='vystupny subor')
	parser.add_argument('-e', '--no-epsilon-rules', dest='eps', action='store_true',
						help='odstranenie epsilon pravidiel')
	parser.add_argument('-d', '--determinization', dest='det', action='store_true',
						help='odstranenie nederminizmu')
	parser.add_argument('-i', '--case-insensitive', dest='ins', action='store_true',
						help='case insensitive')
except:
	sys.stderr.write("Zle argumenty\n")
	sys.exit(1)
args = parser.parse_args()
#print(args)

argument = 0

#otvorenie suborov
if args.inFile!=None:
	try:
		input_file = open(args.inFile.pop(), encoding='utf-8', mode='r')
		argument+=1
	except: 
		sys.stderr.write("Zadany vstupny soubor neexistuje alebo nejde otvorit\n")
		sys.exit(1)
else:
	input_file = sys.stdin

if args.outFile!=None:
	try:
		output_file = open(args.outFile.pop(), encoding='utf-8', mode='w')
		argument+=1
	except: 
		sys.stderr.write("Zadany vystupny subor nejde vytvorit\n")
		sys.exit(1)
else:
	output_file = sys.stdout

#kontrola argumentov
if args.eps == True:
	argument+=1
if args.det == True:
	argument+=1
if args.ins == True:
	argument+=1

if len(sys.argv)-1 != argument:
	sys.stderr.write("Vela argumentov\n")
	sys.exit(1)

if args.eps == True and args.det == True:
	sys.stderr.write("-e a -d nemozu byt zadane sucasne\n")
	sys.exit(1)	

#nacitanie vstupneho suboru
input_text=input_file.read()
#odstranenie komentarov			#|#[^'].*[^\n]$
input_text = re.sub(r"#[^'].*\n|#[^'].*[^\n]$", "", input_text)
#odstranenie medzier
input_text = re.sub(r" *\t*\n*\r*", "", input_text)
#print(input_text)
#kontorla stavov
try:											#\s*$
	stavy = (re.search(r"\(\{(.*)\}.*\}.*\}.*\}\)\s*$", input_text)).group(1)
except:
	sys.stderr.write("1chybny format vstupneho suboru\n")

	sys.exit(40)

stavy = re.split(',', stavy)
for i in range(0,len(stavy)):
	if re.search(r"^_.*|.*_$|^[1-9].*", stavy[i]) != None:
		sys.stderr.write("2chybny format stavov vstupneho suboru\n")
		sys.exit(40)

#kontrola abecedy
try:							#,
	abeceda = (re.search(r"\(\{.*,\{(.*)\}.*\}.*\}\)", input_text)).group(1)
except:
	sys.stderr.write("3chybny format vstupneho suboru\n")
	sys.exit(40)

if abeceda == "":
	sys.stderr.write("abeceda je prazdna\n")
	sys.exit(41)
	
abeceda = re.split(',', abeceda)
for i in range(0,len(abeceda)):
	if re.search(r"^'[\w\s(){},.-># ]*'$|^''''$", abeceda[i]) == None:
		sys.stderr.write("chybny format abecedy vstupneho suboru\n")
		sys.exit(40)

#kontrola pravidiel
try:
	pravidlo = re.split(",",(re.search(r"\(\{.*\{.*,\{(.*)\}.*\}\)", input_text)).group(1))
except:
	sys.stderr.write("chybny format vstupneho suboru\n")
	sys.exit(40)
if pravidlo != ['']:
	for i in range(0,len(pravidlo)):
		#kontrola stavu z ktoreho sa vychadza
		correct = False
		for j in range(0,len(stavy)):
			if stavy[j] == re.sub(r"'.*'.*","", pravidlo[i]):
				correct = True
				break
		if correct == False:
			sys.stderr.write("chybny format pravidiel vstupneho suboru\n")
			sys.exit(41)
		#kontrola abecedy
		correct = False
		for j in range(0,len(abeceda)):										 #or (re.search(r".*('.*').*", pravidlo[i])).group(1) == "''"
			if abeceda[j] == (re.search(r".*('.*').*", pravidlo[i])).group(1) or (re.search(r".*('.*').*", pravidlo[i])).group(1) == "''":
				correct = True
				break
		if correct == False:
			sys.stderr.write("chybny format pravidiel vstupneho suboru\n")
			sys.exit(41)
		#kontrola cieloveho stavu
		correct = False
		for j in range(0,len(stavy)):
			if stavy[j] == re.sub(r".*->","", pravidlo[i]):
				correct = True
				break
		if correct == False:
			sys.stderr.write("chybny format pravidiel vstupneho suboru\n")
			sys.exit(41)	

#kontrola pociatocneho stavu
try:
	start_point = (re.search(r"\(\{.*\{.*\{.*\},(.*),.*{.*\}\)", input_text)).group(1)
except:
	sys.stderr.write("chybny format vstupneho suboru\n")
	sys.exit(40)

if re.search(r"(.*,.*)", start_point) != None:
	sys.stderr.write("chybny format pocitocneho stavu vstupneho suboru\n")
	sys.exit(40)
		
correct = False
for j in range(0,len(stavy)):
	if start_point == stavy[j]:
		correct = True
		break
if correct == False:
	sys.stderr.write("pociatocny stav nie je podmnozinou stavov\n")
	sys.exit(41)

#kontrola koncoveho stavu
try:
	end_points = (re.search(r"\(\{.*\{.*\{.*\{(.*)\}\)", input_text)).group(1)
except:
	sys.stderr.write("chybny format vstupneho suboru\n")
	sys.exit(40)

if end_points != "":
	end_points = re.split(',', end_points)
	for i in range(0,len(end_points)):
		correct = False
		for j in range(0,len(stavy)):
			if end_points[i] == stavy[j]:
				correct = True
				break
		if correct == False:
			sys.stderr.write("koncovy stav nie je podmnozinou stavov\n")
			sys.exit(41)

end_points = ','.join(end_points)

new_rules = [""] * len(pravidlo) *2
najdene_stavy = [""] * len(pravidlo)*2
new_end = [""]
index = 0

if pravidlo != ['']:
	len_pravidlo = len(pravidlo)
	#odstranenie epsilon pravidiel
	if args.det == True or args.eps == True:
		for i in range(0, len_pravidlo):	#[^']
			if re.search(r".*[^']('.*').*", pravidlo[i]).group(1) == "''":	#epsilon
				stav = re.sub(r"'.*'.*", "", pravidlo[i])
				hladam = re.sub(r".*->", "", pravidlo[i])
				for j in range(0, len_pravidlo):
					if hladam == re.sub(r"'.*'.*", "", pravidlo[j]):
						pravidlo.append(stav + re.search(r".*('.*'.*)$",pravidlo[j]).group(1))
						pravidlo[i] = ""									#pravidlo[i] = ""
						

#determinizacia--------------------------------------
if args.det == True:
	#------startpoint-------------
	for i in range(len(pravidlo)):
		first_part1 = re.sub(r"->.*", "", pravidlo[i])
		scnd_part1 = re.sub(r".*->", "", pravidlo[i])
		stav = re.sub(r"'.+'.*", "", first_part1)
		if stav == start_point:
			if scnd_part1 == start_point:
				new_rules[index] = pravidlo[i]
				pravidlo[i] = ""
				index +=1
			else:
				pom = True
				if i+1 == len(pravidlo):							#
					new_rules[index] = pravidlo[i]					#
					pravidlo[i] = ""								#
				for j in range(i+1, len(pravidlo)):
					if pravidlo[j] != "":
						first_part2 = re.sub(r"->.*", "", pravidlo[j])
						scnd_part2 = re.sub(r".*->", "", pravidlo[j])
						#print (new_rules)
						#print (pravidlo[i])
						#print (pravidlo)
						#print ("-------------------------------")
						if first_part1 == first_part2:
							if pom == True:
								new_rules[index] = pravidlo[i] + "_" + scnd_part2
								pom = False
							else:
								new_rules[index] = new_rules[index] + "_" + scnd_part2
							#pravidlo[i] = pravidlo[i] + "_" + scnd_part2
							pravidlo[j] = ""
				index+=1
				pravidlo[i] = ""
	#print(new_rules) 						
	i=0
	najdene_stavy[0] = start_point
	a=1
	pom = True
	# -----ostatne stavy-------------
	while new_rules[i]!='':
		first_part_newrules = re.sub(r"->.*", "", new_rules[i])
		scnd_part_newrules = re.sub(r".*->", "", new_rules[i])
		stav_newrules = re.sub(r"'.+'.*", "", first_part_newrules)
		i+=1
		#print(scnd_part_newrules + "  abc")
		if scnd_part_newrules != start_point:
			hladam_stav = scnd_part_newrules
			b=0
			flag = True
			while najdene_stavy[b] != '':
				if najdene_stavy[b] == hladam_stav:
					flag = False
				b+=1
			if flag == True:
				najdene_stavy[a] = hladam_stav
				a+=1
				#print (hladam_stav)
				hladam = re.split("_",hladam_stav)
				#print(hladam)
				for w in range(0,len(abeceda)):
					for x in range(0,len(hladam)):
						#print(abeceda)
						#print(hladam[x])
						#print(hladam)
						#print(x)
						for y in range(0,len(pravidlo)):
							first_part_pravidlo = re.sub(r"->.*", "", pravidlo[y])
							scnd_part_pravidlo = re.sub(r".*->", "", pravidlo[y])
							stav_pravidlo = re.sub(r"'.+'.*", "", first_part_pravidlo)
							if hladam[x] + abeceda[w] == first_part_pravidlo:
								#print(pravidlo[y])
								if pom == True:												#[^']
									new_rules[index] = scnd_part_newrules + re.search(r".*[^']('.*').*", first_part_pravidlo).group(1) + "->" + scnd_part_pravidlo
									#print(new_rules)
									pom = False
								else:
									foo = re.split('_', re.sub(r".*->", "", new_rules[index]))
									wrt = True
									for r in range(0,len(foo)):
										if foo[r] == scnd_part_pravidlo:
											wrt = False
									if wrt == True:
										new_rules[index] = new_rules[index] + "_" + scnd_part_pravidlo
										#print(new_rules)
										#print("fdsa")
					if (new_rules[index] != ""):					#if (new_rules[index] != ""):
						index+=1
					pom = True	
					
					
					
#print (pravidlo)
#print (new_rules)

if args.det == False:
	najdene_stavy = stavy#re.split(",", stavy)
	new_rules = pravidlo
	new_end = [""] + re.split(",", end_points)


#------------------sorting ----------------------
i = 0
for i in range (len(new_rules)):
	if new_rules[i] != '':
		frst_sort = sorted(re.split('_', re.sub(r"'.*'->.*", "", new_rules[i])))
		scnd_sort = sorted(re.split('_', re.sub(r".*->", "", new_rules[i])))
																					#[^']
		new_rules[i] = '_'.join(frst_sort) + " " + re.sub(r"'-","' -",re.search(r".*[^']('.*'->).*", new_rules[i]).group(1)) + " " + '_'.join(scnd_sort)
	
new_rules.sort()
#print(end_points)
#---------------------
end_points = re.split(",", end_points)
for i in range (0, len(new_rules)):
	scnd_part_newrules = re.sub(r".*-> ", "", new_rules[i])
	scnd_sort = re.split('_', scnd_part_newrules)
	for x in range(0,len(scnd_sort)):
		for z in range(0,len(end_points)):				#for z in range(0,len(end_points)):
			if scnd_sort[x] == end_points[z]:
				push_points = True
				for y in range(0,len(new_end)):
					if new_end[y] == scnd_part_newrules:
						push_points = False
				if push_points == True:
					new_end.append(scnd_part_newrules)



#--najdene stavy sorting----
for i in range (0,len(najdene_stavy)):
	if najdene_stavy[i] != '':
		frst_sort = sorted(re.split('_', najdene_stavy[i]))
		najdene_stavy[i] = '_'.join(frst_sort)
		#print (new_rules[i])
	
najdene_stavy.sort()

#--------zapis automatu----------
output_file.write("(\n")
output_file.write("{")

#stavy
#odstranenie duplicity
for i in range (0,len(najdene_stavy)):
	for j in range (i+1,len(najdene_stavy)):
		if najdene_stavy[i] == najdene_stavy[j]:
			najdene_stavy[j] = ""
najdene_stavy.sort()
for i in range(0,len(najdene_stavy)):
	if najdene_stavy[i] != '':
		output_file.write(najdene_stavy[i])
		if i+1!=len(najdene_stavy):
			output_file.write(", ")

output_file.write("},\n")
output_file.write("{")

#abeceda

abeceda = sorted(abeceda)
for i in range (0,len(abeceda)):
	for j in range (i+1,len(abeceda)):
		if abeceda[i] == abeceda[j]:
			abeceda[j] = ""

for i in range(0,len(abeceda)):
	if abeceda[i] == "''":
		abeceda[i] = "' '"

abeceda = sorted(abeceda)
for i in range(0,len(abeceda)):
	if abeceda[i] != "":									#if abeceda[i] != "":
		output_file.write(abeceda[i])
		if i+1!=len(abeceda):
			output_file.write(", ")
		
output_file.write("},\n")
output_file.write("{\n")

#pravidla
if new_rules != ['']:
	#odstranenie duplicity
	for i in range (0,len(new_rules)):
		for j in range (i+1,len(new_rules)):
			if new_rules[i] == new_rules[j]:
				new_rules[j] = ""
	for i in range (0,len(new_rules)):
		if re.search(r".*('.*').*", new_rules[i]) != None:
			if re.search(r".*[^']('.*').*", new_rules[i]).group(1) == "''":	#[^']
				new_rules[i] = re.sub(r"''", "' '", new_rules[i])

	new_rules.sort()
	#vypis
	for i in range (0,len(new_rules)):
		if new_rules[i] != '':
			output_file.write(new_rules[i])
			if i+1!=len(new_rules):
				output_file.write(",")
			output_file.write("\n")
	
output_file.write("},\n")
#pocitaocny stav
output_file.write(start_point + ",\n")

output_file.write("{")

#koncove stavy
#print(new_end)
new_end = sorted(new_end)
for i in range (1,len(new_end)):
	output_file.write(new_end[i])
	if i+1!=len(new_end):
		output_file.write(", ")

output_file.write("}\n")

output_file.write(")")


if input_file != sys.stdin:
	input_file.close();

if output_file != sys.stdout:
	output_file.close();
