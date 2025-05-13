from naoqi import ALProxy
import numpy as np
import random
import time
import math
import datetime
#import pickle
import os

# Parâmetros do Q-Learning
alpha = 0.3         # Taxa de aprendizado
gamma = 0.9         # Fator de desconto
epsilon = 0.2       # Taxa de exploração
n_actions = 5       # Número de ações possíveis (ajustes de ângulo)
n_states = 100      # Discretização dos ângulos
ANGLE_LIMIT = math.radians(90)
MAX_STEPS = 1
EPISODES = 100

Q_TABLE_FILENAME = "qtable_nao.npy"

def load_q_table():
    if os.path.exists(Q_TABLE_FILENAME):
        print "Carregando tabela Q de {0}...".format(Q_TABLE_FILENAME)
        Q = np.load(Q_TABLE_FILENAME)
        if Q.shape != (n_states, n_actions):
            print "Erro: Tabela Q carregada tem formato {0}, esperado ({1}, {2}). Inicializando nova tabela.".format(Q.shape, n_states, n_actions)
            Q = np.zeros((n_states, n_actions))
    else:
        print "Nenhuma tabela Q encontrada em {0}. Inicializando nova tabela.".format(Q_TABLE_FILENAME)
        Q = np.zeros((n_states, n_actions))
    return Q

def save_q_table(Q):
    print "Salvando tabela Q em {0}...".format(Q_TABLE_FILENAME)
    np.save(Q_TABLE_FILENAME, Q)
    
Q = load_q_table()


# Inicializando a tabela Q
#Q = np.zeros((n_states, n_actions))

def connect_to_robot(ip, port=9559):
    motion = ALProxy("ALMotion", ip, port)
    motion.wakeUp()  # Ativa os motores
    return motion

def get_current_angle(motion, joint_name):
    return motion.getAngles(joint_name, True)[0]

def discretize_angle(angle):
    # Discretiza o ângulo em um estado
    return int(np.clip((angle + np.pi) / (2 * np.pi) * n_states, 0, n_states - 1))

def choose_action(state):
    if random.uniform(0, 1) < epsilon:
        return random.randint(0, n_actions - 1)  # Exploração
    return np.argmax(Q[state])  # Exploração

def move_joint(motion, joint_name, action):
    # Ajuste do ângulo
    angle_adjustment = (action - (n_actions - 1) / 2) * 0.1  # Ajuste de ângulo pequeno
    motion.setStiffnesses(joint_name, 1.0)
    current_angle = get_current_angle(motion, joint_name)

    # Limites de movimento da articulação (ajustar conforme necessário)
    min_angle = -2.0  # Exemplo de limite inferior (ajuste conforme necessário)
    max_angle = 2.0   # Exemplo de limite superior (ajuste conforme necessário)

    min_angle = -math.radians(90)
    max_angle = math.radians(90)

    # Aplicando a mudança de ângulo
    new_angle = np.clip(current_angle + angle_adjustment, min_angle, max_angle)
    motion.angleInterpolation(joint_name, new_angle, 1.0, True)
    return new_angle
'''
def update_Q(state, action, reward, next_state):
    best_next_action = np.argmax(Q[next_state])
    td_target = reward + gamma * Q[next_state][best_next_action]
    Q[state][action] += alpha * (td_target - Q[state][action])
'''
def update_Q(state, action, reward, next_state):
    """
    Atualiza o valor Q para o par (estado, ação) com base no Q-learning.

    Args:
        state (int): O índice do estado atual.
        action (int): O índice da ação tomada no estado.
        reward (float): A recompensa recebida após tomar a ação.
        next_state (int): O índice do próximo estado.
    """
    # Obtém o valor máximo Q do próximo estado
    best_next_value = np.max(Q[next_state])

    # Calcula o target de TD (target de diferença temporal)
    td_target = reward + gamma * best_next_value

    # Atualiza o valor Q com o fator (1 - alpha) para o valor antigo
    Q[state, action] = (1 - alpha) * Q[state, action] + alpha * td_target

def save_q_table_to_txt(filename="q_table.txt"):
    # Salva a tabela Q em um arquivo txt
    return
    np.savetxt(filename, Q, fmt="%.4f", delimiter="\t")

def log_episode_data(filename, episode, total_reward, np_norm, next_position, np_deg, elapsed_ms):
    with open(filename, "a") as f:
        f.write("%d,%.2f,%.2f,%.2f,%.2f,%d\n" % (episode + 1, total_reward, np_norm, next_position, np_deg, elapsed_ms))
        f.flush()

def main(robot_ip):
    motion = connect_to_robot(robot_ip)
    joint_name = "LShoulderPitch"               # Articulação a controlar
    setpoint = 0.79                             # Ângulo alvo em radianos
    log_filename = "qlearning_log_NAO.csv"      # Nome do arquivo de log


    # Inicializando o arquivo de log
    with open(log_filename, "w") as f:
        f.write("episode,total_reward,normalized_position,rad_position,deg_position,timestamp_ms\n")

    # Registra o tempo de início do treinamento
    start_time = datetime.datetime.now()

    for episode in range(EPISODES):         # Número de episódios de treinamento
        current_angle = get_current_angle(motion, joint_name)
        state = discretize_angle(current_angle)
        
        total_reward = 0

        for step in range(MAX_STEPS):         # Número de passos por episódio
            action = choose_action(state)
            next_position = move_joint(motion, joint_name, action)

            current_angle = get_current_angle(motion, joint_name)
            next_state = discretize_angle(current_angle)

            # Calcular a recompensa
            reward = -abs(current_angle - setpoint)  # Recompensa negativa para distância do alvo
            total_reward += reward

            # Calcular a norma da distância
            np_norm = (next_position + ANGLE_LIMIT) / (2 * ANGLE_LIMIT)

            # Converter o ângulo para graus
            np_deg = np.degrees(current_angle)

            # Calcula o tempo decorrido em milissegundos desde o início do treinamento
            current_time = datetime.datetime.now()
            elapsed_ms = int((current_time - start_time).total_seconds() * 1000)

            # Registrar dados do episódio
            log_episode_data(log_filename, episode, total_reward, np_norm, next_position, np_deg, elapsed_ms)

            # Atualizar Q
            update_Q(state, action, reward, next_state)

            

        print("Episode %d/%d Total Reward: %.2f NP: %.2f rad: %.2f deg: %.2f reward: %.2f Time: %dms" % 
              (episode + 1, EPISODES, total_reward, np_norm, next_position, np_deg, reward, elapsed_ms))
 
        state = next_state
            
        if abs(current_angle - setpoint) < 0.1:
            save_q_table(Q)
            print("  Alvo atingido!")
            print("Treinamento concluído!")
            return  # Encerra o programa quando o alvo é atingido
            
        time.sleep(0.1)

        # Salva a tabela Q ao final de cada episódio
        # save_q_table_to_txt()  # Agora salva após cada episódio

    # Caso o treinamento não tenha sido interrompido antes
    print("Treinamento concluído sem atingir o alvo")
    # Salva a tabela Q ao final de todo o treinamento
    # save_q_table()
    #save_q_table_to_txt()  # Salva também após o fim de todos os episódios

if __name__ == "__main__":
    robot_ip = "172.15.0.136" 
    main(robot_ip)
