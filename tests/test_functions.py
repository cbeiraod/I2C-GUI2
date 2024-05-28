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


from i2c_gui2.functions import address_to_phys
from i2c_gui2.functions import swap_endian_16bit
from i2c_gui2.functions import swap_endian_32bit
from i2c_gui2.functions import valid_i2c_address


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
