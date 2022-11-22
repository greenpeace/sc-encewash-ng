# Sciencewashing
Revealing connections on academic publications
## Methodology
The process of collecting and analyzing academic papers is done with separate
steps. There are different Python scripts for each step:
#### journal.py
This script takes selected journals by their ISSN's from a CSV file, separates
them by general fields (Environment, Nutrition and Medical in this case) and
queries Crossref database for designated keywords (taken from a separate CSV
file) for papers published in the last 15 years. The result is papers'
metadata, which are saved as JSON files, one file per journal.
#### trim.py
Here the results are filtered from the broader queries done in the first step
and the manually rejected papers are omitted.
#### parse.py
Third step consist of analyzing the JSON output from Crossref, removing
duplicates and compiling them into another CSV file. This file is used as
the master sheet for collaboration. 
#### scidl.py and grobid.py
This (optional) step downloads papers as PDF files from SciHub, if available,
and parses them into structured JSON files with GrobID. Keywords, abstract and
conflict of interest sections will be available after this step.
#### relational.py
Currently work in progress, here comes the network analysis of the relations
between intitutions, authors and papers.
## Libraries
The following modules have been used in this project:
- crossref-commons
- sci-dl
- s2orc-doc2json (grobid)
- graphcommons
- networkx
## License
Distributed under GPL-3.0 license.
## Contribution
For comments and suggestions, please start entry under project wiki or open an
issue. You can also reach me on yakup.cetinkaya[at]greenpeace[dot]org.
