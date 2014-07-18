import json
import httplib
import siphash
import urllib
import inspect
import os

SGRAPH_HOSTNAME = "sgraph.umbrella.com"
SGRAPH_CERTIFICATE = "umbrella-api.pem"

class SecurityGraphException(Exception):
    """Generic security graph exception"""
    def __init__(self, msg):
        Exception.__init__(self, msg)
        self.msg = msg

    def __str__(self):
        return repr(self.msg)

class SecurityGraph(object):

    def __init__(self, hostname=SGRAPH_HOSTNAME, certificate=SGRAPH_CERTIFICATE, verbose=True):
        self.hostname = hostname
        self.certificate = certificate
        self.connection = None
        self.verbose = verbose

    def log(self, line):
        if self.verbose:
            print("[SGraph] " + line)

    def connect(self):
        self.log("Connecting to " + self.hostname + " ...")
        try:
            current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
            self.connection = httplib.HTTPSConnection(self.hostname, cert_file=current_dir + "/" + self.certificate)
        except:
            print("[SGraph] Error: Exception during connection !")
            return

    def request(self, url):
        try:
            self.log(url)
            if self.connection == None:
                self.connect()
            self.connection.request("GET", url)
            response = self.connection.getresponse()
            self.log(str(response.status) + "\t" + response.reason)
            return json.loads(response.read())
        except:
            return None

    def request_post(self, url, data):
        try:
            headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "*/*", "X-Requested-With" : "XMLHttpRequest"}
            self.log(url)
            if self.connection == None:
                self.connection = httplib.HTTPSConnection(self.hostname, cert_file=self.certificate)
            self.connection.request("POST", url, data, headers)
            response = self.connection.getresponse()
            self.log(str(response.status) + "\t" + response.reason)
            return json.loads(response.read())
        except:
            return None
        
    def score(self, domain):
        return self.request("/label/rface-gbt/name/" + domain + ".json")

    def cooccurrences(self, domain):
        return self.request("/recommendations/name/" + domain + ".json")
    
    def related_domains(self, domain):
        return self.request("/links/name/" + domain + ".json")

    def dnsdb(self, domain):
        return self.request("/dnsdb/name/a/" + domain + ".json")

    def infected(self, urls):
        urls_json = json.dumps(urls);
        hash = siphash.SipHash_2_4('Umbrella/OpenDNS', urls_json).hash()
        digest = "{:x}".format(hash)
        sgraph_url = "/infected/names/" + urllib.quote(digest) + ".json"
        return self.request_post(sgraph_url, urls_json)

    def dnsdb_ip(self, ip):
        return self.request("/dnsdb/ip/a/" + ip + ".json")

    def security(self, domain):
        return self.request("/security/name/" + domain + ".json")

    def whois(self, domain):
        return self.request("/whois/name/" + domain + ".json")

    def as_for_ip(self, ip):
        return self.request("/bgp_routes/ip/" + ip + "/as_for_ip.json")

    def traffic(self, url, start_date, stop_date):
        start = start_date.replace("/", "%2F")
        stop = stop_date.replace("/", "%2F")
        return self.request("/appserver/?v=1&function=domain2-system&domains=" + url + "&locations=&start=" + start + "&stop=" + stop)

if __name__ == "__main__":
    print("Please import the sgraph module !")
