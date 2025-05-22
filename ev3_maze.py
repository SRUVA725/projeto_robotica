from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, UltrasonicSensor, ColorSensor, GyroSensor
from pybricks.parameters import Port, Stop
from pybricks.tools import wait
from pybricks.robotics import DriveBase

# Constants
ScreenHeight = 127
ScreenWidth = 177
numOfRows = 4
numOfCols = 6
size_of_route = 58

# Robot direction
RobotDirection = 0  # 0=North, 1=East, 2=South, 3=West

# Start and Target Positions
StartPosRow = 3
StartPosCol = 1
CurrentPosRow = StartPosRow
CurrentPosCol = StartPosCol
TargetPosRow = 0
TargetPosCol = 3

# Motors and Sensors
ev3 = EV3Brick()
motor_L = Motor(Port.D)
motor_R = Motor(Port.A)
motor_Ultrassonic = Motor(Port.B)
ultra_sonic = UltrasonicSensor(Port.S1)
color_sensor = ColorSensor(Port.S3)
gyro = GyroSensor(Port.S2)
drive = DriveBase(motor_L, motor_R, wheel_diameter=56, axle_track=114)

# Grid setup
Grid = [[{"NorthWall": 0, "EastWall": 0, "SouthWall": 0, "WestWall": 0} for _ in range(numOfCols)] for _ in range(numOfRows)]
route_records = []
shortest_routes = []

gyro.reset_angle(0)

# Funções básicas
def rotate_sensor_degrees(degrees):
    motor_Ultrassonic.run_angle(200, degrees, Stop.HOLD, wait=True)

def detect_edge():
    reflection = color_sensor.reflection()
    ev3.screen.print("Reflexão: {}".format(reflection))
    return reflection < 10

def move_fwd_cell():
    try:
        if detect_edge():
            drive.stop()
            ev3.screen.print("Borda detectada!")
            wait(500)
            return
        drive.straight(150)
    except OSError:
        drive.stop()
        wait(200)

def recallibrate():
    drive.straight(-100)
    wait(500)
    drive.straight(100)
    wait(500)

def turn_left():
    drive.turn(-90)

def turn_right():
    drive.turn(90)

# Função para desvio e retorno ao caminho original
def avoid_obstacle_with_analysis():
    drive.stop()
    wait(200)

    # Girar sensor para a esquerda
    rotate_sensor_degrees(-90)
    wait(300)
    left_distance = ultra_sonic.distance()
    ev3.screen.print("Esq: {} mm".format(left_distance))
    wait(200)

    # Girar sensor para a direita
    rotate_sensor_degrees(180)
    wait(300)
    right_distance = ultra_sonic.distance()
    ev3.screen.print("Dir: {} mm".format(right_distance))
    wait(200)

    # Retornar sensor à frente
    rotate_sensor_degrees(-90)
    wait(200)

    # Decisão de direção e desvio
    if left_distance > right_distance:
        ev3.screen.print("Virando à esquerda")
        turn_left()
    else:
        ev3.screen.print("Virando à direita")
        turn_right()

# Navegação contínua apenas para frente com análise de obstáculo

def continuous_navigation():
    while True:
        if detect_edge():
            ev3.screen.print("Sem chão!")
            drive.stop()
            wait(1000)
            continue

        if ultra_sonic.distance() < 150:
            avoid_obstacle_with_analysis()
        else:
            move_fwd_cell()

def main():
    ev3.screen.clear()
    ev3.screen.print("Navegando...")
    continuous_navigation()

main()