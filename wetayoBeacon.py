import subprocess
import socket
import scanner
import sys
import bluetooth._bluetooth as bluez
from time import sleep
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(15, GPIO.OUT)

bct_BLUETOOTHDEVICE = "hci0"
bct_OGF = "0x08"
bct_OCF_format = "0x0008"
bct_OCF_setting = "0x0006"
bct_OCF_operate = "0x000A"
bct_start = "01"
bct_stop = "00"

bct_IBEACONPROFIX = "1E 02 01 1A 1A FF 4C 00 02 15"
bct_UUID = "77 70 7F 98 A4 DA 45 1E 85 9F 5A 29 FD B8 CD 15"
bct_MAJOR = "00 01"
bct_MINOR = "01 23"
bct_POWER = "C5 00"


def beacon_TX_config(_param):
  result = subprocess.check_output("sudo hciconfig " + bct_BLUETOOTHDEVICE + " " + _param, shell=True)

def beacon_TX_cmd_format(_ocf, _ibeaconprofix, _uuid, _major, _minor, _power):
  _bct_ogf = bct_OGF + " "
  _ocf = _ocf + " "
  _ibeaconprofix = _ibeaconprofix + " "
  _uuid = _uuid + " "
  _major = _major + " "
  _minor = _minor + " "
  result = subprocess.check_output("sudo hcitool -i " + bct_BLUETOOTHDEVICE + " cmd " + _bct_ogf + _ocf + _ibeaconprofix + _uuid + _major + _minor + _power, shell=True)

def beacon_TX_cmd_setting(_ocf, _interval):
  _bct_ogf = bct_OGF + " "
  _ocf = _ocf + " "
  _intervalHEX = '{:04X}'.format(int(_interval/0.625))
  _minInterval = _intervalHEX[2:] + " " + _intervalHEX[:2] + " "
  _maxInterval = _intervalHEX[2:] + " " + _intervalHEX[:2] + " "
  result = subprocess.check_output("sudo hcitool -i " + bct_BLUETOOTHDEVICE + " cmd " + _bct_ogf + _ocf + _maxInterval + _maxInterval + "00 00 00 00 00 00 00 00 00 07 00", shell=True)

def beacon_TX_cmd_operate(_ocf, _param):
  _bct_ogf = bct_OGF + " "
  _ocf = _ocf + " "
  result = subprocess.check_output("sudo hcitool -i " + bct_BLUETOOTHDEVICE + " cmd " + _bct_ogf + _ocf + _param, shell=True)

def beacon_TX_DevTrigger():
  #_bct_uuid = "00 00 " + _str +" AC E8 B4 E0 C2 7D 20 B6 11 B6 11 C7 74"
  beacon_TX_cmd_format(bct_OCF_format, bct_IBEACONPROFIX, bct_UUID, bct_MAJOR, bct_MINOR, bct_POWER)
  sleep(1)

beacon_TX_config("up")
beacon_TX_cmd_format(bct_OCF_format, bct_IBEACONPROFIX, bct_UUID, bct_MAJOR, bct_MINOR, bct_POWER)
beacon_TX_cmd_setting(bct_OCF_setting, 100)
beacon_TX_cmd_operate(bct_OCF_operate, bct_start)
try:
  print "BLE EMIT START"
  while True:
    beacon_TX_DevTrigger()
    print("good")
    dev_id = 0
        
    sock = bluez.hci_open_dev(dev_id)
    print("ble thread started")

    scanner.hci_le_set_scan_parameters(sock)
    scanner.hci_enable_le_scan(sock)

    while True:
        returnedList = scanner.parse_events(sock, 10)
        print(returnedList)
        
        if returnedList:
            GPIO.output(15, True)
            print("turn on")
            time.sleep(1)
            GPIO.output(15, False)
            break

except:
    print("error accessing bluetooth device...")
    sys.exit(1)
    
finally:
  print "BLE EMIT STOP"
  beacon_TX_cmd_operate(bct_OCF_operate, bct_stop)
  GPIO.cleanup()
  print("cleanup")








