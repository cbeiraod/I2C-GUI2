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

from ..i2c_connection_helper import I2C_Connection_Helper
from .address_space_controller import Address_Space_Controller
from .base_chip import Base_Chip

etroc1_version = "0.0.1"

register_model = {
    "Array_Reg_A": {  # Address Space (i.e. separate I2C memory spaces)
        "Memory Size": 48,
        "Register Bits": 8,
        "Register Blocks": {
            "Registers": {  # Register Block (i.e. group of registers to be handled as one unit)
                "Base Address": 0x0000,
                "Registers": {
                    "Reg_A_00": {
                        "offset": 0x0000,
                        "default": 0xF8,
                    },
                    "Reg_A_01": {
                        "offset": 0x0001,
                        "default": 0x37,
                    },
                    "Reg_A_02": {
                        "offset": 0x0002,
                        "default": 0xFF,
                    },
                    "Reg_A_03": {
                        "offset": 0x0003,
                        "default": 0xFF,
                    },
                    "Reg_A_04": {
                        "offset": 0x0004,
                        "default": 0x11,
                    },
                    "Reg_A_05": {
                        "offset": 0x0005,
                        "default": 0x01,
                    },
                    "Reg_A_06": {
                        "offset": 0x0006,
                        "default": 0x00,
                    },
                    "Reg_A_07": {
                        "offset": 0x0007,
                        "default": 0x01,
                    },
                    "Reg_A_08": {
                        "offset": 0x0008,
                        "default": 0x00,
                    },
                    "Reg_A_09": {
                        "offset": 0x0009,
                        "default": 0x00,
                    },
                    "Reg_A_0A": {
                        "offset": 0x000A,
                        "default": 0x00,
                    },
                    "Reg_A_0B": {
                        "offset": 0x000B,
                        "default": 0x02,
                    },
                    "Reg_A_0C": {
                        "offset": 0x000C,
                        "default": 0x08,
                    },
                    "Reg_A_0D": {
                        "offset": 0x000D,
                        "default": 0x20,
                    },
                    "Reg_A_0E": {
                        "offset": 0x000E,
                        "default": 0x80,
                    },
                    "Reg_A_0F": {
                        "offset": 0x000F,
                        "default": 0x00,
                    },
                    "Reg_A_10": {
                        "offset": 0x0010,
                        "default": 0x02,
                    },
                    "Reg_A_11": {
                        "offset": 0x0011,
                        "default": 0x08,
                    },
                    "Reg_A_12": {
                        "offset": 0x0012,
                        "default": 0x20,
                    },
                    "Reg_A_13": {
                        "offset": 0x0013,
                        "default": 0x80,
                    },
                    "Reg_A_14": {
                        "offset": 0x0014,
                        "default": 0x00,
                    },
                    "Reg_A_15": {
                        "offset": 0x0015,
                        "default": 0x02,
                    },
                    "Reg_A_16": {
                        "offset": 0x0016,
                        "default": 0x08,
                    },
                    "Reg_A_17": {
                        "offset": 0x0017,
                        "default": 0x20,
                    },
                    "Reg_A_18": {
                        "offset": 0x0018,
                        "default": 0x80,
                    },
                    "Reg_A_19": {
                        "offset": 0x0019,
                        "default": 0x00,
                    },
                    "Reg_A_1A": {
                        "offset": 0x001A,
                        "default": 0x02,
                    },
                    "Reg_A_1B": {
                        "offset": 0x001B,
                        "default": 0x08,
                    },
                    "Reg_A_1C": {
                        "offset": 0x001C,
                        "default": 0x20,
                    },
                    "Reg_A_1D": {
                        "offset": 0x001D,
                        "default": 0x80,
                    },
                    "Reg_A_1E": {
                        "offset": 0x001E,
                        "default": 0xFF,
                    },
                    "Reg_A_1F": {
                        "offset": 0x001F,
                        "default": 0xFF,
                    },
                    "Reg_A_20": {
                        "offset": 0x0020,
                        "default": 0x00,
                        "read_only": True,
                    },
                },
            },
        },
    },
    "Array_Reg_B": {
        "Memory Size": 32,
        "Register Bits": 8,
        "Register Blocks": {
            "Registers": {
                "Base Address": 0x0000,
                "Registers": {
                    "Reg_B_00": {
                        "offset": 0x0000,
                        "default": 0x1C,
                    },
                    "Reg_B_01": {
                        "offset": 0x0001,
                        "default": 0x01,
                    },
                    "Reg_B_02": {
                        "offset": 0x0002,
                        "default": 0x00,
                    },
                    "Reg_B_03": {
                        "offset": 0x0003,
                        "default": 0x09,
                    },
                    "Reg_B_04": {
                        "offset": 0x0004,
                        "default": 0x00,
                    },
                    "Reg_B_05": {
                        "offset": 0x0005,
                        "default": 0x03,
                    },
                    "Reg_B_06": {
                        "offset": 0x0006,
                        "default": 0x41,
                    },
                    "Reg_B_07": {
                        "offset": 0x0007,
                        "default": 0x38,
                    },
                    "Reg_B_08": {
                        "offset": 0x0008,
                        "default": 0x18,
                    },
                    "Reg_B_09": {
                        "offset": 0x0009,
                        "default": 0x18,
                    },
                    "Reg_B_0A": {
                        "offset": 0x000A,
                        "default": 0x38,
                    },
                    "Reg_B_0B": {
                        "offset": 0x000B,
                        "default": 0x77,
                    },
                },
            },
        },
    },
    "Full_Pixel": {
        "Memory Size": 48,
        "Register Bits": 8,
        "Register Blocks": {
            "Registers": {
                "Base Address": 0x0000,
                "Registers": {
                    "Reg_00": {
                        "offset": 0x0000,
                        "default": 0x1C,
                    },
                    "Reg_01": {
                        "offset": 0x0001,
                        "default": 0x01,
                    },
                    "Reg_02": {
                        "offset": 0x0002,
                        "default": 0x00,
                    },
                    "Reg_03": {
                        "offset": 0x0003,
                        "default": 0x9,
                    },
                    "Reg_04": {
                        "offset": 0x0004,
                        "default": 0x00,
                    },
                    "Reg_05": {
                        "offset": 0x0005,
                        "default": 0x03,
                    },
                    "Reg_06": {
                        "offset": 0x0006,
                        "default": 0x83,
                    },
                    "Reg_07": {
                        "offset": 0x0007,
                        "default": 0x38,
                    },
                    "Reg_08": {
                        "offset": 0x0008,
                        "default": 0x18,
                    },
                    "Reg_09": {
                        "offset": 0x0009,
                        "default": 0x18,
                    },
                    "Reg_0A": {
                        "offset": 0x000A,
                        "default": 0x38,
                    },
                    "Reg_0B": {
                        "offset": 0x000B,
                        "default": 0x77,
                    },
                    "Reg_0C": {
                        "offset": 0x000C,
                        "default": 0xF8,
                    },
                    "Reg_0D": {
                        "offset": 0x000D,
                        "default": 0x37,
                    },
                    "Reg_0E": {
                        "offset": 0x000E,
                        "default": 0x00,
                    },
                    "Reg_0F": {
                        "offset": 0x000F,
                        "default": 0x56,
                    },
                    "Reg_10": {
                        "offset": 0x0010,
                        "default": 0x00,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_11": {
                        "offset": 0x0011,
                        "default": 0x00,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_12": {
                        "offset": 0x0012,
                        "default": 0x00,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_13": {
                        "offset": 0x0013,
                        "default": 0x00,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_14": {
                        "offset": 0x0014,
                        "default": 0x00,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_15": {
                        "offset": 0x0015,
                        "default": 0x00,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_16": {
                        "offset": 0x0016,
                        "default": 0x00,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_17": {
                        "offset": 0x0017,
                        "default": 0x00,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_18": {
                        "offset": 0x0018,
                        "default": 0x00,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_19": {
                        "offset": 0x0019,
                        "default": 0x00,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_1A": {
                        "offset": 0x001A,
                        "default": 0x00,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_1B": {
                        "offset": 0x001B,
                        "default": 0x00,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_1C": {
                        "offset": 0x001C,
                        "default": 0x00,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_1D": {
                        "offset": 0x001D,
                        "default": 0x00,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_1E": {
                        "offset": 0x001E,
                        "default": 0x00,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_1F": {
                        "offset": 0x001F,
                        "default": 0x00,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_20": {
                        "offset": 0x0020,
                        "default": 0x00,
                        "read_only": True,
                    },
                },
            },
        },
    },
    "TDC_Test_Block": {
        "Memory Size": 48,
        "Register Bits": 8,
        "Register Blocks": {
            "Registers": {
                "Base Address": 0x0000,
                "Registers": {
                    "Reg_00": {
                        "offset": 0x0000,
                        "default": 0x00,
                    },
                    "Reg_01": {
                        "offset": 0x0001,
                        "default": 0x80,
                    },
                    "Reg_02": {
                        "offset": 0x0002,
                        "default": 0x61,
                    },
                    "Reg_03": {
                        "offset": 0x0003,
                        "default": 0x09,
                    },
                    "Reg_04": {
                        "offset": 0x0004,
                        "default": 0x51,
                    },
                    "Reg_05": {
                        "offset": 0x0005,
                        "default": 0x1F,
                    },
                    "Reg_06": {
                        "offset": 0x0006,
                        "default": 0x03,
                    },
                    "Reg_07": {
                        "offset": 0x0007,
                        "default": 0x38,
                    },
                    "Reg_08": {
                        "offset": 0x0008,
                        "default": 0x38,
                    },
                    "Reg_09": {
                        "offset": 0x0009,
                        "default": 0x38,
                    },
                    "Reg_0A": {
                        "offset": 0x000A,
                        "default": 0x38,
                    },
                    "Reg_0B": {
                        "offset": 0x000B,
                        "default": 0x3F,
                    },
                    "Reg_0C": {
                        "offset": 0x000C,
                        "default": 0x02,
                    },
                    "Reg_0D": {
                        "offset": 0x000D,
                        "default": 0x00,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_0E": {
                        "offset": 0x000E,
                        "default": 0x00,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_0F": {
                        "offset": 0x000F,
                        "default": 0x00,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_10": {
                        "offset": 0x0010,
                        "default": 0x00,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_11": {
                        "offset": 0x0011,
                        "default": 0x00,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_12": {
                        "offset": 0x0012,
                        "default": 0x00,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_13": {
                        "offset": 0x0013,
                        "default": 0x00,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_14": {
                        "offset": 0x0014,
                        "default": 0x00,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_15": {
                        "offset": 0x0015,
                        "default": 0x00,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_16": {
                        "offset": 0x0016,
                        "default": 0x00,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_17": {
                        "offset": 0x0017,
                        "default": 0x00,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_18": {
                        "offset": 0x0018,
                        "default": 0x00,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_19": {
                        "offset": 0x0019,
                        "default": 0x00,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_1A": {
                        "offset": 0x001A,
                        "default": 0x00,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_1B": {
                        "offset": 0x001B,
                        "default": 0x00,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_1C": {
                        "offset": 0x001C,
                        "default": 0x00,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_1D": {
                        "offset": 0x001D,
                        "default": 0x00,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_1E": {
                        "offset": 0x001E,
                        "default": 0x00,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_1F": {
                        "offset": 0x001F,
                        "default": 0x00,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_20": {
                        "offset": 0x0020,
                        "default": 0x00,
                        "read_only": True,
                    },
                    "Reg_21": {
                        "offset": 0x0021,
                        "default": 0x00,
                        "read_only": True,
                    },
                    "Reg_22": {
                        "offset": 0x0022,
                        "default": 0x00,
                        "read_only": True,
                    },
                    "Reg_23": {
                        "offset": 0x0023,
                        "default": 0x00,
                        "read_only": True,
                    },
                    "Reg_24": {
                        "offset": 0x0024,
                        "default": 0x00,
                        "read_only": True,
                    },
                    "Reg_25": {
                        "offset": 0x0025,
                        "default": 0x00,
                        "read_only": True,
                    },
                    "Reg_26": {
                        "offset": 0x0026,
                        "default": 0x00,
                        "read_only": True,
                    },
                    "Reg_27": {
                        "offset": 0x0027,
                        "default": 0x00,
                        "read_only": True,
                    },
                    "Reg_28": {
                        "offset": 0x0028,
                        "default": 0x00,
                        "read_only": True,
                    },
                    "Reg_29": {
                        "offset": 0x0029,
                        "default": 0x00,
                        "read_only": True,
                    },
                    "Reg_2A": {
                        "offset": 0x002A,
                        "default": 0x00,
                        "read_only": True,
                    },
                    "Reg_2B": {
                        "offset": 0x002B,
                        "default": 0x00,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_2C": {
                        "offset": 0x002C,
                        "default": 0x00,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_2D": {
                        "offset": 0x002D,
                        "default": 0x00,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_2E": {
                        "offset": 0x002E,
                        "default": 0x00,
                        "read_only": True,
                        "display": False,
                    },
                    "Reg_2F": {
                        "offset": 0x002F,
                        "default": 0x00,
                        "read_only": True,
                        "display": False,
                    },
                },
            },
        },
    },
}

register_decoding = {
    "Array_Reg_A": {  # Address Space (i.e. separate I2C memory spaces)
        "Register Blocks": {
            "Registers": {  # Register Block (i.e. group of registers to be handled as one unit)
                "EN_DiscriOut": {
                    "bits": 8,
                    "position": [
                        (
                            "Reg_A_04",
                            "7-0",
                            "7-0",
                        ),  # The tuple should be 1st position is the register, 2nd position the bits in the register, 3rd position the bits in the value
                    ],
                    "info": "{0} enables the discriminator output, active high.\n Each bit in {0}[7:4] represents the row, and each bit in {0}[3:0] represents the column. Users can enable the discriminator output for a specified pixel. Only one row can be specified at a time. That means no more than one bit in {0}[7:4] can be set to 1 at a time.\n When more than one bit is set to 1, or all bits are set to 0 in {0}[3:0], the discriminator output is disabled.\n\nFor example:\n - 0b0010_0100→pixel in row 1 and column 2\n - 0b0001_0001→pixel in row 0 and column 0\n - 0b1000_0100→pixel in row 3 and column 2\n - 0bxxxx_0101→disable discriminator output, but invalid\n - 0b1011_xxxx→invalid\n - 0b0000_0111→disable discriminator output\n - 0b0000_0000→disable discriminator output",
                    "show_binary": "New Line",
                },
                "EN_DiscriOut_Row": {
                    "bits": 4,
                    "position": [
                        ("Reg_A_04", "7-4", "3-0"),
                    ],
                    "show_binary": True,
                },
                "EN_DiscriOut_Column": {
                    "bits": 4,
                    "position": [
                        ("Reg_A_04", "3-0", "3-0"),
                    ],
                    "show_binary": True,
                },
                "DIS_VTHInOut": {
                    "bits": 16,
                    "position": [
                        ("Reg_A_03", "7-0", "15-8"),
                        ("Reg_A_02", "7-0", "7-0"),
                    ],
                    "info": "{0} disables the threshold voltage input/output of the specified pixel, active high. Each bit controls a pixel according the pixels index map.\nOnly one of thresholds can be enabled at a time.\nFor example: DIS_VTHInOut = 0x4000.",
                    "show_binary": "New Line",
                },
                "EN_QInj": {
                    "bits": 16,
                    "position": [
                        ("Reg_A_06", "7-0", "15-8"),
                        ("Reg_A_05", "7-0", "7-0"),
                    ],
                    "info": "{0} enables the charge injection of the specified pixel, active high.\n Each bit controls a pixel.\n Users can specify none or more pixels to enable the charge injection.",
                    "show_binary": "New Line",
                },
                "PD_DACDiscri": {
                    "bits": 16,
                    "position": [
                        ("Reg_A_09", "7-0", "15-8"),
                        ("Reg_A_08", "7-0", "7-0"),
                    ],
                    "info": "{0} powers down the DAC and the discriminator in pixels, active high.\n Each bit controls a pixel.\n Users can specify none or more pixels to control.",
                    "show_binary": "New Line",
                },
                "ROI": {
                    "bits": 16,
                    "position": [
                        ("Reg_A_1F", "7-0", "15-8"),
                        ("Reg_A_1E", "7-0", "7-0"),
                    ],
                    "info": "{0} defines the region of interest. 16-bit vector specifies which pixels are enabled for readout.",
                    "show_binary": "New Line",
                },
                "OE_DMRO_Row": {
                    "bits": 4,
                    "position": [("Reg_A_07", "3-0", "3-0")],
                    "info": "{0} enables the output of DMRO in rows. Each bit represents a row. Only one row can be enabled for output at a time.\nFor example:\n - 0b0000→no DMRO output enabled\n - 0b0001→the row 0 of DMRO output is enabled\n - 0b0100→the row 2 of DMRO output is enabled\n - 0b1010→invalid",
                    "show_binary": True,
                },
                "DMRO_COL": {
                    "bits": 2,
                    "position": [("Reg_A_07", "5-4", "1-0")],
                    "info": "{0} selects DMRO output from a specified column:\n - 0b00→column 0\n - 0b01→column 1\n - 0b10→column 2\n - 0b11→column 3",
                    "show_binary": True,
                },
                "RO_SEL": {
                    "bits": 1,
                    "position": [("Reg_A_07", "6", "0")],
                    "info": "{0} selects readout mode from either SRO or DMRO:\n - Low→DMRO enabled\n - High→SRO enabled",
                },
                "CLSel": {
                    "bits": 2,
                    "position": [("Reg_A_00", "1-0", "1-0")],
                    "info": "Shared by all pixels.\n{0} selects the load capacitance of the preamp first stage:\n - 0b00: 0 fC\n - 0b01: 80 fC\n - 0b10: 80 fC\n - 0b11: 160 fC",
                    "show_binary": False,
                },
                "RfSel": {
                    "bits": 2,
                    "position": [
                        ("Reg_A_00", "3-2", "1-0"),
                    ],
                    "info": "Shared by all pixels.\n{0} selects the feedback resistance:\n - 0b00 --> 20 kOHm\n - 0b01--> 10 kOHm\n - 0b10--> 5.7 kOHm\n - 0b11--> 4.4 kOHm",
                    "show_binary": False,
                },
                "HysSel": {
                    "bits": 4,
                    "position": [
                        ("Reg_A_00", "7-4", "3-0"),
                    ],
                    "info": "Shared by all pixels.\n{0} selects the hysteresis voltage:\n - 0b0000 --> Vhys1\n - 0b0001 --> Vhys2\n - 0b0011 --> Vhys3\n - 0b0111 --> Vhys4\n - 0b1111 --> Vhys5\nVhys1 > Vhys2 > Vhys3 > Vhys4 = Vhys5 = 0",
                    "show_binary": False,
                },
                "IBSel": {
                    "bits": 3,
                    "position": [
                        ("Reg_A_01", "2-0", "2-0"),
                    ],
                    "info": "Shared by all pixels.\n{0} selects the bias current of the input transistor in the preamp:\n - 0b000 --> I1\n - 0b001, 0b010, 0b100 --> I2\n - 0b011, 0b110, 0b101 --> I3\n - 0b111 --> I4\nI1 > I2 > I3 > I4",
                    "show_binary": False,
                },
                "QSel": {
                    "bits": 5,
                    "position": [
                        ("Reg_A_01", "7-3", "4-0"),
                    ],
                    "info": "Shared by all pixels.\n{0} selects the injected charge, from 1 fC(0b00000) to 32 fC(0b11111).\nTypical charge from LGAD sensor is 7 fC(0b00110)",
                    "show_binary": True,
                },
                "VTHIn_Pix0": {
                    "bits": 10,
                    "position": [
                        ("Reg_A_0A", "7-0", "7-0"),
                        ("Reg_A_0B", "1-0", "9-8"),
                    ],
                    "info": "{0} is the threshold voltage input of pixel 0",
                    "show_binary": "New Line",
                },
                "VTHIn_Pix1": {
                    "bits": 10,
                    "position": [
                        ("Reg_A_0B", "7-2", "5-0"),
                        ("Reg_A_0C", "3-0", "9-6"),
                    ],
                    "info": "{0} is the threshold voltage input of pixel 1",
                    "show_binary": "New Line",
                },
                "VTHIn_Pix2": {
                    "bits": 10,
                    "position": [
                        ("Reg_A_0C", "7-4", "3-0"),
                        ("Reg_A_0D", "5-0", "9-4"),
                    ],
                    "info": "{0} is the threshold voltage input of pixel 2",
                    "show_binary": "New Line",
                },
                "VTHIn_Pix3": {
                    "bits": 10,
                    "position": [
                        ("Reg_A_0D", "7-6", "1-0"),
                        ("Reg_A_0E", "7-0", "9-2"),
                    ],
                    "info": "{0} is the threshold voltage input of pixel 3",
                    "show_binary": "New Line",
                },
                "VTHIn_Pix4": {
                    "bits": 10,
                    "position": [
                        ("Reg_A_0F", "7-0", "7-0"),
                        ("Reg_A_10", "1-0", "9-8"),
                    ],
                    "info": "{0} is the threshold voltage input of pixel 4",
                    "show_binary": "New Line",
                },
                "VTHIn_Pix5": {
                    "bits": 10,
                    "position": [
                        ("Reg_A_10", "7-2", "5-0"),
                        ("Reg_A_11", "3-0", "9-6"),
                    ],
                    "info": "{0} is the threshold voltage input of pixel 5",
                    "show_binary": "New Line",
                },
                "VTHIn_Pix6": {
                    "bits": 10,
                    "position": [
                        ("Reg_A_11", "7-4", "3-0"),
                        ("Reg_A_12", "5-0", "9-4"),
                    ],
                    "info": "{0} is the threshold voltage input of pixel 6",
                    "show_binary": "New Line",
                },
                "VTHIn_Pix7": {
                    "bits": 10,
                    "position": [
                        ("Reg_A_12", "7-6", "1-0"),
                        ("Reg_A_13", "7-0", "9-2"),
                    ],
                    "info": "{0} is the threshold voltage input of pixel 7",
                    "show_binary": "New Line",
                },
                "VTHIn_Pix8": {
                    "bits": 10,
                    "position": [
                        ("Reg_A_14", "7-0", "7-0"),
                        ("Reg_A_15", "1-0", "9-8"),
                    ],
                    "info": "{0} is the threshold voltage input of pixel 8",
                    "show_binary": "New Line",
                },
                "VTHIn_Pix9": {
                    "bits": 10,
                    "position": [
                        ("Reg_A_15", "7-2", "5-0"),
                        ("Reg_A_16", "3-0", "9-6"),
                    ],
                    "info": "{0} is the threshold voltage input of pixel 9",
                    "show_binary": "New Line",
                },
                "VTHIn_Pix10": {
                    "bits": 10,
                    "position": [
                        ("Reg_A_16", "7-4", "3-0"),
                        ("Reg_A_17", "5-0", "9-4"),
                    ],
                    "info": "{0} is the threshold voltage input of pixel 10",
                    "show_binary": "New Line",
                },
                "VTHIn_Pix11": {
                    "bits": 10,
                    "position": [
                        ("Reg_A_17", "7-6", "1-0"),
                        ("Reg_A_18", "7-0", "9-2"),
                    ],
                    "info": "{0} is the threshold voltage input of pixel 11",
                    "show_binary": "New Line",
                },
                "VTHIn_Pix12": {
                    "bits": 10,
                    "position": [
                        ("Reg_A_19", "7-0", "7-0"),
                        ("Reg_A_1A", "1-0", "9-8"),
                    ],
                    "info": "{0} is the threshold voltage input of pixel 12",
                    "show_binary": "New Line",
                },
                "VTHIn_Pix13": {
                    "bits": 10,
                    "position": [
                        ("Reg_A_1A", "7-2", "5-0"),
                        ("Reg_A_1B", "3-0", "9-6"),
                    ],
                    "info": "{0} is the threshold voltage input of pixel 13",
                    "show_binary": "New Line",
                },
                "VTHIn_Pix14": {
                    "bits": 10,
                    "position": [
                        ("Reg_A_1B", "7-4", "3-0"),
                        ("Reg_A_1C", "5-0", "9-4"),
                    ],
                    "info": "{0} is the threshold voltage input of pixel 14",
                    "show_binary": "New Line",
                },
                "VTHIn_Pix15": {
                    "bits": 10,
                    "position": [
                        ("Reg_A_1C", "7-6", "1-0"),
                        ("Reg_A_1D", "7-0", "9-2"),
                    ],
                    "info": "{0} is the threshold voltage input of pixel 15",
                    "show_binary": "New Line",
                },
                "dllLate": {
                    "bits": 1,
                    "position": [
                        ("Reg_A_20", "0", "0"),
                    ],
                    "info": "{0} is the lock status prompt",
                    "read_only": True,
                },
            },
        }
    },
    "Array_Reg_B": {  # Address Space (i.e. separate I2C memory spaces)
        "Register Blocks": {
            "Registers": {  # Register Block (i.e. group of registers to be handled as one unit)
                "autoReset_TDC": {
                    "bits": 1,
                    "position": [
                        ("Reg_B_00", "0", "0")
                    ],  # The tuple should be 1st position is the register, 2nd position the bits in the register, 3rd position the bits in the value
                },
                "enableMon_TDC": {
                    "bits": 1,
                    "position": [("Reg_B_00", "1", "0")],
                    "info": "This bit is actually used to control the readout test mode in ROTestGen.",
                },
                "enable_TDC": {
                    "bits": 1,
                    "position": [("Reg_B_00", "2", "0")],
                },
                "polaritySel_TDC": {
                    "bits": 1,
                    "position": [("Reg_B_00", "3", "0")],
                },
                "resetn_TDC": {
                    "bits": 1,
                    "position": [("Reg_B_00", "4", "0")],
                },
                "selRawCode_TDC": {
                    "bits": 1,
                    "position": [("Reg_B_00", "5", "0")],
                },
                "testMode_TDC": {
                    "bits": 1,
                    "position": [("Reg_B_00", "6", "0")],
                },
                "timeStampMode_TDC": {
                    "bits": 1,
                    "position": [("Reg_B_00", "7", "0")],
                },
                "level_TDC": {
                    "bits": 3,
                    "position": [("Reg_B_01", "2-0", "2-0")],
                },
                "offset_TDC": {
                    "bits": 7,
                    "position": [("Reg_B_02", "6-0", "6-0")],
                },
                "dllEnable": {
                    "bits": 1,
                    "position": [("Reg_B_03", "0", "0")],
                    "info": "{0} enables loop control of DLL. The control voltage is tied to ground when dllEnable==low.",
                },
                "dllForceDown": {
                    "bits": 1,
                    "position": [("Reg_B_03", "1", "0")],
                    "info": "{0} forces to pull down the output of the phase detector, active high.",
                },
                "dllCapReset": {
                    "bits": 1,
                    "position": [("Reg_B_03", "2", "0")],
                    "info": "{0} resets the control voltage of DLL to power supply, active high.",
                },
                "dllCPCurrent": {
                    "bits": 4,
                    "position": [("Reg_B_03", "6-3", "3-0")],
                    "info": "{0} is the charge pump current control bits, ranging from 0 to 15uA for charge and discharge.",
                },
                "PhaseAdj": {
                    "bits": 8,
                    "position": [("Reg_B_04", "7-0", "7-0")],
                    "info": "{0} is the Phase selecting control bits, {0}[7:3] for coarse, {0}[2:0] for fine.",
                    "show_binary": "New Line",
                },
                "RefStrSel": {"bits": 8, "position": [("Reg_B_05", "7-0", "7-0")], "info": "{0} is the TDC reference strobe selection."},
                "ENScr_DMRO": {"bits": 1, "position": [("Reg_B_06", "0", "0")], "info": "{0} enables scrambling, active high."},
                "REVCLK_DMRO": {
                    "bits": 1,
                    "position": [("Reg_B_06", "1", "0")],
                    "info": "{0} reverses the clock used for input data latch, active-high. When REVData=0 data is latched at the rising edges of CLKWord, otherwise data is latched at the falling edges of CLKWord.",
                },
                "REVData_DMRO": {"bits": 1, "position": [("Reg_B_06", "2", "0")], "info": "{0} reverses input data, active-high."},
                "TestMode_DMRO": {
                    "bits": 1,
                    "position": [("Reg_B_06", "3", "0")],
                    "info": "{0} is the test mode input, active high. The PRBS7 is sent out in test mode (TestMode == 1) while the data is sent out in normal mode (TestMode == 0).",
                },
                "TestCLK0": {
                    "bits": 1,
                    "position": [("Reg_B_06", "4", "0")],
                    "info": "When {0}=1, the phase shifter is bypassed and off-chip 40MHz and 320MHz are used.",
                },
                "TestCLK1": {
                    "bits": 1,
                    "position": [("Reg_B_06", "5", "0")],
                    "info": "When {0}=1, the TDC reference strobe generator is bypassed and off-chip 40MHz and 320MHz are used.",
                },
                "CLKOutSel": {
                    "bits": 1,
                    "position": [("Reg_B_06", "6", "0")],
                    "info": "{0} selects output from either 40 MHz clock or TDC reference strobe:\n - 0b0: 40 MHz clock\n - 0b1: TDC reference strobe",
                },
                "enableRx_1P28G": {
                    "bits": 1,
                    "position": [("Reg_B_07", "5", "0")],
                    "info": "{0} enables the Rx for 1.28 GHz clock, active high",
                },
                "setCM_1P28G": {
                    "bits": 1,
                    "position": [("Reg_B_07", "4", "0")],
                    "info": "{0} sets the common voltage of the Rx for the 1.28 GHz clock to 1/2 vdd, active high",
                },
                "enableTER_1P28G": {
                    "bits": 1,
                    "position": [("Reg_B_07", "3", "0")],
                    "info": "{0} enables internal termination of the Rx for the 1.28 GHz clock, active high",
                },
                "invertData_1P28G": {
                    "bits": 1,
                    "position": [("Reg_B_07", "2", "0")],
                    "info": "{0} inverts data of the Rx for the 1.28 GHz clock, active high",
                },
                "equ_1P28G": {
                    "bits": 2,
                    "position": [("Reg_B_07", "1-0", "1-0")],
                    "info": "{0} sets the equalization strength of the Rx for the 320 MHz clock\n - 0b00, equalization is turned off\n - 0b11, largest equalization",
                },
                "enableRx_320M": {
                    "bits": 1,
                    "position": [("Reg_B_08", "5", "0")],
                    "info": "{0} enables the Rx for the 320 MHz clock, active high",
                },
                "setCM_320M": {
                    "bits": 1,
                    "position": [("Reg_B_08", "4", "0")],
                    "info": "{0} sets the common voltage of the Rx for the 320 MHz clock to 1/2 vdd, active high",
                },
                "enableTER_320M": {
                    "bits": 1,
                    "position": [("Reg_B_08", "3", "0")],
                    "info": "{0} enables internal termination of the Rx for the 320 MHz clock, active high",
                },
                "invertData_320M": {
                    "bits": 1,
                    "position": [("Reg_B_08", "2", "0")],
                    "info": "{0} inverts data of the Rx for the 320 MHz clock, active high",
                },
                "equ_320M": {
                    "bits": 2,
                    "position": [("Reg_B_08", "1-0", "1-0")],
                    "info": "{0} set the equalization strength of the Rx for the 320 MHz clock\n - 0b00, equalization is turned off\n - 0b11, largest equalization",
                },
                "enableRx_40M": {
                    "bits": 1,
                    "position": [("Reg_B_09", "5", "0")],
                    "info": "{0} enables the Rx for the 40 MHz clock, active high",
                },
                "setCM_40M": {
                    "bits": 1,
                    "position": [("Reg_B_09", "4", "0")],
                    "info": "{0} sets the common voltage of the Rx for the 40 MHz clock to 1/2 vdd, active high",
                },
                "enableTER_40M": {
                    "bits": 1,
                    "position": [("Reg_B_09", "3", "0")],
                    "info": "{0} enables the internal termination of the Rx for the 40 MHz clock, active high",
                },
                "invertData_40M": {
                    "bits": 1,
                    "position": [("Reg_B_09", "2", "0")],
                    "info": "{0} inverts the data of the Rx for the 40 MHz clock, active high",
                },
                "equ_40M": {
                    "bits": 2,
                    "position": [("Reg_B_09", "1-0", "1-0")],
                    "info": "{0} sets the equalization strength of the Rx for the 40 MHz clock\n - 0b00, equalization is turned off\n - 0b11, largest equalization",
                },
                "enableRx_QInj": {"bits": 1, "position": [("Reg_B_0A", "5", "0")], "info": "{0} enables the Rx for the QInj, active high"},
                "setCM_QInj": {
                    "bits": 1,
                    "position": [("Reg_B_0A", "4", "0")],
                    "info": "{0} sets the common voltage of the Rx for the QInj to 1/2 vdd, active high",
                },
                "enableTER_QInj": {
                    "bits": 1,
                    "position": [("Reg_B_0A", "3", "0")],
                    "info": "{0} enables internal termination of the Rx for the QInj, active high",
                },
                "invertData_QInj": {
                    "bits": 1,
                    "position": [("Reg_B_0A", "2", "0")],
                    "info": "{0} inverts data of the Rx for the QInj, active high",
                },
                "equ_QInj": {
                    "bits": 2,
                    "position": [("Reg_B_0A", "1-0", "1-0")],
                    "info": "{0} sets the equalization strength of the Rx for the QInj\n - 0b00, equalization is turned off\n - 0b11, largest equalization",
                },
                "AMPL_CLKTO": {
                    "bits": 3,
                    "position": [("Reg_B_0B", "2-0", "2-0")],
                    "info": "3bits to select different output amplitude.\n - 0b000 = min amplitude(50m)\n - 0b111 = max amplitude(320m)\n(Step size ≈ 40mV)",
                },
                "disCML_CLKTO": {"bits": 1, "position": [("Reg_B_0B", "3", "0")], "info": "{0} disables the CML driver, active high"},
                "AMPL_DOut": {
                    "bits": 3,
                    "position": [("Reg_B_0B", "6-4", "2-0")],
                    "info": "3bits to select different output amplitude.\n - 0b000 = min amplitude(50m)\n - 0b111 = max amplitude(320m)\n(Step size ≈ 40mV)",
                },
                "disCML_DOut": {"bits": 1, "position": [("Reg_B_0B", "7", "0")], "info": "{0} disables the CML driver, active high"},
            },
        }
    },
    "Full_Pixel": {  # Address Space (i.e. separate I2C memory spaces)
        "Register Blocks": {
            "Registers": {  # Register Block (i.e. group of registers to be handled as one unit)
                "autoReset_TDC": {
                    "bits": 1,
                    "position": [
                        ("Reg_00", "0", "0")
                    ],  # The tuple should be 1st position is the register, 2nd position the bits in the register, 3rd position the bits in the value
                    "info": "TDC autoReset mode",
                },
                "enableMon_TDC": {"bits": 1, "position": [("Reg_00", "1", "0")], "info": "Control of readout test mode in ROTestGen"},
                "enable_TDC": {"bits": 1, "position": [("Reg_00", "2", "0")], "info": "Enable TDC"},
                "polaritySel_TDC": {"bits": 1, "position": [("Reg_00", "3", "0")], "info": "TDC Controller control signal polarity select"},
                "resetn_TDC": {"bits": 1, "position": [("Reg_00", "4", "0")], "info": "Reset TDC, low active"},
                "selRawCode_TDC": {"bits": 1, "position": [("Reg_00", "5", "0")], "info": "Select Row data or combination data"},
                "testMode_TDC": {"bits": 1, "position": [("Reg_00", "6", "0")], "info": "TDC test mode select"},
                "timeStampMode_TDC": {"bits": 1, "position": [("Reg_00", "7", "0")], "info": "Calibration data timestamp mode"},
                "level_TDC": {"bits": 3, "position": [("Reg_01", "2-0", "2-0")], "info": "Bubble level"},
                "offset_TDC": {"bits": 7, "position": [("Reg_02", "6-0", "6-0")], "info": "Ripple counter window offest"},
                "dllEnable": {
                    "bits": 1,
                    "position": [("Reg_03", "0", "0")],
                    "info": "{0} enables loop control of DLL. The control voltage is tied to ground when {0}==low.",
                },
                "dllForceDown": {
                    "bits": 1,
                    "position": [("Reg_03", "1", "0")],
                    "info": "Force to pull down the output of the phase detector, active high.",
                },
                "dllCapReset": {
                    "bits": 1,
                    "position": [("Reg_03", "2", "0")],
                    "info": "Reset the control voltage of DLL to power supply, active high.",
                },
                "dllCPCurrent": {
                    "bits": 4,
                    "position": [("Reg_03", "6-3", "3-0")],
                    "info": "Charge pump current control bits, ranging from 0 to 15uA for charge and discharge.",
                },
                "PhaseAdj": {
                    "bits": 8,
                    "position": [("Reg_04", "7-0", "7-0")],
                    "info": "Phase selecting control bits, PhaseAdj <7:3> for coarse, PhaseAdj <2:0> for fine.",
                    "show_binary": True,
                },
                "RefStrSel": {
                    "bits": 8,
                    "position": [("Reg_05", "7-0", "7-0")],
                    "info": "TDC reference strobe selection.",
                    "show_binary": True,
                },
                "RSTN_DMRO": {"bits": 1, "position": [("Reg_06", "0", "0")], "info": "DMRO Reset, active low"},
                "ENScr_DMRO": {"bits": 1, "position": [("Reg_06", "1", "0")], "info": "Enable scrambling, active high"},
                "REVCLK_DMRO": {
                    "bits": 1,
                    "position": [("Reg_06", "2", "0")],
                    "info": "Reversing the clock used for input data latch, active-high. When REVData=0 data is latched at the rising edges of CLKWord, otherwise data is latched at the falling edges of CLKWord.",
                },
                "REVData_DMRO": {"bits": 1, "position": [("Reg_06", "3", "0")], "info": "reversing input data, active- high"},
                "TestMode_DMRO": {
                    "bits": 1,
                    "position": [("Reg_06", "4", "0")],
                    "info": "Test mode input, active high. The PRBS7 is sent out in test mode (TestMode == 1) while the data is sent out in normal mode (TestMode == 1).",
                },
                "TestCLK0": {
                    "bits": 1,
                    "position": [("Reg_06", "5", "0")],
                    "info": "When TestCLK0=1, the phase shifter is bypassed and off-chip 40MHz and 320MHz are used.",
                },
                "TestCLK1": {
                    "bits": 1,
                    "position": [("Reg_06", "6", "0")],
                    "info": "When TestCLK1=1, the TDC reference strobe generator is bypassed and off-chip 40MHz and 320MHz are used.",
                },
                "CLKOutSel": {
                    "bits": 1,
                    "position": [("Reg_06", "7", "0")],
                    "info": "Select output from either 40 MHz clock or TDC reference strobe:\n - 0b0: 40 MHz clock\n - 0b1: TDC reference strobe",
                },
                "enableRx_1P28G": {"bits": 1, "position": [("Reg_07", "5", "0")], "info": "Enable the Rx for 1.28 GHz clock, active high"},
                "setCM_1P28G": {
                    "bits": 1,
                    "position": [("Reg_07", "4", "0")],
                    "info": "Set common voltage of the Rx for the 1.28 GHz clock to 1/2 vdd, active high",
                },
                "enableTER_1P28G": {
                    "bits": 1,
                    "position": [("Reg_07", "3", "0")],
                    "info": "Enable internal termination of the Rx for the 1.28 GHz clock, active high",
                },
                "invertData_1P28G": {
                    "bits": 1,
                    "position": [("Reg_07", "2", "0")],
                    "info": "Invert data of the Rx for the 1.28 GHz clock, active high",
                },
                "equ_1P28G": {
                    "bits": 2,
                    "position": [("Reg_07", "1-0", "1-0")],
                    "info": "Equalization strength of the Rx for the 1.28 GHz clock:\n - 0b00, equalization is turned off\n - 0b11, largest equalization",
                },
                "enableRx_320M": {"bits": 1, "position": [("Reg_08", "5", "0")], "info": "Enable the Rx for 320 MHz clock, active high"},
                "setCM_320M": {
                    "bits": 1,
                    "position": [("Reg_08", "4", "0")],
                    "info": "Set common voltage of the Rx for the 320 MHz clock to 1/2 vdd, active high",
                },
                "enableTER_320M": {
                    "bits": 1,
                    "position": [("Reg_08", "3", "0")],
                    "info": "Enable internal termination of the Rx for the 320 MHz clock, active high",
                },
                "invertData_320M": {
                    "bits": 1,
                    "position": [("Reg_08", "2", "0")],
                    "info": "Invert data of the Rx for the 320 MHz clock, active high",
                },
                "equ_320M": {
                    "bits": 2,
                    "position": [("Reg_08", "1-0", "1-0")],
                    "info": "Equalization strength of the Rx for the 320 MHz clock:\n - 0b00, equalization is turned off\n - 0b11, largest equalization",
                },
                "enableRx_40M": {"bits": 1, "position": [("Reg_09", "5", "0")], "info": "Enable the Rx for 40 MHz clock, active high"},
                "setCM_40M": {
                    "bits": 1,
                    "position": [("Reg_09", "4", "0")],
                    "info": "Set common voltage of the Rx for the 40 MHz clock to 1/2 vdd, active high",
                },
                "enableTER_40M": {
                    "bits": 1,
                    "position": [("Reg_09", "3", "0")],
                    "info": "Enable internal termination of the Rx for the 40 MHz clock, active high",
                },
                "invertData_40M": {
                    "bits": 1,
                    "position": [("Reg_09", "2", "0")],
                    "info": "Invert data of the Rx for the 40 MHz clock, active high",
                },
                "equ_40M": {
                    "bits": 2,
                    "position": [("Reg_09", "1-0", "1-0")],
                    "info": "Equalization strength of the Rx for the 40 MHz clock:\n - 0b00, equalization is turned off\n - 0b11, largest equalization",
                },
                "enableRx_QInj": {"bits": 1, "position": [("Reg_0A", "5", "0")], "info": "Enable the Rx for the QInj, active high"},
                "setCM_QInj": {
                    "bits": 1,
                    "position": [("Reg_0A", "4", "0")],
                    "info": "Set common voltage of the Rx for the QInj to 1/2 vdd, active high",
                },
                "enableTER_QInj": {
                    "bits": 1,
                    "position": [("Reg_0A", "3", "0")],
                    "info": "Enable internal termination of the Rx for the QInj, active high",
                },
                "invertData_QInj": {
                    "bits": 1,
                    "position": [("Reg_0A", "2", "0")],
                    "info": "Invert data of the Rx for the QInj, active high",
                },
                "equ_QInj": {
                    "bits": 2,
                    "position": [("Reg_0A", "1-0", "1-0")],
                    "info": "Equalization strength of the Rx for the QInj:\n - 0b00, equalization is turned off\n - 0b11, largest equalization",
                },
                "AMPL_CLKTO": {
                    "bits": 3,
                    "position": [("Reg_0B", "2-0", "2-0")],
                    "info": "3bits to select different output amplitude.\n - 0b000 = min amplitude(50m)\n - 0b111 = max amplitude(320m)\nStep size ≈ 40mV",
                },
                "disCML_CLKTO": {"bits": 1, "position": [("Reg_0B", "3", "0")], "info": "Disable CML driver, active high"},
                "AMPL_DOut": {
                    "bits": 3,
                    "position": [("Reg_0B", "6-4", "2-0")],
                    "info": "3bits to select different output amplitude.\n - 0b000 = min amplitude(50m)\n - 0b111 = max amplitude(320m)\nStep size ≈ 40mV",
                },
                "disCML_DOut": {"bits": 1, "position": [("Reg_0B", "7", "0")], "info": "Disable CML driver, active high"},
                "CLSel": {
                    "bits": 2,
                    "position": [("Reg_0C", "1-0", "1-0")],
                    "info": "Select of load capacitance of the preamp first stage:\n - 0b00--> 0 fC\n - 0b01--> 80 fC\n - 0b10--> 80 fC\n - 0b01--> 160 fC",
                },
                "RfSel": {
                    "bits": 2,
                    "position": [("Reg_0C", "3-2", "1-0")],
                    "info": "Feedback resistance selection:\n - 0b00--> 20 kOHm\n - 0b01--> 10 kOHm\n - 0b10--> 5.7 kOHm\n - 0b11--> 4.4 kOHm",
                },
                "HysSel": {
                    "bits": 4,
                    "position": [("Reg_0C", "7-4", "3-0")],
                    "info": "Hysteresis voltage selection:\n - 0b0000 --> Vhys1\n - 0b0001 --> Vhys2\n - 0b0011 --> Vhys3\n - 0b0111 --> Vhys4\n - 0b1111 --> Vhys5\nVhys1 > Vhys2 > Vhys3 > Vhys4 = Vhys5 = 0",
                },
                "IBSel": {
                    "bits": 3,
                    "position": [("Reg_0D", "2-0", "2-0")],
                    "info": "Bias current selection of the input transistor in the preamp:\n - 0b000 --> I1\n - 0b001, 0b010, 0b100 --> I2\n - 0b011, 0b110, 0b101 --> I3\n - 0b111 --> I4\nI1 > I2 > I3 > I4",
                },
                "QSel": {
                    "bits": 5,
                    "position": [("Reg_0D", "7-3", "4-0")],
                    "info": "Select injected charge, from 1 fC(0b00000) to 32 fC(0b11111)\nTypical charge from LGAD sensor is 7 fC(0b00111)",
                },
                "VTHIn": {
                    "bits": 10,
                    "position": [
                        ("Reg_0E", "7-0", "7-0"),
                        ("Reg_0F", "1-0", "9-8"),
                    ],
                    "info": "Threshold voltage input of Discriminator , VTHIn[9:0] represents DAC setting",
                    "show_binary": True,
                },
                "EN_QInj": {"bits": 1, "position": [("Reg_0F", "2", "0")], "info": "enable the charge injection"},
                "EN_DiscriOut": {"bits": 1, "position": [("Reg_0F", "3", "0")], "info": "Enable Discriminator Output"},
                "Dis_VTHInOut": {"bits": 1, "position": [("Reg_0F", "4", "0")], "info": "Disable VTHIn Output"},
                "PD_DACDiscri": {
                    "bits": 1,
                    "position": [("Reg_0F", "5", "0")],
                    "info": "Power down the DAC and the discriminator, active low",
                },
                "OE_DMRO": {"bits": 1, "position": [("Reg_0F", "6", "0")], "info": "Output enable of DMRO"},
                "dllLate": {"bits": 1, "position": [("Reg_20", "0", "0")], "info": "Lock status prompt.", "read_only": True},
            },
        }
    },
    "TDC_Test_Block": {  # Address Space (i.e. separate I2C memory spaces)
        "Register Blocks": {
            "Registers": {  # Register Block (i.e. group of registers to be handled as one unit)
                "Dataout_disCMLDriver_BIAS": {
                    "bits": 1,
                    "position": [
                        ("Reg_00", "0", "0")
                    ],  # The tuple should be 1st position is the register, 2nd position the bits in the register, 3rd position the bits in the value
                    "info": "Disable Dataout CML Driver",
                },
                "Clk40Mout_disCMLDriver_BIAS": {"bits": 1, "position": [("Reg_00", "1", "0")], "info": "Disable Clk40M CML Driver"},
                "tdc_offset": {
                    "bits": 7,
                    "position": [("Reg_01", "6-0", "6-0")],
                    "info": "TDC ripple counter metastability window offset.",
                },
                "tdc_enable": {"bits": 1, "position": [("Reg_01", "7", "0")], "info": "TDC enable"},
                "tdc_level": {"bits": 3, "position": [("Reg_02", "2-0", "2-0")], "info": "TDC Encoder bubble tolerance."},
                "tdc_testMode": {"bits": 1, "position": [("Reg_02", "3", "0")], "info": "TDC Test Mode"},
                "tdc_selRawCode": {"bits": 1, "position": [("Reg_02", "4", "0")], "info": "Select TDC Raw code, always \"0\""},
                "tdc_resetn": {"bits": 1, "position": [("Reg_02", "5", "0")], "info": "TDC reset signal"},
                "tdc_polaritySel": {"bits": 1, "position": [("Reg_02", "6", "0")], "info": "TDC controller output signal polarity"},
                "tdc_autoReset": {"bits": 1, "position": [("Reg_02", "7", "0")], "info": "TDC automatic reset signal"},
                "Clk40Mout_AmplSel": {
                    "bits": 3,
                    "position": [("Reg_03", "2-0", "2-0")],
                    "info": "40 MHz clock CML output Amplitude select",
                },
                "tdc_enableMon": {"bits": 1, "position": [("Reg_03", "3", "0")], "info": "40 MHz clock CML output Amplitude select"},
                "tdc_timeStampMode": {"bits": 1, "position": [("Reg_03", "4", "0")], "info": "TDC Calibration data timeStamp Mode"},
                "Dataout_AmplSel": {
                    "bits": 3,
                    "position": [("Reg_04", "2-0", "2-0")],
                    "info": "1.28 GHz Serial data output Amplitude select",
                },
                "ro_testmode": {"bits": 1, "position": [("Reg_04", "3", "0")], "info": "40 MHz clock CML output Amplitude select"},
                "ro_enable": {"bits": 1, "position": [("Reg_04", "4", "0")], "info": "Enable DMRO"},
                "ro_reverse": {"bits": 1, "position": [("Reg_04", "5", "0")], "info": "DMRO output data reverse"},
                "ro_resetn": {"bits": 1, "position": [("Reg_04", "6", "0")], "info": "DMRO reset, low active"},
                "ro_revclk": {"bits": 1, "position": [("Reg_04", "7", "0")], "info": "DMRO 40 MHz clock reverse"},
                "Dataout_Sel": {
                    "bits": 1,
                    "position": [("Reg_05", "0", "0")],
                    "info": "1.28GHz data output when asserted, 320MHz clock pulse output when deserted",
                },
                "Clk320M_Psel": {
                    "bits": 1,
                    "position": [("Reg_05", "1", "0")],
                    "info": "320M Pulse clock comes from external when asserted, otherwise comes from internal",
                },
                "Clk40M_Psel": {
                    "bits": 1,
                    "position": [("Reg_05", "2", "0")],
                    "info": "40M Pulse clock comes from external when asserted, otherwise comes from internal",
                },
                "Clk320M_Sel": {
                    "bits": 1,
                    "position": [("Reg_05", "3", "0")],
                    "info": "320M clock comes from internal divider when asserted, otherwise comes from external input.",
                },
                "Clk40M_Sel": {
                    "bits": 1,
                    "position": [("Reg_05", "4", "0")],
                    "info": "40M clock comes from internal divider when asserted, otherwise comes from external input.",
                },
                "Pulse_Sel": {"bits": 8, "position": [("Reg_06", "7-0", "7-0")], "info": "320M clock pulse location select"},
                "Clk40M_equalizer": {"bits": 2, "position": [("Reg_07", "1-0", "1-0")], "info": "40M clock input eRx equalizer intensity"},
                "Clk40M_invertData": {"bits": 1, "position": [("Reg_07", "2", "0")], "info": "40M clock input eRx data invert"},
                "Clk40M_enableTermination": {
                    "bits": 1,
                    "position": [("Reg_07", "3", "0")],
                    "info": "Enable 40M clock input eRx termination",
                },
                "Clk40M_setCommonMode": {"bits": 1, "position": [("Reg_07", "4", "0")], "info": "Set 40M clock input eRx common mode"},
                "Clk40M_enableRx": {"bits": 1, "position": [("Reg_07", "5", "0")], "info": "Enable 40M clock input eRx"},
                "Clk320M_equalizer": {
                    "bits": 2,
                    "position": [("Reg_08", "1-0", "1-0")],
                    "info": "320M clock input eRx equalizer intensity",
                },
                "Clk320M_invertData": {"bits": 1, "position": [("Reg_08", "2", "0")], "info": "320M clock input eRx data invert"},
                "Clk320M_enableTermination": {
                    "bits": 1,
                    "position": [("Reg_08", "3", "0")],
                    "info": "Enable 320M clock input eRx termination",
                },
                "Clk320M_setCommonMode": {"bits": 1, "position": [("Reg_08", "4", "0")], "info": "Set 320M clock input eRx common mode"},
                "Clk320M_enableRx": {"bits": 1, "position": [("Reg_08", "5", "0")], "info": "Enable 320M clock input eRx"},
                "Clk1G28_equalizer": {
                    "bits": 2,
                    "position": [("Reg_09", "1-0", "1-0")],
                    "info": "1.28G clock input eRx equalizer intensity",
                },
                "Clk1G28_invertData": {"bits": 1, "position": [("Reg_09", "2", "0")], "info": "1.28G clock input eRx data invert"},
                "Clk1G28_enableTermination": {
                    "bits": 1,
                    "position": [("Reg_09", "3", "0")],
                    "info": "Enable 1.28G clock input eRx termination",
                },
                "Clk1G28_setCommonMode": {"bits": 1, "position": [("Reg_09", "4", "0")], "info": "Set 1.28G clock input eRx common mode"},
                "Clk1G28_enableRx": {"bits": 1, "position": [("Reg_09", "5", "0")], "info": "Enable 1.28G clock input eRx"},
                "Pulse_equalizer": {"bits": 2, "position": [("Reg_0A", "1-0", "1-0")], "info": "TDC pulse input eRx equalizer intensity"},
                "Pulse_invertData": {"bits": 1, "position": [("Reg_0A", "2", "0")], "info": "TDC pulse input eRx data invert"},
                "Pulse_enableTermination": {
                    "bits": 1,
                    "position": [("Reg_0A", "3", "0")],
                    "info": "Enable TDC pulse input eRx termination",
                },
                "Pulse_setCommonMode": {"bits": 1, "position": [("Reg_0A", "4", "0")], "info": "Set TDC pulse input eRx common mode"},
                "Pulse_enableRx": {"bits": 1, "position": [("Reg_0A", "5", "0")], "info": "Enable TDC pulse input eRx"},
                "TDCRawData_Sel": {"bits": 1, "position": [("Reg_0B", "0", "0")], "info": "TDC Raw data group select"},
                "GRO_TOT_CK": {"bits": 1, "position": [("Reg_0B", "1", "0")], "info": "GRO TOT clock"},
                "GRO_TOTRST_N": {"bits": 1, "position": [("Reg_0B", "2", "0")], "info": "GRO TOT Reset, active low"},
                "GRO_TOA_Latch": {"bits": 1, "position": [("Reg_0B", "3", "0")], "info": "GRO TOA Latch clock"},
                "GRO_TOA_CK": {"bits": 1, "position": [("Reg_0B", "4", "0")], "info": "GRO TOA clock"},
                "GRO_TOARST_N": {"bits": 1, "position": [("Reg_0B", "5", "0")], "info": "GRO TOA Reset, low active"},
                "GRO_Start": {"bits": 1, "position": [("Reg_0B", "6", "0")], "info": "GRO Start signal, high active"},
                "GROout_disCMLDriver_BIAS": {"bits": 1, "position": [("Reg_0C", "0", "0")], "info": "Disable GRO output CML Driver"},
                "GROout_AmplSel": {"bits": 3, "position": [("Reg_0C", "3-1", "2-0")], "info": "GRO output CML Driver Amplitude selection"},
            },
        }
    },
}


class ETROC1_Chip(Base_Chip):
    def __init__(
        self,
        i2c_address_a,
        i2c_address_b,
        i2c_address_full_pixel,
        i2c_address_tdc_test_block,
        i2c_connection: I2C_Connection_Helper,
        logger: logging.Logger,
    ):
        super().__init__(
            chip_name="ETROC2",
            i2c_connection=i2c_connection,
            logger=logger,
            software_version=etroc1_version,
            register_model=register_model,
            register_decoding=register_decoding,
            # indexer_info=self._indexer_info,
        )

        self._i2c_address_a = i2c_address_a
        self._i2c_address_b = i2c_address_b
        self._i2c_address_full_pixel = i2c_address_full_pixel
        self._i2c_address_tdc_test_block = i2c_address_tdc_test_block

        address_space: Address_Space_Controller = self._address_space["Array_Reg_A"]
        address_space.update_i2c_address(self._i2c_address_a)

        address_space: Address_Space_Controller = self._address_space["Array_Reg_B"]
        address_space.update_i2c_address(self._i2c_address_b)

        address_space: Address_Space_Controller = self._address_space["Full_Pixel"]
        address_space.update_i2c_address(self._i2c_address_full_pixel)

        address_space: Address_Space_Controller = self._address_space["TDC_Test_Block"]
        address_space.update_i2c_address(self._i2c_address_tdc_test_block)

    @property
    def i2c_address_a(self) -> int:
        return self._i2c_address_a

    @i2c_address_a.setter
    def i2c_address_a(self, address: int):
        self._i2c_address_a = address

        address_space: Address_Space_Controller = self._address_space["Array_Reg_A"]
        address_space.update_i2c_address(self._i2c_address_a)

    @property
    def i2c_address_b(self) -> int:
        return self._i2c_address_b

    @i2c_address_b.setter
    def i2c_address_b(self, address: int):
        self._i2c_address_b = address

        address_space: Address_Space_Controller = self._address_space["Array_Reg_B"]
        address_space.update_i2c_address(self._i2c_address_b)

    @property
    def i2c_address_full_pixel(self) -> int:
        return self._i2c_address_full_pixel

    @i2c_address_full_pixel.setter
    def i2c_address_full_pixel(self, address: int):
        self._i2c_address_full_pixel = address

        address_space: Address_Space_Controller = self._address_space["Full_Pixel"]
        address_space.update_i2c_address(self._i2c_address_full_pixel)

    @property
    def i2c_address_tdc_test_block(self) -> int:
        return self._i2c_address_tdc_test_block

    @i2c_address_tdc_test_block.setter
    def i2c_address_tdc_test_block(self, address: int):
        self._i2c_address_tdc_test_block = address

        address_space: Address_Space_Controller = self._address_space["TDC_Test_Block"]
        address_space.update_i2c_address(self._i2c_address_tdc_test_block)
