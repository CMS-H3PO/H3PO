import tarfile
import os

def unpackTar(fileToUnpack,odir):
	os.system("rm -f *txt*")
	tar = tarfile.open(fileToUnpack, "r:gz")
	tar.extractall()
	tar.close()



	files = [f for f in os.listdir('.') if os.path.isfile(f)]
	for f in files:
		if not ".txt" in f:
			continue
		if not ("AK4PFchs" in f or "AK8PFPuppi" in f):
			os.remove(f)
			continue
		if "JRV" in f:
			if "PtResolution" in f:
				newName = f.replace(".txt",".jr.txt")
				os.rename(f,newName)
				continue
			elif "SF" in f:
				newName = f.replace(".txt",".jersf.txt")
				os.rename(f,newName)
				continue
			else:
				print("Deleting ", f)
				os.remove(f)
				continue
		elif "Uncertainty" in f:
			newName = f.replace(".txt",".junc.txt")
			os.remove(f)
			continue
		else:
			newName = f.replace(".txt",".jec.txt")
			os.rename(f,newName)
			continue

	os.system("gzip *txt")
	os.system(f"mv *txt.gz {odir}")	

files = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in files:
	if not "tar.gz" in f:
		continue

	if "UL16APV" in f:
		odir = "/users/mrogul/Work/H3/H3PO/data/jec/2016APV/"
	elif "UL16" in f:
		odir = "/users/mrogul/Work/H3/H3PO/data/jec/2016/"
	elif "UL17" in f:
		odir = "/users/mrogul/Work/H3/H3PO/data/jec/2017/"
	elif "UL18" in f:
		odir = "/users/mrogul/Work/H3/H3PO/data/jec/2018/"

	unpackTar(f,odir)