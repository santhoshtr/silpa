# -*- coding: utf-8 -*-
import sys
sys.path.append("../")
from common import *
from jsonrpc import ServiceProxy
from jsonrpc import JSONRPCException
from jsonrpc import ServiceHandler
import jsonrpc
handler=ServiceHandler("")
print "ready"
mm = ModuleManager()
print mm.getModuleInstance("TTS")

print handler.listMethods()
json=jsonrpc.dumps({"method":"system.listMethods",  "params":[''], 'id':''})
print handler.handleRequest(json)
json=jsonrpc.dumps({"method":"modules.TTS.text_to_wave", "params":["hello"], 'id':''})
print handler.handleRequest(json)
json=jsonrpc.dumps({"method":"modules.Fortune.fortune_ml", "params":[u"ആന"], 'id':''})
print handler.handleRequest(json)
json=jsonrpc.dumps({"method":"modules.Hyphenator.hyphenate", "params":[u"ആനയാരാമോന്‍"], 'id':''})
print handler.handleRequest(json)
json=jsonrpc.dumps({"method":"modules.Hyphenator.hyphenate", "params":[u"hithukollaalo"], 'id':''})
print handler.handleRequest(json)
json=jsonrpc.dumps({"method":"modules.LangGuess.guessLanguage", "params":[u"ആന"], 'id':''})
print handler.handleRequest(json)
json=jsonrpc.dumps({"version":"1.1","method":"modules.Fortune.fortune_ml","id":2,"params":[""]})
print handler.handleRequest(json)
json=jsonrpc.dumps({"version":"1.1","method":"modules.Dictionary.getdef","id":2,"params":["word","freedict-eng-hin"]})
print handler.handleRequest(json)
json=jsonrpc.dumps({"version":"1.1","method":"modules.CharDetails.getdetails","id":2,"params":[u"c"]})
print handler.handleRequest(json)
json=jsonrpc.dumps({"version":"1.1","method":"modules.InexactSearch.compare","id":2,"params":[u"സന്തോഷ്", u"സന്തോഷിന്റെ"]})
print handler.handleRequest(json)
json=jsonrpc.dumps({"version":"1.1","method":"modules.InexactSearch.compare","id":2,"params":[u"സന്തോഷ്", u"ஸந்தௌஷ்"]})
print handler.handleRequest(json)
json=jsonrpc.dumps({"version":"1.1","method":"modules.InexactSearch.compare","id":2,"params":[u"weigt", u"and"]})
print handler.handleRequest(json)
json=jsonrpc.dumps({"version":"1.1","method":"modules.Calendar.convert","id":2,"params":[u"Gregorian", u"Saka", "1998", "01","01"]})
print handler.handleRequest(json)

