from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, UltrasonicSensor, ColorSensor, GyroSensor
from pybricks.parameters import Port, Stop
from pybricks.tools import wait
from pybricks.robotics import DriveBase

# Direção do robô (0=North, 1=East, 2=South, 3=West)
RobotDirection = 0

# Definição da posição inicial e destino do robô
StartPosRow = 3
StartPosCol = 1
CurrentPosRow = StartPosRow
CurrentPosCol = StartPosCol
TargetPosRow = 0
TargetPosCol = 3

# Inicialização do EV3 Brick e dos motores
ev3 = EV3Brick()
motor_L = Motor(Port.D)  # Motor esquerdo conectado na porta D
motor_R = Motor(Port.A)  # Motor direito conectado na porta A
motor_Ultrassonic = Motor(Port.B)  # Motor do sensor ultrassônico na porta B

# Inicialização dos sensores
ultra_sonic = UltrasonicSensor(Port.S1)  # Sensor ultrassônico na porta S1
color_sensor = ColorSensor(Port.S3)      # Sensor de cor na porta S3
gyro = GyroSensor(Port.S2)               # Sensor giroscópio na porta S2

# Inicialização da base de condução do robô (DriveBase)
drive = DriveBase(motor_L, motor_R, wheel_diameter=56, axle_track=114)

# Configuração da grade de navegação
Grid = [[{"NorthWall": 0, "EastWall": 0, "SouthWall": 0, "WestWall": 0} for _ in range(numOfCols)] for _ in range(numOfRows)]
route_records = []  # Lista para armazenar caminhos percorridos
shortest_routes = []  # Lista para armazenar as rotas mais curtas

gyro.reset_angle(0)  # Resetando o giroscópio para garantir leituras precisas

# Função para girar o sensor ultrassônico
def rotate_sensor_degrees(degrees):
    """
    Rotaciona o sensor ultrassônico para medir distâncias laterais.
    Permite a rotação para a esquerda, direita e retorno à posição inicial.
    """
    motor_Ultrassonic.run_angle(200, degrees, Stop.HOLD, wait=True)

# Função para detectar bordas
def detect_edge():
    """
    Mede a reflexão do solo utilizando o sensor de cor.
    Se a reflexão for menor que um limite, significa que há uma borda e o robô deve parar.
    """
    reflection = color_sensor.reflection()
    ev3.screen.print("Reflexão: {}".format(reflection))
    return reflection < 10

# Função para movimentação frontal segura
def move_fwd_cell():
    """
    Move o robô para frente verificando antes se há uma borda.
    Caso detecte uma borda, ele para imediatamente para evitar quedas.
    """
    try:
        if detect_edge():
            drive.stop()
            ev3.screen.print("Borda detectada!")
            wait(500)
            return
        drive.straight(150)  # Movendo 150 mm para frente
    except OSError:
        drive.stop()
        wait(200)

# Função para recalibrar a posição do robô
def recallibrate():
    """
    Caso o robô perceba um desalinhamento, ele recua um pouco e depois avança
    para corrigir pequenos erros na trajetória.
    """
    drive.straight(-100)
    wait(500)
    drive.straight(100)
    wait(500)

# Funções para girar o robô
def turn_left():
    """Gira o robô 90° para a esquerda."""
    drive.turn(-90)

def turn_right():
    """Gira o robô 90° para a direita."""
    drive.turn(90)

# Função para evitar obstáculos e decidir melhor rota
def avoid_obstacle_with_analysis():
    """
    Analisa obstáculos à frente do robô e decide se ele deve desviar pela esquerda ou pela direita.
    Faz medições laterais e escolhe o caminho com maior distância livre.
    """
    drive.stop()
    wait(200)

    # Medir distância à esquerda
    rotate_sensor_degrees(-90)
    wait(300)
    left_distance = ultra_sonic.distance()
    ev3.screen.print("Esq: {} mm".format(left_distance))
    wait(200)

    # Medir distância à direita
    rotate_sensor_degrees(180)
    wait(300)
    right_distance = ultra_sonic.distance()
    ev3.screen.print("Dir: {} mm".format(right_distance))
    wait(200)

    # Retornar sensor à posição frontal
    rotate_sensor_degrees(-90)
    wait(200)

    # Escolher direção para desvio do obstáculo
    if left_distance > right_distance:
        ev3.screen.print("Virando à esquerda")
        turn_left()
    else:
        ev3.screen.print("Virando à direita")
        turn_right()

# Função de navegação contínua com análise de obstáculos
def continuous_navigation():
    """
    Responsável pela movimentação contínua do robô.
    Ele verifica bordas, detecta obstáculos e ajusta sua trajetória automaticamente.
    """
    while True:
        if detect_edge():
            ev3.screen.print("Sem chão!")  # Exibe alerta no EV3
            drive.stop()
            wait(1000)
            continue

        if ultra_sonic.distance() < 150:
            avoid_obstacle_with_analysis()  # Se houver obstáculo, decide o melhor desvio
        else:
            move_fwd_cell()  # Se o caminho estiver livre, avança

# Função principal do código
def main():
    """
    Inicializa o sistema do robô, limpa a tela e inicia a navegação.
    Chama a função continuous_navigation() para que o robô opere de forma autônoma.
    """
    ev3.screen.clear()
    ev3.screen.print("Navegando...")
    continuous_navigation()

# Chamando a função principal para iniciar o robô
main()
