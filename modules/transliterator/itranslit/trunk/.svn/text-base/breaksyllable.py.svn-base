from asci2dv import *
from main import *
vowels = ['a','i','e','o','u']
cons =['b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','w','x','y','z']

def submit(s):
	if asctodv.has_key(s.lower()):
		fout.write(asctodv[s.lower()])
#	else:
#		TranslateName(s.lower())
def submit_matra(s):
	if asctomatra.has_key(s.lower()):
		fout.write(asctomatra[s.lower()])
#	else:
		asctomatra.has_key(s[0].lower())
#		TranslateName(s[1:].lower())


def breakSyllable(syll):
	for i in range( len(syll) ):
		if (syll[i] in cons):
			continue
		else:
			break
	if (i==0):
		print 'no cons part', syll
#		submit(syll)
	else:
#		submit(syll[:i])
		print '\nelse sumit', syll[:i]
#		submit_matra(syll[i:])
		print '\nVowel', syll[i:]
		me = syll[i:]
		print '\n me', me
		print '\n me[0]', me[0]
		print '\n me[1:]', me[1:]
		
 
if __name__ == "__main__":
	ipstr = 'prai'
        breakSyllable(ipstr)
#	fout = open('break_syllable_result', 'wb')
