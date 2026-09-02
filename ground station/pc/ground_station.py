print('GCS DDR2019')

import serial
import time

ser = serial.Serial()
ser.baudrate = 9600
# ser.port = '/dev/rfcomm3'
ser.port = 'COM7'
# ser.timeout = 0.15

ser.close()

time.sleep(1)

ser.open()

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
        print('---> Tx', pwm_L, ',', pwm_R)
    except:
        print('---> Tx', 'XXX, XXX')

def receive_command():
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

        # print("hrt_counter_rx: ", hrt_counter_rx)
        # print("t_millis_rx   : ", t_millis_rx)
        # print("pwm_l_rx      : ", pwm_l_rx)
        # print("pwm_r_rx      : ", pwm_r_rx)

        hrt_counter_rx_val = 0
        t_millis_rx_val = 0
        pwm_l_rx_val = 0
        pwm_r_rx_val = 0

        for i in range(0,len(hrt_counter_rx)):
            hrt_counter_rx_val = hrt_counter_rx_val*10 + hrt_counter_rx[i]

        for i in range(0,len(t_millis_rx)):
            t_millis_rx_val = t_millis_rx_val*10 + t_millis_rx[i]
        
        for i in range(0,len(pwm_l_rx)):
            pwm_l_rx_val = pwm_l_rx_val*10 + pwm_l_rx[i]
        
        for i in range(0,len(pwm_r_rx)):
            pwm_r_rx_val = pwm_r_rx_val*10 + pwm_r_rx[i]

        print('<--- Rx', pwm_l_rx_val , pwm_r_rx_val, hrt_counter_rx_val, t_millis_rx_val)
    except:
        print('<--- Rx', 'XXX, XXX', "RX Error!")

t0 = time.time()

while 1:
    v = int(input("v: ")) # -255, 255
    w = int(input("w: ")) # -255, 255

    Kv = 1.0
    Kw = 1.0

    pwm_L = int(Kv * v - Kw * w)
    pwm_R = int(Kv * v + Kw * w)

    send_command(pwm_L, pwm_R)
    receive_command()

    time.sleep(0.075)

ser.close()
