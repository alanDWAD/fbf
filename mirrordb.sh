#!/bin/bash
BACKUP_DIR="${HOME}/Dropbox/Apps/DWAD Backup"
SQL=$(ls -t "$BACKUP_DIR"/*.gz.0|head -1)
cp "$SQL" dwad.sql.gz
gunzip dwad.sql.gz
echo "DROP DATABASE IF EXISTS dwad; CREATE DATABASE dwad CHARACTER SET utf8 COLLATE utf8_general_ci; USE dwad;" | cat - dwad.sql | mysql -u root -p
rm dwad.sql
