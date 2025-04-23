🤖 Projeto EV3 - Navegação em Labirinto com Sensores
Este projeto utiliza o LEGO Mindstorms EV3 com o sistema ev3dev e a biblioteca python-ev3dev2 para navegar por um labirinto utilizando sensores ultrassônicos, giroscópio e infravermelho. O robô é capaz de detectar obstáculos, seguir linhas e recalibrar sua posição para garantir uma movimentação precisa.

📌 Objetivo
Controlar um robô para que ele navegue de um ponto inicial até um ponto-alvo dentro de uma grade, detectando obstáculos no caminho e recalibrando sua posição quando necessário. Além disso, o robô deve ser capaz de retornar ao ponto de origem após alcançar o destino.

🧠 Funcionalidades
Movimentação com controle PID para curvas mais precisas.

Detecção de obstáculos com sensor infravermelho.

Desvio automático de obstáculos com rota alternativa.

Seguimento de linha para navegação assistida.

Recalibração automática para correção de posição.

Visualização gráfica (placeholder) da posição do robô na tela EV3.

Mapeamento de rotas e armazenamento dos caminhos percorridos.

🛠️ Componentes Utilizados
Motores:

LargeMotor para as rodas (outA e outD)

LargeMotor para o sensor ultrassônico rotativo (outB)

Sensores:

UltrasonicSensor (in1)

GyroSensor (in4)

InfraredSensor (in2)

Display EV3 para visualização da grade e posição

📂 Estrutura do Código
main(): Função principal que inicia a navegação até o destino e o retorno à origem.

solver(): Algoritmo que percorre a grade em busca do destino.

navigate_with_ir(): Alternativa com navegação baseada em linha e desvio de obstáculos.

move_fwd_cell(), turn_PID_without_reset(): Movimentações básicas.

avoid_obstacle(), detect_obstacle(): Lógica de obstáculos com sensor IR.

recallibrate(): Função de recalibração do robô.

draw_grid(), refresh_screen(): Placeholder para renderização da grade (não implementado).

🚀 Como Usar
Suba o código para o EV3 rodando ev3dev.

Conecte os motores e sensores nas portas especificadas.

Execute o script principal:

bash
Copiar
Editar
python3 nome_do_arquivo.py
Observe o robô se mover do ponto inicial ao destino, recalibrando e desviando obstáculos.

🧑‍🏫 Orientador
Projeto desenvolvido sob orientação de Gustavo Molina, que contribuiu com apoio técnico e conceitual ao longo da construção do sistema.

🧾 Licença
Este projeto é open-source e pode ser modificado e utilizado livremente para fins educacionais.
