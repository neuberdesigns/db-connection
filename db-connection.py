import subprocess as sub
import sys
import argparse
import json

parser = argparse.ArgumentParser(description='Connect to a laravel database using its configuration file')
parser.add_argument('-f', '--file', action='store', nargs='?', type=argparse.FileType('r'), required=True, help='the configuration file')
args = parser.parse_args()

# if the script don't need output.
#sub.call("php args.file.name")

# if you want output
php_parse  = 'php -r "print json_encode(require \''+args.file.name+'\');"'

proc = sub.Popen(php_parse, shell=True, stdout=sub.PIPE)
php_json_config = proc.stdout.read()
json_config = json.loads( php_json_config )

default_db = json_config['default']

if default_db != 'mysql' :
	print 'Default is not a MySQL database'
	sys.exit()

mysql_node = json_config['connections']['mysql']
host	 	= mysql_node['host']
db 			= mysql_node['database']
user 		= mysql_node['username']
password	= mysql_node['password']

mysql_cmd = ['mysql', '-h'+host, '-u'+user, '-p'+password, db]

sub.call(mysql_cmd)
