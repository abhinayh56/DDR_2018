import serial
import serial.tools.list_ports

ports = serial.tools.list_ports.comports()

print("1 ---")
print(ports)

print("2 ---")
print(type(ports))

print("3 ---")

for port in ports:
    print("--")
    print(port)
    print("-")
    print("port.device        : ", port.device)
    print("port.name          : ", port.name)
    print("port.description   : ", port.description)
    print("port.hwid          : ", port.hwid)
    print("port.vid           : ", port.vid)
    print("port.pid           : ", port.pid)
    print("port.serial_number : ", port.serial_number)
    print("port.location      : ", port.location)
    print("port.manufacturer  : ", port.manufacturer)
    print("port.product       : ", port.product)
    print("port.interface     : ", port.interface)

print("4 ---")























# for port in ports:
#     print(port.device)



# ser = serial.Serial()
# ser.baudrate = 9600
# ser.port = 'COM11'
# ser.open()
# ser.close()