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

$bds = glob('saved-bds/*.xml');

$names = [];

foreach ($bds as $bd) {
  try {
    $xml=simplexml_load_file($bd);
    if($xml) {
      $names[] = (string)$xml->designName;
    }
  } catch (Exception $e) {
    error_log("Error reading file name", 0)  ;
  }
}
echo json_encode(array_values($names));

?>
