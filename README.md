# literaturereview_generaor
BY LANFEI LIU IN UNIVERSITY OF MICHIGAN


AIM OF THIS PROJECT:

This project is designed to export an literature review table in order to find current research achievements and figure out the research gaps. 
I search the papers which contain "rain garden" and are published in 2016, from Elsevier API and Springer API. 
I retrieve their titles, authors, pulication years, and abstracts and then pick out possible useful staticial relationships, conclusions and suggestions from each article's abstract.

STEPS:

You just need to run "Lanfei_interact.py" on terminal.
Then type in infos according to the guidiance showing on terminal

FILE LIST:

"Lanfei_interact.py"----The Python file
"README.md"----the README file
"scopus_forid.txt" ----The cache data from Elsevier Scopus Search API
"scopus_abstract.txt" ----The cache data from Elsevier Abstract Retrieval API
"scopus_abstract.csv"---- The output file containing articles' metadata, abstract and analysis of abstract from Elsevier
"springer_abstract.txt." ----The cache data from Springer Metadata API
"springer_abstract.csv",----The output file containing articles' metadata, abstract and analysis of abstract from Springer
"merged_abstract.csv"----The final output file, which is merged with "scopus_abstract.csv" and "springer_abstract.csv"


RELATIVE API SOURCES

*Elsevier Scopus Search API---to retrieve a paper's metadata(including Scopus id) from Elsevier
http://api.elsevier.com/documentation/SCOPUSSearchAPI.wadl
*Elsevier Abstract Retrieval API----retrieve a paper's abstract in Elsevier by its Scopus id
http://api.elsevier.com/documentation/AbstractRetrievalAPI.wadl
*Springer Metadata API---to retrieve a paper's metadata(containing abstract) from Springer
https://dev.springer.com/restfuloperations
https://dev.springer.com/adding-constraints
https://dev.springer.com/querystring-parameters
https://dev.springer.com/example-metadata-response
		

WHY THIS PROJECT?

I do this project because I did a literature review table manually in last summer and I found it is very time consuming. So I try to figure out doing this table by programming. I got all the metadata and abstract I wanted, but not all the papers containing staticial relationship, conclusion and suggestion in their abstract. It would be better if I analyse full text, but it would need more time and be more difficult.
