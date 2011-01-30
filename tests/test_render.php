<?php
define ('HOSTNAME', 'http://localhost:8080/JSONRPC');
$url = HOSTNAME;
// Open the Curl session
$session = curl_init($url);
// If it's a POST, put the POST data in the body
$postvars = '{"method": "modules.Render.render_text", "params": ["Your text goes here", "png", 100, 100], "id":"jsonrpc"}';
curl_setopt ($session, CURLOPT_POST, true);
curl_setopt ($session, CURLOPT_POSTFIELDS, $postvars);
// Don't return HTTP headers. Do return the contents of the call
curl_setopt($session, CURLOPT_HEADER, false);
curl_setopt($session, CURLOPT_RETURNTRANSFER, true);
// Make the call
$json = curl_exec($session);
// The web service returns json. Set the Content-Type appropriately
header("Content-Type: application/json");
echo $json;
$obj =  json_decode($json,false);
$result  =  $obj->{"result"};
echo $result;
curl_close($session);
?>
