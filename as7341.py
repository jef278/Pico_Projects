# MicroPython AS7341 Driver (Raspberry Pi Pico)
# J. Clark – 2026
#
# Supports:
#  - Reading all 8 spectral channels F1–F8
#  - Clear and NIR channels
#  - Basic device configuration

import time

class AS7341:
    I2C_ADDR = 0x39

    # Register map
    REG_ENABLE = 0x80
    REG_ATIME = 0x81
    REG_WTIME = 0x83
    REG_SP_LOW = 0xD0
    REG_CH0_DATA_L = 0x95  # First channel register

    def __init__(self, i2c):
        self.i2c = i2c

        # Confirm sensor is present
        devices = i2c.scan()
        if self.I2C_ADDR not in devices:
            raise OSError("AS7341 not found on I2C bus")

        # Basic enable sequence
        self._write_reg(self.REG_ENABLE, 0x01)   # PON
        time.sleep(0.01)
        self._write_reg(self.REG_ENABLE, 0x03)   # PON + Spectral EN
        time.sleep(0.01)

        # Integration time
        self._write_reg(self.REG_ATIME, 100)     # adjust as needed

    # I2C helpers ---------------------------------------------------

    def _write_reg(self, reg, value):
        self.i2c.writeto_mem(self.I2C_ADDR, reg, bytes([value]))

    def _read_reg(self, reg):
        return self.i2c.readfrom_mem(self.I2C_ADDR, reg, 1)[0]

    def _read_u16(self, reg):
        data = self.i2c.readfrom_mem(self.I2C_ADDR, reg, 2)
        return data[1] << 8 | data[0]

    # Public API ----------------------------------------------------

    def read_channels(self):
        """
        Returns dictionary of F1–F8, CLEAR, NIR readings
        """

        # Trigger measurement
        self._write_reg(0xFA, 0x10)
        time.sleep(0.05)

        # Read sequence block (F1–F8)
        base = 0x95
        readings = []

        for i in range(8):
            val = self._read_u16(base + (i * 2))
            readings.append(val)

        # Clear channel & NIR
        clear = self._read_u16(0xE6)
        nir = self._read_u16(0xE8)

        return {
            "F1_415nm": readings[0],
            "F2_445nm": readings[1],
            "F3_480nm": readings[2],
            "F4_515nm": readings[3],
            "F5_555nm": readings[4],
            "F6_590nm": readings[5],
            "F7_630nm": readings[6],
            "F8_680nm": readings[7],
            "CLEAR": clear,
            "NIR": nir
        }