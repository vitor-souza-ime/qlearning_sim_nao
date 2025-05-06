````markdown
# Controle de Juntas do Robô NAO por Q-Learning

## Descrição

Este projeto implementa um controle de juntas do robô NAO utilizando Q-Learning. O objetivo é treinar o robô para atingir um ângulo alvo específico, ajustando a posição das suas juntas por meio de um processo de aprendizagem por reforço.

A técnica de Q-Learning é usada para aprender a política de controle ideal, ajustando as posições das juntas com base na recompensa associada à proximidade do ângulo alvo.

## Requisitos

- **CoppeliaSim**: Simulador de robótica utilizado para a simulação do robô NAO.
- **Biblioteca RemoteAPIClient**: Utilizada para estabelecer a comunicação entre o código Python e o CoppeliaSim.
- **Python 3.x**: A linguagem de programação utilizada para implementar o código.

### Dependências

1. **CoppeliaSim** (anteriormente V-REP) com a API remota habilitada.
2. **numpy**: Biblioteca para manipulação de arrays e operações matemáticas.
3. **math**: Biblioteca padrão do Python para cálculos matemáticos.

Instale a biblioteca `numpy` com o seguinte comando:
```bash
pip install numpy
````

## Arquitetura

### Classe `NAORobotController`

A classe `NAORobotController` é responsável por controlar o robô NAO dentro da simulação CoppeliaSim, realizando as operações de:

* **Conectar e configurar a simulação**.
* **Obter e ajustar as posições das juntas do robô**.
* **Implementar o algoritmo de Q-Learning para aprender o controle das juntas**.

### Q-Learning

O Q-Learning é implementado de forma simplificada para ajustar uma única junta do braço esquerdo do robô NAO. A cada episódio, o algoritmo tenta alcançar um ângulo alvo ajustando a posição da junta com base na política epsilon-greedy.

### Parâmetros de Q-Learning

* **EPSILON**: Taxa de exploração inicial (20%).
* **ALPHA**: Taxa de aprendizado (20%).
* **GAMMA**: Fator de desconto (90%).
* **NUM\_EPISODES**: Número de episódios para o treinamento (100 episódios).
* **MAX\_STEPS**: Número máximo de passos por episódio (1 passo).
* **NUM\_ACTIONS**: Número de ações possíveis (-1, 0, +1 para diminuir, manter e aumentar o ângulo, respectivamente).
* **ANGLE\_LIMIT**: Limite do ângulo em radianos (±90 graus).
* **MIN\_EPSILON**: Valor mínimo para o epsilon (decai ao longo do tempo).
* **EPSILON\_DECAY**: Taxa de decaimento do epsilon (0.995 por episódio).

## Como Usar

1. **Conectar ao CoppeliaSim**: O código utiliza a biblioteca `RemoteAPIClient` para conectar-se ao CoppeliaSim. A simulação do robô NAO deve estar configurada com a API remota habilitada.

2. **Rodar o Código**: Basta executar o script Python para iniciar o treinamento do robô.

```bash
python nao_qlearning.py
```

O robô irá aprender a ajustar a posição da junta do braço esquerdo para atingir um ângulo de 45° ao longo de 100 episódios.

3. **Resultados**: Durante o treinamento, o código imprime a recompensa total acumulada por episódio, o ângulo atual da junta e informações sobre o progresso do treinamento.

## Detalhes do Algoritmo de Q-Learning

* **Estados**: O estado é baseado na posição da junta, discretizada em 10 estados possíveis.
* **Ações**: A ação pode ser -1 (diminuir o ângulo), 0 (manter o ângulo) ou +1 (aumentar o ângulo).
* **Recompensa**: A recompensa é calculada como a distância negativa entre a posição atual da junta e o ângulo alvo de 45° (quanto mais próximo, maior a recompensa).

### Ajuste de Parâmetros

É possível ajustar os parâmetros do Q-Learning, como `EPSILON`, `ALPHA`, `GAMMA`, e o número de episódios, para testar o desempenho do algoritmo em diferentes condições.

## Conclusão

O controle de juntas do robô NAO usando Q-Learning permite que o robô aprenda de forma autônoma a ajustar suas juntas para atingir posições específicas, utilizando técnicas de aprendizado por reforço. Este projeto pode ser expandido para incluir múltiplas juntas ou diferentes objetivos de controle.

## Licença

Este projeto é de código aberto e está licenciado sob a Licença MIT.

