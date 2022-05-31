
ms_1 :: MultiSocket(127.0.0.1, 15641, 127.0.0.1, 8080)
    -> Queue(10000)
    -> Unstrip(2)
    -> StoreData(0, 00)
    -> [0]switch :: SimpleRoundRobinSched();


ms_2 :: MultiSocket(127.0.0.1, 15640, 127.0.0.1, 8081)
    -> Queue(10000)
    -> Unstrip(2)
    -> StoreData(0, 01)
    -> [1]switch;

switch -> link_1 :: BandwidthRatedUnqueue(128000, BURST_BYTES 250)
    -> classifier :: Classifier(0/3030, -)

classifier[0] -> Strip(2) -> ms_1
classifier[1] -> Strip(2) -> ms_2

ControlSocket("TCP", 7777);
