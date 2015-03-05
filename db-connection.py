#!/usr/bin/python

import subprocess as sub
import sys
import argparse
import json
import re

def laravelGatherInfo(path):
	php_parse  = 'php -r "print json_encode(require \''+path+'\');"'

	proc = sub.Popen(php_parse, shell=True, stdout=sub.PIPE)
	php_json_config = proc.stdout.read()
	json_config = json.loads( php_json_config )

	default_db = json_config['default']
	
	connection 	= json_config['connections']['mysql']
	host	 	= connection['host']
	db 			= connection['database']
	user 		= connection['username']
	password	= connection['password']
	
	return {'dbname':default_db, 'host':host, 'database':db, 'user':user, 'password':password};

def wordpressGatherInfo(file):
	data = None
	fileContents = file.read()
	regexDbHost = "(//)?define\('DB_HOST',\s?'([a-zA-Z0-9_@./-]+)'\)"
	regexDbName = "(//)?define\('DB_NAME',\s?'([a-zA-Z-1_@-]+)'\)"
	regexDbUser = "(//)?define\('DB_USER',\s?'([a-zA-Z0-9_@-]+)'\)"
	regexDbPass = "(//)?define\('DB_PASSWORD',\s?'([a-zA-Z_0-9@-]+)'\)"
	
	host 		= wordpressExtractVarInfo( re.findall(regexDbHost, fileContents) )
	db 		= wordpressExtractVarInfo( re.findall(regexDbName, fileContents) )
	user 	= wordpressExtractVarInfo( re.findall(regexDbUser, fileContents) )
	pswd 	= wordpressExtractVarInfo( re.findall(regexDbPass, fileContents) )
	
	if host or db or user or pswd :
		data = {'dbname':'mysql', 'host':host, 'database':db, 'user':user, 'password':pswd};
	
	return data;
	
def wordpressExtractVarInfo(regexResult):
	varValue = None
	for row in regexResult :
		if row[0]=='' :
			varValue = row[1]
			
	return varValue


dbdata = None	
connection_comand = None
available = ['mysql']
parser = argparse.ArgumentParser(description='Connect to a Laravel or Wordpress database using its configuration file')
parser.add_argument('--file', '-f', action='store', nargs='?', type=argparse.FileType('r'), required=True, help='the configuration file')
parser.add_argument('--laravel', action='store_true', default=True, help='if its a Laravel configuration file')
parser.add_argument('--wordpress', action='store_true', default=False, help='if its a Wordpress configuration file')
parser.add_argument('--dump', '-d', action='store', default=False, type=argparse.FileType('w'), help='dump the database to the especified file')
parser.add_argument('--send', '-s', action='store', default=False, type=argparse.FileType('r'), help='import especified file to the database')
args = parser.parse_args()


if args.wordpress :
	dbdata = wordpressGatherInfo( args.file )
elif args.laravel :
	dbdata = laravelGatherInfo( args.file.name )


if dbdata == None :
	print 'An error ocurred: Could not define database info'
	sys.exit()

if not (dbdata['dbname'] in available) :
	print dbdata['dbname']+' is not supported yet'
	sys.exit()

if dbdata['dbname']=='mysql' :
	cmd = dbdata['dbname']
	
	if args.dump :
		cmd = 'mysqldump'
	
	connection_comand = [cmd, '-h'+dbdata['host'], '-u'+dbdata['user'], '-p'+dbdata['password'], dbdata['database']]
	
if not connection_comand==None :
	sub.call(connection_comand, stdout=args.dump, stdin=args.send)
