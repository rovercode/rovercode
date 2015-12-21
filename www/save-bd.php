<?php
	$filename = str_replace(' ', '_',$_POST["designName"]);
	$filename = str_replace('.', '_',$filename);
	$fd = fopen("saved-bds/$filename".".xml", "w");
	$fileContents = array (
		$_POST["designName"] => 'designName',
		$_POST["bdString"] => 'bd',
	);
	$xml = new SimpleXMLElement('<root/>');
	array_walk_recursive($fileContents, array($xml, 'addChild'));
	fwrite($fd, $xml->asXML());
	echo "Your design has been saved to the Rover";
	fclose($fd);
?>
