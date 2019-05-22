.DEFAULT_GOAL := mydefault
.ONESHELL:

# ssh client must be properly configures with private keys & config to
# be able to directly access any host with 'ssh <host>'...

#hosts = bc-veilleuse bc-ui bc-water bc-hq bc-watch bc-power
#services = basecamp bt_scanner pir_scanner sms_operator heater interphone logbook operator power pushover_operator scheduler veilleuse water nightwatch
#containers = grafana influxdb nginx

#version:
	# updating version file
#	@sleep 1
#	cd source
#	./update_version.sh
#	@cat _version_.txt
#	$(foreach service,$(services), scp _version_.txt $(service)/;)
#	cd ..

erase:
	@/bin/echo -e "\x1B[01;93m -= Erasing the device on ttyUSB0 =- \x1B[0m"
	@sleep 1
	esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
	@/bin/echo -e "done"

build_fw:
	@/bin/echo -e "\x1B[01;93m -= Building the custom firmware =- \x1B[0m"
	@sleep 1
	cd ~/code/micropython/ports/esp32; make clean; make

deploy_fw:
	@/bin/echo -e "\x1B[01;93m -= Deploying the custom firmware =- \x1B[0m"
	@sleep 1
	cd ~/code/micropython/ports/esp32; make deploy

deploy:
	@/bin/echo -e "\x1B[01;93m -= Deploying the python code =- \x1B[0m"
	@sleep 1
	@/bin/echo -e "boot.py"
	ampy -p /dev/ttyUSB0 put boot.py
	#ampy -p /dev/ttyUSB0 put dep_install.py
	#ampy -p /dev/ttyUSB0 run check_fw.py
	#ampy -p /dev/ttyUSB0 ls
	ampy -p /dev/ttyUSB0 reset

mydefault:
	# ok

.PHONY: upgrade_OS restart stop start scp_private_ini get_private_ini scp_supervisord_conf_to_hosts scp_to_hosts deploy clean
