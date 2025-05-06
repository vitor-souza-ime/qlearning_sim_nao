**NAO Robot Joint Control Using Q-Learning**
This project implements a Q-Learning algorithm to control the joints of the NAO robot in a CoppeliaSim simulation. The goal is to adjust the angle of a specific joint (left arm) to reach a defined target angle using reinforcement learning.
Description
The program uses the coppeliasim_zmqremoteapi_client library to interact with CoppeliaSim and control the NAO robot's joints. The Q-Learning algorithm is configured to learn the best action (increase, decrease, or maintain the angle) based on a Q-table that maps discrete states to actions.
Main Components

Class NAORobotController: Manages the connection to CoppeliaSim, configures the robot's joints, and executes Q-Learning training.
Q-Learning Parameters:
EPSILON: Initial exploration rate (0.2).
ALPHA: Learning rate (0.2).
GAMMA: Discount factor (0.9).
NUM_EPISODES: Number of episodes (100).
NUM_ACTIONS: Possible actions (-1: decrease, 0: maintain, +1: increase).
ANGLE_LIMIT: Angle limit (±90° in radians).


Reward: Calculated as the negative of the absolute difference between the current angle and the target angle.
Exploration: Uses an epsilon-greedy policy with epsilon decay.

Prerequisites

Python 3.8 or higher
CoppeliaSim (version compatible with ZMQ Remote API)
Python libraries:pip install numpy coppeliasim-zmqremoteapi-client



How to Run

Set up CoppeliaSim:

Ensure CoppeliaSim is installed and configured.
Load the NAO robot scene in CoppeliaSim.


Install dependencies:
pip install -r requirements.txt


Run the program:
python qlearning01.py

The program will start the simulation, execute Q-Learning training to achieve a target angle of 45°, and display the progress of each episode.

Stop the simulation:

The program automatically terminates after reaching the target angle (with a tolerance of ±0.5°) or after completing the defined episodes.
The simulation is stopped, and the connection is closed at the end.



Code Structure

qlearning01.py: Main script containing the controller and Q-Learning algorithm implementation.
Class NAORobotController:
Methods for connecting to CoppeliaSim, configuring joints, selecting actions, and updating the Q-table.
q_learning function to execute training.


Function main: Initializes the controller, runs the training, and handles exceptions.

Results

The program prints the progress of each episode, including the total reward and the current angle in radians and degrees.
Training ends when the current angle is within ±0.5° of the target angle (45°).

Limitations

The example simplifies control to a single joint (left arm).
State space discretization is basic (10 states).
The simulation may be sensitive to CoppeliaSim configuration.

Contributions
Contributions are welcome! To suggest improvements or report issues:

Open an issue in the repository.
Submit a pull request with your changes.

License
This project is licensed under the MIT License.



**Controle de Juntas do Robô NAO por Q-Learning**

Este projeto implementa um algoritmo de Q-Learning para controlar as juntas do robô NAO em uma simulação no CoppeliaSim. O objetivo é ajustar o ângulo de uma junta específica (braço esquerdo) para alcançar um ângulo alvo definido, utilizando aprendizado por reforço.
Descrição
O programa utiliza a biblioteca coppeliasim_zmqremoteapi_client para interagir com o CoppeliaSim e controlar as juntas do robô NAO. O algoritmo de Q-Learning é configurado para aprender a melhor ação (aumentar, diminuir ou manter o ângulo) com base em uma tabela Q que mapeia estados discretos a ações.
Principais Componentes:

Classe NAORobotController: Gerencia a conexão com o CoppeliaSim, configura as juntas do robô e executa o treinamento por Q-Learning.
Parâmetros de Q-Learning:
EPSILON: Taxa de exploração inicial (0.2).
ALPHA: Taxa de aprendizado (0.2).
GAMMA: Fator de desconto (0.9).
NUM_EPISODES: Número de episódios (100).
NUM_ACTIONS: Ações possíveis (-1: diminuir, 0: manter, +1: aumentar).
ANGLE_LIMIT: Limite de ângulo (±90° em radianos).


Recompensa: Calculada como a negativa da diferença absoluta entre o ângulo atual e o ângulo alvo.
Exploração: Utiliza política epsilon-greedy com decaimento de epsilon.

Pré-requisitos:

Python 3.8 ou superior
CoppeliaSim (versão compatível com a API ZMQ Remote)
Bibliotecas Python:pip install numpy coppeliasim-zmqremoteapi-client



Como Executar

Configurar o CoppeliaSim:

Certifique-se de que o CoppeliaSim está instalado e configurado.
Carregue a cena do robô NAO no CoppeliaSim.


Executar o programa:
python qlearning01.py

O programa iniciará a simulação, executará o treinamento por Q-Learning para alcançar um ângulo alvo de 45° e exibirá o progresso de cada episódio.

Parar a simulação:

O programa encerra automaticamente após encontrar o ângulo alvo (com tolerância de ±0.5°) ou após completar os episódios definidos.
A simulação é parada e a conexão encerrada ao final.



Estrutura do Código

qlearning01.py: Script principal contendo a implementação do controlador e do algoritmo Q-Learning.
Classe NAORobotController:
Métodos para conexão com CoppeliaSim, configuração de juntas, escolha de ações e atualização da tabela Q.
Função q_learning para executar o treinamento.


Função main: Inicializa o controlador, executa o treinamento e gerencia exceções.

Resultados

O programa imprime o progresso de cada episódio, incluindo a recompensa total e o ângulo atual em radianos e graus.
O treinamento termina quando o ângulo atual está dentro de ±0.5° do ângulo alvo (45°).

Limitações

O exemplo simplifica o controle para uma única junta (braço esquerdo).
A discretização do espaço de estados é básica (10 estados).
A simulação pode ser sensível à configuração do CoppeliaSim.

Contribuições
Contribuições são bem-vindas! Para sugerir melhorias ou relatar problemas:

Abra uma issue no repositório.
Envie um pull request com suas alterações.

Licença
Este projeto está licenciado sob a MIT License.
