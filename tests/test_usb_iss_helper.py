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

from unittest.mock import call
from unittest.mock import patch

import pytest
from usb_iss import defs

from i2c_gui2.i2c_messages import I2CMessages
from i2c_gui2.i2c_usb_iss_helper import USB_ISS_Helper


@pytest.fixture
def port():
    yield "port"


@pytest.fixture
def clock():
    yield 100


@pytest.fixture
def use_serial():
    yield False


@pytest.fixture
def baud_rate():
    yield 96000


@pytest.fixture
def verbose():
    yield True


@pytest.fixture
def max_seq_byte():
    yield 8


@pytest.fixture
def dummy_connect():
    yield False


@pytest.fixture
def usb_iss_test(port, clock, use_serial, baud_rate, verbose, max_seq_byte, dummy_connect):
    yield USB_ISS_Helper(
        port=port,
        clock=clock,
        use_serial=use_serial,
        baud_rate=baud_rate,
        verbose=verbose,
        max_seq_byte=max_seq_byte,
        dummy_connect=dummy_connect,
    )


@pytest.fixture
def mock_usb_iss(port, clock, use_serial, baud_rate, verbose, max_seq_byte, dummy_connect):
    with patch('i2c_gui2.i2c_usb_iss_helper.UsbIss') as mock_class:
        mock_class.return_value = mock_class
        yield mock_class


@pytest.fixture
def usb_iss_mocked(mock_usb_iss, port, clock, use_serial, baud_rate, verbose, max_seq_byte, dummy_connect):
    mock_usb_iss.open.return_value = True
    mock_usb_iss.read_module_id.return_value = 7
    mock_usb_iss.read_fw_version.return_value = "My Version"
    mock_usb_iss.read_serial_number.return_value = "My Serial"

    yield USB_ISS_Helper(
        port=port,
        clock=clock,
        use_serial=use_serial,
        baud_rate=baud_rate,
        verbose=verbose,
        max_seq_byte=max_seq_byte,
        dummy_connect=dummy_connect,
    )

    mock_usb_iss.assert_called_once()
    mock_usb_iss.assert_has_calls([call(dummy=dummy_connect, verbose=verbose)])

    mock_usb_iss.open.assert_called_once()

    mock_usb_iss.read_module_id.assert_called_once()

    mock_usb_iss.read_fw_version.assert_called_once()

    mock_usb_iss.read_serial_number.assert_called_once()

    use_hardware = False
    if clock >= 100:
        use_hardware = True

    if not (use_serial and baud_rate is not None):
        mock_usb_iss.setup_i2c.assert_called_once()
        mock_usb_iss.setup_i2c.assert_has_calls([call(clock, use_hardware, defs.IOType.ANALOGUE_INPUT, defs.IOType.ANALOGUE_INPUT)])
    else:
        mock_usb_iss.setup_i2c_serial.assert_called_once()
        mock_usb_iss.setup_i2c_serial.assert_has_calls([call(clock, use_hardware, baud_rate)])

    # mock_usb_iss.close.assert_not_called()


@pytest.mark.parametrize('use_serial', [True, False])
def test_init(port, clock, use_serial, baud_rate, usb_iss_mocked):
    assert usb_iss_mocked.connected

    assert usb_iss_mocked.fw_version == "My Version"
    assert usb_iss_mocked.serial == "My Serial"
    assert usb_iss_mocked.port == port
    assert usb_iss_mocked.clock == clock
    assert usb_iss_mocked.use_serial == use_serial
    if use_serial:
        assert usb_iss_mocked.baud_rate == baud_rate


@pytest.mark.parametrize('dummy_connect', [True])
def test_no_mock(usb_iss_test):
    assert usb_iss_test.connected


def test_invalid_clock(port, use_serial, baud_rate, verbose, max_seq_byte, dummy_connect):
    with pytest.raises(Exception) as e_info:
        USB_ISS_Helper(
            port=port,
            clock=5000,
            use_serial=use_serial,
            baud_rate=baud_rate,
            verbose=verbose,
            max_seq_byte=max_seq_byte,
            dummy_connect=dummy_connect,
        )
    assert e_info.match(r"^Received a wrong clock value: 5000 kHz")


@pytest.mark.parametrize('use_serial', [True])
@pytest.mark.parametrize('baud_rate', [None])
def test_serial_override(usb_iss_mocked):
    assert not usb_iss_mocked.use_serial


@pytest.mark.parametrize("connected", [True, False])
@pytest.mark.parametrize("device_address", [0x30])
def test__check_i2c_device(mock_usb_iss, usb_iss_mocked, connected, device_address):
    mock_usb_iss.i2c = mock_usb_iss
    mock_usb_iss.test.return_value = connected

    mock_usb_iss.test.assert_not_called()
    assert usb_iss_mocked._check_i2c_device(device_address) == connected


@pytest.mark.parametrize("write_type,bitlength", [("Normal", 8), ("Normal", 16)])
@pytest.mark.parametrize("device_address", [0x30])
@pytest.mark.parametrize("word_address", [0x14])
@pytest.mark.parametrize("data", [[0x01, 0x21], [0x13, 0x34, 0x42]])
def test__write_i2c_device_memory(mock_usb_iss, usb_iss_mocked, write_type, bitlength, device_address, word_address, data):
    mock_usb_iss.i2c = mock_usb_iss
    usb_iss_mocked._write_i2c_device_memory(device_address, word_address, data, write_type, bitlength)

    if write_type == "Normal":
        if bitlength == 16:
            mock_usb_iss.write_ad2.assert_has_calls([call(device_address, word_address, data)])
        elif bitlength == 8:
            mock_usb_iss.write_ad1.assert_has_calls([call(device_address, word_address, data)])


@pytest.mark.parametrize("write_type,bitlength", [("Alternate", 16), ("Normal", 24)])
@pytest.mark.parametrize("device_address", [0x30])
@pytest.mark.parametrize("word_address", [0x14])
@pytest.mark.parametrize("data", [[0x01, 0x21]])
def test_fail__write_i2c_device_memory(mock_usb_iss, usb_iss_mocked, write_type, bitlength, device_address, word_address, data):
    mock_usb_iss.i2c = mock_usb_iss
    with pytest.raises(Exception) as e_info:
        usb_iss_mocked._write_i2c_device_memory(device_address, word_address, data, write_type, bitlength)

    if write_type == "Normal":
        if bitlength not in [8, 16]:
            assert e_info.match(r"^Unknown bit size trying to be sent")
    else:
        assert e_info.match(r"^Unknown write type chosen for the USB ISS")


@pytest.mark.parametrize("read_type,bitlength", [("Normal", 8), ("Normal", 16), ("Repeated Start", 8), ("Repeated Start", 16)])
@pytest.mark.parametrize("device_address", [0x30])
@pytest.mark.parametrize("word_address", [0x14])
@pytest.mark.parametrize("words", [2])
def test__read_i2c_device_memory(mock_usb_iss, usb_iss_mocked, read_type, bitlength, device_address, word_address, words):
    mock_usb_iss.i2c = mock_usb_iss
    data = [i for i in range(words)]
    if read_type == "Normal":
        if bitlength == 16:
            mock_usb_iss.read_ad2.return_value = data
        elif bitlength == 8:
            mock_usb_iss.read_ad1.return_value = data
    elif read_type == "Repeated Start":
        mock_usb_iss.direct.return_value = data

    read_data = usb_iss_mocked._read_i2c_device_memory(device_address, word_address, words, read_type, bitlength)

    if read_type == "Normal":
        if bitlength == 16:
            mock_usb_iss.read_ad2.assert_has_calls([call(device_address, word_address, words)])
            assert read_data == data
        elif bitlength == 8:
            mock_usb_iss.read_ad1.assert_has_calls([call(device_address, word_address, words)])
            assert read_data == data
    elif read_type == "Repeated Start":
        if bitlength == 16:
            direct_msg = [
                defs.I2CDirect.START,
                defs.I2CDirect.WRITE3,
                device_address << 1,
                (word_address >> 8) & 0xFF,
                word_address & 0xFF,
                defs.I2CDirect.RESTART,
                defs.I2CDirect.WRITE1,
                (device_address << 1) | 0x01,
                getattr(defs.I2CDirect, f"READ{words-1}"),
                defs.I2CDirect.NACK,
                defs.I2CDirect.READ1,
                defs.I2CDirect.STOP,
            ]
        if bitlength == 8:
            direct_msg = [
                defs.I2CDirect.START,
                defs.I2CDirect.WRITE2,
                device_address << 1,
                word_address & 0xFF,
                defs.I2CDirect.RESTART,
                defs.I2CDirect.WRITE1,
                (device_address << 1) | 0x01,
                getattr(defs.I2CDirect, f"READ{words-1}"),
                defs.I2CDirect.NACK,
                defs.I2CDirect.READ1,
                defs.I2CDirect.STOP,
            ]
        mock_usb_iss.direct.assert_has_calls([call(direct_msg)])
        assert read_data == data


@pytest.mark.parametrize("read_type,bitlength", [("Normal", 24), ("Repeated Start", 8), ("Repeated Start", 12), ("Alternate", 8)])
@pytest.mark.parametrize("device_address", [0x30])
@pytest.mark.parametrize("word_address", [0x14])
@pytest.mark.parametrize("words", [2, 24])
def test_fail__read_i2c_device_memory(mock_usb_iss, usb_iss_mocked, read_type, bitlength, device_address, word_address, words):
    mock_usb_iss.i2c = mock_usb_iss
    mock_usb_iss.direct.return_value = [i for i in range(words - 1)]
    with pytest.raises(Exception) as e_info:
        usb_iss_mocked._read_i2c_device_memory(device_address, word_address, words, read_type, bitlength)

    if read_type == "Normal":
        if bitlength not in [8, 16]:
            assert e_info.match(r"^Unknown bit size trying to be sent")
    elif read_type == "Repeated Start":
        if bitlength not in [8, 16]:
            assert e_info.match(r"^Unknown bit size trying to be sent")
        else:
            if words > 16:
                assert e_info.match(r"^USB ISS does not support a block read of more than 16 bytes")
            else:
                mock_usb_iss.direct.assert_called_once()
                assert e_info.match(r"^Did not receive the expected number of bytes")
    else:
        assert e_info.match(r"^Unknown read type chosen for the USB ISS")


def test__direct_i2c(mock_usb_iss, usb_iss_mocked):
    mock_usb_iss.i2c = mock_usb_iss
    mock_usb_iss.direct.return_value = "My very unique string"

    commands = [
        I2CMessages.NACK,
        I2CMessages.WRITE1,
        2,
        I2CMessages.WRITE2,
        2,
        2,
        I2CMessages.WRITE3,
        2,
        2,
        2,
        I2CMessages.WRITE4,
        2,
        2,
        2,
        2,
        I2CMessages.WRITE5,
        2,
        2,
        2,
        2,
        2,
        I2CMessages.WRITE6,
        2,
        2,
        2,
        2,
        2,
        2,
        I2CMessages.WRITE7,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        I2CMessages.WRITE8,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        I2CMessages.WRITE9,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        I2CMessages.WRITE10,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        I2CMessages.WRITE11,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        I2CMessages.WRITE12,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        I2CMessages.WRITE13,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        I2CMessages.WRITE14,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        I2CMessages.WRITE15,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        I2CMessages.WRITE16,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
    ]
    message = usb_iss_mocked._direct_i2c(commands)

    mock_usb_iss.direct.assert_called_once()
    assert message == "My very unique string"


def test_fail__direct_i2c(mock_usb_iss, usb_iss_mocked):
    mock_usb_iss.i2c = mock_usb_iss

    commands = [256]

    with pytest.raises(Exception) as e_info:
        usb_iss_mocked._direct_i2c(commands)

    assert e_info.match(r"^Unknown I2C command")
