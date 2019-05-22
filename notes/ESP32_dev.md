# ESP32 development notes 📶

## LOLIN D32 pro
https://wiki.wemos.cc/products:d32:d32_pro
+ 4MB FLASH / 4MB PSRAM (v2.0.0, green point on top)
+ 16MB FLASH / 8MB PSRAM (v2.0.0, mauve point on top)
+ LOLIN I2C port, LOLIN TFT port
+ TF (uSD) card slot, supporting SPI mode.
+ schematic: https://wiki.wemos.cc/_media/products:d32:sch_d32_pro_v2.0.0.pdf
+ WROVER32 datasheet: https://www.espressif.com/sites/default/files/documentation/esp32-wrover_datasheet_en.pdf
+ official store page here: https://www.aliexpress.com/store/product/LOLIN-D32-Pro-V2-0-0-wifi-bluetooth-board-based-ESP-32-esp32-Rev1-ESP32-WROVER/1331105_32883116057.html?spm=a2g1y.12024536.productList_2559240.subject_0

## uPython ESP32 features:
+ all the ESP8266 features!
+ REPL (Python prompt) over UART0.
+ 16k stack for the MicroPython task and 96k Python heap.
+ Many of MicroPython's features are enabled: unicode, arbitrary-precision integers, single-precision floats, complex numbers, frozen bytecode, as well as many of the internal modules.
+ Internal filesystem using the flash (currently 2M in size).
+ The machine module with GPIO, UART, SPI, software I2C, ADC, DAC, PWM, TouchPad, WDT and Timer.
+ The network module with WLAN (WiFi) support.

## install the proper tools

+ install python3 (already available on ubuntu 18.04)
+ `sudo apt install python3-pip screen`
+ sudo -EH pip3 install --upgrade pip
+ sudo -EH pip3 install esptool adafruit-ampy

## ...and test them by flashing a ready-to-use micropython firmware
+ download firmware from https://micropython.org/download#esp32
  + for the D32 pro, we're using the _esp32spiram_ version of the micropython fw
+ plug in the ESP32 pro and watch the result from ` dmesg`  to get the USB endpoint (let's say it's ttyUSB0)
+ `sudo chmod 666 /dev/ttyUSB0`
+ erase the flash: `esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash`
```
esptool.py v2.6
Serial port /dev/ttyUSB0
Connecting....
Chip is ESP32D0WDQ5 (revision 1)
Features: WiFi, BT, Dual Core, 240MHz, VRef calibration in efuse, Coding Scheme None
MAC: 30:ae:a4:cf:02:48
Uploading stub...
Running stub...
Stub running...
Erasing flash (this may take a while)...
Chip erase completed successfully in 5.6s
Hard resetting via RTS pin...
```
note: MAC address is shown (that's cool to enable WIFI filtering on MAC address)
+ program it now:
  + `esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 ./esp32spiram-20190516-v1.10-352-g2630d3e51.bin`
```
esptool.py v2.6
Serial port /dev/ttyUSB0
Connecting........_
Chip is ESP32D0WDQ5 (revision 1)
Features: WiFi, BT, Dual Core, 240MHz, VRef calibration in efuse, Coding Scheme None
MAC: 30:ae:a4:cf:02:48
Uploading stub...
Running stub...
Stub running...
Changing baud rate to 460800
Changed.
Configuring flash size...
Auto-detected Flash size: 16MB
Flash params set to 0x0240
Compressed 1221664 bytes to 743998...
Wrote 1221664 bytes (743998 compressed) at 0x00001000 in 17.1 seconds (effective 572.4 kbit/s)...
Hash of data verified.

Leaving...
Hard resetting via RTS pin...
```
+ then open a REPL session: `sudo screen /dev/ttyUSB0 115200` 
  + try `help()` for example...
  + try `CTRL+D` for a soft reboot, the micropython firmware version will be shown
+ close the REPL session (ctrl+a then `k`+`y` to confirm, use `byobu-ctrl-a emacs` if ctrl+a interferes with byobu)
+ and then you can use `ampy -p /dev/ttyUSB0 get /boot.py` to read/write to the filesystem
  + note: you can simplify ampy usage with:
    + export AMPY_PORT=/dev/ttyUSB0

+ some other basic fw-related stuff:
  + to double-check the flash size:
```python
   import esp
   esp.flash_size()
   > 4194304
```
  + to double-check the fs size:
```python
   import uos
   fs_stat = uos.statvfs('/')
   fs_size = fs_stat[0] * fs_stat[2]
   fs_free = fs_stat[0] * fs_stat[3]
   print("File System Size {:,} - Free Space {:,}".format(fs_size, fs_free))
   > File System Size 2,072,576 - Free Space 2,068,480
```
  + so we have a 4MB flash size split between 2MB for the micropython firmware, and 2MB for the filesystem. It makes sense...
  + RAM size (heap):
```python
import gc
gc.collect()
gc.mem_free()
```
    + gives 4092688 bytes => 4MB RAM! :)

+ note: `ampy -p /dev/ttyUSB0 put ./check_fw.py` and then running `import check_fw` within the REPL will show the same useful info.

## flashing micropython on D32 pro
the LOLIN D32 pro devices have various flash/RAM configuration: 4MB flash/4MB PSRAM or 16MB flash/8MB PSRAM. Currently, only 4MB of RAM seems to be usable by micropython (see http://www.packom.org/esp8266/16mb/flash/eeprom/2016/10/14/esp8266-16mbyte-flash_handling.html), and the ESP32 micropython firmware uses a hardcoded value of 2MB for the filesystem size.
So, we are going to build a custom ESP32 fw that suits our devices, and uses all the flash available for the filesystem...

## so let's start building and flashing a custom-tailored micropython firware

Let's do it:
```shell
git clone --recurse-submodules https://github.com/micropython/micropython.git
cd micropython
cd ports
cd esp32
make
(extract the supported git hash)
git clone https://github.com/espressif/esp-idf.git
cd esp-idf
git checkout <previsouly extracted hash> 5c88c5996dbde6208e3bec05abc21ff6cd822d26
git submodule update --init --recursive
sudo apt-get install gcc git wget make libncurses-dev flex bison gperf python python-pip python-setuptools python-serial python-cryptography python-future python-pyparsing
sudo -EH pip3 install pyserial pyparsing
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

+ get the micropython-lib
  + files in the modules/ subdir link to the micropython-lib project, and you need to clone this project on the same level as _micropython_
  + 
  + then try `cat ./urequests.py` in _modules/_ to check if everything is fine

+ OPTIONAL: freezing files/modules (see next section)

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

+ Let's modify the last line of `micropython/ports/esp32/modules/flashbdev.py` to:
```
# 14MB here, leaving 2MB for the fw
bdev = FlashBdev(14 * 1024 * 1024 // FlashBdev.SEC_SIZE)
```
```
+ then `make`, `make erase` and `make deploy` (+`make clean` beforehand  if any makefile config has changed)
+ ampy -p /dev/ttyUSB0 run ./check_fw.py:
flash_size:  16777216
File System Size 14,651,392 - Free Space 14,647,296
stack: 736 out of 15360
GC: total: 4098240, used: 6720, free: 4091520
```

## frozen modules and files

The previous process can be done over again while putting new files in _modules/_.
They will be pre-compiled and made available in the firmware, reducing the loading time.

## try the unix port

+ sudo apt-get install build-essential libreadline-dev libffi-dev git pkg-config
+ make axtls
+ make
+ micropython
+ micropython -m upip install micropython-pystone
+ micropython
  >>> import pystone
  >>> pystone.main()
  Pystone(1.2) time for 50000 passes = 0.724
This machine benchmarks at 69060.8 pystones/second

## how to use upip on device?
+ from inside the REPL:
  + import upip
  + upip.install("micropython-pystone_lowmem")
  + import pystone_lowmem
  + pystone_lowmem.main()

--- old stuff ---

### 


## ESP8266

### uPython ESP8266 features:
Supported features include:

    REPL (Python prompt) over UART0.
    Garbage collector, exceptions.
    Unicode support.
    Builtin modules: gc, array, collections, io, struct, sys, esp, network, many more.
    Arbitrary-precision long integers and 30-bit precision floats.
    WiFi support.
    Sockets using modlwip.
    GPIO and bit-banging I2C, SPI support.
    1-Wire and WS2812 (aka Neopixel) protocols support.
    Internal filesystem using the flash.
    WebREPL over WiFi from a browser (clients at https://github.com/micropython/webrepl).
    Modules for HTTP, MQTT, many other formats and protocols via https://github.com/micropython/micropython-lib .

Work-in-progress documentation is available at http://docs.micropython.org/en/latest/esp8266/.

### Wemos D1 pro specs
https://wiki.wemos.cc/products:d1:d1_mini_pro
+ single core 32 bit microcontroller @80MHz
+ 160kB SRAM
+ 16MB flash
+ Wifi (no BT)
+ 2x SPI, 1x I2C, 2x I2S, 2x UART, one-wire, interrupt, pwm
+ 11 (10?) digital IO, 1 analog Input
+ 10-bit ADC (3.2V max input), no CAN
+ lithium battery interface (3.7V), 500mA charging current, Battery Connector: PH-2 2.0mm
+ Pinout:
Pin	Function	ESP-8266 Pin
TX	TXD	TXD
RX	RXD	RXD
A0	Analog input, max 3.3V input	A0
16	IO	GPIO16
5	IO, SCL	GPIO5
4	IO, SDA	GPIO4
0	IO, 10k Pull-up	GPIO0
2	IO, 10k Pull-up, BUILTIN_LED	GPIO2
14	IO, SCK	GPIO14
12	IO, MISO	GPIO12
13	IO, MOSI	GPIO13
15	IO, 10k Pull-down, SS	GPIO15
GND	Ground	GND
5V	5V	-
3V3	3.3V	3.3V
RST	Reset	RST
_All of the IO pins have interrupt/pwm/I2C/one-wire support except D0._
_All of the IO pins run at 3.3V._
+ schematic: https://wiki.wemos.cc/_media/products:d1:sch_d1_mini_pro_v2.0.0.pdf
+ firmware: compiler un spécifique car 16MB non conventionnel?
+ oui, ça fonctionne bien, en faisant comme ca: https://github.com/micropython/micropython/issues/2335
    First of all you should have a ESP8266 board with 16MB memory. I have the Wemos D1 Pro. The description below work on a Mac.

    Start with upgrading the SEPTools: pip install esptool --upgrade

    Compile the esp-open-sdk by following the instructions This will download during make the 2.1.0 SDK (at least at time of writing these instructions) You will need the file esp_init_data_default.bin later on (the file is located in the directory esp-open-sdk/ESP8266_NONOS_SDK-2.1.0-18-g61248df/bin/) For your convenience, copy the file to a separate directory.

    Compile the MicroPython port to ESP8266 by following the instructions

    You will end up with a file called firmware-combined.bin which you can also copy to the directory already containing esp_init_data_default.bin. Change to this directory

    First erase the ESP8266: esptool.py --port /dev/cu.SLAB_USBtoUART --baud 460800 erase_flash

    Flash both the micropython firmware and the esp_init_data_default.bin: esptool.py --port /dev/cu.SLAB_USBtoUART --baud 460800 write_flash -fm dio -fs 16MB 0 firmware-combined.bin 0xffc000 esp_init_data_default.bin

    Open a serial terminal to your ESP8288 (e.g. with the serial monitor included in the Arduino IDE) and reset the ESP8288

    Type into the serial terminal following commands:

    >>> import esp
    >>> esp.flash_size()

    I get following result:
    16777216
    
    So now we can use the full 16MB of the board!
+ Memory issues

  You can usually get the following error using MicroPython: MemoryError: memory allocation failed, allocating xxxx bytes. The RAM is very limited, especially on the ESP8266. If you run into this issue, you can cross-compile the python files that you want load to the board to reduce the RAM use.
  
  To do that, you need to use Linux (sorry) and clone the repositories:
  
      WiPy: pycom/pycom-micropython-sigfox
      ESP32/ESP8266: micropython/esp32
  
  Then, go to the folder mpy-cross using a terminal, and type make. Wait a couple of seconds/minutes. Then, you can compile the python files using ./mpy-cross <filename.py> to get the .mpy files.
  
  Then, load only the .mpy files not the .py files! Otherwise, the board tries to load the .py and you get the same error again.
+ consommation des cartes en idle, wifi & deep-sleep: https://www.youtube.com/watch?v=yZjpYmWVLh8
+ Connection d'une batterie: https://macsbug.wordpress.com/2017/05/08/battery-and-battery-interface-of-lolin32/

### uPython libs
+ http://docs.micropython.org/en/latest/esp8266/library/index.html

#### Installing a custom module
+ once connected to wifi/internet:
```
import upip
upip.install('notes-pico')
```

#### RTC
https://docs.micropython.org/en/latest/esp8266/esp8266/general.html?highlight=ntptime#real-time-clock

#### internal LED
```
led = machine.Pin(5, machine.Pin.OUT)
>>> led.value(0)
>>> led.value(1)
```

#### GPIOs
http://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/pins.html#gpio-pins
#### External interrupts!
http://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/pins.html#external-interrupts
#### Timers!
http://docs.micropython.org/en/latest/esp8266/esp8266/quickref.html#timers
#### PWM!
http://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/pwm.html#pulse-width-modulation
+ example of pulsing a led: http://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/pwm.html#fading-an-led
+ controling a servo: http://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/pwm.html#control-a-hobby-servo
#### ADC!
http://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/adc.html#analog-to-digital-conversion
#### CPU freq, deep-sleep
http://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/powerctrl.html#power-control

```
>>> import esp
>>> esp.flash_size()
4194304
=> 4Mo FLASH
```
```
>>> import os
>>> os.statvfs('//')
(4096, 4096, 506, 505, 505, 0, 0, 0, 0, 255)
=> 2Mo fs
```

mieux:

```
import uos
fs_stat = uos.statvfs('/')
fs_size = fs_stat[0] * fs_stat[2]
fs_free = fs_stat[0] * fs_stat[3]
print("File System Size {:,} - Free Space {:,}".format(fs_size, fs_free))
```

#### Boot script
+ boot.py => executed first
+ main.py => run after boot.py
+ a good basic boot.py script:
```python
# boot.py
def wlan_connect(ssid='KNET_nio101', password='netgear99A', hostname='wemos-d32-one'):
    import network
    wlan = network.WLAN(network.STA_IF)
    if not wlan.active() or not wlan.isconnected():
        wlan.active(True)
        wlan.config(dhcp_hostname=hostname)
        print('connecting to:', ssid)
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
        print('network config:', wlan.ifconfig())

wlan_connect()
```
