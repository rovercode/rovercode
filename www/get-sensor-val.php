<?php

  $objRedis = new Redis();
  $objRedis->connect( "localhost" );

  /* Pass straight through to motor command queue */
  $objRedis -> rPush('commandQueue', json_encode($_POST));

  $done = false;
  while
  $value = $objRedis->blpop('replyQueue', 10);
  echo $value;
  ob_flush();
  flush();
?>
