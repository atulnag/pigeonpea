#!/bin/bash

# Phase 1

sequence=$1

#mask information with "dustmaker"
dustmasker -in $sequence -infmt fasta -parse_seqids -outfmt maskinfo_asn1_bin -out ${sequence}_dust.asnb

#generate counts file for windowmasker
windowmasker -in $sequence -infmt fasta -mk_counts -parse_seqids -out ${sequence}.counts

#Generate file containing masking information
windowmasker -in $sequence -infmt fasta -ustat ${sequence}.counts -parse_seqids -outfmt maskinfo_asn1_bin -out ${sequence}_mask.asnb

#create BLAST database with masking information
makeblastdb -in $sequence -dbtype nucl -parse_seqids -mask_data ${sequence}_dust.asnb,${sequence}_mask.asnb -out $sequence -logfile ${sequence}_blast.log

#verify if masking information is added properly
blastdbcmd -db $sequence -info
