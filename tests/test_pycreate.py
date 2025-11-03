from pycreate2.OI import RESPONSE_SIZES, calc_query_data_len


def test_packet_id():
    packet_id = 100
    if packet_id in RESPONSE_SIZES:
        packet_size = RESPONSE_SIZES[packet_id]
        assert packet_size == 80
    else:
        assert False


def test_packet_length():
    pkts = [21, 22, 23, 24, 25]
    packet_len = calc_query_data_len(pkts)
    assert packet_len == 8
    pkts = [100]
    packet_len = calc_query_data_len(pkts)
    assert packet_len == 80
