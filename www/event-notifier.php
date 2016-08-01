<?php
header('Content-Type: text/event-stream;charset=UTF-8');
header('Cache-Control: no-cache');
header("Connection: keep-alive");
set_time_limit(0);

$objRedis = new Redis();
$objRedis->connect( "localhost" );

$numStateEvents = $objRedis->llen('eventQueue');
for ($i = 0; $i < $numStateEvents; $i++) {
	$objRedis->lpop('eventQueue');
}

while(true) {
	$event = $objRedis->lpop('eventQueue');
	if ($event) {
		echo "data: {$event}\n\n";
		ob_flush();
		flush();
	}
}
?>
