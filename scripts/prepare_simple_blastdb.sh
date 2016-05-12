#!/bin/bash

# Phase 1

sequence=$1
dtype=$2

#create BLAST database with masking information
makeblastdb -in $sequence -dbtype ${dtype} -parse_seqids -hash_index -out $sequence -logfile ${sequence}_blast.log

#verify if masking information is added properly
blastdbcmd -db $sequence -info
