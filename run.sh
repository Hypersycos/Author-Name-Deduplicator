#!/usr/bin/env bash
python3 main.py authorlist distance -d 3 -f "$1" -o thesaurus.txt
python3 main.py authorlist distance -d 3 -f "$1" -a -o thesaurus_alphabetical.txt