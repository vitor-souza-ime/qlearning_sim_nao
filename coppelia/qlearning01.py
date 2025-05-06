#   *   *   *   *   *   *   *   *   *   *   *   *   *   
#                        IME                        *
#                  PGED  06/05/2025                 *
#    Controle de Juntas do Robô NAO por Q-Learning  *
#   *   *   *   *   *   *   *   *   *   *   *   *   *   

import time
import math
import numpy as np
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

EPSILON = 0.2
ALPHA = 0.2  # Taxa de aprendizado
GAMMA = 0.9  # Fator de desconto
NUM_EPISODES = 100
MAX_STEPS = 1
NUM_ACTIONS = 3  # Ações: -1 (diminuir), 0 (manter), +1 (aumentar)
ANGLE_LIMIT = math.radians(90)  # Limite dos ângulos em radianos

# Parâmetros de exploração
MIN_EPSILON = 0.01
EPSILON_DECAY = 0.995
DELTA=0.5

#   *   *   *   *   *   *   *   *   *   *   *   *   *   
#              Classe NaoRobotController            *
#   *   *   *   *   *   *   *   *   *   *   *   *   *
class NAORobotController:
    def __init__(self):
        print("Iniciando conexão com CoppeliaSim...")
        self.client = RemoteAPIClient()
        self.sim = self.client.getObject('sim')
        
        print("Conectado. Configurando simulação...")
        self.client.setStepping(True)
        
        # Obter o handle do robô NAO
        self.nao_handle = self.sim.getObject('/NAO')
        
        # Obter os handles das juntas do NAO
        self.joint_handles = self.get_joint_handles()
        print(f"Encontradas {len(self.joint_handles)} juntas.")

        # Configuração do Q-Learning
        self.q_table = np.zeros((10, NUM_ACTIONS))  # Tabela Q: (estado, número de ações)
        self.epsilon = EPSILON

    def get_joint_handles(self):
        joint_names = [
            'HeadYaw', 'HeadPitch',
            'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw',
            'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw',
            'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll',
            'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll'
        ]
        handles = []
        for name in joint_names:
            try:
                handle = self.sim.getObject(f'/NAO/{name}')
                handles.append(handle)
            except Exception as e:
                print(f"Aviso: Não foi possível obter o handle para a junta {name}. Erro: {e}")
        return handles

    def set_joint_positions(self, positions):
        if len(positions) != len(self.joint_handles):
            raise ValueError(f"Número de posições ({len(positions)}) deve corresponder ao número de juntas ({len(self.joint_handles)})")
        
        for i, position in enumerate(positions):
            self.sim.setJointTargetPosition(self.joint_handles[i], position)
        
        self.client.step()

    def get_joint_position(self, joint_index):
        return self.sim.getJointPosition(self.joint_handles[joint_index])

    def get_state_index(self, position):
        """Convert position to state index (simplificado para o exemplo)."""
        return int((position + ANGLE_LIMIT) / (2 * ANGLE_LIMIT) * 10)  # Normaliza e discretiza

    def choose_action(self, state_index):
        """Escolher uma ação usando a política epsilon-greedy."""
        if np.random.rand() < self.epsilon:
            return np.random.choice(NUM_ACTIONS)  # Escolher ação aleatória
        else:
            return np.argmax(self.q_table[state_index])  # Escolher a melhor ação

    def update_q_table(self, state_index, action, reward, next_state_index):
        best_next_action = np.max(self.q_table[next_state_index])
        self.q_table[state_index, action] = (1 - ALPHA) * self.q_table[state_index, action] + \
                                             ALPHA * (reward + GAMMA * best_next_action)

    def q_learning(self, episodes, angle):
        self.sim.startSimulation()

        for episode in range(episodes):
            current_position = self.get_joint_position(2)  # Usar braço esquerdo para simplificação
            state_index = self.get_state_index(current_position)
            total_reward = 0

            for _ in range(MAX_STEPS):
                action = self.choose_action(state_index)
                next_position = current_position + (action - 1) * 0.1  # Ajustar o ângulo
                next_position = np.clip(next_position, -ANGLE_LIMIT, ANGLE_LIMIT)
                
                # Cria a lista de posições para todas as juntas
                positions = [self.get_joint_position(i) for i in range(len(self.joint_handles))]
                positions[2] = next_position  # Ajustar o braço
                
                self.set_joint_positions(positions)  # Atualiza todas as posições das juntas
                #time.sleep(0.1)
                
                # Calcular recompensa (quanto mais próximo do ângulo alvo, maior a recompensa)
                                
                target_position = math.radians(angle)  # Ângulo alvo
                reward = -abs(target_position - next_position)     
                
                next_state_index = self.get_state_index(next_position)
                self.update_q_table(state_index, action, reward, next_state_index)
                
                state_index = next_state_index
                current_position = next_position
                total_reward += reward

            # Decaimento do epsilon
            self.epsilon = max(MIN_EPSILON, self.epsilon * EPSILON_DECAY)
            np_norm = (next_position + ANGLE_LIMIT) / (2 * ANGLE_LIMIT)
            np_deg = math.degrees(next_position)
            print(f"Episode {episode + 1}/{episodes} Total Reward: {total_reward:.4f} NP: {np_norm:.4f} rad: {next_position:.4f} deg: {np_deg:.2f}")
            if abs(np_deg-angle)<=DELTA:
                print(f"Ãngulo alvo de {angle}° encontrado.")
                return
            

    def close(self):
        print("Parando a simulação...")
        self.sim.stopSimulation()
        print("Simulação encerrada.")

#   *   *   *   *   *   *   *   *   *   *   *   *   *   
#                     Função Main                   *
#   *   *   *   *   *   *   *   *   *   *   *   *   *
if __name__ == "__main__":
    controller = NAORobotController()
    try:
        controller.q_learning(NUM_EPISODES,45)
        time.sleep(5);
    except Exception as e:
        print(f"Erro durante a execução: {e}")
    finally:
        print("Conexão encerrada!")        
        controller.close()                      # Encerra conexão 

#   *   *   *   *   *   *   *   *   *   *   *   *   *   
#                     Fim do Programa               *
#   *   *   *   *   *   *   *   *   *   *   *   *   *
