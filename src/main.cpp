/*
  Project: DDR2019
  Arduino Uno and Bluetooth serial communication
  Input is given from ground station
*/

#include <Arduino.h>

// assign motor pins
#define ML1 2
#define ML2 3
#define MR1 7
#define MR2 4
#define ENL 5
#define ENR 6

// cyclic time
uint64_t freq_cyclic_hz = 100;
uint64_t t_loop_us = static_cast<uint64_t>(1000000.0 / static_cast<double>(freq_cyclic_hz)); // microseconds
uint64_t last_loop_time_us = 0;																 // last loop time in microseconds

// maximum and command pwm value for motor driver
int16_t PWM_MAX = 225; // @12 Volt
int16_t pwm_L;
int16_t pwm_R;

// define packet structure for communication
byte pkt_rx[10] = {0x15, 0xEC, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0xD2};
byte pkt_rx_crc[5] = {0x00, 0x00, 0x00, 0x00, 0x00};
uint8_t crc;
uint64_t pkt_rx_last_valid_time;
uint64_t comm_out_timeout = 1500; // milliseconds
uint32_t hrt_counter = 0;		  // high resolution timer counter
uint64_t tx_pkt_freq = 10;
uint64_t tx_pkt_counter_trig = static_cast<uint64_t>(static_cast<double>(freq_cyclic_hz) / static_cast<double>(tx_pkt_freq));
uint64_t tx_pkt_counter = 1;

// function prototypes
void setup_motor_pins();
void receive_data(int16_t &pwm_L, int16_t &pwm_R);
byte new_msg_available();
void send_data();
void drive_robot(int16_t pwm_L, int16_t pwm_R);
void drive_motor_L(int16_t pwm);
void drive_motor_R(int16_t pwm);
int16_t saturate(int16_t x, int16_t x_min, int16_t x_max);
uint8_t crc8(const uint8_t *data, uint32_t length);

void setup()
{
	Serial.begin(9600); // initialize serial communication at 9600 baud rate for bluetooth module

	setup_motor_pins();

	pwm_L = 0;
	pwm_R = 0;

	drive_robot(pwm_L, pwm_R);

	pkt_rx_last_valid_time = millis();
	last_loop_time_us = micros();
	tx_pkt_counter = 1;
}

void loop()
{
	receive_data(pwm_L, pwm_R);
	drive_robot(pwm_L, pwm_R);

	tx_pkt_counter++;
	if (tx_pkt_counter >= tx_pkt_counter_trig)
	{
		send_data();
		tx_pkt_counter = 1;
	}

	while (micros() - last_loop_time_us < t_loop_us)
	{
	}
	last_loop_time_us = micros();
}

void receive_data(int16_t &pwm_L, int16_t &pwm_R)
{
	while (Serial.available() > 0)
	{
		byte b = Serial.read();
		for (int i = 0; i < 9; i++)
		{
			pkt_rx[i] = pkt_rx[i + 1];
		}
		pkt_rx[9] = b;

		byte n = new_msg_available();

		if ((millis() - pkt_rx_last_valid_time) > comm_out_timeout)
		{
			pwm_L = 0;
			pwm_R = 0;
		}
		else
		{
			if (n == 0x00)
			{
				pkt_rx_last_valid_time = millis();
				pwm_L = (((int16_t)pkt_rx[3]) << 8) | pkt_rx[4];
				pwm_R = (((int16_t)pkt_rx[5]) << 8) | pkt_rx[6];
			}
			else
			{
			}
		}
	}
}

byte new_msg_available()
{
	bool pkt_available = (pkt_rx[0] == 0x15) && (pkt_rx[1] == 0xEC) && (pkt_rx[8] == 0x04) && (pkt_rx[9] == 0xD2);
	if (pkt_available == true)
	{
		pkt_rx_crc[0] = pkt_rx[2];
		pkt_rx_crc[1] = pkt_rx[3];
		pkt_rx_crc[2] = pkt_rx[4];
		pkt_rx_crc[3] = pkt_rx[5];
		pkt_rx_crc[4] = pkt_rx[6];
		uint8_t crc = crc8(pkt_rx_crc, sizeof(pkt_rx_crc));
		bool pkt_valid = (crc == pkt_rx[7]);

		if (pkt_valid == true)
		{
			return pkt_rx[2];
		}
		else
		{
			return 0xFF;
		}
	}
	else
	{
		return 0xFF;
	}
}

void send_data()
{
	Serial.print(hrt_counter);
	Serial.print(',');
	Serial.print(millis());
	Serial.print(',');
	Serial.print(pwm_L);
	Serial.print(',');
	Serial.print(pwm_R);
	Serial.print('\n');

	hrt_counter++;
}

void setup_motor_pins()
{
	pinMode(ML1, OUTPUT);
	pinMode(ML2, OUTPUT);
	pinMode(MR1, OUTPUT);
	pinMode(MR2, OUTPUT);
	pinMode(ENL, OUTPUT);
	pinMode(ENR, OUTPUT);
}

void drive_robot(int16_t pwm_L_, int16_t pwm_R_)
{
	drive_motor_L(pwm_L_);
	drive_motor_R(pwm_R_);
}

void drive_motor_L(int16_t pwm)
{
	pwm = saturate(pwm, -PWM_MAX, PWM_MAX);
	if (pwm >= 0)
	{
		digitalWrite(ML1, HIGH);
		digitalWrite(ML2, LOW);
		analogWrite(ENL, pwm);
	}
	else
	{
		digitalWrite(ML1, LOW);
		digitalWrite(ML2, HIGH);
		analogWrite(ENL, -pwm);
	}
}

void drive_motor_R(int16_t pwm)
{
	pwm = saturate(pwm, -PWM_MAX, PWM_MAX);
	if (pwm >= 0)
	{
		digitalWrite(MR1, HIGH);
		digitalWrite(MR2, LOW);
		analogWrite(ENR, pwm);
	}
	else
	{
		digitalWrite(MR1, LOW);
		digitalWrite(MR2, HIGH);
		analogWrite(ENR, -pwm);
	}
}

int16_t saturate(int16_t x, int16_t x_min, int16_t x_max)
{
	if (x > x_max)
	{
		return x_max;
	}
	else if (x < x_min)
	{
		return x_min;
	}
	else
	{
		return x;
	}
}

uint8_t crc8(const uint8_t *data, uint32_t length)
{
	const uint8_t polynomial = 0x07;
	uint8_t crc = 0x00;
	for (uint8_t i = 0; i < length; i++)
	{
		crc ^= data[i];
		for (uint8_t j = 0; j < 8; j++)
		{
			if (crc & 0x80)
			{
				crc = (crc << 1) ^ polynomial;
			}
			else
			{
				crc <<= 1;
			}
		}
	}
	return crc;
}