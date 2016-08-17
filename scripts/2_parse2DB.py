#For Regular Expressions
import re
#For call to standalone BLAST
import subprocess
import sys
#For MySQL
import MySQLdb as mdb

error = open("errors2.txt","w")

try:
	con = mdb.connect('localhost','Ccajan','Ccajan','Ccajan')
	file = open("../blastdb/CCids.txt")

	for line in file:
		line= line.strip()
		cols = line.split("\t")
		Accession = cols[0]
		print Accession
		try:
			with open("../blastdb/PigeonPeaProteins/Seqs/"+Accession+'.fa','r') as f:
				ProteinSeq = f.read()
			with open("../blastdb/PigeonPeaCDS/Seqs/"+Accession+'.fa','r') as f:
				CDS = f.read()
			Location = cols[1]
			data = Location.split(":")
			if data[3] == "+":
				strand = "plus"
			else:
				strand = "minus"
			if int(data[1]) < int(data[2]):
				start = data[1]
				stop = data[2]
				pstart = (int(start) - 1000) if (int(start) - 1000) > 1 else 1
			else:
				start = data[2]
				stop = data[1]
				pstart = int(start) + 1000
			#print str(pstart)+" "+str(start)+" "+str(stop)
			Gene = "blastdbcmd -db ../blastdb/PigeonPeaG/PigeonPea.scafSeq.LG_V5.0.fa -entry "+ data[0]+" -range "+start+"-"+stop+" -strand "+strand
			Promotor = "blastdbcmd -db ../blastdb/PigeonPeaG/PigeonPea.scafSeq.LG_V5.0.fa -entry "+ data[0]+" -range "+str(pstart)+"-"+start+" -strand "+strand

			p = subprocess.Popen(Gene, stdout=subprocess.PIPE, shell=True)
			(output, err) = p.communicate()

			## Wait for date to terminate. Get return returncode ##
			p_status = p.wait()

			if p_status == 0:
				Gene = re.sub(r'>(.*)',r'>'+Accession+'|G|'+'\g<1>',output)
			else:
				error.write("Command output : "+output)
				error.write("Command exit status/return code : "+str(p_status))

			p = subprocess.Popen(Promotor, stdout=subprocess.PIPE, shell=True)
			(output, err) = p.communicate()

			## Wait for date to terminate. Get return returncode ##
			p_status = p.wait()

			if p_status == 0:
				Promotor = re.sub(r'>(.*)',r'>'+Accession+'|P|'+'\g<1>',output)
			else:
				error.write("Command output : "+output)
				error.write("Command exit status/return code : "+str(p_status))
			sql = "INSERT INTO SeqData VALUES (%s, %s, %s, %s, %s, %s)"

			#sql = "UPDATE SeqData SET Promoter=%s WHERE Promoter LIKE %s"
			with con:
				cur = con.cursor()
				#cur.execute(sql,(mdb.escape_string(str(Promotor)),("blastdbcmd"+"%")))
				cur.execute(sql,\
					(Accession,mdb.escape_string(str(ProteinSeq)),CDS,mdb.escape_string(str(Location)),\
						mdb.escape_string(str(Gene)),mdb.escape_string(str(Promotor))))

				con.commit()
		except IOError as e:
			error.write("%s  IOError: %d: %s\n" % (Accession, e.args[0],e.args[1]))
			continue
except mdb.Error, e:
	error.write("DBError %d: %s\n" % (e.args[0],e.args[1]))
	sys.exit(1)
