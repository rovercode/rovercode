<?php
header('Content-Type: text/event-stream;charset=UTF-8');
header('Cache-Control: no-cache');
header("Connection: keep-alive");

while(true) {
	$time = date('r');
	echo "data: Rover is alive. The server time is: {$time}\n\n";
	ob_flush();
	flush();
	sleep(30);
}
?>
