<?php

  $objRedis = new Redis();
  $objRedis->connect( "localhost" );

  /* Pass straight through to motor command queue */
  $objRedis -> rPush('commandQueue', json_encode($_POST));
?>
