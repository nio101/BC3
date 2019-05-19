# boot.py

import esp
from machine import Pin, PWM
import network
import uos
import gc
import ntptime
import utime


def wlan_connect(ssid, password, hostname):
	wlan = network.WLAN(network.STA_IF)
	if not wlan.active() or not wlan.isconnected():
		wlan.active(True)
		wlan.config(dhcp_hostname=hostname)
		print('scanning wifi networks...')
		wlan.scan()
		print('connecting to:', ssid)
		wlan.connect(ssid, password)
		while not wlan.isconnected():
			pass
		print('MAC address:',":".join(["{0:02x}".format(c) for c in wlan.config('mac')]))
		print('network config:', wlan.ifconfig())

def fs_size():
   fs_stat = uos.statvfs('/')
   fs_size = fs_stat[0] * fs_stat[2]
   fs_free = fs_stat[0] * fs_stat[3]
   return "filesystem size: {0:0.1f}MB - free space: {0:0.1f}MB".format(fs_size/(1024*1024), fs_free/(1024*1024))

esp.osdebug(None)
print()
print("=== boot.py ===")

pwm_led = PWM(Pin(5), freq=2, duty=512) # create and configure the led in one go
#wlan_connect(ssid='KNET_nio101', password='netgear99A')
wlan_connect(ssid='Livebox-3586', password='iWVNmv3fQS4c3nctAk', hostname='D32ProOne')
pwm_led = PWM(Pin(5), freq=1, duty=1000)

print("getting current time from pool.ntp.org...")
ntptime.settime()
print("local_time: {0:02d}/{1:02d}/{2:02d} {3:02d}:{4:02d}:{5:02d}".format(utime.localtime()[2], utime.localtime()[1], utime.localtime()[0], utime.localtime()[3], utime.localtime()[4], utime.localtime()[5]))
print("flash_size: {0:0.1f}MB ".format(esp.flash_size()/(1024*1024)))
print(fs_size())
gc.collect()
print("RAM_size: {0:0.1f}MB ".format(gc.mem_free()/(1024*1024)))

print()
