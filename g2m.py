import os
import sys
from os.path import expanduser



NexusGroup="com.winter.eyas"
GradleFolder=""
SYSTEM="unix"

home = expanduser("~")
print(home)

if(sys.platform == "win32"):
	print(sys.platform+" is windows system!!")
	SYSTEM="windows"
	GradleFolder=home+ "\.gradle\caches\modules-2\\files-2.1\\"
else:
	print(sys.platform+" is unix system!!")
	GradleFolder=home+ "/.gradle/caches/modules-2/files-2.1/" 

releasejars=[]
snapshotjars=[]
for path, subdirs, files in os.walk(GradleFolder+NexusGroup):
	for name in files:
		file=os.path.join(path,name)
		if file.endswith(".jar") and (not file.endswith("sources.jar")):
		  #print(file)
			artifactPath=""
			if(SYSTEM=="unix"):
			  artifactPath=file.split("/files-2.1/")[1]
			elif(SYSTEM=="windows"):
				artifactPath=file.split("\\files-2.1\\")[1]
			#print(artifactPath)
			if(artifactPath.endswith("SNAPSHOT.jar")):
				snapshotjars.append(artifactPath)
			else:
				releasejars.append(artifactPath)

print("get the snapshot jars: "+ str(len(snapshotjars)) +"\n")
for snapshotPath in snapshotjars:
	print(snapshotPath)

print("\n********************\n")
print("get the release jars: "+ str(len(releasejars)) +"\n")

for releasePath in releasejars:
	print(releasePath)				


snapshotDicts=[]
releaseDicts=[]

for item in snapshotjars:
	mavenArtifact={}
	itemArray=[]
	if(SYSTEM=="unix"):
	  itemArray=item.split("/")
	elif(SYSTEM=="windows"):
		itemArray=item.split("\\")
	mavenArtifact["groupID"]=itemArray[0]
	mavenArtifact["artifactID"]=itemArray[1]
	mavenArtifact["version"]=itemArray[2]
	mavenArtifact["deployFile"]=GradleFolder+item
	snapshotDicts.append(mavenArtifact)


for item in releasejars:
	mavenArtifact={}
	itemArray=[]
	if(SYSTEM=="unix"):
	  itemArray=item.split("/")
	elif(SYSTEM=="windows"):
		itemArray=item.split("\\")
	mavenArtifact["groupID"]=itemArray[0]
	mavenArtifact["artifactID"]=itemArray[1]
	mavenArtifact["version"]=itemArray[2]
	mavenArtifact["deployFile"]=GradleFolder+item
	releaseDicts.append(mavenArtifact)

print("\n*************\n")
for snapshotDict in snapshotDicts:
	#print(snapshotDict)
	mavenCommand= "mvn deploy:deploy-file \
	 -DgroupId=" + snapshotDict["groupID"] + " \
  -DartifactId=" + snapshotDict["artifactID"] + " \
  -Dversion=" + snapshotDict["version"] + " \
  -Dpackaging=jar  \
  -Dfile="+ snapshotDict["deployFile"] + " \
  -DrepositoryId=winter-snapshot \
  -Durl=http://localhost:8081/nexus/content/repositories/winter-snapshot/ "
	os.system(mavenCommand)

print("\n*************\n")
for releaseDict in releaseDicts:
	#print(releaseDict)
	mavenCommand= "mvn deploy:deploy-file \
	 -DgroupId=" + releaseDict["groupID"] + " \
  -DartifactId=" + releaseDict["artifactID"] + " \
  -Dversion=" + releaseDict["version"] + " \
  -Dpackaging=jar  \
  -Dfile="+ releaseDict["deployFile"] + " \
  -DrepositoryId=winter-release \
  -Durl=http://localhost:8081/nexus/content/repositories/winter-release/ "
	os.system(mavenCommand)	
