# DB Connection
Connect to a Laravel or Wordpress database using its configuration file

## Laravel config file
Simply specify the database config file
```
db-connection.py path/to/laravel/app/config/database.php
```
## WordPress config file
```
db-connection.py path/to/wordpress/wp-config.php --wordpress
```
## Import
```
db-connection.py path/to/laravel/app/config/database.php -s path/to/my/file/to/import/input.sql
```
## Export
```
db-connection.py path/to/laravel/app/config/database.php -d path/to/my/file/to/export/output.sql
```

### Arguments
__--laravel__: _(default)_ If its a Laravel configuration file 

__--wordpress__: If its a Wordpress configuration file

__--dump__ or __-d__: Dump the database to the especified file

__--send__ or __-s__: Import especified file to the database
