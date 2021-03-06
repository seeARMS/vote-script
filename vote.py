import StringIO
import socket
import urllib
import pycurl
import json
import string
import random


import socks 
import stem.process
from stem.control import Controller

from stem.util import term

SOCKS_PORT = 7000

# Set socks proxy and wrap the urllib module

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', SOCKS_PORT)
socket.socket = socks.socksocket

# Perform DNS resolution through the socket

def getaddrinfo(*args):
  return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]


socket.getaddrinfo = getaddrinfo

def token_gen(size=32, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
   return ''.join(random.choice(chars) for _ in range(size))


def query(url):
  """
  Uses pycurl to fetch a site using the proxy on the SOCKS_PORT.
  """

  output = StringIO.StringIO()

  data = json.dumps({"token": token_gen(), "voteTag": "vote"})
  headers = ['Accept: application/json', 
			 'Host: www.smarttechchallenge.ca',
			 'Origin': 'http://www.smarttechchallenge.ca',
			 'Referer': 'http://www.smarttechchallenge.ca/entry/7879601',
			 'User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36']
			 
  
  
  query = pycurl.Curl()
  query.setopt(pycurl.URL, url)
  query.setopt(pycurl.PROXY, 'localhost')
  query.setopt(pycurl.PROXYPORT, SOCKS_PORT)
  query.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5)
  query.setopt(pycurl.HTTPHEADER, headers)
  query.setopt(pycurl.WRITEFUNCTION, output.write)
  query.setopt(pycurl.POST, 1)
  query.setopt(pycurl.POSTFIELDS, data)

  try:
	for (i in range(0,10):
		query.perform()
    return output.getvalue()
  except pycurl.error as exc:
    return "Unable to reach %s (%s)" % (url, exc)

# Start an instance of Tor, and print Tor's bootstrap info as it starts

def print_bootstrap_lines(line):
  if "Bootstrapped " in line:
    print term.format(line, term.Color.BLUE)


print term.format("Starting Tor:\n", term.Attr.BOLD)

tor_process = stem.process.launch_tor_with_config(
  config = {
    'SocksPort': str(SOCKS_PORT)
  },
  init_msg_handler = print_bootstrap_lines,
)

print term.format("\nChecking our endpoint:\n", term.Attr.BOLD)
	print term.format(query("http://www.smarttechchallenge.ca/js/vote/7879601/1"),term.Color.BLUE)

tor_process.kill()  # stops tor
