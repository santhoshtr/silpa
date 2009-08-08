#!/usr/bin/python
# -*- coding: UTF-8 -*-

## trans.py - Contains the transliteration script for English to Indic Scripts
## Copyright (C) 2009 Red Hat, Inc.
## Copyright (C) 2009 Pravin Satpute <psatpute@redhat.com>

## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.


import sys
vowels = ['a','i','e','o','u']
cons =['b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','w','x','y','z']
from asci2dv import *
import main
#`:from olang import *
#from asci2dv import asctomatra

def ConsReplace(alphabet):
	if asctodv.has_key(alphabet):
		print asctodv[alphabet]
		fout.write(asctodv[alphabet])
		return asctodv[alphabet]
	else:
		print alphabet
		fout.write(alphabet)
		return alphabet

def MatraReplace(alphabet):
	if asctomatra.has_key(alphabet):
		print asctomatra[alphabet]
		fout.write(asctomatra[alphabet])
		return asctomatra[alphabet]
	else:
		print alphabet
		fout.write(alphabet)
		return alphabet


def checkprevious(prev, present, buffer):
	if ((prev in cons) & (present in cons)):
		buffer += '्'
		fout.write('्')
		buffer += ConsReplace(present)
	else:
		if ((prev in cons) & (present in vowels)):
			buffer += MatraReplace(present)
		else:
			buffer += ConsReplace(present)	

def submit(s):
	if asctodv.has_key(s.lower()):
		fout.write(asctodv[s.lower()])
	else:
		TranslateName(s.lower())

def submit_matra(s):
	if asctomatra.has_key(s.lower()):
		fout.write(asctomatra[s.lower()])
	else:
		if asctomatra.has_key(s[0].lower()):
			fout.write(asctomatra[s[0].lower()])
		else: 
			fout.write(s[0])
		print '\nasctomatra.has_key(s[0].lower())', s[0]
		TranslateName(s[1:].lower())
#		print '\nTranslateName(s[1:].lower())', s[1:]

def breakSyllable(syll):
	for i in range( len(syll) ):
		if (syll[i] in cons):
			continue
		else:
			break
	if (i==0):
		print 'no cons part'
		submit(syll)
	if ((i+1)==len(syll)):
		submit(syll[:(i+1)])		
	else:
		print '\nin Else', i
		submit(syll[:i])
		print '\nsubmit(syll[:i]', syll[:i]
		if (i != len(syll)):
			submit_matra(syll[i:])		
#		print '\nsubmit_matra(syll[i:])', syll[i:]
#	print '\nVowel', syll[i:]
	
def SyllableSplitting(ipstr):
	syllable = []
	for i in range( len(ipstr) ):
		if (len(syllable) == 0):
			syllable.append(ipstr[i])
		else:
			if syllable[len(syllable)-1] in cons:
				syllable.append(ipstr[i])
			else: 
				if ipstr[i] in cons:
					s = "".join(str(x) for x in syllable)
					print '\nsyllable', s
					if asctodv.has_key(s.lower()):
						fout.write(asctodv[s.lower()])
					else:
						breakSyllable(s.lower())


					list([syllable.pop() for z in xrange(len(syllable))])
					syllable.append(ipstr[i])
				else:
					syllable.append(ipstr[i])
	s = "".join(str(x) for x in syllable)
	print '\n last syllable', s
	if asctodv.has_key(s.lower()):
		fout.write(asctodv[s.lower()])
	else:
		breakSyllable(s.lower())

	

def TranslateName(ipstr):
#	global fout
#	fout = open(output, "wb")
	print "string tranlating name %s", ipstr

	buffer = ''
	if asctodv.has_key(ipstr):
		fout.write(asctodv[ipstr])
	else:
		for i in range( len(ipstr) ):
			print  i
			if (i==0):
	
				buffer += ConsReplace(ipstr[i])
				i= i+1
			else:
				checkprevious(ipstr[i-1] ,ipstr[i], buffer)
				i= i+1
#	fout.close
#	fout = open(output)
#	textbuffer = fout.read()
#	print buffer
#	print outfilename.readline()


def TranslateFile(filename, output, textbuffer, flag):
	global fout
	fout = open(output, "wb")
	if (flag==1):
		TranslateName(filename.lower())
	else:
		ipfile = open(filename)
		flines = ipfile.readlines()
		linecount = len(flines)
		for l in flines:
		  w = l.split()
		  for i in range( len(w)):
		  	print  w[i]
			fout.write(w[i])
			fout.write("\t")
			print w[i]
			if asctodv.has_key(w[i].lower()):
				fout.write(asctodv[w[i].lower()])
			else:
				SyllableSplitting(w[i].lower())
#		TranslateName(w[i].lower())
			fout.write("\n")
			i=1+1
		ipfile.close
	fout.close
	fout = open(output)
	textbuffer = fout.read()
#	print textbuffer
	fout.close
	

if __name__ == "__main__":
	name = sys.argv[1]
#	print ipstr.lower()
#	hello = gui.HelloWorld()
#	hello.main()
	outfilename = sys.argv[2]
	fout = open(outfilename, 'wb')
	TranslateFile(name)

#	SyllableSplitting(name)
#	TranslateName(name.lower(),fout)
	fout.close
#	choice = raw_input('do you want transliteration in other language: ')
#	scr_name = raw_input('please enter script: ')
#	if choice == 'y':
#		print 'proceed'
#		change_scr(outfilename, scr_name )
#	else:
#	    'end of program'
