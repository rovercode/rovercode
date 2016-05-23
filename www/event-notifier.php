<?php
header('Content-Type: text/event-stream;charset=UTF-8');
header('Cache-Control: no-cache');
header("Connection: keep-alive");

$objRedis = new Redis();
$objRedis->connect( "localhost" );

while(true) {
	$event = $objRedis->lpop('eventQueue');
	if ($event) {
		echo "data: {$event}\n\n";
		ob_flush();
		flush();
	}
}
?>
