import re

fh = open("ip.txt", 'r')
ip = {}
count = 1
for line in fh.readlines():
	print line
	op = re.findall("\d+\.\d+\.\d+\.\d+",line)
	for each_ip in op:
	  if each_ip not in ip:
	    ip[each_ip] = count
	  else:
	    ip[each_ip] += count
	
print ip
result = []
print ip.items()

ap = sorted(ip.items(), key=check1,reverse=True)
print "first big ip :", ap[0][0], ap[0][1]
print "second big ip :", ap[1][0], ap[2][1]
print "third big ip :", ap[2][0], ap[2][1]


fh.close()


