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

from ..i2c_connection_helper import I2C_Connection_Helper
from ..i2c_connection_helper import valid_endianness
from ..i2c_connection_helper import valid_read_type
from ..i2c_connection_helper import valid_write_type


class Address_Space_Controller:
    def __init__(
        self,
        name: str,
        i2c_address: int,
        address_space_size: int,
        logger: logging.Logger,
        i2c_connection: I2C_Connection_Helper,
        address_bitlength: int = 8,
        address_endianness: str = 'big',
        word_bitlength: int = 8,
        word_endianness: str = 'big',
        read_type: str = 'Normal',
        write_type: str = 'Normal',
        address_space_map: dict = {},
    ):
        self._name = name
        self._i2c_address = i2c_address
        self._address_space_size = address_space_size
        self._logger = logger

        if address_endianness not in valid_endianness:
            raise RuntimeError(f"An invalid endianness was set for the device I2C address: {address_endianness}")
        if word_endianness not in valid_endianness:
            raise RuntimeError(f"An invalid endianness was set for the device I2C word address: {word_endianness}")
        if read_type not in valid_read_type:
            raise RuntimeError(f"An invalid read type was chosen: {read_type}")
        if write_type not in valid_write_type:
            raise RuntimeError(f"An invalid write type was chosen: {write_type}")

        self._i2c_connection = i2c_connection
        self._address_bitlength = address_bitlength
        self._address_endianness = address_endianness
        self._word_bitlength = word_bitlength
        self._word_endianness = word_endianness
        self._read_type = read_type
        self._write_type = write_type

        self._not_read = True
        self._memory = [None for _ in range(self._address_space_size)]
        self._defaults = [None for _ in range(self._address_space_size)]
        self._read_only_map = [True for _ in range(self._address_space_size)]
        self._blocks = {}
        self._register_map = {}
        self._register_blocks = {}
        for block_name in address_space_map:
            if "Base Address" in address_space_map[block_name]:
                base_address = address_space_map[block_name]["Base Address"]

                self._blocks[block_name] = {
                    "Base Address": base_address,
                    "Length": len(
                        address_space_map[block_name]["Registers"]
                    ),  # Note: Assuming that all the listed registers in a block are contiguous in the memory space
                }
                if "Write Base Address" in address_space_map[block_name]:
                    self._blocks[block_name]["Write Base Address"] = address_space_map[block_name]["Write Base Address"]

                for register in address_space_map[block_name]["Registers"]:
                    offset = address_space_map[block_name]["Registers"][register]["offset"]
                    default = address_space_map[block_name]["Registers"][register]["default"]
                    full_address = base_address + offset
                    read_only = False
                    if 'read_only' in address_space_map[block_name]["Registers"][register]:
                        read_only = address_space_map[block_name]["Registers"][register]['read_only']

                    self._register_map[block_name + "/" + register] = full_address
                    self._read_only_map[full_address] = read_only
                    self._memory[full_address] = default
                    self._defaults[full_address] = default
            elif "Indexer" in address_space_map[block_name]:
                indexer_info = address_space_map[block_name]['Indexer']
                min_address, max_address, base_addresses = self._get_indexed_block_address_range(
                    block_name, indexer_info, address_space_map[block_name]['Registers']
                )

                if (
                    max_address >= min_address
                ):  # Note: even though not frequently used, a block covering the whole array is needed for bulk read/write operations
                    self._blocks[block_name] = {"Base Address": min_address, "Length": max_address - min_address + 1}

                for block_ref in base_addresses:  # Note: it is a block ref and not a block name because this is a block array
                    self._blocks[block_ref] = {
                        "Base Address": base_addresses[block_ref]['base_address'],
                        "Length": len(
                            address_space_map[block_name]["Registers"]
                        ),  # Note: Assuming that all the listed registers in a block are contiguous in the memory space
                    }

                for register in address_space_map[block_name]["Registers"]:
                    offset = address_space_map[block_name]["Registers"][register]["offset"]
                    default = address_space_map[block_name]["Registers"][register]["default"]
                    for base_name in base_addresses:
                        base_address = base_addresses[base_name]['base_address']
                        full_address = base_address + offset
                        read_only = False
                        if 'read_only' in address_space_map[block_name]["Registers"][register]:
                            read_only = address_space_map[block_name]["Registers"][register]['read_only']

                        full_register_name = base_name + "/" + register
                        self._register_map[full_register_name] = full_address
                        self._read_only_map[full_address] = read_only
                        self._memory[full_address] = default
                        self._defaults[full_address] = default

            else:
                self._logger.error(
                    "An impossible condition occured, there was a memory block defined which does not have a base address and does not have an indexer"
                )

        self._bytes_per_word = ceil(self._word_bitlength / 8)
        self._has_readonly = False
        for val in self._read_only_map:
            if val:
                self._has_readonly = True
                break

    def __len__(self):
        return self._address_space_size

    def __getitem__(self, index):
        if isinstance(index, int):
            return self._memory[index]
        elif isinstance(index, tuple):
            block_name, register_name = index
            return self._memory[self._register_map[block_name + "/" + register_name]]
        else:
            raise RuntimeError("Unknown index for address space controller get")

    def __setitem__(self, index, value):
        if isinstance(index, int):
            self._memory[index] = value
        elif isinstance(index, tuple):
            block_name, register_name = index
            self._memory[self._register_map[block_name + "/" + register_name]] = value
        else:
            raise RuntimeError("Unknown index for address space controller set")

    def __iter__(self):
        for i in self._memory:
            yield i

    def _get_indexed_block_address_range(self, block_name, indexer_info, register_map):
        indexer_function = indexer_info['function']

        block_info = {}
        for idx in range(len(indexer_info['vars'])):
            var = indexer_info['vars'][idx]
            min = indexer_info['min'][idx]
            max = indexer_info['max'][idx]

            old_block_info = block_info
            block_info = {}

            if var == "block" and min is None and max is None:
                param = block_name
                if len(old_block_info) == 0:
                    block_info[param] = {
                        'params': {'block': param},
                    }
                else:
                    for old in old_block_info:
                        block_info[old + ":" + param] = {}
                        block_info[old + ":" + param]['params'] = (old_block_info[old]['params']).copy()
                        block_info[old + ":" + param]['params']['block'] = str(param)
            else:
                for val_idx in range(max - min):
                    i = min + val_idx
                    if len(old_block_info) == 0:
                        block_info[i] = {
                            'params': {var: i},
                        }
                    else:
                        for old in old_block_info:
                            block_info[old + ":" + str(i)] = {}
                            block_info[old + ":" + str(i)]['params'] = (old_block_info[old]['params']).copy()
                            block_info[old + ":" + str(i)]['params'][var] = i

        min_address = None
        max_address = None
        for key in block_info:
            address = indexer_function(**(block_info[key]['params']))
            block_info[key]['base_address'] = address
            if min_address is None or address < min_address:
                min_address = address
            if max_address is None or address > max_address:
                max_address = address

        max_offset = None
        for register in register_map:
            offset = register_map[register]['offset']
            if max_offset is None or offset > max_offset:
                max_offset = offset

        return min_address, max_address + max_offset, block_info

    def update_i2c_address(self, address: int):
        if address != self._i2c_address:
            self._i2c_address = address
            self._not_read = True

            if address is not None:
                self._logger.info(f"Updated address space '{self._name}' to the I2C address {address:#04x}")
            else:
                self._logger.info(f"Reset the I2C address for the address space '{self._name}'")

    # def update_register_map(self, register_map: dict[str, int]):
    #    self._register_map = register_map

    def get_register(self, block_name, register_name):
        return self._memory[self._register_map[block_name + "/" + register_name]]

    def get_register_address(self, block_name, register_name):
        return self._register_map[block_name + "/" + register_name]

    def set_register(self, block_name, register_name, value):
        self._memory[self._register_map[block_name + "/" + register_name]] = value

    def read_memory_block(self, base_address, word_count):
        if self._i2c_address is None:
            self._logger.error(f"Unable to read address space '{self._name}' because the i2c address is not set")
            return False

        self._logger.info(
            f"Reading a block of {word_count} words ({self._bytes_per_word} bytes each) starting at address {base_address} in the address space '{self._name}'"
        )

        tmp = self._i2c_connection.read_device_memory(
            self._i2c_address,
            base_address,
            word_count=word_count,
            address_bitlength=self._address_bitlength,
            address_endianness=self._address_endianness,
            word_bitlength=self._word_bitlength,
            word_endianness=self._word_endianness,
            read_type=self._read_type,
        )
        for idx in range(word_count):
            self._memory[base_address + idx] = tmp[idx]

        return True

    def read_memory_word(self, address):
        return self.read_memory_block(address, 1)

    def write_memory_block(self, base_address, word_count, readback_check: bool = True, readback_base_address=None):
        if self._i2c_address is None:
            self._logger.error(f"Unable to write address space '{self._name}' because the i2c address is not set")
            return False

        has_read_only = False
        for idx in range(word_count):
            if self._read_only_map[base_address + idx]:
                has_read_only = True
                break
        if has_read_only:
            self._logger.info(
                f"The block of {word_count} words starting at address {base_address} in the address space '{self._name}' covers one or more words which are read only, it will be broken down into smaller blocks which do not cover the read only words"
            )
            return self.write_memory_block_with_split_for_read_only(base_address, word_count, readback_check, readback_base_address)

        self._logger.info(f"Writing a block of {word_count} words starting at address {base_address} in the address space '{self._name}'")

        self._i2c_connection.write_device_memory(
            self._i2c_address,
            base_address,
            self._memory[base_address : base_address + word_count],
            address_bitlength=self._address_bitlength,
            address_endianness=self._address_endianness,
            word_bitlength=self._word_bitlength,
            word_endianness=self._word_endianness,
            write_type=self._write_type,
        )

        if readback_check:
            if readback_base_address is None:
                readback_base_address = base_address

            tmp = self._i2c_connection.read_device_memory(
                self._i2c_address,
                readback_base_address,
                word_count=word_count,
                address_bitlength=self._address_bitlength,
                address_endianness=self._address_endianness,
                word_bitlength=self._word_bitlength,
                word_endianness=self._word_endianness,
                read_type=self._read_type,
            )

            failed = []
            for idx in range(word_count):
                if self._memory[base_address + idx] != tmp[idx]:
                    failed += [base_address + idx]
                    self._memory[base_address + idx] = tmp[idx]
            if len(failed) != 0:
                failed = ["0x{:0x}".format(i) for i in failed]
                self._logger.error(
                    f"Failure to write memory block at address {base_address:#0x} with {word_count} words in the '{self._name}' address space (I2C address {self._i2c_address:#02x}). The following addresses failed to write: {', '.join(failed)}"
                )
                return False

        return True

    def write_memory_word(self, address, readback_check: bool = True, readback_address=None):
        if self._read_only_map[address]:
            self._logger.info(
                f"Unable to write to the word at address {address:#0x} in the address space '{self._name}' because it is read only"
            )
            return False

        return self.write_memory_block(address, 1, readback_check, readback_address)

    def write_memory_block_with_split_for_read_only(
        self, base_address, word_count, readback_check: bool = True, readback_base_address=None
    ):
        start_address = None
        ranges = []

        if readback_base_address is None:
            readback_base_address = base_address

        for idx in range(word_count):
            if not self._read_only_map[base_address + idx] and start_address is None:
                start_address = base_address + idx
            if self._read_only_map[base_address + idx] and start_address is not None:
                ranges += [(start_address, base_address + idx - start_address, start_address - base_address + readback_base_address)]
                start_address = None
        if start_address is not None:
            ranges += [(start_address, base_address + idx - start_address + 1, start_address - base_address + readback_base_address)]

        success = True
        self._logger.info(f"Found {len(ranges)} ranges without read only registers")
        for range_param in ranges:
            if not self.write_memory_block(range_param[0], range_param[1], readback_check, range_param[2]):
                success = False

        return success

    def read_all(self):
        if self._i2c_address is None:
            self._logger.error(f"Unable to read address space '{self._name}' because the i2c address is not set")
            return

        self._logger.info(f"Reading the full '{self._name}' address space")

        if self.read_memory_block(0, self._address_space_size):
            self._not_read = False

    def read_block(self, block_name):
        if self._i2c_address is None:
            self._logger.error(f"Unable to read address space '{self._name}' because the i2c address is not set")
            return

        block = self._blocks[block_name]
        self._logger.info("Attempting to read block {}".format(block_name))

        self.read_memory_block(block["Base Address"], block["Length"])

    def read_register(self, block_name, register_name):
        self._logger.detailed_trace(f'Address_Space_Controller::read_register("{block_name}", "{register_name}")')
        if self._i2c_address is None:
            self._logger.error(f"Unable to read address space '{self._name}' because the i2c address is not set")
            return

        self._logger.info(f"Attempting to read register {register_name} in block {block_name}")

        self.read_memory_block(self._register_map[block_name + "/" + register_name], 1)

    def write_all(self, readback_check: bool = True):
        if self._i2c_address is None:
            self._logger.error(f"Unable to write address space '{self._name}' because the i2c address is not set")
            return False

        if self._has_readonly:
            self._logger.info(
                f"Unable to write the full '{self._name}' address space because there are some read only registers, breaking it into smaller blocks"
            )
            return self.write_memory_block_with_split_for_read_only(0, self._address_space_size, readback_check)

        self._logger.info("Writing the full '{}' address space".format(self._name))
        return self.write_memory_block(0, self._address_space_size, readback_check)

    def write_block(self, block_name, readback_check: bool = True):
        if self._i2c_address is None:
            self._logger.error(f"Unable to write address space '{self._name}' because the i2c address is not set")
            return False

        block = self._blocks[block_name]
        self._logger.info("Attempting to write block {}".format(block_name))

        base_address = block["Base Address"]
        original_base_address = base_address
        if "Write Base Address" in block:
            base_address = block["Write Base Address"]

        return self.write_memory_block(base_address, block["Length"], readback_check, original_base_address)

    def write_register(self, block_name, register_name, readback_check: bool = True):
        self._logger.detailed_trace(f'Address_Space_Controller::write_register("{block_name}", "{register_name}", {readback_check})')
        if self._i2c_address is None:
            self._logger.error(f"Unable to write address space '{self._name}' because the i2c address is not set")
            return False

        self._logger.info("Attempting to write register {} in block {}".format(register_name, block_name))

        address = self._register_map[block_name + "/" + register_name]
        original_address = address
        if "Write Base Address" in self._blocks[block_name]:
            new_base = self._blocks[block_name]["Write Base Address"]
            old_base = self._blocks[block_name]["Base Address"]
            address = address - old_base + new_base

        return self.write_memory_block(address, 1, readback_check, original_address)

    def reset_to_defaults(self):
        # register_count = len(self._register_map)
        # count = 0
        for address in self._memory:
            self._memory[address] = self._defaults[address]
            # count += 1
