import time
import math
import numpy as np
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

EPSILON = 0.2
ALPHA = 0.2  # Taxa de aprendizado
GAMMA = 0.9  # Fator de desconto
NUM_EPISODES = 100
MAX_STEPS = 1
NUM_ACTIONS = 5  # Ações: -0.2 rad, -0.1 rad, 0, +0.1 rad, +0.2 rad
ANGLE_LIMIT = math.radians(90)  # Limite dos ângulos em radianos
EPISODES=100

# Parâmetros de exploração
MIN_EPSILON = 0.01
EPSILON_DECAY = 0.995
DELTA = 0.5

# Arquivo de log
LOG_FILENAME = "qlearning_log_SIM.csv"

class NAORobotController:
    def __init__(self):
        print("Iniciando conexão com CoppeliaSim...")
        self.client = RemoteAPIClient()
        self.sim = self.client.getObject('sim')

        print("Conectado. Configurando simulação...")
        self.client.setStepping(True)
        self.nao_handle = self.sim.getObject('/NAO')
        self.joint_handles = self.get_joint_handles()
        print(f"Encontradas {len(self.joint_handles)} juntas.")

        self.q_table = np.zeros((100, NUM_ACTIONS))
        self.epsilon = EPSILON

        # Inicializa arquivo de log
        with open(LOG_FILENAME, 'w') as f:
            f.write("episode,total_reward,normalized_position,rad_position,deg_position\n")

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
            raise ValueError("Número de posições inválido.")
        for i, position in enumerate(positions):
            self.sim.setJointTargetPosition(self.joint_handles[i], position)
        self.client.step()

    def get_joint_position(self, joint_index):
        return self.sim.getJointPosition(self.joint_handles[joint_index])

    def get_state_index(self, position):
        return int((position + ANGLE_LIMIT) / (2 * ANGLE_LIMIT) * 10)

    def choose_action(self, state_index):
        if np.random.rand() < self.epsilon:
            return np.random.choice(NUM_ACTIONS)
        else:
            return np.argmax(self.q_table[state_index])

    def update_q_table(self, state_index, action, reward, next_state_index):
        best_next_action = np.max(self.q_table[next_state_index])
        self.q_table[state_index, action] = (1 - ALPHA) * self.q_table[state_index, action] + \
                                             ALPHA * (reward + GAMMA * best_next_action)

    def q_learning(self, episodes, angle):
        self.sim.startSimulation()

        for episode in range(EPISODES):
            current_position = self.get_joint_position(2)
            state_index = self.get_state_index(current_position)
            total_reward = 0

            for _ in range(MAX_STEPS):
                action = self.choose_action(state_index)
                angle_adjustment = (action - 2) * 0.1
                next_position = current_position + angle_adjustment
                next_position = np.clip(next_position, -ANGLE_LIMIT, ANGLE_LIMIT)

                positions = [self.get_joint_position(i) for i in range(len(self.joint_handles))]
                positions[2] = next_position
                self.set_joint_positions(positions)

                target_position = math.radians(angle)
                reward = -abs(target_position - next_position)

                next_state_index = self.get_state_index(next_position)
                self.update_q_table(state_index, action, reward, next_state_index)

                state_index = next_state_index
                current_position = next_position
                total_reward += reward

            self.epsilon = max(MIN_EPSILON, self.epsilon * EPSILON_DECAY)

            # Calculando o np_norm corretamente
            np_norm = (next_position + ANGLE_LIMIT) / (2 * ANGLE_LIMIT)  # Normalização do ângulo
            np_deg = math.degrees(next_position)  # Conversão para graus

            with open(LOG_FILENAME, 'a') as f:
                f.write(f"{episode+1},{total_reward:.2f},{np_norm:.2f},{next_position:.2f},{np_deg:.2f}\n")

            print(f"Episode {episode + 1}/{episodes} Total Reward: {total_reward:.2f} NP: {np_norm:.2f} rad: {next_position:.2f} deg: {np_deg:.2f} reward: {reward:.2f}")
            if abs(np_deg - angle) <= DELTA:
                print(f"Ângulo alvo de {angle}° encontrado.")
                return

    def close(self):
        print("Parando a simulação...")
        self.sim.stopSimulation()
        print("Simulação encerrada.")

if __name__ == "__main__":
    controller = NAORobotController()
    try:
        controller.q_learning(NUM_EPISODES, 45)
        time.sleep(5)
    except Exception as e:
        print(f"Erro durante a execução: {e}")
    finally:
        print("Conexão encerrada!")
        controller.close()
