# 라즈베리파이

사용 스펙 : 라즈베리파이 4 (8G), 라즈비안 OS, Python

<br>

## 기능

1. ibeacon 송신 (버스 데이터 정보)

2. ibeacon 수신 (사용자 하차여부 정보)
3. GPIO핀을 이용한 버스 하차벨 동작
4. 스피커 출력 (버스 데이터를 이용한 TTS)

<br><br>

## 설치 방법

### 1. 라즈베리파이에 블루투스 모듈 설치

```sh
$ sudo apt-get install -y libusb-dev
$ sudo apt-get install -y libdbus-1-dev
$ sudo apt-get install -y libglib2.0-dev
$ sudo apt-get install -y libudev-dev
$ sudo apt-get install -y libical-dev
$ sudo apt-get install -y libreadline-dev
$ sudo apt-get install -y libdbus-glib-1-dev
```

### 2. blueZ설치

```sh
$ sudo mkdir bluez
$ cd bluez
$ sudo wget www.kernel.org/pub/linux/bluetooth/bluez-5.19.tar.gz
$ sudo gunzip bulez-5.19.tar.gz
$ sudo tar xvf bluez-5.19.tar

$ cd bluez-5.19
$ sudo ./configure --disable-systemd
$ sudo make
$ sudo make install
$ sudo apt-get install python-bluez
$ sudo shutdown -r now
```

### 3. git pull

```sh
$ cd ~
$ sudo apt-get install git
$ git clone https://github.com/Wetayo/raspberrypi.git
```

### 4. 실행

```sh
$ cd raspberrypi
$ sudo python ./wetayoBeacon.py
```

<br><br>

## 파일 내용

1. wetayoBeacon : 전체적인 비콘 송신을 담당하고 scanner모듈을 이용해 수신도 하는 최종 모듈로 UUID/Major/Minor를 16bit로 설정해주어야 한다.
2. scanner : 수신하는 모듈로 Major와 Minor를 10진수로 설정해주어야 한다.
