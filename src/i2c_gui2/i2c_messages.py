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
"""The i2c_messages module

Contains the I2CMessages class, which is only a utility class to help building
custom I2C command sequences using user friendly names.

"""

from __future__ import annotations

from enum import Enum


class I2CMessages(Enum):
    """Class to wrap the I2C Messages unique identifiers

    This is a temporary description

    Examples
    --------
    >>> from i2c_gui2.i2c_messages import I2CMessages
    >>> single_command = I2CMessages.READ7
    >>> command_sequence = [I2CMessages.START, I2CMessages.NACK, I2CMessages.READ2, I2CMessages.STOP]

    """

    # nb: using same IDs as defined for the USB-ISS
    START = 0x01
    RESTART = 0x02
    STOP = 0x03
    NACK = 0x04  # NACK after next read
    READ1 = 0x20
    READ2 = 0x21
    READ3 = 0x22
    READ4 = 0x23
    READ5 = 0x24
    READ6 = 0x25
    READ7 = 0x26
    READ8 = 0x27
    READ9 = 0x28
    READ10 = 0x29
    READ11 = 0x2A
    READ12 = 0x2B
    READ13 = 0x2C
    READ14 = 0x2D
    READ15 = 0x2E
    READ16 = 0x2F
    WRITE1 = 0x30
    WRITE2 = 0x31
    WRITE3 = 0x32
    WRITE4 = 0x33
    WRITE5 = 0x34
    WRITE6 = 0x35
    WRITE7 = 0x36
    WRITE8 = 0x37
    WRITE9 = 0x38
    WRITE10 = 0x39
    WRITE11 = 0x3A
    WRITE12 = 0x3B
    WRITE13 = 0x3C
    WRITE14 = 0x3D
    WRITE15 = 0x3E
    WRITE16 = 0x3F
