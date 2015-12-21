<?php
$bds = glob('saved-bds/*.xml');

foreach($bds as $bd) {
	$xml=simplexml_load_file($bd) or die("Error: Bad BD xml file.");
	if ((string)$xml->designName == $_GET["designName"])
	{
		echo (string)$xml->bd;
		break;
	}
}



?>
