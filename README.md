# hmmer_dom_parser

Author: Murat Buyukyoruk

    hmmer_dom_parser help:

This script is developed parse hmmsearch or hmmscan domain table outfile (domtblout) to extract domain positions in each accession based on i-Evalue.

SeqIO and Seq packages from Bio is required to fetch sequences. Additionally, tqdm is required to provide a progress bar since some multifasta files can contain long and many sequences.

Syntax:

    python hmmer_dom_parser.py -i demo_hmmsearch_domtblout.txt -o out_summary.txt -e 0.001 -s 20 -qc 50 -tc 50

hmmer_dom_parser dependencies:

tqdm                                                    refer to https://pypi.org/project/tqdm/

Input Paramaters (REQUIRED):
----------------------------
    -i/--input              domtblout   Specify a hmmsearch domtblout file

    -o/--output             Output      Specify a output filename.
	
    -e/--evalue             i-Evalue    Specify an E-value cut off (i.e., 0.001).
    
    -s/--score              bit score   Specify an bit score cut off (i.e., 20).

    -qc/--query_coverage    coverage    Specify a coverage cut off for query (i.e., 50).

    -tc/--target_coverage   coverage    Specify a coverage cut off for HMM target (i.e., 50).

Basic Options:
--------------
    -h/--help               HELP        Shows this help text and exits the run.
