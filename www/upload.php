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

$existingFiles = glob('saved-bds/*.xml');
$target_dir = "saved-bds/";
$target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);
$uploadOk = 1;


$nameOk = false;
$suffix = 1;
$new_xml = simplexml_load_file($_FILES["fileToUpload"]["tmp_name"])
                                or die("There was an error uploading your file");

while (!$nameOk) {
    $nameOk = true;
    foreach ($existingFiles as $file) {
        $xml=simplexml_load_file($file);
        if (trim($new_xml->designName) == trim($xml->designName)) {
            if ($suffix == 1) {
                $new_xml->designName = $new_xml->designName.'_'.$suffix;
            } else {
                $new_xml->designName = substr($new_xml->designName, 0, -1).$suffix;
            }
            $nameOk = false;
            $suffix++;
            break;
        }
    }
}

$newFileName = str_replace(" ", "_", $new_xml->designName);
$newFileName = str_replace(".", "_", $newFileName);

if (!in_array($newFileName, $existingFiles)) {
    file_put_contents($target_dir.$newFileName.".xml", $new_xml->asXml());
    echo "Your design has been uploaded with the name " . $newFileName . ".";
} else {
    echo "Sorry, there was an issue with the name of your file.";
}

?>
