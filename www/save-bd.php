<?php
/**
 * File Upload Handler
 * 
 * PHP version 5
 *
 * @category File_Io
 * @package  Rovercode
 * @author   Brady L. Hurlburt <bradyhurlburt@gmail.com>
 * @license  http://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html GPL v2
 * @link     https://github.com/aninternetof/rover-code
 */
$filename = str_replace(' ', '_', $_POST["designName"]);
$filename = str_replace('.', '_', $filename);
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
