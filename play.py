#!/usr/bin/python3

import main
import sys

start=None
verb=None

if len(sys.argv)>0:
	if sys.argv.count('start')==1:
		start=True
	if sys.argv.count('nostart')==1:
		start=False
	if sys.argv.count('verbose')==1:
		verb=True
	if sys.argv.count('noverbose')==1:
		verb=False

main.play_human_gui(verb, start)
