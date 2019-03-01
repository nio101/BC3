# ESP development notes 📶

## ESP32

Let's start with the LOLIN ESP32 pro (https://wiki.wemos.cc/products:d32:d32_pro)

### Wemos D32 pro (/D32)
https://wiki.wemos.cc/products:d32:d32_pro
+ 4MB FLASH / 4MB PSRAM (v2.0.0, green point on top)
+ 16MB FLASH / 8MB PSRAM (v2.0.0, mauve point on top)
+ LOLIN I2C port, LOLIN TFT port
+ TF (uSD) card slot, supporting SPI mode.
+ schematic: https://wiki.wemos.cc/_media/products:d32:sch_d32_pro_v2.0.0.pdf
+ WROVER32 datasheet: https://www.espressif.com/sites/default/files/documentation/esp32-wrover_datasheet_en.pdf
+ official store page here: https://www.aliexpress.com/store/product/LOLIN-D32-Pro-V2-0-0-wifi-bluetooth-board-based-ESP-32-esp32-Rev1-ESP32-WROVER/1331105_32883116057.html?spm=a2g1y.12024536.productList_2559240.subject_0

### uPython ESP32 features:
+ all the ESP8266 features!
+ REPL (Python prompt) over UART0.
+ 16k stack for the MicroPython task and 96k Python heap.
+ Many of MicroPython's features are enabled: unicode, arbitrary-precision integers, single-precision floats, complex numbers, frozen bytecode, as well as many of the internal modules.
+ Internal filesystem using the flash (currently 2M in size).
+ The machine module with GPIO, UART, SPI, software I2C, ADC, DAC, PWM, TouchPad, WDT and Timer.
+ The network module with WLAN (WiFi) support.

### flashing the latest micropython (for the first version with 4MB flash/4MB PSRAM)

+ sudo -EH pip3 install --upgrade pip
+ sudo -EH pip3 install esptool
+ sudo -EH pip3 install adafruit-ampy
+ download firmware from https://micropython.org/download#esp32
  + for the 4MB FLASH/4MB PSRAM version, we're using the _esp32spiram_ version of the micropython fw
+ plug in the ESP32 pro and watch the result from ` dmesg`  to get the USB endpoint (let's say it's ttyUSB0)
+ `sudo chmod 666 /dev/ttyUSB0`
+ erase the flash: `esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash`
```
esptool.py v2.4.1
Serial port /dev/ttyS7
Connecting........___
Detecting chip type... ESP32
Chip is ESP32D0WDQ6 (revision 1)
Features: WiFi, BT, Dual Core
MAC: 30:ae:a4:8b:47:74
Uploading stub...
Running stub...
Stub running...
Erasing flash (this may take a while)...
Chip erase completed successfully in 6.5s
Hard resetting via RTS pin...
```
note: MAC address is shown (that's cool to enable WIFI filtering on MAC address)
+ program it now:
  + `esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 ./esp32spiram-20190214-v1.10-98-g4daee3170.bin`
```
esptool.py v2.4.1
Serial port /dev/ttyS7
Connecting....
Detecting chip type... ESP32
Chip is ESP32D0WDQ6 (revision 1)
Features: WiFi, BT, Dual Core
MAC: 30:ae:a4:8b:47:74
Uploading stub...
Running stub...
Stub running...
Configuring flash size...
Auto-detected Flash size: 4MB
Compressed 1046048 bytes to 653808...
Wrote 1046048 bytes (653808 compressed) at 0x00001000 in 57.5 seconds (effective 145.6 kbit/s)...
Hash of data verified.

Leaving...
Hard resetting via RTS pin...
```
+ then open a REPL session: `sudo screen /dev/ttyS7 115200` 
  + try `help()` for example...
+ close the REPL session (ctrl+a then `k`+`y` to confirm, use `byobu-ctrl-a emacs` if ctrl+a interferes with byobu)
+ and then you can use `ampy -p /dev/ttyUSB0 get /boot.py` to read/write to the filesystem
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
  + so we have a 4MB flash size split between 2MB for the micropython firmware, and 2MB for the filesystem. It makes sense!

--- old stuff ---

### Wemos D32 specs
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

Work-in-progress documentation is available at http://docs.micropython.org/en/latest/esp8266/ .

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
+ oui, ça fonctionne bien, en faisant comme ca:
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

