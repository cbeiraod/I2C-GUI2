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

# from unittest.mock import call
from unittest.mock import patch

import pytest

from i2c_gui2.chips.address_space_controller import Address_Space_Controller
from i2c_gui2.i2c_connection_helper import I2C_Connection_Helper


@pytest.fixture
def asc_name():
    yield "test_name"


@pytest.fixture
def asc_i2c_address():
    yield 0x21


@pytest.fixture
def asc_address_space_size():
    yield 10


@pytest.fixture
def asc_i2c_connection():
    with patch('i2c_gui2.i2c_connection_helper.I2C_Connection_Helper') as mock_class:
        yield mock_class


# @pytest.fixture(scope="function", params=[10, 20])
# def asc_address_space_size(request):
#    yield request.param


@pytest.fixture
def asc_test(asc_name, asc_i2c_address, asc_address_space_size, asc_i2c_connection, logger):
    conn = I2C_Connection_Helper(max_seq_byte=8, no_connect=True)
    yield Address_Space_Controller(
        name=asc_name,
        i2c_address=asc_i2c_address,
        address_space_size=asc_address_space_size,
        logger=logger,
        i2c_connection=conn,
    )


def test_init(asc_address_space_size, asc_test):
    assert asc_test._not_read
    for index in range(asc_address_space_size):
        assert asc_test._memory[index] is None


def test_init_name(asc_name, asc_test):
    assert asc_test._name == asc_name


def test_init_address(asc_i2c_address, asc_test):
    assert asc_test._i2c_address == asc_i2c_address


@pytest.mark.parametrize('asc_address_space_size', [10, 200])
def test_init_address_space_size(asc_address_space_size, asc_test):
    assert asc_test._address_space_size == asc_address_space_size
    assert len(asc_test._memory) == asc_address_space_size
    assert len(asc_test) == asc_address_space_size


def test_getitem_address(asc_test):
    assert asc_test[0] is None
    asc_test._memory[0] = 20
    assert asc_test[0] == 20
    asc_test._memory[0] = 10
    assert asc_test[0] == 10


def test_getitem_indexed(asc_test):
    asc_test._register_map["A/B"] = 5
    assert asc_test["A", "B"] is None
    asc_test._memory[5] = 20
    assert asc_test["A", "B"] == 20
    asc_test._memory[5] = 10
    assert asc_test["A", "B"] == 10


def test_setitem_address(asc_test):
    asc_test[0] = 20
    assert asc_test._memory[0] == 20
    asc_test[0] = 10
    assert asc_test._memory[0] == 10


def test_setitem_indexed(asc_test):
    asc_test._register_map["A/B"] = 5
    asc_test["A", "B"] = 20
    assert asc_test._memory[5] == 20
    asc_test["A", "B"] = 10
    assert asc_test._memory[5] == 10


def test_iter(asc_address_space_size, asc_test):
    tmp = []

    for index in range(asc_address_space_size):
        asc_test._memory[index] = index * 2

    for entry in asc_test:
        tmp.append(entry)

    for index in range(asc_address_space_size):
        assert tmp[index] == index * 2


def test_update_i2c_address_nochange(asc_i2c_address, asc_test):
    asc_test._not_read = False
    asc_test.update_i2c_address(asc_i2c_address)
    assert not asc_test._not_read
    assert asc_test._i2c_address == asc_i2c_address


def test_update_i2c_address_value(caplog, asc_name, asc_test):
    caplog.set_level(logging.DEBUG)

    asc_test._not_read = False
    asc_test.update_i2c_address(0x12)
    assert asc_test._not_read
    assert asc_test._i2c_address == 0x12

    log_tuples = caplog.record_tuples
    assert len(log_tuples) == 1
    assert log_tuples[0][0] == "Test_Logger"
    assert log_tuples[0][1] == logging.INFO
    assert asc_name in log_tuples[0][2]
    assert "0x12" in log_tuples[0][2]
    assert "Updated" in log_tuples[0][2]


def test_update_i2c_address_none(caplog, asc_name, asc_test):
    caplog.set_level(logging.DEBUG)

    asc_test._not_read = False
    asc_test.update_i2c_address(None)
    assert asc_test._not_read
    assert asc_test._i2c_address is None

    log_tuples = caplog.record_tuples
    assert len(log_tuples) == 1
    assert log_tuples[0][0] == "Test_Logger"
    assert log_tuples[0][1] == logging.INFO
    assert asc_name in log_tuples[0][2]
    assert "Reset" in log_tuples[0][2]
