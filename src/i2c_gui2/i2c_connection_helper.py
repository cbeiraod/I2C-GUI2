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
from math import ceil
from math import floor
from time import sleep

from .functions import address_to_phys
from .functions import bytes_to_word_list
from .functions import valid_i2c_address
from .functions import word_list_to_bytes
from .i2c_messages import I2CMessages

valid_endianness = ['little', 'big']
valid_read_type = ['Normal', 'Repeated Start']
valid_write_type = ['Normal']


class I2C_Connection_Helper:
    def __init__(
        self,
        max_seq_byte: int,
        successive_i2c_delay_us: int = 10000,
        no_connect: bool = False,
    ):
        self._max_seq_byte = max_seq_byte

        self._no_connect = no_connect

        self._successive_i2c_delay_us = successive_i2c_delay_us

        self._logger = logging.getLogger("I2C_Log")
        self._logger.setLevel(logging.NOTSET)

        self._is_connected = False

    @property
    def logger(self):
        return self._logger

    @property
    def connected(self):
        return self._is_connected

    def _check_i2c_device(self, device_address: int):
        raise RuntimeError("Derived classes must implement the individual device access functions: _check_i2c_device")

    def _write_i2c_device_memory(
        self,
        device_address: int,
        word_address: int,
        byte_data: list[int],
        write_type: str = 'Normal',
    ):
        raise RuntimeError("Derived classes must implement the individual device access functions: _write_i2c_device_memory")

    def _read_i2c_device_memory(
        self,
        device_address: int,
        word_address: int,
        byte_count: int,
        read_type: str = 'Normal',
    ) -> list[int]:
        raise RuntimeError("Derived classes must implement the individual device access functions: _read_i2c_device_memory")

    def _direct_i2c(self, commands: list[I2CMessages]) -> list[int]:
        raise RuntimeError("Derived classes must implement the individual device access functions: _direct_i2c")

    def validate_connection_params(self):
        raise RuntimeError("Derived classes must implement validation of the connection parameters")

    def connect(self):
        raise RuntimeError("Derived classes must implement the connect method")

    def disconnect(self):
        raise RuntimeError("Derived classes must implement the disconnect method")

    def check_i2c_device(self, device_address: int):
        self._logger.info("Trying to find the I2C device with address 0x{:02x}".format(device_address))

        if not self._is_connected or self._no_connect:
            self._logger.info("The I2C device is not connected or you are using software emulated mode.")
            return False

        if not self._check_i2c_device(device_address):
            self._logger.info("The I2C device 0x{:02x} can not be found.".format(device_address))
            return False

        self._logger.info("The I2C device 0x{:02x} was found.".format(device_address))
        return True

    def read_device_memory(
        self,
        device_address: int,
        word_address: int,
        word_count: int = 1,
        address_bitlength: int = 8,
        address_endianness: str = 'big',
        word_bitlength: int = 8,
        word_endianness: str = 'big',
        read_type: str = 'Normal',
    ):
        if not self._is_connected:
            raise RuntimeError("You must first connect to a device before trying to read registers from it")

        if not valid_i2c_address(device_address):
            raise RuntimeError("Invalid I2C address received: {:#04x}".format(device_address))

        if address_endianness not in valid_endianness:
            raise RuntimeError(f"A wrong address endianness was set: {address_endianness}")

        if word_endianness not in valid_endianness:
            raise RuntimeError(f"A wrong word endianness was set: {word_endianness}")

        if read_type not in valid_read_type:
            raise RuntimeError(f"A wrong read type was set: {read_type}")

        word_bytes = ceil(word_bitlength / 8)

        address_chars = ceil(address_bitlength / 4)

        if word_count == 1:
            self._logger.info(
                (f"Reading the register {{:#0{address_chars+2}x}} of the I2C device with address {{:#04x}}:").format(
                    word_address, device_address
                )
            )
        else:
            self._logger.info(
                (
                    f"Reading a register block with size {{}} starting at register {{:#0{address_chars+2}x}} of"
                    f" the I2C device with address {{:#04x}}:"
                ).format(word_count, word_address, device_address)
            )

        byte_data = []
        if self._no_connect:
            if word_count == 1:
                if word_bytes == 1:
                    byte_data = [42]
                else:
                    byte_data = [0 for _ in range(word_bytes - 1)]
                    if word_endianness == 'big':
                        byte_data += [42]
                    else:  # if word_endianness == 'little':
                        byte_data = [42] + byte_data
            else:
                byte_data = [i for i in range(word_count * word_bytes)]
            self._logger.debug("Software emulation (no connect) is enabled, so returning dummy values: {}".format(repr(byte_data)))
        elif self._max_seq_byte is None:
            word_address = address_to_phys(word_address, address_bitlength, address_endianness)
            byte_data = self._read_i2c_device_memory(device_address, word_address, word_count * word_bytes, read_type=read_type)
            self._logger.debug("Got data: {}".format(repr(byte_data)))
        else:
            byte_data = []
            words_per_call = floor(self._max_seq_byte / word_bytes)
            if words_per_call == 0:
                raise RuntimeError(
                    "The word length is too big for the maximum number of bytes in a single call, it is impossible"
                    " to read data in these conditions"
                )
            sequential_calls = ceil(word_count / words_per_call)
            self._logger.debug("Breaking the read into {} individual reads of {} words".format(sequential_calls, words_per_call))

            for i in range(sequential_calls):
                # Add here the possibility to call an external update function (for progress bars in GUI for instance)

                this_block_address = word_address + i * words_per_call
                this_block_words = min(words_per_call, word_count - i * words_per_call)
                bytes_to_read = this_block_words * word_bytes

                self._logger.debug(
                    (f"Read operation {{}}: reading {{}} words starting from {{:#0{address_chars+2}x}}").format(
                        i, this_block_words, this_block_address
                    )
                )

                this_block_address = address_to_phys(this_block_address, address_bitlength, address_endianness)
                this_data = self._read_i2c_device_memory(device_address, this_block_address, bytes_to_read, read_type=read_type)
                self._logger.debug("Got data: {}".format(repr(this_data)))

                byte_data += this_data
                sleep(self._successive_i2c_delay_us * 10**-6)

            # Clear the progress from the function above

        # Merge byte data back into words
        return bytes_to_word_list(byte_data, word_bytes, word_endianness)

    def write_device_memory(
        self,
        device_address: int,
        word_address: int,
        data: list[int],
        address_bitlength: int = 8,
        address_endianness: str = 'big',
        word_bitlength: int = 8,
        word_endianness: str = 'big',
        write_type: str = 'Normal',
    ):
        if not self._is_connected:
            raise RuntimeError("You must first connect to a device before trying to write registers to it")

        if not valid_i2c_address(device_address):
            raise RuntimeError("Invalid I2C address received: {:#04x}".format(device_address))

        if address_endianness not in valid_endianness:
            raise RuntimeError(f"A wrong address endianness was set: {address_endianness}")

        if word_endianness not in valid_endianness:
            raise RuntimeError(f"A wrong word endianness was set: {word_endianness}")

        if write_type not in valid_read_type:
            raise RuntimeError(f"A wrong write type was set: {write_type}")

        address_chars = ceil(address_bitlength / 4)
        word_chars = ceil(word_bitlength / 4)
        word_bytes = ceil(word_bitlength / 8)
        word_count = len(data)

        if word_count == 1:
            self._logger.info(
                (
                    f"Writing the value {{:#0{word_chars+2}x}} to the register {{:#0{address_chars+2}x}} of"
                    f" the I2C device with address {{:#04x}}:"
                ).format(data[0], word_address, device_address)
            )
        else:
            self._logger.info(
                (
                    f"Writing a register block with size {{}} starting at register {{:#0{address_chars+2}x}} of"
                    f" the I2C device with address {{:#04x}}. Writing the value array: {{}}"
                ).format(word_count, word_address, device_address, repr(data))
            )

        if self._no_connect:
            self._logger.debug("Software emulation (no connect) is enabled, so no write action is taken.")
        elif self._max_seq_byte is None:
            self._logger.debug("Writing the full block at once.")
            word_address = address_to_phys(word_address, address_bitlength, address_endianness)
            byte_data = word_list_to_bytes(data, word_bytes, word_endianness)
            self._write_i2c_device_memory(device_address, word_address, byte_data, write_type=write_type)
        else:
            words_per_call = floor(self._max_seq_byte / word_bytes)
            if words_per_call == 0:
                raise RuntimeError(
                    "The word length is too big for the maximum number of bytes in a single call, it is impossible to"
                    " write data in these conditions"
                )
            sequential_calls = ceil(word_count / words_per_call)
            self._logger.debug("Breaking the write into {} individual writes of {} words".format(sequential_calls, words_per_call))

            for i in range(sequential_calls):
                # Add here the possibility to call an external update function (for progress bars in GUI for instance)

                this_block_address = word_address + i * words_per_call
                this_block_words = min(words_per_call, word_count - i * words_per_call)
                bytes_to_write = this_block_words * word_bytes
                self._logger.debug(
                    (f"Write operation {{}}: writing {{}} words starting from {{:#0{address_chars+2}x}}").format(
                        i, bytes_to_write, this_block_address
                    )
                )

                this_data = data[i * words_per_call : i * words_per_call + this_block_words]
                self._logger.debug("Current block: {}".format(repr(this_data)))

                this_block_address = address_to_phys(this_block_address, address_bitlength, address_endianness)
                this_byte_data = word_list_to_bytes(this_data, word_bytes, word_endianness)
                self._write_i2c_device_memory(device_address, this_block_address, this_byte_data, write_type=write_type)

                sleep(self._successive_i2c_delay_us * 10**-6)

            # Clear the progress from the function above
