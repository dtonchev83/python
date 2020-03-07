import subprocess
import shlex
import sys
import xml.etree.ElementTree as ET
import os

'''
1 download ear files from svn reveision id

svn log https://svn-brcd.mobiltel.bg/svn/TIBCO -r 10620 -v --xml
svn export -r 10620  https://svn-brcd.mobiltel.bg/svn/TIBCO/TIBCO/MDF/MDFRules/Deployment/rulesconfig.properties

2 check name for every ear file in svn revision
3 map to the application on the environment
4 export configuration xml from the ear
5 prepare configuration xml files for every environment

'''
#create earlist
earlist = []

#scan the revision
def observerSvnID(svnid):
    svnid = svnid
    svnLog_raw_command = f"svn log https://svn-brcd.mobiltel.bg/svn/TIBCO -r {svnid} -v  --non-interactive --no-auth-cache --username capplan  --password Capplan11 --xml"
    svnLog_arg = shlex.split(svnLog_raw_command)
    return svnLog_arg

#call scan function with parmeter that was given to script
set1 = observerSvnID(sys.argv[1])

#define/format the output of the scan function
xml_string = subprocess.run(set1, capture_output=True, encoding='utf-8')

#capturing the STDOUT
pretty_xml = xml_string.stdout
#defining document root
root = ET.fromstring(pretty_xml)
#print(root.tag)

#print(type(xml_string.stdout))
#str(pretty_xml,"ascii")
print(pretty_xml)


#iterate over every 'path' element of root tag and add the ears to earlist
for xml_line in root.iter('path'):
    #print(xml_line.text)
    file_name = xml_line.text
    if ".ear" in file_name:
        #print(file_name,"is ear")
        earlist.append(file_name)
        print(earlist)

#download the ear file(s)
def downloadSvnID(svnid, path):
    svnid = svnid
    path = path
    os.chdir("/home/docker/dtonchev/ad")
    svnGetCommand = f"svn export -r {svnid}  'https://svn-brcd.mobiltel.bg/svn/TIBCO{path}' --non-interactive --no-auth-cache --username capplan --password Capplan11"
    print(svnGetCommand)
    svnGet_arg = shlex.split(svnGetCommand)
    print(svnGet_arg)
    subprocess.run(svnGet_arg)


if earlist:
    for entry in earlist:
        downloadSvnID(sys.argv[1],entry)



#copy ear to tibco host, run AppManage and generate xml file, copy that xml file back to home host
ssh_ear_xml = "uname -a"
ssh_generate_xml = 
ssh_copy_xml_from_tibco_to_home = 








 