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

from i2c_gui2.i2c_messages import I2CMessages


def test_start():
    assert I2CMessages.START.value == 0x01


def test_restart():
    assert I2CMessages.RESTART.value == 0x02


def test_stop():
    assert I2CMessages.STOP.value == 0x03


def test_nack():
    assert I2CMessages.NACK.value == 0x04  # NACK after next read


def test_read1():
    assert I2CMessages.READ1.value == 0x20


def test_read2():
    assert I2CMessages.READ2.value == 0x21


def test_read3():
    assert I2CMessages.READ3.value == 0x22


def test_read4():
    assert I2CMessages.READ4.value == 0x23


def test_read5():
    assert I2CMessages.READ5.value == 0x24


def test_read6():
    assert I2CMessages.READ6.value == 0x25


def test_read7():
    assert I2CMessages.READ7.value == 0x26


def test_read8():
    assert I2CMessages.READ8.value == 0x27


def test_read9():
    assert I2CMessages.READ9.value == 0x28


def test_read10():
    assert I2CMessages.READ10.value == 0x29


def test_read11():
    assert I2CMessages.READ11.value == 0x2A


def test_read12():
    assert I2CMessages.READ12.value == 0x2B


def test_read13():
    assert I2CMessages.READ13.value == 0x2C


def test_read14():
    assert I2CMessages.READ14.value == 0x2D


def test_read15():
    assert I2CMessages.READ15.value == 0x2E


def test_read16():
    assert I2CMessages.READ16.value == 0x2F


def test_write1():
    assert I2CMessages.WRITE1.value == 0x30


def test_write2():
    assert I2CMessages.WRITE2.value == 0x31


def test_write3():
    assert I2CMessages.WRITE3.value == 0x32


def test_write4():
    assert I2CMessages.WRITE4.value == 0x33


def test_write5():
    assert I2CMessages.WRITE5.value == 0x34


def test_write6():
    assert I2CMessages.WRITE6.value == 0x35


def test_write7():
    assert I2CMessages.WRITE7.value == 0x36


def test_write8():
    assert I2CMessages.WRITE8.value == 0x37


def test_write9():
    assert I2CMessages.WRITE9.value == 0x38


def test_write10():
    assert I2CMessages.WRITE10.value == 0x39


def test_write11():
    assert I2CMessages.WRITE11.value == 0x3A


def test_write12():
    assert I2CMessages.WRITE12.value == 0x3B


def test_write13():
    assert I2CMessages.WRITE13.value == 0x3C


def test_write14():
    assert I2CMessages.WRITE14.value == 0x3D


def test_write15():
    assert I2CMessages.WRITE15.value == 0x3E


def test_write16():
    assert I2CMessages.WRITE16.value == 0x3F
