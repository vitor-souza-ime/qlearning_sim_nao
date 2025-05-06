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
