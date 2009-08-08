lang_codes={'en_US':0,'hi_IN': 0x0901,'bn_IN': 0x0981, 'pa_IN':0x0A01,'gu_IN':0x0A81 , 'or_IN': 0x0B01,'ta_IN': 0x0B81,'te_IN' : 0x0C01,	'ka_IN' :0x0C81	,'ml_IN': 0x0D01}
lang_bases= [0x0901,0x0981,0x0A01,0x0A81 ,  0x0B01,0x0B81,0x0C01, 0x0C81	, 0x0D01]
for lang in lang_bases:
	print	"[",
	for i in range(0,127):
		print "\""+unichr(lang+ i).encode("utf-8")+"\",",
	print	"]"
			
