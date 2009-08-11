# -*- coding: utf-8 -*-
from jsonrpc import ServiceProxy
from jsonrpc import JSONRPCException
from jsonrpc import ServiceHandler
import jsonrpc
handler=ServiceHandler("")
print handler.listMethods()
json=jsonrpc.dumps({"method":"system.listMethods",  "params":[''], 'id':''})
print handler.handleRequest(json)
json=jsonrpc.dumps({"method":"modules.Fortune.fortune_ml", "params":[u"ആന"], 'id':''})
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

