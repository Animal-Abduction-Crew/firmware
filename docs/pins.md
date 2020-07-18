# Pins auf dem PI

## Übersicht

```
   3V3  (1) (2)  5V    
 GPIO2  (3) (4)  5V    
 GPIO3  (5) (6)  GND   
 GPIO4  (7) (8)  GPIO14
   GND  (9) (10) GPIO15
GPIO17 (11) (12) GPIO18
GPIO27 (13) (14) GND   
GPIO22 (15) (16) GPIO23
   3V3 (17) (18) GPIO24
GPIO10 (19) (20) GND   
 GPIO9 (21) (22) GPIO25
GPIO11 (23) (24) GPIO8 
   GND (25) (26) GPIO7 
 GPIO0 (27) (28) GPIO1 
 GPIO5 (29) (30) GND   
 GPIO6 (31) (32) GPIO12
GPIO13 (33) (34) GND   
GPIO19 (35) (36) GPIO16
GPIO26 (37) (38) GPIO20
   GND (39) (40) GPIO21
```

## Rad rechts

```python
GPIO_PWM = 18 # PWM pin
GPIO_IN1 = 14 # motor control pin
GPIO_IN2 = 15 # motor control pin
```

## Rad Links

```python
GPIO_PWM = 12 # PWM pin
GPIO_IN1 = 7 # motor control pin
GPIO_IN2 = 8 # motor control pin
```

## Greifer

```python
GPIO_PWM = 13 # PWM pin
GPIO_IN1 = 5 # motor control pin
GPIO_IN2 = 6 # motor control pin

RUNNING_TIME = 1 # seconds
PWM_FREQUENCY = 50000 # Hz
PWM_DUTY_CYCLE = 60 # percent°
```

## Ultrasonic

```python
Trigger  17
Echo     27

Trigger  10
Echo     09
```

## Schalter


## Infrarot

```
link       Pin 2
rechts     Pin 3
mitte      Pin 4

max zu:  16
max auf: 21
```
