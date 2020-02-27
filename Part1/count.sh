#!/bin/bash

pdf2txt.py -o text.txt -t text $1
(grep -o -i the text.txt | wc -l | tr -d '[:space:]') > count.txt
