<?php

$bds = glob('saved-bds/*.xml');

$names = [];

foreach($bds as $bd) {
	$xml=simplexml_load_file($bd) or die("Error: Bad BD xml file.");
	$names[] = (string)$xml->designName;
}
echo json_encode(array_values($names));

?>
