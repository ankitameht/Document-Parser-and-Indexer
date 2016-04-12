############################################

#Ankita Mehta 

############################################


'''
	BUILDING INDEXER
'''
import string
import unicodedata
import time
from nltk.corpus import stopwords
from stemming.porter2 import stem


C = ['amusementsinmath16713gut16713.txt','beetonsbookofnee15147gut15147.txt', 'alicesadventures19033gut19033.txt', 'littlebrother30142gutpg30142.txt', 'theadventuresofs01661gut1661.txt']

punct = set(string.punctuation)

list_sw = stopwords.words('english')
for i in range(len(list_sw)):
	list_sw[i] = unicodedata.normalize('NFKD', list_sw[i]).encode('ascii','ignore')

#Indexer features: no punct, No stopwords, utf-8 encoded, 
#		stores line_no, doc_name	
#		structure {term(Key): {Doc_name(k): line_no(val)}(Val) }
inverted_index = {}
#Preprocessing data
for d in C:
	start = time.time()
	f = open(d, 'r')	#Open file
	line = f.read()	#Create a list of lines
	line = line.split('\r\n')
	#parse each line
	for i in range(len(line)):
		iLine = line[i].lower()	#make lowercase
		#Remove punctuation
		tStr = ''
		for k in range(len(iLine)):
			if iLine[k] not in punct:
				tStr = tStr + iLine[k]
			else:
				tStr = tStr + ' '
		#Remove stopwords
		text = tStr.split()
		temp = []
		for p in range(len(text)):
			if text[p] not in list_sw:
				temp.append(text[p])
		#Apply Stemming
		for term in temp:
			term = stem(term)
			#term = term.decode('utf-8')
			if term in inverted_index.keys():
				l = inverted_index[term]
				if d not in l.keys():
					lin = []
					lin.append(i)
					l[d] = lin
				else:
					lin = l[d]
					lin.append(i)
					l[d] = lin
				inverted_index[term] = l
			else:
				l = {}
				lin = []
				lin.append(i)
				l[d] = lin
				inverted_index[term] = l
	f.close()
	for m in sorted(inverted_index.keys()):
		if (len(m)>2 and m[0] == '\/' and m[1] == 'x'):
			del inverted_index[m]
	end = time.time()
	print "Finished building index for doc :" + d + " Time : " + str(start - end)
'''
	BIGRAM INDEXER
'''

#Index features: no punct, No stopwords, utf-8 encoded,
#				bigrams-> term - > freq, lengthofterm
bigram_index = {}
for d in C:
	start = time.time()
	f = open(d, 'r')	#Open file
	line = f.read()	#Create a list of lines
	line = line.split('\r\n')
	#parse each line
	for i in range(len(line)):
		iLine = line[i].lower()	#make lowercase
		#Remove punctuation
		tStr = ''
		for k in range(len(iLine)):
			if iLine[k] not in punct:
				tStr = tStr + iLine[k]
			else:
				tStr = tStr + ' '
		#Remove stopwords
		text = tStr.split()
		temp = []
		for p in range(len(text)):
			if text[p] not in list_sw:
				temp.append(text[p])
		#Apply Stemming
		for term in temp:
			term = stem(term)
			if(term[0] != '\/'):
				for j in range(len(term)-1):
					l1 = {}
					bigram = term[j]+term[j+1]
					if bigram in bigram_index.keys():
						l1 = bigram_index[bigram]
						if term in l1.keys():
							l2 = l1[term]
							l2[0] = l2[0] + 1
							l1[term] = l2
					else:
						l2 = [1,len(term)]
						l1[term] = l2
					bigram_index[bigram] = l1
				#start & end bigram
				bigram = '$'+term[0]
				l1 = {}
				if bigram in bigram_index.keys():
					l1 = bigram_index[bigram]
					if term in l1.keys():
						l2 = l1[term]
						l2[0] = l2[0] + 1
				else:
					l2 = [1,len(term)]
				l1[term] = l2
				bigram_index[bigram] = l1

				bigram = term[len(term)-1]+'$'
				l1 = {}
				if bigram in bigram_index.keys():
					l1 = bigram_index[bigram]
					if term in l1.keys():
						l2 = l1[term]
						l2[0] = l2[0] + 1
				else:
					l2 = [1,len(term)]
				l1[term] = l2
				bigram_index[bigram] = l1
	#Output
	end = time.time()
	print "Finished building bi-gram index for doc :" + d + " Time : " + str(start - end)

bi_keys = bigram_index.keys()
bi_keys.sort()
'''
for term in keys:
	print term +'\n' + str(bigram_index[term])
	break
'''
'''
	QUERY ENGINE
'''
#Jaccard Coefficient
#finding intersection - keeping threshold 1
def computeIntersection(bi):
	threshold = 2
	inter = []
	all_shortlisted = {}
	#dictionary stucture: term -> bigram count
	for i in bi:
		#get query terms of bigrams
		if i in bigram_index.keys():
			termList = bigram_index[i].keys()
			#Add to dictionary
			for j in termList:
				if j in all_shortlisted.keys():
					all_shortlisted[j] = all_shortlisted[j] + 1
				else:
					all_shortlisted[j] = 1
	#get intersected terms
	for i in all_shortlisted.keys():
		if all_shortlisted[i] >= threshold:
			inter.append(i)
	return inter

#Calculate jaccard coefficient
def computeJaccardIndex(query, term):
	intersection = set(query).intersection(term)
	return (len(intersection) / float(len(query) + len(term) - len(intersection)))

def getbestCorrected(query):
	#Get Bigrams
	bi_q = [] #consists of bigrams of query
	for i in range(len(query)-1):
		bi_q.append(query[i]+query[i+1])
	bi_q.append('$'+query[0])
	bi_q.append(query[len(query)-1]+'$')
	#Get intersection
	inter = computeIntersection(bi_q)
	for term in inter:
		#get its bigrams
		if(term == inter[0]):
			res = term
			bi_t = [] #consists of bigrams of query
			for i in range(len(term)-1):
				bi_t.append(term[i]+term[i+01])
			bi_t.append('$'+term[0])
			bi_t.append(term[len(term)-1]+'$')
			#get jaccard coefficient
			jc = computeJaccardIndex(bi_q,bi_t)
			maxm = jc
		else:
			bi_t = [] #consists of bigrams of query
			for i in range(len(term)-1):
				bi_t.append(term[i]+term[i+01])
			bi_t.append('$'+term[0])
			bi_t.append(term[len(term)-1]+'$')
			#get jaccard coefficient
			jc = computeJaccardIndex(bi_q,bi_t)
			if(maxm<jc):
				maxm = jc
				res = term
	return res
	

'''
'''
r = int(raw_input("Wanna query? (1/0)"))
while(r==1):
	query = str(raw_input("Input your query:")) #Sample query : Alice in wonderland
	query = query.split()
	for i in query:
		u = i
		i = stem(i)
		j = getbestCorrected(i)
		count_i = 0
		if i in inverted_index.keys():
			for k in inverted_index[i].keys():
				count_i = count_i + len(inverted_index[i][k])
		count_j = 0
		if j in inverted_index.keys():
			for k in inverted_index[j].keys():
				count_j = count_j + len(inverted_index[j][k])
		if (i not in list_sw and j not in list_sw):
			if(count_j>count_i):
				i = j
		#
		print "Showing Resuls for :" + i
		if i in inverted_index.keys():
			print "\t" + str(inverted_index[i])
		else:
			if i in list_sw:
				print "\t a stop word: (assumed available in all docs)"
			else:
				print "\tNo Results Found"
	r = int(raw_input("Wanna query? (1/0)"))


