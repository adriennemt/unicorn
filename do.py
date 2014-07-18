#!/usr/bin/env python

import sys
import pprint
from datetime import datetime 
import json
import os

sys.path.append('./sgraph-api')
import sgraph

if not os.path.isdir("results"):
	print ("Creating result directory")
	os.mkdir("results")

domains = list()

print ("Reading monitor file")
with open('monitor.txt','rU') as f:
	lines = f.readlines()
	
	for line in lines:
		domain = line.strip()
		
		if len(domain) == 0:
			continue
		domains.append(domain)
print (domains)


sg = sgraph.SecurityGraph(verbose=False)

timestamp = datetime.now().strftime('%Y%m%d-%H%M')

print ("Requesting domain IPs")
for domain in domains:
	print(domain)
	data = sg.dnsdb(domain)
	
	if "rrs_tf" not in data:
		continue
	rrs_tf = data["rrs_tf"]
	
	if len(rrs_tf) == 0:
		continue
	rrs_first = rrs_tf[0]

	if "rrs" not in rrs_first:
		continue
	rrs = rrs_first["rrs"]

	with open("results/" + domain + "-" + timestamp + ".txt", "w") as f:
		for rr in rrs:
			if "type" in rr and rr["type"] == "A":

				ip = rr["rr"]

				pprint.pprint(ip)
				#pprint.pprint(rr)
				f.write (ip + "\n")


#next step is to make the file generation happen automatically (set a cronjob)








	