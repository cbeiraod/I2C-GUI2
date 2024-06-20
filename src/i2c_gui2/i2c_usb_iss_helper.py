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

from typing import Union

from usb_iss import UsbIss
from usb_iss import defs

from .i2c_connection_helper import I2C_Connection_Helper
from .i2c_messages import I2CMessages

valid_clocks = [20, 50, 100, 400, 1000]
software_clocks = [20, 50, 100, 400]
hardware_clocks = [100, 400, 1000]


class USB_ISS_Helper(I2C_Connection_Helper):
    """Class to handle the USB-ISS connection

    This class is a wrapper around the usb_iss library, providing a simplified interface for the
    usage in the ETROC DAQ assuming only I2C is used, with optional GPIO for the extra pins

    Parameters
    ----------
    port
        The port where the USB-ISS device can be found

    clock
        The clock frequency to use for I2C communication. It must be a valid clock from the
        list: 20, 50, 100, 400, 1000. For clock frequencies where there is both software and
        hardware support, the hardware version will be given precedence.

    use_serial
        Whether to use the extra pins on the USB-ISS as a serial interface, if not they will be
        GPIO (by default set to analog in). The serial port is only enabled if the baud rate is
        also set.

    baud_rate
        The baud rate to use for the serial communication

    verbose
        Whether to output detailed information to the terminal

    max_seq_byte
        The maximum number of sequential bytes supported in a single I2C message. The limit is not
        necessarily from the USB-ISS and may be from the device it is communicating with. TODO: Add
        an option to set this limit per operation so different limits can be set for different devices.

    dummy_connect
        If set, the connection to the USB-ISS will be emulated and a dummy device will be configured

    Raises
    ------
    SerialException
        If the serial object can not be found

    ValueError
        If a wrong value is passed to the clock configuration

    RuntimeError
        For other issues communicating with the USB-ISS device

    Examples
    --------
    >>> import i2c_gui2
    >>> usbiss = i2c_gui2.USB_ISS_Helper("/dev/ttyACM0")
    >>> usbiss.version()

    """

    _port: str
    _clock: int
    _verbose: bool
    _use_serial: bool
    _baud_rate: Union[int, None]
    _iss: UsbIss
    _fw_version: int
    _serial: str

    def __init__(
        self,
        port: str,
        clock: int,
        use_serial: bool = False,
        baud_rate: Union[int, None] = None,
        verbose: bool = False,
        max_seq_byte: int = 8,
        dummy_connect: bool = False,
    ):
        super().__init__(max_seq_byte=max_seq_byte, no_connect=dummy_connect)
        if clock not in valid_clocks:
            raise ValueError(f"Received a wrong clock value: {clock} kHz")

        self._port = port
        self._clock = clock
        self._verbose = verbose
        self._use_serial = use_serial
        self._baud_rate = baud_rate

        if self._use_serial and self._baud_rate is None:
            self._use_serial = False

        if not self._use_serial:
            self._baud_rate = None

        self._iss = UsbIss(dummy=dummy_connect, verbose=self._verbose)
        self._iss.open(port)

        module_id = self._iss.read_module_id()
        if module_id != 7 and not dummy_connect:
            raise RuntimeError(f"Got an unexpected value for the module ID of the USB-ISS device: {module_id}")

        self._fw_version = self._iss.read_fw_version()
        self._serial = self._iss.read_serial_number()

        self._use_hardware = False
        if self._clock in hardware_clocks:
            self._use_hardware = True

        if not self._use_serial:
            self._iss.setup_i2c(self._clock, self._use_hardware, defs.IOType.ANALOGUE_INPUT, defs.IOType.ANALOGUE_INPUT)
        else:
            self._iss.setup_i2c_serial(self._clock, self._use_hardware, self._baud_rate)

        self._is_connected = True

    def __del__(self):
        if hasattr(self, "_iss"):
            if self._iss is not None:
                self._iss.close()

    @property
    def fw_version(self) -> int:
        """The fw_version property getter method

        This method returns the firmware version of the USB-ISS firmware

        Returns
        -------
        int
            The firmware version number.
        """
        return self._fw_version

    @property
    def serial(self) -> str:
        """The serial_number property getter method

        This method returns the serial number of the USB-ISS firmware

        Returns
        -------
        str
            The serial number.
        """
        return self._serial

    @property
    def port(self) -> str:
        """The port property getter method

        This method returns the port the USB-ISS is connected to

        Returns
        -------
        str
            The port.
        """
        return self._port

    @property
    def clock(self) -> int:
        """The clock property getter method

        This method returns the clock frequency the USB-ISS I2C is configured to

        Returns
        -------
        int
            The clock frequency.
        """
        return self._clock

    @property
    def use_serial(self) -> bool:
        """The use_serial property getter method

        This method returns if the extra pins on the USB-ISS are being used as a serial communication

        Returns
        -------
        bool
            If the extra pins on the USB-ISS are being used as a serial communication
        """
        return self._use_serial

    @property
    def baud_rate(self) -> Union[int, None]:
        """The baud_rate property getter method

        This method returns the baud rate the extra pins on the USB-ISS used as a serial communication are set to

        Returns
        -------
        int
            If the extra pins on the USB-ISS are being used as a serial communication
        None
            If the USB-ISS is not configured to use the serial port for communication
        """
        return self._baud_rate

    def _check_i2c_device(self, device_address: int) -> bool:
        """The internal method to check if an i2c device with the given address is connected

        This method overrides the one from the base class.

        Parameters
        ----------
        device_address
            The I2C address of the device to check. It must be a 7-bit address as per the I2C standard

        Returns
        -------
        bool
            The presence or absence of the device with the `device_address`
        """
        return self._iss.i2c.test(device_address)

    def _write_i2c_device_memory(
        self,
        device_address: int,
        word_address: int,
        byte_data: list[int],
        write_type: str = 'Normal',
        address_bitlength: int = 8,
    ):
        """The internal method to write byte data to an i2c device with the given address.

        This method overrides the one from the base class.

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
            If a not supported configuration is chosen
        """
        if write_type == 'Normal':
            if address_bitlength == 16:
                self._iss.i2c.write_ad2(device_address, word_address, byte_data)
            elif address_bitlength == 8:
                self._iss.i2c.write_ad1(device_address, word_address, byte_data)
            else:
                raise RuntimeError("Unknown bit size trying to be sent")
        else:
            raise RuntimeError("Unknown write type chosen for the USB ISS")

    def _read_i2c_device_memory(
        self,
        device_address: int,
        word_address: int,
        byte_count: int,
        read_type: str = 'Normal',
        address_bitlength: int = 8,
    ) -> list[int]:
        """The internal method to read byte data from an i2c device with the given address.

        This method overrides the one from the base class.

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
            If a not supported configuration is chosen

        Returns
        -------
        list[int]
            The list of bytes in the order presented on the I2C bus. If multibyte registers are being read, then
            the words must be correctly put back together by taking into account the data endianness sent by the
            I2C device.
        """
        if read_type == 'Normal':
            if address_bitlength == 16:
                return self._iss.i2c.read_ad2(device_address, word_address, byte_count)
            if address_bitlength == 8:
                return self._iss.i2c.read_ad1(device_address, word_address, byte_count)
            else:
                raise RuntimeError("Unknown bit size trying to be sent")
        elif read_type == "Repeated Start":
            direct_msg = [defs.I2CDirect.START]

            device_address_byte = device_address << 1
            if address_bitlength == 8:
                direct_msg += [
                    defs.I2CDirect.WRITE2,
                    device_address_byte,
                    word_address & 0xFF,
                ]
            elif address_bitlength == 16:
                direct_msg += [
                    defs.I2CDirect.WRITE3,
                    device_address_byte,
                    (word_address >> 8) & 0xFF,
                    word_address & 0xFF,
                ]
            else:
                raise RuntimeError("Unknown bit size trying to be sent")

            direct_msg += [
                defs.I2CDirect.RESTART,
                defs.I2CDirect.WRITE1,
                device_address_byte | 0x01,
            ]

            if byte_count <= 16:
                if byte_count > 1:
                    direct_msg += [
                        getattr(defs.I2CDirect, f"READ{byte_count-1}"),
                    ]
            else:
                raise RuntimeError("USB ISS does not support a block read of more than 16 bytes")

            direct_msg += [
                defs.I2CDirect.NACK,
                defs.I2CDirect.READ1,
                defs.I2CDirect.STOP,
            ]

            retVal = self._iss.i2c.direct(direct_msg)

            if len(retVal) != byte_count:
                raise RuntimeError("Did not receive the expected number of bytes")
            else:
                return retVal
        else:
            raise RuntimeError("Unknown read type chosen for the USB ISS")

    def _direct_i2c(self, commands: list[I2CMessages]) -> list[int]:  # noqa: C901
        """The internal method to send arbitrary I2C messages to the I2C bus.

        This method overrides the one from the base class.

        Parameters
        ----------
        commands
            The I2C commands to be sent to the I2C bus in the order they are to be sent.

        Raises
        ------
        RuntimeError
            If an unknown command is trying to be sent

        Returns
        -------
        list[int]
            The list of bytes returned to the I2C Bus in the order presented on the I2C bus.
        """
        direct_msg = []

        idx = 0
        while True:
            if idx >= len(commands):
                break

            command = commands[idx]
            if command not in I2CMessages:
                raise RuntimeError("Unknown I2C command")

            direct_msg += [command.value]
            if command == I2CMessages.WRITE1:
                direct_msg += [commands[idx + 1]]
                idx += 2
            elif command == I2CMessages.WRITE2:
                direct_msg += [commands[idx + 1]]
                direct_msg += [commands[idx + 2]]
                idx += 3
            elif command == I2CMessages.WRITE3:
                direct_msg += [commands[idx + 1]]
                direct_msg += [commands[idx + 2]]
                direct_msg += [commands[idx + 3]]
                idx += 4
            elif command == I2CMessages.WRITE4:
                direct_msg += [commands[idx + 1]]
                direct_msg += [commands[idx + 2]]
                direct_msg += [commands[idx + 3]]
                direct_msg += [commands[idx + 4]]
                idx += 5
            elif command == I2CMessages.WRITE5:
                direct_msg += [commands[idx + 1]]
                direct_msg += [commands[idx + 2]]
                direct_msg += [commands[idx + 3]]
                direct_msg += [commands[idx + 4]]
                direct_msg += [commands[idx + 5]]
                idx += 6
            elif command == I2CMessages.WRITE6:
                direct_msg += [commands[idx + 1]]
                direct_msg += [commands[idx + 2]]
                direct_msg += [commands[idx + 3]]
                direct_msg += [commands[idx + 4]]
                direct_msg += [commands[idx + 5]]
                direct_msg += [commands[idx + 6]]
                idx += 7
            elif command == I2CMessages.WRITE7:
                direct_msg += [commands[idx + 1]]
                direct_msg += [commands[idx + 2]]
                direct_msg += [commands[idx + 3]]
                direct_msg += [commands[idx + 4]]
                direct_msg += [commands[idx + 5]]
                direct_msg += [commands[idx + 6]]
                direct_msg += [commands[idx + 7]]
                idx += 8
            elif command == I2CMessages.WRITE8:
                direct_msg += [commands[idx + 1]]
                direct_msg += [commands[idx + 2]]
                direct_msg += [commands[idx + 3]]
                direct_msg += [commands[idx + 4]]
                direct_msg += [commands[idx + 5]]
                direct_msg += [commands[idx + 6]]
                direct_msg += [commands[idx + 7]]
                direct_msg += [commands[idx + 8]]
                idx += 9
            elif command == I2CMessages.WRITE9:
                direct_msg += [commands[idx + 1]]
                direct_msg += [commands[idx + 2]]
                direct_msg += [commands[idx + 3]]
                direct_msg += [commands[idx + 4]]
                direct_msg += [commands[idx + 5]]
                direct_msg += [commands[idx + 6]]
                direct_msg += [commands[idx + 7]]
                direct_msg += [commands[idx + 8]]
                direct_msg += [commands[idx + 9]]
                idx += 10
            elif command == I2CMessages.WRITE10:
                direct_msg += [commands[idx + 1]]
                direct_msg += [commands[idx + 2]]
                direct_msg += [commands[idx + 3]]
                direct_msg += [commands[idx + 4]]
                direct_msg += [commands[idx + 5]]
                direct_msg += [commands[idx + 6]]
                direct_msg += [commands[idx + 7]]
                direct_msg += [commands[idx + 8]]
                direct_msg += [commands[idx + 9]]
                direct_msg += [commands[idx + 10]]
                idx += 11
            elif command == I2CMessages.WRITE11:
                direct_msg += [commands[idx + 1]]
                direct_msg += [commands[idx + 2]]
                direct_msg += [commands[idx + 3]]
                direct_msg += [commands[idx + 4]]
                direct_msg += [commands[idx + 5]]
                direct_msg += [commands[idx + 6]]
                direct_msg += [commands[idx + 7]]
                direct_msg += [commands[idx + 8]]
                direct_msg += [commands[idx + 9]]
                direct_msg += [commands[idx + 10]]
                direct_msg += [commands[idx + 11]]
                idx += 12
            elif command == I2CMessages.WRITE12:
                direct_msg += [commands[idx + 1]]
                direct_msg += [commands[idx + 2]]
                direct_msg += [commands[idx + 3]]
                direct_msg += [commands[idx + 4]]
                direct_msg += [commands[idx + 5]]
                direct_msg += [commands[idx + 6]]
                direct_msg += [commands[idx + 7]]
                direct_msg += [commands[idx + 8]]
                direct_msg += [commands[idx + 9]]
                direct_msg += [commands[idx + 10]]
                direct_msg += [commands[idx + 11]]
                direct_msg += [commands[idx + 12]]
                idx += 13
            elif command == I2CMessages.WRITE13:
                direct_msg += [commands[idx + 1]]
                direct_msg += [commands[idx + 2]]
                direct_msg += [commands[idx + 3]]
                direct_msg += [commands[idx + 4]]
                direct_msg += [commands[idx + 5]]
                direct_msg += [commands[idx + 6]]
                direct_msg += [commands[idx + 7]]
                direct_msg += [commands[idx + 8]]
                direct_msg += [commands[idx + 9]]
                direct_msg += [commands[idx + 10]]
                direct_msg += [commands[idx + 11]]
                direct_msg += [commands[idx + 12]]
                direct_msg += [commands[idx + 13]]
                idx += 14
            elif command == I2CMessages.WRITE14:
                direct_msg += [commands[idx + 1]]
                direct_msg += [commands[idx + 2]]
                direct_msg += [commands[idx + 3]]
                direct_msg += [commands[idx + 4]]
                direct_msg += [commands[idx + 5]]
                direct_msg += [commands[idx + 6]]
                direct_msg += [commands[idx + 7]]
                direct_msg += [commands[idx + 8]]
                direct_msg += [commands[idx + 9]]
                direct_msg += [commands[idx + 10]]
                direct_msg += [commands[idx + 11]]
                direct_msg += [commands[idx + 12]]
                direct_msg += [commands[idx + 13]]
                direct_msg += [commands[idx + 14]]
                idx += 15
            elif command == I2CMessages.WRITE15:
                direct_msg += [commands[idx + 1]]
                direct_msg += [commands[idx + 2]]
                direct_msg += [commands[idx + 3]]
                direct_msg += [commands[idx + 4]]
                direct_msg += [commands[idx + 5]]
                direct_msg += [commands[idx + 6]]
                direct_msg += [commands[idx + 7]]
                direct_msg += [commands[idx + 8]]
                direct_msg += [commands[idx + 9]]
                direct_msg += [commands[idx + 10]]
                direct_msg += [commands[idx + 11]]
                direct_msg += [commands[idx + 12]]
                direct_msg += [commands[idx + 13]]
                direct_msg += [commands[idx + 14]]
                direct_msg += [commands[idx + 15]]
                idx += 16
            elif command == I2CMessages.WRITE16:
                direct_msg += [commands[idx + 1]]
                direct_msg += [commands[idx + 2]]
                direct_msg += [commands[idx + 3]]
                direct_msg += [commands[idx + 4]]
                direct_msg += [commands[idx + 5]]
                direct_msg += [commands[idx + 6]]
                direct_msg += [commands[idx + 7]]
                direct_msg += [commands[idx + 8]]
                direct_msg += [commands[idx + 9]]
                direct_msg += [commands[idx + 10]]
                direct_msg += [commands[idx + 11]]
                direct_msg += [commands[idx + 12]]
                direct_msg += [commands[idx + 13]]
                direct_msg += [commands[idx + 14]]
                direct_msg += [commands[idx + 15]]
                direct_msg += [commands[idx + 16]]
                idx += 17
            else:
                idx += 1

        return self._iss.i2c.direct(direct_msg)
