Changelog
=========

0.1.4 (2024-06-26)
------------------

* Added reading of the SEU Counters to the efficient reading

0.1.3 (2024-06-26)
------------------

* Fixed efficient reading function

0.1.2 (2024-06-26)
------------------

* Added a method for effiecient reading of etroc2
* Started adding GUI classes

0.1.1 (2024-06-26)
------------------

* Added classes for ETROC1 chip and AD5593R chip

0.1.0 (2024-06-24)
------------------

* Quickly added address_space_controller, base_chip and etroc2_chip (without associated testing infrastructure) so we can be ready for the next SEU campaign
* Added additional log levels
* Implemented the usb_iss_helper class derived from the i2c_connection_helper base class
* Implemented the i2c_connection_helper base class
* Added word_list_to_bytes and bytes_to_word_list functions
* Added address byte adjustment function for different endianness and bit lengths
* Added I2C address validation function
* Added endian swap functions to the generic functions file

0.0.2 (2024-05-24)
------------------

* Added tests for the I2C Connection Helper base class
* Implemented the I2C Messages class
* Added tests for validating the I2C messages values for building custom I2C commands
* Created initial tests for the address_space_controller class

0.0.1 (2024-05-22)
------------------

* First release on PyPI.
* Added automated publishing of tagged versions to pypi

0.0.0 (2024-05-22)
------------------

* Base setup of all the tools for handling this project
