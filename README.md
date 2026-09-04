# DDR2019
Differential drive robot for learning basic of arduino programming.

## Instructions for firmware

1. Use Arduino IDE or Visual Studio Code with PlatformIO extension
2. Connect Arduino UNO to the PC using usb cable and select corresponding comport in the IDE.
3. Upload the firmware

## Instructions for ground station pc

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