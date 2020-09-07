# pubmed-eponyms

Python scripts for searching pubmed using Biopython and working with eponymous terms.

## Citing
In addition to citing this GitHub repository (https://github.com/cornish/pubmed-eponyms), please cite the following paper:

** reference to be added **


## License
Gnu Public License v3, see text of the full license in project.


## Dependencies:
- [Python 3.6](https://www.python.org/downloads/) and up
- [BioPython](https://pypi.python.org/pypi/biopython)


## Script files
1. rebase_terms.py
2. permute_terms.py
3. pubmed_search_to_csv.py
4. remove_pmid_dupes.py
5. pubmed_journals_by_year.py


## Data files:
1. 321 chemistry eponyms.txt
2. 321 chemistry eponyms - split - edits - utf8.csv
3. data/terms_re-base.csv
4. data/terms_permuted.csv
5. data/term_results.csv
5. data/pmid_results.csv
6. data/pmid_results - dupes removed.csv
7. data/journal_counts.csv


download_images_from_gene_list.py
--------------
### Usage:

`download_images_from_gene_list.py input_file output_file tissue output_dir [-v hpa_version] [-w workers]`

For a list of gene ids and a tissue type, this script will get the list of images and image metadata for HPA images, download the full-sized HPA images, and output a file listing information about the retrieved images.  This file requires a .txt input file of ENSG IDs and outputs a .csv file. HPA ENSG IDs can be obtained here: http://www.proteinatlas.org/about/download. Large downloads can take a LONG time.

### Parameters:

**input_file**: A txt file list of ENSG IDs (one per line) without a header in the style of:  
ENSG00000000003  
ENSG00000000005  
ENSG00000000419  

**output_file**: A CSV file with 6 columns:
- version: HPA version 
- image_file: the name of the image file downloaded
- ensg_id: the Ensembl gene id
- tissue: the tissue represented in the image
- antibody: the id of the antibody in the image
- protein_url: the HPA url for the ensg_id
- image_url: the HPA url the image was downloaded from

**tissue**: A valid tissue type recognized by the HPA website. A list of known tissue types are given in Appendix A (for normals) and Appendix B (for cancers) of this file. If there are spaces in the tissue name, enclose the whole name in double quotes, for example: "Heart muscle".

**output_dir**: A folder to contain the downloaded JPEG images.  It will be created if it does not exist.

**hpa_version**: Either 18 or 19, defaults to 19.

**workers**: The number of threads to use for downloading images. Optional. Defaults to 3. For large downloads, 50 might be more appropriate.  Please avoid using an excessive number of workers (100 or more).

