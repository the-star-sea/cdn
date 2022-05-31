
ms :: MultiSocket(127.0.0.1, 15641, 127.0.0.1, 8080)
    -> Queue(10000)
    -> link_1 :: BandwidthRatedUnqueue(128000, BURST_BYTES 250)
    -> ms

ControlSocket("TCP", 7777);
