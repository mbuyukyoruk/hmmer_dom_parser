import argparse
import pdb
import subprocess
import sys
import os
import textwrap

try:
    import tqdm
except:
    print("tqdm module is not installed! Please install tqdm and try again.")
    sys.exit()


parser = argparse.ArgumentParser(prog='python hmmer_dom_parser.py',
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog=textwrap.dedent('''\

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

      	'''))
parser.add_argument('-i', '--input', required=True, type=str, dest='filename', help='Specify a hmmsearch domtblout file.\n')
parser.add_argument('-e', '--evalue', required=True, type=float, dest='E_value', help='Specify an E-value cut off (i.e., 0.001).\n')
parser.add_argument('-s', '--score', required=False, type=float, dest='score_thresh', default= 0, help='Specify an bit score cut off (i.e., 20).\n')
parser.add_argument('-qc', '--query_coverage', required=False, type=float, dest='qcov_thresh', default= 0, help='Specify a coverage cut off for query (i.e., 50).\n')
parser.add_argument('-tc', '--target_coverage', required=False, type=float, dest='tcov_thresh', default= 0, help='Specify a coverage cut off for HMM target (i.e., 50).\n')
parser.add_argument('-o', '--out', required=True, type=str, dest='out', help='Specify a output file name.\n')


results = parser.parse_args()
filename = results.filename
E_value = results.E_value
out = results.out
qcov_thresh = results.qcov_thresh
tcov_thresh = results.tcov_thresh
score_thresh = results.score_thresh

os.system("> " + out)

proc = subprocess.Popen("wc -l < " + filename, shell=True, stdout=subprocess.PIPE, text=True)
length = int(proc.communicate()[0].split('\n')[0])

proc = subprocess.Popen("grep 'Program' " + filename, shell=True, stdout=subprocess.PIPE, text=True)
proc_out = proc.communicate()[0].split('\n')[0]
program = proc_out.split()[-1]

f = open(out, 'a')
sys.stdout = f

print("Accession\thit\ti-Evalue\tbit_score\tEnv_start\tEnv_stop\tquery_len\tquery_cov\ttarget_len\ttarget_cov")

with tqdm.tqdm(range(length)) as pbar:
    with open(filename,'r') as file:
        for line in file:
            pbar.update()
            if program == "hmmsearch":
                if line[0] != "#" and len(line.split())!=0:
                    arr = line.split(" ")
                    new_list = [x for x in arr if x != '']
                    arr = new_list
                    acc = arr[0]
                    hit = arr[3]
                    qseq_len = arr[2]
                    tseq_len = arr[5]
                    iE = arr[12]
                    temp = float(iE)
                    score = arr[13]
                    temp_score = float(score)
                    env_start = arr[19]
                    env_stop = arr[20]
                    t_start = arr[15]
                    t_stop = arr[16]
                    qcov = float((int(env_stop) - int(env_start))*100/int(qseq_len))
                    tcov = float((int(t_stop) - int(t_start))*100/int(tseq_len))

                    if (temp <= E_value) and qcov >= qcov_thresh and tcov >= tcov_thresh and temp_score >= score_thresh :
                        print(acc + "\t" + hit + "\t" + iE + "\t" + score + "\t" + env_start + "\t" + env_stop + "\t" + qseq_len + "\t" + str(round(qcov,2)) + "\t" + tseq_len + "\t" + str(round(tcov,2)))

            elif program == "hmmscan":

                if line[0] != "#" and len(line.split()) != 0:
                    arr = line.split(" ")
                    new_list = [x for x in arr if x != '']
                    arr = new_list
                    hit = "|".join(arr[0:2])
                    tseq_len = arr[2]
                    acc = arr[3]
                    qseq_len = arr[5]
                    iE = arr[12]
                    temp = float(iE)
                    score = arr[13]
                    temp_score = float(score)
                    env_start = arr[19]
                    env_stop = arr[20]
                    t_start = arr[15]
                    t_stop = arr[16]
                    qcov = float((int(env_stop) - int(env_start))*100/int(qseq_len))
                    tcov = float((int(t_stop) - int(t_start))*100/int(tseq_len))

                    if (temp <= E_value) and qcov >= qcov_thresh and tcov >= tcov_thresh and temp_score >= score_thresh :
                        print(acc + "\t" + hit + "\t" + iE + "\t" + score + "\t" + env_start + "\t" + env_stop + "\t" + qseq_len + "\t" + str(round(qcov,2)) + "\t" + tseq_len + "\t" + str(round(tcov,2)))



