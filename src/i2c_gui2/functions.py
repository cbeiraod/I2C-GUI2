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
