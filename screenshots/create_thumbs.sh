#!/bin/bash
# Ordner "thumbs" anlegen
mkdir -p thumbs

# Bilder in Thumbnails konvertieren
for img in *.png
do
 convert "$img" -resize 150x150 "thumbs/$img"
done
