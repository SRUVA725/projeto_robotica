from ev3dev2.motor import LargeMotor, MoveSteering, Motor
from ev3dev2.sensor.lego import UltrasonicSensor, GyroSensor, InfraredSensor
from ev3dev2.display import Display
from time import sleep

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
motor_L = LargeMotor('outD')
motor_R = LargeMotor('outA')
motor_Ultrassonic = LargeMotor('outB')  # Motor para o sensor ultrassônico
ultra_sonic = UltrasonicSensor('in1')
gyro = GyroSensor('in4')
ir_sensor = InfraredSensor('in2')

# Grid setup
Grid = [[{"NorthWall": 0, "EastWall": 0, "SouthWall": 0, "WestWall": 0} for _ in range(numOfCols)] for _ in range(numOfRows)]

route_records = []
shortest_routes = []

# Initialize robot direction and position
gyro.reset()

# Function to rotate the ultrasonic sensor by a certain number of degrees
def rotate_sensor_degrees(degrees):
    motor_Ultrassonic.on_for_degrees(10, degrees)  # Gira o motor por 'degrees' graus

# Function for moving the robot forward
def move_no_PID_bump():
    motor_L.on(10)
    motor_R.on(10)

# Function for moving the robot backward
def move_reverse_nopid():
    motor_L.on(-10)
    motor_R.on(-10)

# Turning with PID
def turn_PID_without_reset(goal):
    Kp = 5
    Ki = 0.9
    Kd = 5
    power_L = 0
    power_R = 0
    previous_error = 0
    count = 0

    while True:
        error = gyro.angle - goal
        proportional = error * Kp
        derivative = (error - previous_error) * Kd
        integral = -(proportional - derivative) * Ki
        adjust = proportional + derivative + integral
       
        if adjust < 0 and adjust > -1:
            adjust = -2
        if adjust > 0 and adjust < 1:
            adjust = 2

        motor_L.on(adjust)
        motor_R.on(-adjust)

        if gyro.angle == goal:
            count += 1
            if count > 200:
                motor_L.off()
                motor_R.off()
                previous_error = 0
                break

# Move one cell forward
def move_fwd_cell():
    motor_L.reset_angle(0)
    motor_R.reset_angle(0)

    while True:
        if motor_L.angle >= 471 and motor_R.angle >= 471:
            motor_L.off()
            motor_R.off()
            break
        elif ultra_sonic.distance_centimeters <= 4:
            motor_L.off()
            motor_R.off()
            break

    turn_PID_without_reset(0)

# Re-calibrate the robot
def recallibrate():
    timer_limit_2 = 3000
    timer_2 = 0

    # reverse to align with wall
    motor_L.on(-10)
    motor_R.on(-10)
    sleep(3)

    motor_L.off()
    motor_R.off()
    sleep(0.5)

    # move forward to bump the front wall
    motor_L.on(10)
    motor_R.on(10)
    sleep(3)

    motor_L.off()
    motor_R.off()
    sleep(0.5)

# Draw grid and robot on display
def draw_grid():
    # This function will handle drawing walls and the robot's position on the grid
    pass

def refresh_screen():
    draw_grid()
    draw_robot_position()

def draw_robot_position():
    pass

# Function to detect obstacles with the infrared sensor
def detect_obstacle():
    distance = ir_sensor.distance()  # Assumindo que o sensor retorna a distância
    if distance < 20:  # Ajuste o valor conforme o seu sensor
        return True
    return False

# Function to follow a line using the infrared sensor
def follow_line():
    # Assume que o sensor IR detecta a linha como uma diferença de intensidade de luz.
    line_detected = ir_sensor.value()  # A leitura do valor do sensor IR
    if line_detected == 1:  # Valor que indica que a linha foi detectada
        motor_L.on(20)
        motor_R.on(20)
    else:
        motor_L.on(10)
        motor_R.on(10)

# Function to avoid an obstacle detected by the infrared sensor
def avoid_obstacle():
    if detect_obstacle():
        # Exemplo de desvio simples: parar e girar para a esquerda
        motor_L.off()
        motor_R.off()
        turn_left()
        turn_PID_without_reset(90)  # Girar 90 graus
        move_fwd_cell()

# Function to navigate using the infrared sensor and avoid obstacles
def navigate_with_ir():
    while True:
        # Detectar se o caminho está livre
        if detect_obstacle():
            avoid_obstacle()  # Desvia do obstáculo
        else:
            # Se não houver obstáculo, siga a linha
            follow_line()
            move_fwd_cell()

# Main Solver Logic
def solver():
    route_records.append({'x': CurrentPosRow, 'y': CurrentPosCol})

    # Robot's main pathfinding
    while (CurrentPosCol != TargetPosCol) or (CurrentPosRow != TargetPosRow):
        if ultra_sonic.distance_centimeters < 15:
            turn_left()
            continue
       
        move_fwd_cell()
        # Update the position
        if RobotDirection == 0:
            CurrentPosRow += 1
        elif RobotDirection == 1:
            CurrentPosCol += 1
        elif RobotDirection == 2:
            CurrentPosRow -= 1
        elif RobotDirection == 3:
            CurrentPosCol -= 1

        route_records.append({'x': CurrentPosRow, 'y': CurrentPosCol})
        turn_right()

# Move to target direction
def move_to_target(target):
    while RobotDirection != target:
        if RobotDirection > target:
            if RobotDirection == 3 and target == 0:
                turn_right()
            else:
                turn_left()
        else:
            if RobotDirection == 0 and target == 3:
                turn_left()
            else:
                turn_right()

    move_fwd_cell()
    if ultra_sonic.distance_centimeters < 15:
        recallibrate()

# Main program flow
def main():
    # Initialize grid, solve the maze, and return to home
    solver()
    print("Reached Target!")

    # Implement returning to the start/home
    for route in reversed(shortest_routes):
        move_to_target(route['x'])

if __name__ == "__main__":
    main()
