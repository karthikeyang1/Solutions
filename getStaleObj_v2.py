'''
Created on 04-Nov-2015

@author: karthikeyanG

version : 2.0
Purpose of this script:
This script is the newer version. old version is 1.0
This script fixes the issue where the same VLAN/VXLAN, MAC is not displayed for all stale entries.Just one entry is displayed before.

'''
import os
import sys
import re
import paramiko

def staleCheck(ip, username, password,vmmsrc):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username=username, password=password, timeout =  30)
    
    stdin, stdout, stderr = ssh.exec_command("moquery -c fvEpDefRef")
    EpDef = stdout.read()
    stdin, stdout, stderr = ssh.exec_command("moquery -c fvVDEp")
    VDEp = stdout.read()
    stdin, stdout, stderr = ssh.exec_command("moquery -c fvTunDefRef")
    TunDef = stdout.read()

    encap_val = ""
    ##### Parsing the fvEpDefRef list############
    EpDef_list = EpDef.split("# fv.EpDefRef")
    epdef_1 = []
    for ep in EpDef_list:
        a1 = None
	if vmmsrc != '':
          if re.search("vmmSrc\s+\:\s+%s" %(vmmsrc),ep):
            a1 = re.search("\[(v.?lan)-(\d+)\]\-.*epdefref-([\S:]+)",ep)
    	else:
            a1 = re.search("\[(v.?lan)-(\d+)\]\-.*epdefref-([\S:]+)",ep)
	if a1 != None:
           temp = (a1.group(2),a1.group(3))
    	   epdef_1.append(temp)
    epdef_1 = sorted(epdef_1)
    epdef_pair = [epdef_1[i] for i in range(len(epdef_1)) if i == 0 or epdef_1[i] != epdef_1[i-1]]
    print " "
    print "Printing the Encap-VLAN/VXLAN,Mac - fvEpDefRef pairs"
    print "=============================================="
    print epdef_pair
    print " "
    print " "
    print " "
    ##### Parsing the fvVDEp list #############
    vdep_list = VDEp.split("# fv.VDEp")
    vdep_1 = []
    for vd in vdep_list:
	b1 = None
	if vmmsrc != '':
	  if re.search("vmmSrc\s+:\s+%s" %(vmmsrc),vd):
	     b1 = re.search("vdep\-([\S:]+)\-encap\-\[v.?lan\-(\d+)\]",vd)
	else:
	     b1 = re.search("vdep\-([\S:]+)\-encap\-\[v.?lan\-(\d+)\]",vd)
	if b1 != None:
		temp1 = (b1.group(2),b1.group(1))
		vdep_1.append(temp1)
    vdep_1 = sorted(vdep_1)
    vdep_pair = [vdep_1[i] for i in range(len(vdep_1)) if i == 0 or vdep_1[i] != vdep_1[i-1]]
    print "Printing the Encap-VLAN/VXLAN,Mac - fvVDEp pairs"
    print "=========================================="
    print vdep_pair
    print " "
    print " "
    print " "
    ##### Parsing the fvTunDefRef list ##########
    tundef_list = TunDef.split("# fv.TunDefRef")
    tundef_1 = []
    for tn in tundef_list:
        c1 = None
	if vmmsrc != '':
	  if re.search("vmmSrc\s+\:\s+%s" %(vmmsrc),tn):
             c1 = re.search("\[v.?lan-(\d+)\]\-.*tundefref-([\S:]+)",ep)
        else:
             c1 = re.search("\[v.?lan-(\d+)\]\-.*tundefref-([\S:]+)",ep)
        if c1 != None:
                temp2 = (c1.group(1),c1.group(2))
                tundef_1.append(temp2)
    tundef_1 = sorted(tundef_1)
    tundef_pair = [tundef_1[i] for i in range(len(tundef_1)) if i == 0 or tundef_1[i] != tundef_1[i-1]]
    print " "
    print "Printing the Encap-VLAN/VXLAN,Mac - fvTunDefRef pairs"
    print "=============================================="
    print tundef_pair
    print " "
    print " "
    print " "

    ####### Checking for stale fvEpDefRef entries ############## 
    x1 = set(epdef_pair)
    y1 = set(vdep_pair)
    z1 = [x for x in epdef_pair if x not in vdep_pair]
    print "===================================================="
    print "Printing the Encap-VLAN/VXLAN,Mac,dn for stale fvEpDefRef "
    print "===================================================="
    if z1 == []:
	print " **** No stale fvEpDefRef present ****"
    else:
        final = []
        for x,y in z1:
           op = re.findall("dn\s+\:\s+(.*\[v.?lan-%s\]\-.*epdefref-%s.*)\nencap" %(x,y),EpDef)
           if op != None:
	      for each_op in op:
	         each_op_m = re.search("(uni.*\[v.?lan-%s\]\-.*epdefref-%s)" %(x,y),each_op)
	         temp = [x,y,each_op_m.group(1)]
	         final.append(temp)
	cnt = 1
        for i in final:
	    if i[1] != []:
	      if re.search("vlan",i[2]):	
	         print str(cnt)+".) Encap-VLAN:"+i[0]+", Mac:"+i[1]+", dn:"+i[2] 
	      elif re.search("vxlan",i[2]):
	         print str(cnt)+".) Encap-VXLAN:"+i[0]+", Mac:"+i[1]+", dn:"+i[2] 
	      cnt = cnt+1
    print " "
    print " "
    print " "
    ######## Checking for stale fvTunDefRef entries ############
    x1 = set(tundef_pair)
    y1 = set(vdep_pair)
    z1 = [x for x in tundef_pair if x not in vdep_pair]
    print "===================================================="
    print "Printing the Encap-VLAN/VXLAN,Mac,dn for stale fvTunDefRef "
    print "===================================================="
    if z1 == []:
        print " **** No stale fvTunDefRef present ****"
    else:
        final = []
        for x,y in z1:
           op = re.findall("dn\s+\:\s+(.*\[v.?lan-%s\]\-.*tundefref-%s.*)\nencap" %(x,y),TunDef)
           if op != None:
	      for each_op in op:
	         each_op_m = re.search("(uni.*\[v.?lan-%s\]\-.*tundefref-%s)" %(x,y),each_op)
                 temp = [x,y,each_op_m.group(1)]
                 final.append(temp)
        cnt = 1
	for i in final:
            if i[1] != []:
	      if re.search("vlan",i[2]):	
                 print str(cnt)+".) Encap-VLAN:"+i[0]+", Mac:"+i[1]+", dn:"+i[2]
	      elif re.search("vxlan",i[2]):
	         print str(cnt)+".) Encap-VXLAN:"+i[0]+", Mac:"+i[1]+", dn:"+i[2] 
	      cnt = cnt+1
    print " "
    print " "
    print " "
    return 1 



if __name__ == "__main__":
    if (len(sys.argv) == 4):
        ip = sys.argv[1]
        username = sys.argv[2]
        password = sys.argv[3]
        vmmsrc = ''
    elif (len(sys.argv) == 5):
        ip = sys.argv[1]
        username = sys.argv[2]
        password = sys.argv[3]
        vmmsrc = sys.argv[4]
    else:
        print "usage: python getStaleObj.py Apic_ip username password vmmSrc*"
        print "*vmmSrc is optional. Its value can be 'avs'"
        exit(1)

    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    sys.stdout.flush()
    sys.stderr.flush()

    if staleCheck(ip, username, password,vmmsrc) == 0:
        print "failed"
        exit(1)

