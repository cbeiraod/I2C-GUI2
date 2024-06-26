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


import pytest

from i2c_gui2.functions import address_to_phys
from i2c_gui2.functions import bytes_to_word_list
from i2c_gui2.functions import is_valid_hostname
from i2c_gui2.functions import is_valid_ip
from i2c_gui2.functions import swap_endian_16bit
from i2c_gui2.functions import swap_endian_32bit
from i2c_gui2.functions import valid_i2c_address
from i2c_gui2.functions import validate_hostname
from i2c_gui2.functions import word_list_to_bytes


def test_is_valid_hostname_localhost():
    assert is_valid_hostname("localhost")


def test_is_valid_hostname_google():
    assert is_valid_hostname("google.com")


def test_is_valid_hostname_google_rightdot():
    assert is_valid_hostname("google.com.")


def test_is_valid_hostname_numeric():
    assert not is_valid_hostname("12345.123")


def test_is_valid_hostname_name():
    assert not is_valid_hostname("name")


def test_is_valid_hostname_with_space():
    assert not is_valid_hostname("na me.com")
    assert not is_valid_hostname("name.c om")


def test_is_valid_hostname_too_long():
    assert not is_valid_hostname(
        "This is a very long string which should not be found to be a valid hostname but we should test it anyway just to be sure. The string really has to be very long indeed because the maximum length is 253 characters, so it is not as short as it initially sounds..."
    )


def test_is_valid_ip():
    assert is_valid_ip("192.168.1.0")


def test_is_valid_ip_notIP():
    assert not is_valid_ip("192.168.1.300")
    assert not is_valid_ip("192.168.1")


def test_validate_hostname():
    assert validate_hostname("google.com")
    assert validate_hostname("192.168.1.0")


def test_validate_hostname_notValid():
    assert not validate_hostname("192.188.2")


def test_swap_endian_16bit():
    assert swap_endian_16bit(0x1234) == 0x3412


def test_swap_endian_16bit_truncates():
    assert swap_endian_16bit(0x31234) == 0x3412


def test_swap_endian_32bit():
    assert swap_endian_32bit(0x12345678) == 0x78563412


def test_swap_endian_32bit_truncates():
    assert swap_endian_32bit(0xA12345678) == 0x78563412


def test_valid_i2c_addres_wrong_type():
    assert not valid_i2c_address("hello")


def test_valid_i2c_addres_outside_range():
    assert not valid_i2c_address(0x80)
    assert not valid_i2c_address(0xFF)
    assert not valid_i2c_address(-1)


def test_valid_i2c_addres():
    assert valid_i2c_address(0x21)


def test_address_to_phys_8bit_big():
    assert address_to_phys(0x21, bitlength=8, endianness='big') == 0x21


def test_address_to_phys_8bit_little():
    assert address_to_phys(0x21, bitlength=8, endianness='little') == 0x21


def test_address_to_phys_16bit_big():
    assert address_to_phys(0x2113, bitlength=16, endianness='big') == 0x2113


def test_address_to_phys_16bit_little():
    assert address_to_phys(0x2113, bitlength=16, endianness='little') == 0x1321


def test_address_to_phys_32bit_big():
    assert address_to_phys(0x21763454, bitlength=32, endianness='big') == 0x21763454


def test_address_to_phys_32bit_little():
    assert address_to_phys(0x21763454, bitlength=32, endianness='little') == 0x54347621


def test_address_to_phys_fail():
    with pytest.raises(Exception) as e_info:
        address_to_phys(0x21763454, bitlength=23, endianness='little')
    assert e_info.match(r"^Endian swap not implemented for bit length 23")


def test_word_list_to_bytes_8bit_big():
    assert word_list_to_bytes([0x32, 0x86], bytelength=1, endianness='big') == [0x32, 0x86]


def test_word_list_to_bytes_8bit_little():
    assert word_list_to_bytes([0x32, 0x86], bytelength=1, endianness='little') == [0x32, 0x86]


def test_word_list_to_bytes_16bit_big():
    assert word_list_to_bytes([0x3210, 0x8654], bytelength=2, endianness='big') == [0x32, 0x10, 0x86, 0x54]


def test_word_list_to_bytes_16bit_little():
    assert word_list_to_bytes([0x3210, 0x8654], bytelength=2, endianness='little') == [0x10, 0x32, 0x54, 0x86]


def test_word_list_to_bytes_32bit_big():
    assert word_list_to_bytes([0x32103456, 0x86285031], bytelength=4, endianness='big') == [0x32, 0x10, 0x34, 0x56, 0x86, 0x28, 0x50, 0x31]


def test_word_list_to_bytes_32bit_little():
    assert word_list_to_bytes([0x32103456, 0x86285031], bytelength=4, endianness='little') == [
        0x56,
        0x34,
        0x10,
        0x32,
        0x31,
        0x50,
        0x28,
        0x86,
    ]


def test_bytes_to_word_list_8bit_big():
    assert bytes_to_word_list([0x21, 0x34], bytelength=1, endianness='big') == [0x21, 0x34]


def test_bytes_to_word_list_8bit_little():
    assert bytes_to_word_list([0x21, 0x34], bytelength=1, endianness='little') == [0x21, 0x34]


def test_bytes_to_word_list_16bit_big():
    assert bytes_to_word_list([0x21, 0x34], bytelength=2, endianness='big') == [0x2134]


def test_bytes_to_word_list_16bit_little():
    assert bytes_to_word_list([0x21, 0x34], bytelength=2, endianness='little') == [0x3421]


def test_bytes_to_word_list_32bit_big():
    assert bytes_to_word_list([0x21, 0x34, 0x76, 0x12], bytelength=4, endianness='big') == [0x21347612]


def test_bytes_to_word_list_32bit_little():
    assert bytes_to_word_list([0x21, 0x34, 0x76, 0x12], bytelength=4, endianness='little') == [0x12763421]
