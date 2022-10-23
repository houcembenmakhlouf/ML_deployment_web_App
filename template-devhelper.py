#!/usr/bin/python3

from optparse import OptionParser

import json

import datetime

import time

import fileinput

from urllib.parse import urlencode
import pycurl


DEVNULL = "/dev/null"

TEMPLATEHOST = "localhost"
TEMPLATEPORT = 10000
SENDRECORD = 0
HEADER = "application/json"
TIMESTEP = 86400

def getcmdline():
	"""
	Read command line arguments.
	"""
	usage = "usage: %prog [options] arg"
	p = OptionParser()
	p.add_option("--input", action = "store", dest = "input", help = ('Input filename [default: %s]'%(DEVNULL)), default = DEVNULL)	
	p.add_option("--serverhost", action = "store", dest = "serverhost", help = ('Server hostname or ip [default: %s]'%(TEMPLATEHOST)), default = TEMPLATEHOST)
	p.add_option("--serverport", action = "store", dest = "serverport", help = ('Server port [default: %s]'%(TEMPLATEPORT)), default = TEMPLATEPORT)
	p.add_option("--sendrecord", action = "store", dest = "sendrecord", help = ('Send record [default: %d ]'%(SENDRECORD)), default = SENDRECORD)
	p.add_option("--timestep", action = "store", dest = "timestep", help = ('Time step [default: %d]'%(TIMESTEP)), default = TIMESTEP)
	p.add_option("--log", action = "store", dest = "log", help = ('Log the processed files, discard input files found in this log [default: %s]'%(DEVNULL)), default = DEVNULL)

	(o, a) = p.parse_args()
	return o


def main():
	o = getcmdline()
	c = {}
	c['input'] = str(o.input)
	c['serverhost'] = str(o.serverhost)
	c['serverport'] = str(o.serverport)
	c['sendrecord'] = int(o.sendrecord)
	c['timestep'] = int(o.timestep)
	c['log'] = str(o.log)

	crl = pycurl.Curl()
	crl.setopt(crl.URL, 'http://' + c['serverhost'] + ':' + c['serverport'] + '/process')
	crl.setopt(pycurl.HTTPHEADER, ['Content-Type:application/json'])
	crl.setopt(pycurl.POST, 1)

	cnt = 0

	records = []
	
	for line in fileinput.input(c['input']):
		records.append(line)
	js = json.loads(records[c['sendrecord']])
	js['timestep'] = c['timestep']
	r = {'payload':js}
	crl.setopt(crl.POSTFIELDS, json.dumps(r))
	crl.perform()
	fileinput.close()


if __name__ == "__main__":
    main() 
