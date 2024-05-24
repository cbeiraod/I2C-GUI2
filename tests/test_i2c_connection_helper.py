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

import pytest

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
    assert e_info.match(r"^Derived classes must implement the individual device access functions:")


def test_not_implemented_write_i2c_device_memory(i2c_ch_test):
    with pytest.raises(Exception) as e_info:
        i2c_ch_test._write_i2c_device_memory(0x21, 10, [1, 2])
    assert e_info.match(r"^Derived classes must implement the individual device access functions:")


def test_not_implemented_read_i2c_device_memory(i2c_ch_test):
    with pytest.raises(Exception) as e_info:
        i2c_ch_test._read_i2c_device_memory(0x21, 10, 5)
    assert e_info.match(r"^Derived classes must implement the individual device access functions:")


def test_not_implemented_direct_i2c(i2c_ch_test):
    with pytest.raises(Exception) as e_info:
        i2c_ch_test._direct_i2c([I2CMessages.START, I2CMessages.STOP])
    assert e_info.match(r"^Derived classes must implement the individual device access functions:")


def test_not_implemented_validate_connection_params(i2c_ch_test):
    with pytest.raises(Exception) as e_info:
        i2c_ch_test.validate_connection_params()
    assert e_info.match(r"^Derived classes must implement validation of the connection parameters")


def test_not_implemented_connect(i2c_ch_test):
    with pytest.raises(Exception) as e_info:
        i2c_ch_test.connect()
    assert e_info.match(r"^Derived classes must implement the connect method")


def test_not_implemented_disconnect(i2c_ch_test):
    with pytest.raises(Exception) as e_info:
        i2c_ch_test.disconnect()
    assert e_info.match(r"^Derived classes must implement the disconnect method")


@pytest.fixture()
def return_value():
    yield None


@pytest.fixture()
def fake_connect(monkeypatch, return_value):
    def replace():
        return return_value

    monkeypatch.setattr(I2C_Connection_Helper, "_check_i2c_device", lambda *args, **kwargs: replace())


@pytest.mark.parametrize('i2c_ch_no_connect', [True, False])
@pytest.mark.parametrize('return_value', [True, False])
def test_check_i2c_device(caplog, return_value, fake_connect, i2c_ch_no_connect, i2c_ch_test):
    caplog.set_level(logging.DEBUG, "I2C_Log")

    assert i2c_ch_test._check_i2c_device(0x21) == return_value  # Sanity check the monkeypatching works

    i2c_ch_test._is_connected = not i2c_ch_no_connect

    found = i2c_ch_test.check_i2c_device(0x21)

    if i2c_ch_no_connect:
        assert not found
    else:
        if return_value is False:
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
