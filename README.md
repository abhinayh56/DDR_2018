# DDR_2018

**Objective:** To build a simple Differential Drive Robot (DDR) using inexpensive components and involving a lot of hands-on experiments and learning.

## Info
List of components used are
1. BO motors
2. L293D motor driver IC
3. HC05 bluetooth module
4. Arduino UNO
5. Acrylic sheet
6. Soldiering setup
7. Solid core wires
8. Perforated PCB
9. Nose plier etc.

## Instructions for firmware

1. Use Arduino IDE or Visual Studio Code with PlatformIO extension
2. Connect Arduino UNO to the PC using usb cable and select corresponding comport in the IDE.
3. Upload the firmware

## Instructions for pc ground station

1. Install python 3.12 in the pc
2. Open *pc* folder inside the *ground station folder* in Visual studio code
3. Create python virtual environment

```sh
python 3.12 -m venv venv
```

4. Activate the virtual environment

For Windows pc use the following command

```sh
venv/Scripts/activate
```

For Linux based pc use the following command

```sh
. venv/Scripts/activate
```

4. Install requirements in the virtual environment

```sh
pip install -r requirements.txt
```

5. Run the python script *ground_station.py*

## Instructions for android phone ground station

Note: The above applicaiton were build for old version of android os. It might not work on current version.

1. Copy the following files from *ground station/android_phone* to android mobile phone
    1. DDR_bluetooth_transmitter_V0.0.apk
    2. DDR_bluetooth_transmitter_V1.0.apk
2. Try installing both *DDR_bluetooth_transmitter_V0.0.apk* and run the application
3. If step 2 does not work try installing and running *DDR_bluetooth_transmitter_V1.0.apk*.
