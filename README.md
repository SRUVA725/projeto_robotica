# 🤖 Projeto EV3 - Navegação Autônoma com Sensores
Este projeto utiliza o LEGO Mindstorms EV3 com o sistema ev3dev e a biblioteca pybricks para permitir a navegação autônoma de um robô dentro de um ambiente pré-definido. O robô usa sensores para detectar obstáculos, bordas no chão e ajustar sua rota dinamicamente, garantindo uma movimentação eficiente e precisa.

---

## 📌 Objetivo
O robô deve se deslocar de um ponto inicial até um ponto-alvo dentro de um grid, tomando decisões de movimento com base nas leituras dos sensores. Ele precisa evitar obstáculos, recalibrar sua posição caso detecte desalinhamento e navegar de maneira segura sem cair de bordas detectadas pelo sensor de cor.
O projeto também permite que o robô faça ajustes na trajetória utilizando giroscópio e medições laterais, garantindo que ele consiga escolher a melhor rota caso encontre barreiras inesperadas.

---

## 🧠 Funcionalidades

**Movimentação automática e segura**
- O robô usa o giroscópio para monitorar sua orientação e garantir que ele siga um trajeto estável e preciso.
- Os motores são controlados pelo código para avançar, girar e recalibrar a posição do robô conforme necessário.
**Detecção de obstáculos**
- O sensor ultrassônico mede a distância à frente do robô. Quando detecta um obstáculo próximo, o robô para e decide a melhor rota alternativa, girando para a esquerda ou para a direita.
**Identificação de bordas e mudanças no solo**
- O sensor de cor mede a reflexão do chão. Se detectar um valor baixo de reflexão, significa que há uma borda ou mudança no piso, evitando que o robô caia ou se mova para áreas indesejadas.
**Navegação precisa e correção de trajetória**
- O giroscópio auxilia na correção de pequenos desvios, garantindo que o robô continue na trajetória planejada sem perder o rumo.
- Caso o robô perceba que está desalinhado, ele utiliza um pequeno recuo seguido de avanço para se recalibrar.
**Análise inteligente do caminho**
- A combinação do sensor ultrassônico com a rotação do motor permite ao robô medir distâncias laterais antes de escolher a melhor rota para desviar dos obstáculos.


---

## 🛠️ Componentes Utilizados

**Motores**
- Motor Esquerdo → Porta D
- Motor Direito → Porta A
- Motor do Sensor Ultrassônico → Porta B
**Sensores**
- Sensor Ultrassônico → Porta S1
- Sensor Giroscópio → Porta S2
- Sensor de Cor → Porta S3


---

## 📂 Estrutura do Código

##rotate_sensor_degrees(degrees)##
- Essa função controla o motor responsável pela rotação do sensor ultrassônico. O parâmetro degrees determina o ângulo de rotação, permitindo que o sensor possa medir distâncias à frente, à esquerda ou à direita do robô.
##detect_edge()##
- O sensor de cor verifica a reflexão do solo para determinar se há uma borda. Se a reflexão for menor que um certo limiar, significa que o robô está próximo a uma queda, então ele deve parar. Além disso, a função imprime o valor da reflexão na tela do EV3 Brick.
##move_fwd_cell()##
- Essa função faz o robô avançar uma célula no grid. Antes de se movimentar, ele verifica se há uma borda usando detect_edge(). Se houver, ele para imediatamente. Caso contrário, ele move 150 mm para frente.
##recallibrate()##
- Se o robô perceber que está desalinhado, ele realiza um pequeno recuo seguido de um avanço. Isso ajuda a ajustar sua posição para que continue seguindo corretamente o trajeto.
##turn_left() e turn_right()##
- São funções para girar o robô 90° para a esquerda ou para a direita, respectivamente. Elas ajudam na navegação dentro do grid.
- avoid_obstacle_with_analysis()##
- Essa função permite ao robô evitar obstáculos de forma inteligente. Ele para o movimento e usa rotate_sensor_degrees() para medir a distância à esquerda e à direita. Com base na análise dessas distâncias, decide qual direção seguir e executa a rotação correspondente.
##continuous_navigation()##
- - Essa função principal é responsável pela movimentação contínua do robô. Em um loop infinito, ele:
- - Verifica bordas usando detect_edge(). Se detectar, ele para e espera.
- - Verifica obstáculos com ultra_sonic.distance(). Se um obstáculo estiver próximo, ele usa avoid_obstacle_with_analysis() para decidir a melhor rota.
- - Move para frente caso o caminho esteja livre.
##main()##
- Essa função inicializa a navegação do robô. Ela limpa a tela do EV3, imprime a mensagem de início e chama continuous_navigation() para executar o movimento e tomar decisões em tempo real.

---

## 🚀 Grupo

...

```bash
python ev3_maze.py
```

## 🧑‍🏫 Orientador

Projeto desenvolvido sob orientação de [Gustavo Molina](https://github.com/gustavomolina17/gustavomolina17), que contribuiu com apoio técnico e conceitual ao longo da construção do sistema.
