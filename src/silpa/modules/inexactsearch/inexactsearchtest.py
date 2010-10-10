#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Approximate Search
# Copyright 2008 Santhosh Thottingal <santhosh.thottingal@gmail.com>
# http://www.smc.org.in
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# If you find any bugs or have any suggestions email: santhosh.thottingal@gmail.com
# URL: http://www.smc.org.in


import sys
import re

class ApproximateSearch():
	
	def syllabalize_ml(self, text):
		signs = [
		u'\u0d02', u'\u0d03', u'\u0d3e', u'\u0d3f', u'\u0d40', u'\u0d41',
		u'\u0d42', u'\u0d43', u'\u0d44', u'\u0d46', u'\u0d47', u'\u0d48',
		u'\u0d4a', u'\u0d4b', u'\u0d4c', u'\u0d4d']
		limiters = ['.','\"','\'','`','!',';',',','?']

		chandrakkala = u'\u0d4d'
		lst_chars = []
		for char in text:
			if char in limiters:
				lst_chars.append(char)
			elif char in signs:
				lst_chars[-1] = lst_chars[-1] + char
			else:
				try:
					if lst_chars[-1][-1] == chandrakkala:
						lst_chars[-1] = lst_chars[-1] + char
					else:
						lst_chars.append(char)
				except IndexError:
					lst_chars.append(char)

		return lst_chars


	def bigram_search(self, str1, str2, syllable_search=False):
		"""Return approximate string comparator measure (between 0.0 and 1.0)
		using bigrams.
		USAGE:
		score = bigram(str1, str2)

		ARGUMENTS:
		str1  The first string
		str2  The second string

		DESCRIPTION:
		Bigrams are two-character sub-strings contained in a string. For example,
		'peter' contains the bigrams: pe,et,te,er.

		This routine counts the number of common bigrams and divides by the
		average number of bigrams. The resulting number is returned.
		"""

		# Quick check if the strings are the same - - - - - - - - - - - - - - - - - -
		#
		if (str1 == str2):
			result_string = "<div  style='float: left; background-color: green;' title=\"  Bigram comparator : string1: %s, string2: %s. Exact Match found" % (str1, str2)
			result_string = result_string + "\">"+str1+ "</div>"
			return 	result_string

		bigr1 = []
		bigr2 = []

		# Make a list of bigrams for both strings - - - - - - - - - - - - - - - - - -
		#
		if(syllable_search):
			str1_syllables = self. syllabalize_ml(str1)
			str2_syllables = self. syllabalize_ml(str2)
			for i in range(1,len(str1_syllables)):
				bigr1.append(str1_syllables[i-1:i+1])
			for i in range(1,len(str2_syllables)):
				bigr2.append(str2_syllables[i-1:i+1])
		else:	
			for i in range(1,len(str1)):
				bigr1.append(str1[i-1:i+1])
			for i in range(1,len(str2)):
				bigr2.append(str2[i-1:i+1])

		# Compute average number of bigrams - - - - - - - - - - - - - - - - - - - - -
		#
		average = (len(bigr1)+len(bigr2)) / 2.0
		if (average == 0.0):
			return str1

		# Get common bigrams  - - - - - - - - - - - - - - - - - - - - - - - - - - - -
		#
		common = 0.0

		if (len(bigr1) < len(bigr2)):  # Count using the shorter bigram list
			short_bigr = bigr1
			long_bigr  = bigr2
		else:
			short_bigr = bigr2
			long_bigr  = bigr1

		for b in short_bigr:
			if (b in long_bigr):
				if long_bigr.index(b) == short_bigr.index(b) :
					common += 1.0
				else:
					dislocation=(long_bigr.index(b) - short_bigr.index(b))/ average
					if dislocation < 0 :
						dislocation = dislocation * -1
					common += 1.0 - dislocation
				long_bigr[long_bigr.index(b)] = []  # Mark this bigram as counted

		w = common / average
		print common, average
		return w

if __name__ == "__main__":
	appx_search=ApproximateSearch()
	print appx_search.bigram_search(u"ആന",u"ആനയ്ക്കു്")
	print appx_search.bigram_search(u"ആന",u"ആനയ്ക്കു്", True)
	print appx_search.bigram_search(u"പാല",u"പാലക്കാട്", True)
	print appx_search.bigram_search(u"പാലക്കാട്",u"പാലക്കാട്ടെ", True)
	print appx_search.bigram_search(u"തലവര",u"വരതല", True)
