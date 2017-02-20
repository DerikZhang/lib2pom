import os
import os.path
import shutil
import zipfile
import sys 

def copyRepo(rootdir,tempdir):
	for parent,dirnames,filenames in os.walk(rootdir):
		for dirname in dirnames:
			print('parent is: %s' % parent)
			print("dirname is %s" % dirname)

		for filename in filenames:
			if ".jar" in filename and "jar." not in filename:
				shutil.copyfile(os.path.join(parent,filename),tempdir+"/"+filename)
			# print("parent is: %s" % parent)
			# print("filename is:%s" % filename)
			# print("the full name of the file is: %",os.path.join(parent,filename))

def analyzeJar(tempdir,outputdir):
	acount = 0
	shown = 0
	outputfile = outputdir+"/result.xml"
	fp = open(outputfile,'w')
	fp.write('<dependencies>\n')
	for parent,dirnames,filenames in os.walk(tempdir):
		for filename in filenames:
			jar = zipfile.ZipFile(os.path.join(parent,filename),"r")
			for jarfilename in jar.namelist():
				# print("jarfilename: %s" % jarfilename)
				if 'pom.properties' in jarfilename:
					acount+=1
					print("filename is %s" % filename)
					# print(jar.read(jarfilename))
					profile = jar.read(jarfilename)
					# print(profile)
					properties = {}
					for line in profile.decode('utf-8').split('\n'):
						if line.find('#') >= 0:
							continue
						if line.find('=') > 0:
							shown+=1
							strs = line.replace('\r', '').split('=')
							properties[strs[0]] = strs[1]
					fp.write('\t<dependency>\n')
					fp.write('\t\t<groupId>'+properties['groupId']+'</groupId>\n')
					fp.write('\t\t<artifactId>'+properties['artifactId']+'</artifactId>\n')
					fp.write('\t\t<version>'+properties['version']+'</version>\n')
					fp.write('\t</dependency>\n')
	fp.write('</dependencies>\n')					
	print("acount:%s" % acount)
	print("shown:%s" % shown) 
	fp.close()


if __name__ == '__main__':
	rootdir = "C:/Users/DerikZhang/.m2/repository"
	print(len(sys.argv))
	if len(sys.argv) <= 1:
		tempdir = "temp"
	else:
		tempdir = sys.argv[1]
	print(tempdir)
	# copyRepo(rootdir,tempdir) # copy jar from repo to temp for test
	outputdir = "./"
	analyzeJar(tempdir,outputdir)
