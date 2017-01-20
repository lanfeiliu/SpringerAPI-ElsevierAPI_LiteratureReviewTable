import unittest
import requests
import json
import csv
import os

print "Warning: you must run this program in an University Network!!!\n"

#Interactive input
keyword = raw_input("Please enter your key word:") 

date_int = int(raw_input("Please enter the published year:"))
while date_int < 2000:
	print "The published year must be after 2000!"
	date_int = int(raw_input("Please enter the published year:"))

elsevier_keyword = "{" + keyword + "}"
#"?q=(%22rain%20garden%22%20AND%20year:2016)"
springer_keyword = "?q=("+ "%22" + keyword.replace(" ", "%20") + "%22" + "%20AND%20year:" + str(date_int) + ")"


###Get metadata and scopus id of each article from Elsevier Scopus Search API
#see document http://api.elsevier.com/documentation/SCOPUSSearchAPI.wadl
elsevier_api_key = raw_input("Please enter your elsevier api key: ") 

url_scopus = 'http://api.elsevier.com/content/search/scopus'

# Building the Elsevier Scopus Search query parameters dictionary
#search articles which contain "rain garden" and are published in 2016
query_scopus = {}
query_scopus["query"] = elsevier_keyword  
query_scopus["date"] = str(date_int) + "-" + str(date_int + 1)    # the date range associated with the search
query_scopus["count"] = 200            #items per page
query_scopus["sort"] = "citedby-count"  #the sort field name and order

#Get cache from Scopus Search API/use cache 
try: 
	###Pick out articles from cache
	for_scopus = open('scopus_forid.txt').read()
	#transit text dictionary to dictionary
	d_scopus = json.loads(for_scopus)
except:
	#request 10 articles from Scopus
	#need both query paramters and head parameters
	request_scopus = requests.get(url_scopus,params=query_scopus,
							headers={'Accept':'application/json',
									'X-ELS-APIKey': elsevier_api_key})
	d_scopus = request_scopus.json()
	#Gitbash--Check url
	#print request_scopus.url
	#Gitbash--Get result printed
	#print json.dumps(request_scopus.json(),
					# sort_keys=True,
					# indent=4, separators=(',', ': '))
	#Gitbash
	#print "--------Result of Elsevier Scopus Search API-----------"
	#print pretty(d_scopus)[:2000]
	#cache the data from Scopus and collected
	fr_scopus = open("scopus_forid.txt","w")
	fr_scopus.write(json.dumps(d_scopus))
	fr_scopus.close()

#Get all SCOPUS_ID
scopusid_list= [str(i["dc:identifier"]) for i in d_scopus["search-results"]["entry"]]
# Gitbash--check the Scopus ID list
# print scopusid_list
# [['SCOPUS_ID:84963894274'], ['SCOPUS_ID:84976503372'], ['SCOPUS_ID:85003434350'], ['SCOPUS_ID:84955622088'], ['SCOPUS_ID:84985027777'], ['SCOPUS_ID:84976463590'], ['SCOPUS_ID:84959528991'], ['SCOPUS_ID:84963800499'], ['SCOPUS_ID:84957433628'], ['SCOPUS_ID:84976489746']]
print "--------Elsevier Scopus Search API cache is finished-----------"


#Get abstract and further analysis according to each article's Scopus id from Elsevier Abstract Retrieval API
#see document http://api.elsevier.com/documentation/AbstractRetrievalAPI.wadl
#Must use University Network!!!!!!!!!!
def get_abstractdc(SCOPUS_ID):
	url_abstract = ("http://api.elsevier.com/content/abstract/scopus_id/" + SCOPUS_ID)
	resp = requests.get(url_abstract,
					headers={'Accept':'application/json',
							 'X-ELS-APIKey': elsevier_api_key})
	return json.loads(resp.text.encode('utf-8'))

#Get cache from Elsevier Abstract Retrieval API/use cache 
try: 
	for_abstract = open('scopus_abstract.txt').read()
	results_lst = json.loads(for_abstract)
except:
	results_lst = []
	for sid in scopusid_list:
		#print type(sid)
		results_lst.append(get_abstractdc(sid))	
	#print results_lst
	fr_abstract = open("scopus_abstract.txt","w")
	fr_abstract.write(json.dumps(results_lst))
	fr_abstract.close()
print "--------Elsevier Abstract Retrieval API cache is finished-----------"

# Get a sample abstract dictionary to check the structure
# fr_scopus = open("scopus_abstract.txt","w")
# fr_scopus.write(json.dumps(get_abstractdc('SCOPUS_ID:84963894274')))
# fr_scopus.close()

#Get analysis of each artcle's metadata and abstract
#see document http://kitchingroup.cheme.cmu.edu/blog/2015/04/03/Getting-data-from-the-Scopus-API/
class Scopus_Article():
	def __init__(self, results={}):#input each result
		self.result = results
		self.title = results['abstracts-retrieval-response']['coredata']['dc:title'].encode('utf-8')
		self.journal = results['abstracts-retrieval-response']['coredata']['prism:publicationName'].encode('utf-8')
		self.date = results['abstracts-retrieval-response']['coredata']['prism:coverDate'].encode('utf-8')
		self.citesnumber = int(results['abstracts-retrieval-response']['coredata']['citedby-count'].encode('utf-8'))
		self.abstract = results['abstracts-retrieval-response']['coredata']['dc:description'].encode('utf-8')
	
	def author(self):
		name_lst = [i['ce:indexed-name'] for i in self.result['abstracts-retrieval-response']['authors']['author']]
		combine_name = ', '.join(name_lst)
		return combine_name

	def removeQM(self):
		abstract_clean = "Copyright, " + self.abstract[3:]
		return abstract_clean 

	def significant(self):
		sentences_lst = (self.removeQM()).split('.')
		i = 0
		for s in sentences_lst :
			if 'significan' in s:
				return s
				i +=1
			elif 'associat' in s:
				return s
				i +=1
		if i == 0:
			return 'None'

	def conclusion(self):
		sentences_lst = (self.removeQM()).split('.')
		i = 0
		for s in sentences_lst :
			if 'conclu' in s:
				return s
				i +=1
		if i == 0:
			return 'None'

	def suggest(self):
		sentences_lst = (self.removeQM()).split('.')
		i = 0
		for s in sentences_lst :
			if 'suggest' in s:
				return s
				i +=1
		if i == 0:
			return 'None'

# #Create scopus csv file
article_insts = [Scopus_Article(results) for results in results_lst]

file1=open('scopus_abstract.csv','wb')
writer=csv.writer(file1)

titlelst = [i.title for i in article_insts]
authorlst = [i.author() for i in article_insts]
journallst = [i.journal for i in article_insts]
datelst = [i.date for i in article_insts]
citeslst = [i.citesnumber for i in article_insts]
abstractlst = [i.removeQM() for i in article_insts]
significantlst = [i.significant() for i in article_insts]
conclusionlst = [i.conclusion() for i in article_insts]
suggestlst = [i.suggest() for i in article_insts]

writer.writerow(['title','authors',"journal", "date", "cites number", "abstract", "significant relationship", "conclusion", "suggestion"])
writer.writerows(zip(titlelst, authorlst,journallst,datelst,citeslst,abstractlst,significantlst,conclusionlst,suggestlst))

print "--------scopus_abstract.csv is finished-----------"
# Write code to collect 3 top cited articles and the number of cites here.
d_cites = {}
for i in article_insts:
	if i.author() not in d_cites:
		author_lst = i.author().split(',')
		first_author = author_lst[0]
		key = first_author + ',' + i.date[:4]
		d_cites[key] = i.citesnumber 

top_citers = (sorted(d_cites.items(), key = lambda x:x[1], reverse=True))[:3]
print top_citers #[(u'Booth D.B.,2016', 12), (u'Gao Y.,2016', 4), (u'Sicard P.,2016', 2)]


###Springer Metadata API
#https://dev.springer.com/restfuloperations
#https://dev.springer.com/adding-constraints
#https://dev.springer.com/querystring-parameters
#https://dev.springer.com/example-metadata-response
springer_api_key = raw_input("Please enter your springer api key: ") 

base_url_springer = 'http://api.springer.com/metadata/json'

# Building the Springer Metadata API parameters dictionary
url_params_springer = {}
url_params_springer["api_key"] = springer_api_key
url_params_springer["p"] = 200   #10 results will be returned

try: 
	###Pick out articles' SCOPUS_ID 
	for_springer = open('springer_abstract.txt').read()
	#transit text dictionary to dictionary
	d_springer = json.loads(for_springer)

except:
	#request 200 articles from Scopus, search articles which contain "rain garden" and are published in 2016
	#see document https://dev.springer.com/adding-constraints
	d_springer = requests.get(base_url_springer + springer_keyword
								,params=url_params_springer).json()
	#for Gitbash
	print "--------Result of Springer Metadata API-----------"
	#print pretty(d_springer)[:2000]
	# cache the data from Scopus and collected
	fr_springer = open("springer_abstract.txt","w")
	fr_springer.write(json.dumps(d_springer))
	fr_springer.close()

abstract_list_springer = [i["abstract"] for i in d_springer["records"]]

#Get analysis of each artcle's metadata and abstract
class Springer_Article():
	def __init__(self, records={}):#input each result
		self.records= records
		self.title = records['title'].encode('utf-8')	
		self.journal = records['publicationName'].encode('utf-8')
		self.date = records['publicationDate'].encode('utf-8')
		self.citesnumber = 'N/A'
		self.abstract = records['abstract'].encode('utf-8')[8:]
	
	def author(self):
		name_lst = [i['creator'].encode('utf-8') for i in self.records['creators']]
		combine_name = ', '.join(name_lst)
		return combine_name

	def significant(self):
		sentences_lst = (self.abstract).split('.')
		i = 0
		for s in sentences_lst :
			if 'significan' in s:
				return s
				i +=1
			elif 'associat' in s:
				return s
				i +=1
		if i == 0:
			return 'None'

	def conclusion(self):
		sentences_lst = (self.abstract).split('.')
		i = 0
		for s in sentences_lst :
			if 'conclu' in s:
				return s
				i +=1
		if i == 0:
			return 'None'

	def suggest(self):
		sentences_lst = (self.abstract).split('.')
		i = 0
		for s in sentences_lst :
			if 'suggest' in s:
				return s
				i +=1
		if i == 0:
			return 'None'

#remove duplicate articles between Elsevier and Springer
article_insts2 = [Springer_Article(records) for records in d_springer['records']]

for i in article_insts2:
	if i.title in titlelst:
		article_insts2.remove(i)

# #Create Springer csv file
titlelst2 = [i.title for i in article_insts2]
authorlst2 = [i.author() for i in article_insts2]
journallst2 = [i.journal for i in article_insts2]
datelst2 = [i.date for i in article_insts2]
citeslst2 = [i.citesnumber for i in article_insts2]
abstractlst2 = [i.abstract for i in article_insts2]
significantlst2 = [i.significant() for i in article_insts2]
conclusionlst2 = [i.conclusion() for i in article_insts2]
suggestlst2 = [i.suggest() for i in article_insts2]

file1=open('springer_abstract.csv','wb')
writer=csv.writer(file1)

writer.writerow(['title','authors',"journal", "date", "cites number", "abstract", "significant relationship", "conclusion", "suggestion"])
writer.writerows(zip(titlelst2, authorlst2,journallst2,datelst2,citeslst2,abstractlst2,significantlst2,conclusionlst2,suggestlst2))

print "--------springer_abstract.csv is finished-----------"

#Merge two csv files
#see document https://pythonhosted.org/brewery/examples/merge_multiple_files.html

fout=open("merged_abstract.csv","w")
# first file:
for line in open("scopus_abstract.csv"):
	fout.write(line)
# now the rest:    

f = open("springer_abstract.csv")
f.next() # skip the header
for line in f:
	fout.write(line)
f.close() # not really needed

fout.close()
print "--------merged_abstract.csv is finished-----------"

#open the file like double click on screen
os.system("merged_abstract.csv")

