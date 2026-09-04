# DDR_2018

**Objective:** To build a simple Differential Drive Robot (DDR) using inexpensive components and involving a lot of hands-on experiments and learning.

## Info
List of components used are
1. Arduino UNO
2. HC05 bluetooth module
3. BO motors
4. Wheels
5. Caster wheel
6. L293D motor driver IC
7. L298N motor driver module
8. L7805 voltage regulator
9. Capacitors
10. Acrylic sheet
11. Soldiering setup
12. Solid core (single core) wires
13. Perforated PCB
14. Nose pliers etc.

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

5. Install requirements in the virtual environment
```sh
pip install -r requirements.txt
```

6. Run the python script *ground_station.py*
7. The robot is controlled by following four keyboard arrow buttons
    1. Up arrow key: Forward
    2. Down arrow key: Reverse
    3. Left arrow key: Turn left
    4. Tight arrow key: Turn right

## Instructions for android phone ground station
**Note:** The above applicaiton were build for old version of android os. It might not work on current version.
1. Copy the following files from *ground station/android_phone* to android mobile phone
    1. DDR_bluetooth_transmitter_V0.0.apk
    2. DDR_bluetooth_transmitter_V1.0.apk
2. Try installing both *DDR_bluetooth_transmitter_V0.0.apk* and run the application
3. If step 2 does not work try installing and running *DDR_bluetooth_transmitter_V1.0.apk*.
