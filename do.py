#!/usr/bin/env python

from urllib2 import Request, urlopen
import os, sys
import json
import pprint
from datetime import datetime 

token = os.getenv('INVESTIGATE_TOKEN', False)
headers = { 'Authorization': 'Bearer ' + token }

def dns_db(domain):
	request = Request('https://investigate.api.opendns.com/dnsdb/name/a/' + domain + '.json', headers=headers)
	response_body = urlopen(request).read()
	return json.loads(response_body)

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

timestamp = datetime.now().strftime('%Y%m%d-%H%M')

print ("Requesting domain IPs")
for domain in domains:
	print(domain)
	data = dns_db(domain)
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








	