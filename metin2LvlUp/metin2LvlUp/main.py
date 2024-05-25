import pydirectinput as pyd
import time

times = 10
time.sleep(2)

ch1_coord = (973, 321)
ch2_coord = (966, 354)
ch3_coord = (966, 380)
ch4_coord = (966, 413)
ch5_coord = (966, 441)
ch6_coord = (966, 470)
ch7_coord = (966, 500)
ch8_coord = (966, 530)

time.sleep(2)

while True:

    pyd.keyDown('2')
    time.sleep(0.5)
    pyd.keyUp('2')

    print("am apasat 2")

    pyd.keyDown('2')
    time.sleep(0.5)
    pyd.keyUp('2')
    print("am apasat 2")

    pyd.keyDown('2')
    time.sleep(0.5)
    pyd.keyUp('2')
    print("am apasat 2")

    pyd.keyDown('space')
    time.sleep(13)
    pyd.keyUp('space')
    print("am apasat space")

    pyd.keyDown('z')
    time.sleep(1)
    pyd.keyUp('z')
    print("am apasat z")

    pyd.keyDown('x')
    time.sleep(1)
    pyd.keyUp('x')
    print("am apasat x")

    if times % 8 == 1:
        pyd.leftClick(ch1_coord[0], ch1_coord[1])
        time.sleep(2.5)
        pyd.rightClick(ch1_coord[0], ch1_coord[1])
    elif times % 8 == 2:
        pyd.leftClick(ch2_coord[0], ch2_coord[1])
        time.sleep(2.5)
        pyd.rightClick(ch1_coord[0], ch1_coord[1])
    elif times % 8 == 3:
        pyd.leftClick(ch3_coord[0], ch3_coord[1])
        time.sleep(2.5)
        pyd.rightClick(ch1_coord[0], ch1_coord[1])
    elif times % 8 == 4:
        pyd.leftClick(ch4_coord[0], ch4_coord[1])
        time.sleep(2.5)
        pyd.rightClick(ch1_coord[0], ch1_coord[1])
    elif times % 8 == 5:
        pyd.leftClick(ch5_coord[0], ch5_coord[1])
        time.sleep(2.5)
        pyd.rightClick(ch1_coord[0], ch1_coord[1])
    elif times % 8 == 6:
        pyd.leftClick(ch6_coord[0], ch6_coord[1])
        time.sleep(2.5)
        pyd.rightClick(ch1_coord[0], ch1_coord[1])
    elif times % 8 == 7:
        pyd.leftClick(ch7_coord[0], ch7_coord[1])
        time.sleep(2.5)
        pyd.rightClick(ch1_coord[0], ch1_coord[1])
    elif times % 8 == 0:
        pyd.leftClick(ch8_coord[0], ch8_coord[1])
        time.sleep(2.5)
        pyd.rightClick(ch1_coord[0], ch1_coord[1])

    times += 1
