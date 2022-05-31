
ms_1 :: MultiSocket(127.0.0.1, 15641, 127.0.0.1, 8080)
    -> Queue(10000)
    -> link_1 :: BandwidthRatedUnqueue(128000, BURST_BYTES 250)
    -> ms_1

ms_2 :: MultiSocket(127.0.0.1, 15640, 127.0.0.1, 8081)
    -> Queue(10000)
    -> link_2 :: BandwidthRatedUnqueue(128000, BURST_BYTES 250)
    -> ms_2

ControlSocket("TCP", 7777);
