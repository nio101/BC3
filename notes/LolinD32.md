# Specs
## Wemos D32 specs
https://wiki.wemos.cc/products:d32:d32
+ white point on top
+ dual core 32bit microcontroler @240Mhz
+ 512kB SRAM
+ 4MB Flash
+ Wifi -access point & wifi user at the same time! (^o^) -
+ BT 4.2
+ 22 digital IO, 6 analog input, 2 analog outputs
+ 4x SPI, 2x I2C, 2x I2S, 2x UART
+ 12-bit ADC, CAN, touch sensor, temperature sensor
+ lithium battery interface (3.7V), 500mA charging current, Battery Connector: PH-2 2.0mm
+ Pinout?
analog inputs: VP, VN, 32, 33, 34, 35
analog outputs: 25, 26
LED_BUILTIN: 5
22 digital IO
+ Schematic: https://wiki.wemos.cc/_media/products:d32:sch_d32_v1.0.0.pdf
+ WROOM32 datasheet: https://www.espressif.com/sites/default/files/documentation/esp32-wroom-32_datasheet_en.pdf

## Wemos D32 pro (/D32)
https://wiki.wemos.cc/products:d32:d32_pro
+ 4MB FLASH / 4MB PSRAM (v2.0.0, green point on top)
+ 16MB FLASH / 8MB PSRAM (v2.0.0, mauve point on top)
+ LOLIN I2C port, LOLIN TFT port
+ TF (uSD) card slot, supporting SPI mode.
+ schematic: https://wiki.wemos.cc/_media/products:d32:sch_d32_pro_v2.0.0.pdf
+ WROVER32 datasheet: https://www.espressif.com/sites/default/files/documentation/esp32-wrover_datasheet_en.pdf
+ official store page here: https://www.aliexpress.com/store/product/LOLIN-D32-Pro-V2-0-0-wifi-bluetooth-board-based-ESP-32-esp32-Rev1-ESP32-WROVER/1331105_32883116057.html?spm=a2g1y.12024536.productList_2559240.subject_0

# flashing micropython on Lolin D32/D32 pro
those devices have various flash/RAM configuration
+ 4MB flash/512kB SRAM for the lolin D32
+ 4MB flash/4MB PSRAM & 16MB flash/8MB PSRAM for the lolin D32 pro

Currently:
+ only 4MB of RAM seems to be usable by micropython (see http://www.packom.org/esp8266/16mb/flash/eeprom/2016/10/14/esp8266-16mbyte-flash_handling.html)
+ the ESP32 micropython fw uses a hardcoded value of 2MB for the filesystem
So, we are going to build a custom ESP32 fw that suits our devices, and uses all the flash available for the filesystem...

Let's do it:
```shell
git clone https://github.com/micropython/micropython.git
cd micropython
cd ports
cd esp32
make
(extract the supported git hash)
git clone https://github.com/espressif/esp-idf.git
cd esp-idf
git checkout <previsouly extracted hash>
git submodule update --init --recursive
sudo apt-get install gcc git wget make libncurses-dev flex bison gperf python python-pip python-setuptools python-serial python-cryptography python-future python-pyparsing
```
+ follow the instructions here to setup the toolchain: https://docs.espressif.com/projects/esp-idf/en/latest/get-started/linux-setup.html
+ follow then the instructions on the micropython esp32 port page to set up the makefile
+ note on the dio flag:
> --flash_mode dio. Most ESP32 modules are using dual I/O.
for the D32, we will then have this makefile:
```
ESPIDF = /home/nio/code/micropython/ports/esp32/esp-idf
PORT = /dev/ttyUSB0
FLASH_MODE = dio
# 16MB or 4MB, depending on the D32
FLASH_SIZE = 4MB
#CROSS_COMPILE = xtensa-esp32-elf-
# for D32 pro:
# SDKCONFIG = boards/sdkconfig.spiram
# for D32:
SDKCONFIG = boards/sdkconfig

include Makefile
```
+ back to the root micropython directory: `make -C mpy-cross` to compile the micropython cross compiler
```shell
git submodule init lib/berkeley-db-1.xx
git submodule update
cd ports/esp32
```
+ OPTIONAL: freezing files/modules

+ finally, just use `make` in the ports/esp32 directory to build the custom firmware
  + if you get an error about pyparsing, juste use: `sudo pip install pyparsing` then `make` again
  + you'll then get .bin files in the build subdirectory...
+ to flash the new firmware:
  + `make erase`
  + `make deploy`

+ now let's test it:
```
import esp
esp.flash_size() 
>4194304
import uos
fs_stat = uos.statvfs('/')
fs_size = fs_stat[0] * fs_stat[2]
fs_free = fs_stat[0] * fs_stat[3]
print("File System Size {:,} - Free Space {:,}".format(fs_size, fs_free))
>File System Size 2,072,576 - Free Space 2,068,480
import gc
gc.collect()
gc.mem_free()
>122304
```
so, for the D32, we have: 4MB flash, 2MB filesystem, 122KB RAM (out of 512KB)

+ Let's modify the `micropython/ports/esp32/modules/flashbdev.py` file to reflect ` micropython/ports/esp8266/modules/flashbdev.py`:
```batch
import esp

class FlashBdev:

    SEC_SIZE = 4096
    RESERVED_SECS = 1
    START_SEC = esp.flash_user_start() // SEC_SIZE + RESERVED_SECS
    NUM_BLK = 0x6b - RESERVED_SECS

    def __init__(self, blocks=NUM_BLK):
        self.blocks = blocks

    def readblocks(self, n, buf):
        #print("readblocks(%s, %x(%d))" % (n, id(buf), len(buf)))
        esp.flash_read((n + self.START_SEC) * self.SEC_SIZE, buf)

    def writeblocks(self, n, buf):
        #print("writeblocks(%s, %x(%d))" % (n, id(buf), len(buf)))
        #assert len(buf) <= self.SEC_SIZE, len(buf)
        esp.flash_erase(n + self.START_SEC)
        esp.flash_write((n + self.START_SEC) * self.SEC_SIZE, buf)

    def ioctl(self, op, arg):
        #print("ioctl(%d, %r)" % (op, arg))
        if op == 4:  # BP_IOCTL_SEC_COUNT
            return self.blocks
        if op == 5:  # BP_IOCTL_SEC_SIZE
            return self.SEC_SIZE

size = esp.flash_size()
if size < 1024*1024:
    bdev = None
else:
    # 200K at the flash end is reserved for SDK params storage
bdev = FlashBdev((size - 204800) // FlashBdev.SEC_SIZE - FlashBdev.START_SEC)
```
+ then `make`, `make erase` and `make deploy`
+ 
