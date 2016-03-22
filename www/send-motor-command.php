<?php

  $objRedis = new Redis();
  $objRedis->connect( "localhost" );

  /* Pass straight through to motor command queue */
  $objRedis -> rPush('motorQueue', json_encode($_POST));

  echo("made it through Redis php. success!");
?>
