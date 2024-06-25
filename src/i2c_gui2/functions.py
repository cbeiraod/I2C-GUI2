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

from __future__ import annotations

import logging
import re


def is_valid_hostname(hostname: str):
    if hostname[-1] == ".":
        # strip exactly one dot from the right, if present
        hostname = hostname[:-1]
    if len(hostname) > 253:
        return False

    labels = hostname.split(".")

    if len(labels) == 1:
        if labels[0] != "localhost":
            return False

    # the TLD must not be all-numeric
    if re.match(r"[0-9]+$", labels[-1]):
        return False

    allowed = re.compile(r"(?!-)[a-z0-9-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(label) for label in labels)


def is_valid_ip(hostname: str):
    fields = hostname.split(".")

    if len(fields) != 4:
        return False

    allowed = re.compile(r"\d{1,3}$")

    return all(allowed.match(field) and int(field) < 256 and int(field) >= 0 for field in fields)


def validate_hostname(hostname: str):
    if is_valid_hostname(hostname):
        return True

    if is_valid_ip(hostname):
        return True

    return False


# Function from: https://stackoverflow.com/a/35804945
def addLoggingLevel(levelName, levelNum, methodName=None):
    """
    Comprehensively adds a new logging level to the `logging` module and the
    currently configured logging class.

    `levelName` becomes an attribute of the `logging` module with the value
    `levelNum`. `methodName` becomes a convenience method for both `logging`
    itself and the class returned by `logging.getLoggerClass()` (usually just
    `logging.Logger`). If `methodName` is not specified, `levelName.lower()` is
    used.

    To avoid accidental clobberings of existing attributes, this method will
    raise an `AttributeError` if the level name is already an attribute of the
    `logging` module or if the method name is already present

    Example
    -------
    >>> addLoggingLevel('TRACE', logging.DEBUG - 5)
    >>> logging.getLogger(__name__).setLevel("TRACE")
    >>> logging.getLogger(__name__).trace('that worked')
    >>> logging.trace('so did this')
    >>> logging.TRACE
    5
    """
    if not methodName:
        methodName = levelName.lower()

    if hasattr(logging, levelName):
        raise AttributeError('{} already defined in logging module'.format(levelName))
    if hasattr(logging, methodName):
        raise AttributeError('{} already defined in logging module'.format(methodName))
    if hasattr(logging.getLoggerClass(), methodName):
        raise AttributeError('{} already defined in logger class'.format(methodName))

    # This method was inspired by the answers to Stack Overflow post
    # http://stackoverflow.com/q/2183233/2988730, especially
    # http://stackoverflow.com/a/13638084/2988730
    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(levelNum):
            self._log(levelNum, message, args, **kwargs)

    def logToRoot(message, *args, **kwargs):
        logging.log(levelNum, message, *args, **kwargs)

    logging.addLevelName(levelNum, levelName)
    setattr(logging, levelName, levelNum)
    setattr(logging.getLoggerClass(), methodName, logForLevel)
    setattr(logging, methodName, logToRoot)


def swap_endian_16bit(value: int):
    value = value & 0xFFFF  # Limit value to 16 bits

    value_swapped = (value >> 8) | ((value & 0xFF) << 8)

    return value_swapped


def swap_endian_32bit(value: int):
    value = value & 0xFFFFFFFF  # Limit value to 32 bits

    value_swapped = (value >> 24) | ((value & 0xFF0000) >> 8) | ((value & 0xFF00) << 8) | ((value & 0xFF) << 24)

    return value_swapped


def valid_i2c_address(value: int):
    if not isinstance(value, int):
        return False

    if value > 127 or value < 0:
        return False

    return True


def address_to_phys(address: int, bitlength: int = 8, endianness: str = 'big'):
    if endianness == 'little':
        if bitlength == 8:
            pass
        elif bitlength == 16:
            address = swap_endian_16bit(address)
        elif bitlength == 32:
            address = swap_endian_32bit(address)
        else:
            raise RuntimeError(f"Endian swap not implemented for bit length {bitlength}")

    return address


def word_list_to_bytes(word_list: list[int], bytelength: int = 1, endianness: str = 'big'):
    if bytelength == 1:
        byte_list = word_list
    else:
        byte_list = []
        if endianness == 'big':
            for word in word_list:
                for byte_offset in range(bytelength):
                    byte_list += [(word >> ((bytelength - 1 - byte_offset) * 8)) & 0xFF]
        else:  # if endianness == 'little':
            for word in word_list:
                for byte_offset in range(bytelength):
                    byte_list += [(word >> (byte_offset * 8)) & 0xFF]

    return byte_list


def bytes_to_word_list(byte_list: list[int], bytelength: int = 1, endianness: str = 'big'):
    if bytelength == 1:
        word_list = byte_list
    else:
        word_list = []
        word_count = int(len(byte_list) / bytelength)
        # Do the if outside the for loops, in this way there is a single if evaluation,
        # instead of multiple if evaluations for each iteration
        if endianness == 'big':
            for word_idx in range(word_count):
                word = 0
                byte_base_idx = word_idx * bytelength
                for byte_offset in range(bytelength):
                    byte_idx = byte_base_idx + byte_offset
                    word += byte_list[byte_idx] << ((bytelength - 1 - byte_offset) * 8)
                word_list += [word]
        else:  # if endianness == 'little':
            for word_idx in range(word_count):
                word = 0
                byte_base_idx = word_idx * bytelength
                for byte_offset in range(bytelength):
                    byte_idx = byte_base_idx + byte_offset
                    word += byte_list[byte_idx] << (byte_offset * 8)
                word_list += [word]
    return word_list
