print('GCS DDR2018')

import time
import pygame
import serial
import serial.tools.list_ports

port = ""

print("===")
print("Available serial ports:")
port_list = []
for i, port in enumerate(serial.tools.list_ports.comports()):
    print("    ", i + 1 , ". ", port.device, "-", port.description)
    port_list.append(port.device)

user_input = int(input("Select the serial port to connect to the DDR2018 robot. (Enter the number corresponding to the port): "))
port_name = port_list[user_input - 1]

ser = serial.Serial()
ser.baudrate = 9600
# ser.port = '/dev/rfcomm3'
ser.port = port_name
# ser.timeout = 0.15

ser.close()

time.sleep(1)

ser.open()

print("===")

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Keyboard Input")
running = True

def crc8(data):
    polynomial = 0x07
    crc = 0x00
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x80:
                crc = (crc << 1) ^ polynomial
            else:
                crc <<= 1
    return crc & 0xFF

def limit(n, min_val, max_val):
    return max(min_val, min(n, max_val))

def send_command(pwm_L_, pwm_R_):
    pwm_L = pwm_L_ & (0b1111111111111111)
    pwm_R = pwm_R_ & (0b1111111111111111)

    pwm_Lh = pwm_L >> 8
    pwm_Ll = pwm_L & (0b11111111)
    pwm_Rh = pwm_R >> 8
    pwm_Rl = pwm_R & (0b11111111)

    tx_pkt = [0x15, 0xEC, 0x00, pwm_Lh, pwm_Ll, pwm_Rh, pwm_Rl, 0x00, 0x04, 0xD2]

    crc = crc8(bytearray(tx_pkt[2:7]))
    tx_pkt[7] = crc

    tx_pkt = bytearray(tx_pkt)

    try:
        ser.write(tx_pkt)
        print('---> Tx : ', pwm_L_, ',', pwm_R_)
    except:
        print('---> Tx : ', 'XXX, XXX')

def receive_command():
    ser.flushInput()
    try:
        rx_pkt = ser.readline()
        rx_pkt = list(rx_pkt)
        index_comma = []
        n = len(rx_pkt)
        for i in range(0,n):
            if(rx_pkt[i]==44):
                index_comma.append(i)
        # print("index_comma: ", index_comma)

        hrt_counter_rx = []
        t_millis_rx = []
        pwm_l_rx = []
        pwm_r_rx = []

        for i in range(0,index_comma[0]):
            hrt_counter_rx.append(rx_pkt[i]-48)
        for i in range(index_comma[0]+1, index_comma[1]):
            t_millis_rx.append(rx_pkt[i]-48)
        for i in range(index_comma[1]+1, index_comma[2]):
            pwm_l_rx.append(rx_pkt[i]-48)
        for i in range(index_comma[2]+1, n-1):
            pwm_r_rx.append(rx_pkt[i]-48)

        hrt_counter_rx_val = 0
        t_millis_rx_val = 0
        pwm_l_rx_val = 0
        pwm_r_rx_val = 0

        for i in range(0,len(hrt_counter_rx)):
            hrt_counter_rx_val = hrt_counter_rx_val*10 + hrt_counter_rx[i]

        for i in range(0,len(t_millis_rx)):
            t_millis_rx_val = t_millis_rx_val*10 + t_millis_rx[i]

        pwm_l_rx_is_negative = False
        for i in range(0,len(pwm_l_rx)):
            if(pwm_l_rx[i]==(-3)):
                pwm_l_rx_is_negative = True
                continue
            pwm_l_rx_val = pwm_l_rx_val*10 + pwm_l_rx[i]
        if(pwm_l_rx_is_negative == True):
            pwm_l_rx_val = -1 * pwm_l_rx_val

        pwm_r_rx_is_negative = False
        for i in range(0,len(pwm_r_rx)):
            if(pwm_r_rx[i]==(-3)):
                pwm_r_rx_is_negative = True
                continue
            pwm_r_rx_val = pwm_r_rx_val*10 + pwm_r_rx[i]
        if(pwm_r_rx_is_negative == True):
            pwm_r_rx_val = -1 * pwm_r_rx_val

        print('<--- Rx : ', pwm_l_rx_val, ',' , pwm_r_rx_val, ",                 " , hrt_counter_rx_val, ",     ", t_millis_rx_val)

    except:
        print('<--- Rx : ', 'XXX, XXX', "RX Error!")

t0 = time.time()

v, w = int(0), int(0)

while running:
    v_input = "0"
    w_input = "0"

    # Process pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get current keyboard state
    keys = pygame.key.get_pressed()

    dv = 25
    dw = 25

    if keys[pygame.K_UP]:
        print("UP")
        v = v + dv

    if keys[pygame.K_DOWN]:
        print("DOWN")
        v = v - dv

    if keys[pygame.K_LEFT]:
        print("LEFT")
        w = w + dw

    if keys[pygame.K_RIGHT]:
        print("RIGHT")
        w = w - dw

    v = limit(v, -255, 255)
    w = limit(w, -255, 255)

    # ESC to quit
    if keys[pygame.K_ESCAPE]:
        running = False

    # v_input = input("v: ") # -255, 255
    # w_input = input("w: ") # -255, 255

    if((v_input == "q") or (w_input == "q") or (running == False)):
        send_command(int(0), int(0))
        time.sleep(0.25)
        break

    # try:
    #     v = int(v_input) # -255, 255
    #     w = int(w_input) # -255, 255
    # except:
    #     pass

    Kv = 1.0
    Kw = 1.0

    pwm_L = int(Kv * v - Kw * w)
    pwm_R = int(Kv * v + Kw * w)

    send_command(pwm_L, pwm_R)
    receive_command()

    pygame.time.Clock().tick(25)
    time.sleep(0.01)

pygame.quit()
ser.close()
