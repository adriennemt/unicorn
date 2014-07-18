import sgraph
import pprint
import datetime
import json

sg = sgraph.SecurityGraph()
pp = pprint.PrettyPrinter(indent = 4)

print("----- Example : Score")
data = sg.score("bibikun.ru")
pp.pprint(data)

print("----- Example : Co-occurrences")
data = sg.cooccurrences("www.test.com")
pp.pprint(data)

print("----- Example : Related Domains")
data = sg.related_domains("www.test.com")
pp.pprint(data)

print("----- Example : Traffic History")
today = datetime.date.today()
today_str = today.strftime("%Y/%m/%d/00")
data = sg.traffic("wikileaks.org", "2013/12/13/00", today_str)
pp.pprint(data)
with open('output.json', 'w') as outfile:
  json.dump(data, outfile)
