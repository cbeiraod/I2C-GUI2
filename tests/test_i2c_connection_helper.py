# -*- coding: utf-8 -*-
#############################################################################
# zlib License
#
# (C) 2024 Cristóvão Beirão da Cruz e Silva <cbeiraod@cern.ch>
#
# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the authors be held liable for any damages
# arising from the use of this software.
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
#
# 1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.
#############################################################################

import logging
import random
from math import ceil
from unittest.mock import call
from unittest.mock import patch

import pytest

from i2c_gui2.functions import bytes_to_word_list
from i2c_gui2.functions import word_list_to_bytes
from i2c_gui2.i2c_connection_helper import I2C_Connection_Helper
from i2c_gui2.i2c_messages import I2CMessages


@pytest.fixture
def i2c_ch_max_seq_byte():
    yield 8


@pytest.fixture
def i2c_ch_i2c_delay():
    yield 1000


@pytest.fixture
def i2c_ch_no_connect():
    yield True


@pytest.fixture
def i2c_ch_test(i2c_ch_max_seq_byte, i2c_ch_i2c_delay, i2c_ch_no_connect):
    yield I2C_Connection_Helper(
        max_seq_byte=i2c_ch_max_seq_byte,
        successive_i2c_delay_us=i2c_ch_i2c_delay,
        no_connect=i2c_ch_no_connect,
    )


def test_init(i2c_ch_test):
    assert not i2c_ch_test._is_connected
    assert isinstance(i2c_ch_test._logger, logging.Logger)


def test_max_seq_byte(i2c_ch_max_seq_byte, i2c_ch_test):
    assert i2c_ch_max_seq_byte == i2c_ch_test._max_seq_byte


def test_i2c_delay(i2c_ch_i2c_delay, i2c_ch_test):
    assert i2c_ch_i2c_delay == i2c_ch_test._successive_i2c_delay_us


def test_no_connect(i2c_ch_no_connect, i2c_ch_test):
    assert i2c_ch_no_connect == i2c_ch_test._no_connect


def test_logger(caplog, i2c_ch_test):
    assert isinstance(i2c_ch_test.logger, logging.Logger)
    assert i2c_ch_test.logger == i2c_ch_test._logger

    caplog.set_level(logging.DEBUG, "I2C_Log")
    i2c_ch_test.logger.info("Test Debug")

    log_tuples = caplog.record_tuples
    assert len(log_tuples) == 1
    assert log_tuples[0][0] == "I2C_Log"
    assert log_tuples[0][1] == logging.INFO
    assert log_tuples[0][2] == "Test Debug"


def test_connected(i2c_ch_test):
    assert not i2c_ch_test.connected


def test_not_implemented_check_i2c_devices(i2c_ch_test):
    with pytest.raises(Exception) as e_info:
        i2c_ch_test._check_i2c_device(0x21)
    assert e_info.match(r"^Derived classes must implement the individual device access methods:")


def test_not_implemented_write_i2c_device_memory(i2c_ch_test):
    with pytest.raises(Exception) as e_info:
        i2c_ch_test._write_i2c_device_memory(0x21, 10, [1, 2])
    assert e_info.match(r"^Derived classes must implement the individual device access methods:")


def test_not_implemented_read_i2c_device_memory(i2c_ch_test):
    with pytest.raises(Exception) as e_info:
        i2c_ch_test._read_i2c_device_memory(0x21, 10, 5)
    assert e_info.match(r"^Derived classes must implement the individual device access methods:")


def test_not_implemented_direct_i2c(i2c_ch_test):
    with pytest.raises(Exception) as e_info:
        i2c_ch_test._direct_i2c([I2CMessages.START, I2CMessages.STOP])
    assert e_info.match(r"^Derived classes must implement the individual device access methods:")


@pytest.fixture()
def connect_return_value():
    yield None


@pytest.fixture()
def fake_connect(monkeypatch, connect_return_value):
    def replace():
        return connect_return_value

    monkeypatch.setattr(I2C_Connection_Helper, "_check_i2c_device", lambda *args, **kwargs: replace())


@pytest.mark.parametrize('connect_return_value', [True, False])
def test_fake_connect_monkeypatch(connect_return_value, fake_connect, i2c_ch_test):
    assert i2c_ch_test._check_i2c_device(0x21) == connect_return_value


@pytest.mark.parametrize('i2c_ch_no_connect', [True, False])
@pytest.mark.parametrize('connect_return_value', [True, False])
def test_check_i2c_device(caplog, connect_return_value, fake_connect, i2c_ch_no_connect, i2c_ch_test):
    caplog.set_level(logging.DEBUG, "I2C_Log")

    assert i2c_ch_test._check_i2c_device(0x21) == connect_return_value  # Sanity check the monkeypatching works

    i2c_ch_test._is_connected = not i2c_ch_no_connect

    found = i2c_ch_test.check_i2c_device(0x21)

    if i2c_ch_no_connect:
        assert not found
    else:
        if connect_return_value is False:
            assert not found
        else:
            assert found

    log_tuples = caplog.record_tuples
    assert len(log_tuples) == 2
    assert log_tuples[0][0] == "I2C_Log"
    assert log_tuples[1][0] == "I2C_Log"
    assert log_tuples[0][1] == logging.INFO
    assert log_tuples[1][1] == logging.INFO
    # assert log_tuples[0][2] == "Test Debug"


def test_read_device_memory_not_connected(i2c_ch_test):
    with pytest.raises(Exception) as e_info:
        i2c_ch_test.read_device_memory(0x21, 0x00, 1)
    assert e_info.match(r"^You must first connect to a device before trying to read registers from it")


def test_write_device_memory_not_connected(i2c_ch_test):
    with pytest.raises(Exception) as e_info:
        i2c_ch_test.write_device_memory(0x21, 0x00, [0x54])
    assert e_info.match(r"^You must first connect to a device before trying to write registers to it")


def test_read_device_memory_invalid_device_address(i2c_ch_test):
    i2c_ch_test._is_connected = True
    with pytest.raises(Exception) as e_info:
        i2c_ch_test.read_device_memory(0x80, 0x00, 1)
    assert e_info.match(r"^Invalid I2C address received: 0x80")


def test_write_device_memory_invalid_device_address(i2c_ch_test):
    i2c_ch_test._is_connected = True
    with pytest.raises(Exception) as e_info:
        i2c_ch_test.write_device_memory(0x80, 0x00, [0x54])
    assert e_info.match(r"^Invalid I2C address received: 0x80")


def test_read_device_memory_invalid_address_endianness(i2c_ch_test):
    i2c_ch_test._is_connected = True
    with pytest.raises(Exception) as e_info:
        i2c_ch_test.read_device_memory(0x21, 0x00, 1, address_endianness='blabla')
    assert e_info.match(r"^A wrong address endianness was set: blabla")


def test_write_device_memory_invalid_address_endianness(i2c_ch_test):
    i2c_ch_test._is_connected = True
    with pytest.raises(Exception) as e_info:
        i2c_ch_test.write_device_memory(0x21, 0x00, [0x54], address_endianness='blabla')
    assert e_info.match(r"^A wrong address endianness was set: blabla")


def test_read_device_memory_invalid_word_endianness(i2c_ch_test):
    i2c_ch_test._is_connected = True
    with pytest.raises(Exception) as e_info:
        i2c_ch_test.read_device_memory(0x21, 0x00, 1, word_endianness='blabla')
    assert e_info.match(r"^A wrong word endianness was set: blabla")


def test_write_device_memory_invalid_word_endianness(i2c_ch_test):
    i2c_ch_test._is_connected = True
    with pytest.raises(Exception) as e_info:
        i2c_ch_test.write_device_memory(0x21, 0x00, [0x54], word_endianness='blabla')
    assert e_info.match(r"^A wrong word endianness was set: blabla")


def test_read_device_memory_invalid_read_type(i2c_ch_test):
    i2c_ch_test._is_connected = True
    with pytest.raises(Exception) as e_info:
        i2c_ch_test.read_device_memory(0x21, 0x00, 1, read_type='blabla')
    assert e_info.match(r"^A wrong read type was set: blabla")


def test_write_device_memory_invalid_read_type(i2c_ch_test):
    i2c_ch_test._is_connected = True
    with pytest.raises(Exception) as e_info:
        i2c_ch_test.write_device_memory(0x21, 0x00, 1, write_type='blabla')
    assert e_info.match(r"^A wrong write type was set: blabla")


@pytest.mark.parametrize('words', [1, 2, 4])
@pytest.mark.parametrize('bitlength', [8, 16])
@pytest.mark.parametrize('endianness', ['big', 'little'])
def test_read_device_memory_no_connect(caplog, i2c_ch_test, words, bitlength, endianness):
    caplog.set_level(logging.DEBUG, "I2C_Log")
    i2c_ch_test._is_connected = True

    word_list = i2c_ch_test.read_device_memory(0x21, 0x00, words, word_bitlength=bitlength, word_endianness=endianness)

    log_tuples = caplog.record_tuples
    assert len(log_tuples) == 2
    assert log_tuples[0][0] == "I2C_Log"
    assert log_tuples[1][0] == "I2C_Log"
    assert log_tuples[0][1] == logging.INFO
    assert log_tuples[1][1] == logging.DEBUG
    assert "Software emulation (no connect) is enabled, so returning dummy values:" in log_tuples[1][2]

    assert len(word_list) == words
    if words == 1:
        assert "Reading the register" in log_tuples[0][2]
        assert word_list[0] == 42
    else:
        assert "Reading a register block with size" in log_tuples[0][2]
        if bitlength == 8:
            for i in range(words):
                assert word_list[i] == i
        else:
            byte_list = [i for i in range(words * ceil(bitlength / 8))]
            compare_list = bytes_to_word_list(byte_list, ceil(bitlength / 8), endianness)
            assert word_list == compare_list


@pytest.mark.parametrize('words', [1, 2, 4])
@pytest.mark.parametrize('bitlength', [8, 16])
@pytest.mark.parametrize('endianness', ['big', 'little'])
def test_write_device_memory_no_connect(caplog, i2c_ch_test, words, bitlength, endianness):
    caplog.set_level(logging.DEBUG, "I2C_Log")
    i2c_ch_test._is_connected = True

    word_list = [i for i in range(words)]

    i2c_ch_test.write_device_memory(0x21, 0x00, word_list, word_bitlength=bitlength, word_endianness=endianness)

    log_tuples = caplog.record_tuples
    assert len(log_tuples) == 2
    assert log_tuples[0][0] == "I2C_Log"
    assert log_tuples[1][0] == "I2C_Log"
    assert log_tuples[0][1] == logging.INFO
    assert log_tuples[1][1] == logging.DEBUG
    assert log_tuples[1][2] == "Software emulation (no connect) is enabled, so no write action is taken."

    assert len(word_list) == words
    if words == 1:
        assert "Writing the value" in log_tuples[0][2]
    else:
        assert "Writing a register block with size" in log_tuples[0][2]


@pytest.mark.parametrize('i2c_ch_max_seq_byte', [None])
@pytest.mark.parametrize('i2c_ch_no_connect', [False])
@pytest.mark.parametrize('words', [1, 2])
@pytest.mark.parametrize('bitlength', [8, 16])
@pytest.mark.parametrize('endianness', ['big', 'little'])
def test_read_device_memory_no_max_seq_byte(caplog, i2c_ch_test, words, bitlength, endianness):
    caplog.set_level(logging.DEBUG, "I2C_Log")
    i2c_ch_test._is_connected = True

    with patch('i2c_gui2.i2c_connection_helper.I2C_Connection_Helper._read_i2c_device_memory') as function:
        ret_list = [random.getrandbits(8) for _ in range(words * ceil(bitlength / 8))]
        function.return_value = ret_list

        word_list = i2c_ch_test.read_device_memory(0x21, 0x00, words, word_bitlength=bitlength, word_endianness=endianness)

        function.assert_called_once()
        function.assert_has_calls([call(0x21, 0x00, words * ceil(bitlength / 8), read_type="Normal", address_bitlength=8)])

        log_tuples = caplog.record_tuples
        assert len(log_tuples) == 2
        assert log_tuples[0][0] == "I2C_Log"
        assert log_tuples[1][0] == "I2C_Log"
        assert log_tuples[0][1] == logging.INFO
        assert log_tuples[1][1] == logging.DEBUG
        assert "Got data:" in log_tuples[1][2]

        assert len(word_list) == words

        compare_list = bytes_to_word_list(ret_list, ceil(bitlength / 8), endianness)
        assert word_list == compare_list

        if words == 1:
            assert "Reading the register" in log_tuples[0][2]
        else:
            assert "Reading a register block with size" in log_tuples[0][2]


@pytest.mark.parametrize('i2c_ch_max_seq_byte', [None])
@pytest.mark.parametrize('i2c_ch_no_connect', [False])
@pytest.mark.parametrize('words', [1, 2])
@pytest.mark.parametrize('bitlength', [8, 16])
@pytest.mark.parametrize('endianness', ['big', 'little'])
def test_write_device_memory_no_max_seq_byte(caplog, i2c_ch_test, words, bitlength, endianness):
    caplog.set_level(logging.DEBUG, "I2C_Log")
    i2c_ch_test._is_connected = True

    word_list = [random.getrandbits(bitlength) for _ in range(words)]
    byte_list = word_list_to_bytes(word_list, ceil(bitlength / 8), endianness)

    with patch('i2c_gui2.i2c_connection_helper.I2C_Connection_Helper._write_i2c_device_memory') as function:
        i2c_ch_test.write_device_memory(0x21, 0x00, word_list, word_bitlength=bitlength, word_endianness=endianness)

        function.assert_called_once()
        function.assert_has_calls([call(0x21, 0x00, byte_list, write_type="Normal", address_bitlength=8)])

        log_tuples = caplog.record_tuples
        assert len(log_tuples) == 2
        assert log_tuples[0][0] == "I2C_Log"
        assert log_tuples[1][0] == "I2C_Log"
        assert log_tuples[0][1] == logging.INFO
        assert log_tuples[1][1] == logging.DEBUG
        assert log_tuples[1][2] == "Writing the full block at once."

        if words == 1:
            assert "Writing the value" in log_tuples[0][2]
        else:
            assert "Writing a register block with size" in log_tuples[0][2]


@pytest.mark.parametrize('i2c_ch_max_seq_byte', [1, 2, 8])
@pytest.mark.parametrize('i2c_ch_no_connect', [False])
@pytest.mark.parametrize('words', [1, 2, 8])
@pytest.mark.parametrize('bitlength', [8, 16])
@pytest.mark.parametrize('endianness', ['big', 'little'])
def test_read_device_memory(caplog, i2c_ch_test, words, bitlength, endianness, i2c_ch_max_seq_byte):
    caplog.set_level(logging.DEBUG, "I2C_Log")
    i2c_ch_test._is_connected = True

    with patch('i2c_gui2.i2c_connection_helper.I2C_Connection_Helper._read_i2c_device_memory') as function:
        ret_list = [random.getrandbits(8) for _ in range(min(words * ceil(bitlength / 8), i2c_ch_max_seq_byte))]
        function.return_value = ret_list

        if ceil(bitlength / 8) > i2c_ch_max_seq_byte:
            with pytest.raises(Exception) as e_info:
                word_list = i2c_ch_test.read_device_memory(0x21, 0x00, words, word_bitlength=bitlength, word_endianness=endianness)
            assert e_info.match(r"^The word length is too big for the maximum number of bytes")

            function.assert_not_called()
        else:
            word_list = i2c_ch_test.read_device_memory(0x21, 0x00, words, word_bitlength=bitlength, word_endianness=endianness)

            num_calls = ceil(words * ceil(bitlength / 8) / i2c_ch_max_seq_byte)
            addr_step = i2c_ch_max_seq_byte / (bitlength / 8)

            function.assert_has_calls(
                [
                    call(
                        0x21,
                        int(i * addr_step),
                        min(words * ceil(bitlength / 8), i2c_ch_max_seq_byte),
                        read_type="Normal",
                        address_bitlength=8,
                    )
                    for i in range(num_calls)
                ]
            )

            log_tuples = caplog.record_tuples
            assert len(log_tuples) == 2 * num_calls + 2
            for i in range(2 * num_calls + 2):
                assert log_tuples[i][0] == "I2C_Log"
                if i == 0:
                    assert log_tuples[i][1] == logging.INFO
                else:
                    assert log_tuples[i][1] == logging.DEBUG
                if i == 0:
                    continue
                elif i == 1:
                    assert f"Breaking the read into {num_calls}" in log_tuples[i][2]
                else:
                    if i % 2 == 0:
                        assert f"Read operation {int(i/2 - 1)}" in log_tuples[i][2]
                    else:
                        assert "Got data:" in log_tuples[i][2]

            assert len(word_list) == words

            compare_list = []
            for i in range(num_calls):
                compare_list += ret_list
            compare_list = bytes_to_word_list(compare_list, ceil(bitlength / 8), endianness)
            assert word_list == compare_list

            if words == 1:
                assert "Reading the register" in log_tuples[0][2]
            else:
                assert "Reading a register block with size" in log_tuples[0][2]


@pytest.mark.parametrize('i2c_ch_max_seq_byte', [1, 2, 8])
@pytest.mark.parametrize('i2c_ch_no_connect', [False])
@pytest.mark.parametrize('words', [1, 2, 8])
@pytest.mark.parametrize('bitlength', [8, 16])
@pytest.mark.parametrize('endianness', ['big', 'little'])
def test_write_device_memory(caplog, i2c_ch_test, words, bitlength, endianness, i2c_ch_max_seq_byte):
    caplog.set_level(logging.DEBUG, "I2C_Log")
    i2c_ch_test._is_connected = True

    word_list = [random.getrandbits(bitlength) for _ in range(words)]
    byte_list = word_list_to_bytes(word_list, ceil(bitlength / 8), endianness)

    with patch('i2c_gui2.i2c_connection_helper.I2C_Connection_Helper._write_i2c_device_memory') as function:

        if ceil(bitlength / 8) > i2c_ch_max_seq_byte:
            with pytest.raises(Exception) as e_info:
                i2c_ch_test.write_device_memory(0x21, 0x00, word_list, word_bitlength=bitlength, word_endianness=endianness)
            assert e_info.match(r"^The word length is too big for the maximum number of bytes")

            function.assert_not_called()
        else:
            i2c_ch_test.write_device_memory(0x21, 0x00, word_list, word_bitlength=bitlength, word_endianness=endianness)

            num_calls = ceil(words * ceil(bitlength / 8) / i2c_ch_max_seq_byte)
            addr_step = i2c_ch_max_seq_byte / (bitlength / 8)

            function.assert_has_calls(
                [
                    call(
                        0x21,
                        int(i * addr_step),
                        byte_list[
                            i * i2c_ch_max_seq_byte : i * i2c_ch_max_seq_byte + min(words * ceil(bitlength / 8), i2c_ch_max_seq_byte)
                        ],
                        write_type="Normal",
                        address_bitlength=8,
                    )
                    for i in range(num_calls)
                ]
            )

            log_tuples = caplog.record_tuples
            assert len(log_tuples) == 2 * num_calls + 2
            for i in range(2 * num_calls + 2):
                assert log_tuples[i][0] == "I2C_Log"
                if i == 0:
                    assert log_tuples[i][1] == logging.INFO
                else:
                    assert log_tuples[i][1] == logging.DEBUG
                if i == 0:
                    continue
                elif i == 1:
                    assert f"Breaking the write into {num_calls}" in log_tuples[i][2]
                else:
                    if i % 2 == 0:
                        assert f"Write operation {int(i/2 - 1)}" in log_tuples[i][2]
                    else:
                        assert "Current block:" in log_tuples[i][2]

            if words == 1:
                assert "Writing the value" in log_tuples[0][2]
            else:
                assert "Writing a register block with size" in log_tuples[0][2]
