#!/bin/sh
rsync --rsh="ssh" --delete-after --exclude=".*" -rz $1@dwad.org:/var/www/dwad-resources/ ./media
