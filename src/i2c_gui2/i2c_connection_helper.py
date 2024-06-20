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
"""The i2c_connection_helper module

Contains the I2C_Connection_Helper class, which is only a base class from which
derived classes which implement I2C communication should inherit from.

"""

from __future__ import annotations

import logging
from math import ceil
from math import floor
from time import sleep
from time import time_ns

from .functions import address_to_phys
from .functions import bytes_to_word_list
from .functions import valid_i2c_address
from .functions import word_list_to_bytes
from .i2c_messages import I2CMessages

valid_endianness = ['little', 'big']
valid_read_type = ['Normal', 'Repeated Start']
valid_write_type = ['Normal']


class I2C_Connection_Helper:
    """Base Class to handle an I2C Connection

    This is a base class from which derived classes should inherit and implement
    the necessary methods.

    This base class sets up many of the internal features of an I2C connection,
    such as an internal log for logging I2C activity.

    Parameters
    ----------
    max_seq_byte
        The maximum number of bytes which can be transmitted in a single I2C command

    successive_i2c_delay_us
        The minimum delay in microseconds (us) between successive I2C commands

    no_connect
        Mostly used for debugging, if set to True, no physical cconnection will
        actually be attempted, but default values will be returned as I2C responses

    """

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

        self._lastI2COperation = time_ns()

    @property
    def logger(self):
        """The logger property getter method

        This method returns the internal logger of the I2C Connection object

        Returns
        -------
        logging.Logger
            The logger
        """
        return self._logger

    @property
    def connected(self):
        """The connected property getter method

        This method returns the connection status of the I2C connection

        Returns
        -------
        bool
            The state of the connection
        """
        return self._is_connected

    def _check_i2c_device(self, device_address: int) -> bool:
        """The internal method to check if an i2c device with the given address is connected

        This method must be implemented by the derived classes

        Parameters
        ----------
        device_address
            The I2C address of the device to check. It must be a 7-bit address as per the I2C standard

        Raises
        ------
        RuntimeError
            If the derived class has not implemented this method

        Returns
        -------
        bool
            The presence or absence of the device with the `device_address`
        """
        raise RuntimeError("Derived classes must implement the individual device access methods: _check_i2c_device")

    def _write_i2c_device_memory(
        self,
        device_address: int,
        word_address: int,
        byte_data: list[int],
        write_type: str = 'Normal',
        address_bitlength: int = 8,
    ):
        """The internal method to write byte data to an i2c device with the given address.

        This method must be implemented by the derived classes.

        Parameters
        ----------
        device_address
            The I2C address of the device to write to. It must be a 7-bit address as per the I2C standard.

        word_address
            The address of the first byte to be written to. The address should have its endianness correctly
            set such that the MSB of `word_address` is the first byte sent on the I2C lines.

        byte_data
            The byte data to be written to the I2C device. The data is written to the I2C bus in the order
            given, so the endianness of the data must be correctly set, assuming the device contains registers
            larger than 8 bits.

        write_type
            The type of protocol used for the actual writing procedure to the device.

        address_bitlength
            The length in bits of the address

        Raises
        ------
        RuntimeError
            If the derived class has not implemented this method
        """
        raise RuntimeError("Derived classes must implement the individual device access methods: _write_i2c_device_memory")

    def _read_i2c_device_memory(
        self,
        device_address: int,
        word_address: int,
        byte_count: int,
        read_type: str = 'Normal',
        address_bitlength: int = 8,
    ) -> list[int]:
        """The internal method to read byte data from an i2c device with the given address.

        This method must be implemented by the derived classes.

        Parameters
        ----------
        device_address
            The I2C address of the device to write to. It must be a 7-bit address as per the I2C standard.

        word_address
            The address of the first byte to be read from. The address should have its endianness correctly
            set such that the MSB of `word_address` is the first byte sent on the I2C lines.

        byte_count
            The number of bytes to be read from the I2C device. If multybyte registers are to be read, the
            number of bytes should be given, not the number of words.

        read_type
            The type of protocol used for the actual reading procedure from the device. Supported protocols
            are "Normal" and "Repeated Start". The Repeated Start protocol is implemented by the AD5593R chip.

        address_bitlength
            The length in bits of the address

        Raises
        ------
        RuntimeError
            If the derived class has not implemented this method

        Returns
        -------
        list[int]
            The list of bytes in the order presented on the I2C bus. If multibyte registers are being read, then
            the words must be correctly put back together by taking into account the data endianness sent by the
            I2C device.
        """
        raise RuntimeError("Derived classes must implement the individual device access methods: _read_i2c_device_memory")

    def _direct_i2c(self, commands: list[I2CMessages]) -> list[int]:
        """The internal method to send arbitrary I2C messages to the I2C bus.

        This method must be implemented by the derived classes.

        Parameters
        ----------
        commands
            The I2C commands to be sent to the I2C bus in the order they are to be sent.

        Raises
        ------
        RuntimeError
            If the derived class has not implemented this method

        Returns
        -------
        list[int]
            The list of bytes returned to the I2C Bus in the order presented on the I2C bus.
        """
        raise RuntimeError("Derived classes must implement the individual device access methods: _direct_i2c")

    def check_i2c_device(self, device_address: int) -> bool:
        """The user method to check if a device with the `device_address` is connected to the I2C bus.

        This method makes use of the internal method _check_i2c_device

        Parameters
        ----------
        device_address
            The I2C address of the device to write to. It must be a 7-bit address as per the I2C standard.

        Raises
        ------
        RuntimeError
            If there is any problem during runtime

        Returns
        -------
        bool
            The presence or absence of the device with the `device_address`
        """
        self._logger.info("Trying to find the I2C device with address 0x{:02x}".format(device_address))

        if not self._is_connected or self._no_connect:
            self._logger.info("The I2C device is not connected or you are using software emulated mode.")
            return False

        now = time_ns()
        if now - self._lastI2COperation < self._successive_i2c_delay_us * 1000:
            sleep(self._successive_i2c_delay_us * 10**-6)
        self._lastI2COperation = now

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
    ) -> list[int]:
        """The user method to read register data from a device on the I2C bus with the given `device_address`.

        This method makes use of the internal method _read_i2c_device_memory

        Parameters
        ----------
        device_address
            The I2C address of the device to write to. It must be a 7-bit address as per the I2C standard.

        word_address
            The address of the first byte to be read from.

        word_count
            The number of register words to be read from the I2C device.

        address_bitlength
            The bit length of the address, typical values are 8 and 16.

        address_endianness
            The endianness of the address as presented on the I2C bus. This parameter does not make any
            difference for 8-bit addresses.

        word_bitlength
            The bit length of the register words, typical values are 8 and 16.

        word_endianness
            The endianness of the register words as presented on the I2C bus. This parameter does not make any
            difference for 8-bit register words.

        read_type
            The type of protocol used for the actual reading procedure from the device. Supported protocols
            are "Normal" and "Repeated Start". The Repeated Start protocol is implemented by the AD5593R chip.

        Raises
        ------
        RuntimeError
            If there is an issue identified during runtime

        Returns
        -------
        list[int]
            The list of word in order. The words have been put together according to the endianness options set.
        """
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
            now = time_ns()
            if now - self._lastI2COperation < self._successive_i2c_delay_us * 1000:
                sleep(self._successive_i2c_delay_us * 10**-6)
            byte_data = self._read_i2c_device_memory(
                device_address, word_address, word_count * word_bytes, read_type=read_type, address_bitlength=address_bitlength
            )
            self._lastI2COperation = now
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
                now = time_ns()
                if now - self._lastI2COperation < self._successive_i2c_delay_us * 1000:
                    sleep(self._successive_i2c_delay_us * 10**-6)
                this_data = self._read_i2c_device_memory(
                    device_address, this_block_address, bytes_to_read, read_type=read_type, address_bitlength=address_bitlength
                )
                self._lastI2COperation = now
                self._logger.debug("Got data: {}".format(repr(this_data)))

                byte_data += this_data

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
        """The user method to write register data to a device on the I2C bus with the given `device_address`.

        This method makes use of the internal method _write_i2c_device_memory

        Parameters
        ----------
        device_address
            The I2C address of the device to write to. It must be a 7-bit address as per the I2C standard.

        word_address
            The address of the first byte to be written to.

        data
            The register word data to be written to the I2C device.

        address_bitlength
            The bit length of the address, typical values are 8 and 16.

        address_endianness
            The endianness of the address as presented on the I2C bus. This parameter does not make any
            difference for 8-bit addresses.

        word_bitlength
            The bit length of the register words, typical values are 8 and 16.

        word_endianness
            The endianness of the register words as presented on the I2C bus. This parameter does not make any
            difference for 8-bit register words.

        write_type
            The type of protocol used for the actual writing procedure to the device.

        Raises
        ------
        RuntimeError
            If there is an issue identified during runtime
        """
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
            now = time_ns()
            if now - self._lastI2COperation < self._successive_i2c_delay_us * 1000:
                sleep(self._successive_i2c_delay_us * 10**-6)
            self._write_i2c_device_memory(
                device_address, word_address, byte_data, write_type=write_type, address_bitlength=address_bitlength
            )
            self._lastI2COperation = now
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
                now = time_ns()
                if now - self._lastI2COperation < self._successive_i2c_delay_us * 1000:
                    sleep(self._successive_i2c_delay_us * 10**-6)
                self._write_i2c_device_memory(
                    device_address, this_block_address, this_byte_data, write_type=write_type, address_bitlength=address_bitlength
                )
                self._lastI2COperation = now

            # Clear the progress from the function above
