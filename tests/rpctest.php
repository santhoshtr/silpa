<?php
// PHP Proxy example for Silpa Web services. 
// Santhosh Thottingal 
// 05 Nov 2010
define ('HOSTNAME', 'http://silpa.smc.org.in/JSONRPC');

$url = HOSTNAME;

// Open the Curl session
$session = curl_init($url);
// If it's a POST, put the POST data in the body
$postvars = '{"method": "modules.Payyans.ASCII2Unicode", "params": ["hmÀjnI","karthika"], "id":"jsonrpc"}';
//$postvars = '{"method": "modules.Dictionary.getdef", "params": ["banana", "en-ml"], "id":"jsonrpc"}';
curl_setopt ($session, CURLOPT_POST, true);
curl_setopt ($session, CURLOPT_POSTFIELDS, $postvars);

// Don't return HTTP headers. Do return the contents of the call
curl_setopt($session, CURLOPT_HEADER, false);
curl_setopt($session, CURLOPT_RETURNTRANSFER, true);

// Make the call
$json = curl_exec($session);

// The web service returns XML. Set the Content-Type appropriately
header("Content-Type: application/json");
echo $json;
curl_close($session);

?>
