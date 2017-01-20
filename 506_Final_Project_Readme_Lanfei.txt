506 Final Project Readme. 
Lanfei Liu

1.Describe your project in 1-4 sentences. Include the basic summary of what it does, and the output that it should generate/how one can use the output and/or what question the output answers. 

	*This project is designed to export an literature review table in order to find current research achievements and figure out the research gaps. I search the papers which contain "rain garden" and are published in 2016, from Elsevier API and Springer API. I retrieve their titles, authors, pulication years, and abstracts and then pick out possible useful staticial relationships, conclusions and suggestions from each article's abstract.



2. Explain exactly what needs to be done to run your program (what file to run, anything the user needs to input, anything else) and what we should see once it is done running (should it have created a new text file or CSV? What should it basically look like?).

(Your program running should depend on cached data, but OK to write a program that would make more sense to run on live data and tell us to e.g. use a sample value in order to run it on cached data.)

EXAMPLE:
First run python myproject.py
Then, when it asks for a 3-letter airport code, type an airport abbreviation. You should type "DTW" to use the cached data.
You should have a new file in your directory afterward called airport_info.csv which contains... <explain further>
etc.

	*You just need to run the python file "Lanfei.py"directly. You should have several new files in your directory afterward, they are:

	"scopus_forid.txt" which contains the cache data from Elsevier Scopus Search API
	"scopus_abstract.txt" which contains the cache data from Elsevier Abstract Retrieval API
	"scopus_abstract.csv", which is the output file containing articles' metadata, abstract and analysis of abstract from Elsevier
	"springer_abstract.txt." which contains the cache data from Springer Metadata API
	"springer_abstract.csv", which is the output file containing articles' metadata, abstract and analysis of abstract from Springer
	and finally, "scopus_abstract.csv" and "springer_abstract.csv" will be merged into "merged_abstract.csv".




3. List all the files you are turning in, with a brief description of each one. (At minimum, there should be 1 Python file, 1 file containing cached data, and the README file, but if your project requires others, that is fine as well! Just make sure you have submitted them all.)
	"Lanfei.py"----The Python file
	"506_Final_Project_Readme_Lanfei.txt"----the README file
	"scopus_forid.txt" ----The cache data from Elsevier Scopus Search API
	"scopus_abstract.txt" ----The cache data from Elsevier Abstract Retrieval API
	"scopus_abstract.csv"---- The output file containing articles' metadata, abstract and analysis of abstract from Elsevier
	"springer_abstract.txt." ----The cache data from Springer Metadata API
	"springer_abstract.csv",----The output file containing articles' metadata, abstract and analysis of abstract from Springer
	"merged_abstract.csv"----The final output file, which is merged with "scopus_abstract.csv" and "springer_abstract.csv"




4. Any Python packages/modules that must be installed in order to run your project (e.g. requests, or requests_oauthlib, or...):
	unittest
	requests
	json
	csv



5. What API sources did you use? Provide links here and any other description necessary.
	*Elsevier Scopus Search API---to retrieve a paper's metadata(including Scopus id) from Elsevier
	http://api.elsevier.com/documentation/SCOPUSSearchAPI.wadl
	*Elsevier Abstract Retrieval API----retrieve a paper's abstract in Elsevier by its Scopus id
	http://api.elsevier.com/documentation/AbstractRetrievalAPI.wadl
	*Springer Metadata API---to retrieve a paper's metadata(containing abstract) from Springer
	https://dev.springer.com/restfuloperations
	https://dev.springer.com/adding-constraints
	https://dev.springer.com/querystring-parameters
	https://dev.springer.com/example-metadata-response
		



6. Approximate line numbers in Python file to find the following mechanics requirements (this is so we can grade your code!):


- Sorting with a key function:

	159-168
- Use of list comprehension OR map OR filter:
	48
	97
	139
	144-152
	203
	254
	261-269
- Class definition beginning 
	1:
- Class definition beginning 
		87
		206
		
	2:
- Creating instance of one class:

		139
		
	- Creating instance of a second class:

		254

- Calling any method on any class instance (list all approx line numbers where this happens, or line numbers where there is a chunk of code in which a bunch of methods are invoked):

	
- (If applicable) Beginnings of function definitions outside classes:

	144-152
	261-269
- Beginning of code that handles data caching/using cached data:

	21
	66
	184

- Test cases: 
	297-350



8. Rationale for project: why did you do this project? Why did you find it interesting? Did it work out the way you expected?
	I do this project because I did a literature review table manually in last summer and I found it is very time consuming. So I try to figure out doing this table by programming. I got all the metadata and abstract I wanted, but not all the papers containing staticial relationship, conclusion and suggestion in their abstract. It would be better if I analyse full text, but it would need more time and be more difficult.