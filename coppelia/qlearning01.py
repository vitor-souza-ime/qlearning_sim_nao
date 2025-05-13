#   *   *   *   *   *   *   *   *   *   *   *   *   *   
#                        IME                        *
#                  PGED  06/05/2025                 *
#    Controle de Juntas do Robô NAO por Q-Learning  *
#   *   *   *   *   *   *   *   *   *   *   *   *   *   

import time
import math
import numpy as np
from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import datetime
import os

# Hiperparâmetros
EPSILON = 0.2
ALPHA = 0.2
GAMMA = 0.9
NUM_EPISODES = 100
MAX_STEPS = 1
NUM_ACTIONS = 5
ANGLE_LIMIT = math.radians(90)
EPISODES = 100
MIN_EPSILON = 0.01
EPSILON_DECAY = 0.995
DELTA = 0.5

# Arquivos
LOG_FILENAME = "qlearning_log_SIM.csv"
QTABLE_FILENAME = "qtable_nao.npy"

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

        # Carrega Q-table se existir
        if os.path.exists(QTABLE_FILENAME):
            with open(QTABLE_FILENAME, 'rb') as f:
                self.q_table = np.load("qtable_nao.npy")
            print("Q-table carregada com sucesso.")
        else:
            self.q_table = np.zeros((100, NUM_ACTIONS))
            print("Q-table nova criada.")

        self.epsilon = EPSILON

        # Inicializa arquivo de log
        with open(LOG_FILENAME, 'w') as f:
            f.write("episode,total_reward,normalized_position,rad_position,deg_position,action,timestamp_ms\n")

        self.start_time = datetime.datetime.now()

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

    def initialize_arm_position(self):
        print("Inicializando posição do braço esquerdo...")
        shoulder_joint_index = 2  # LShoulderPitch
        target_angle = math.radians(90)
        self.sim.setJointTargetPosition(self.joint_handles[shoulder_joint_index], target_angle)
        for _ in range(10):
            self.client.step()
            time.sleep(0.1)
        current_angle = self.get_joint_position(shoulder_joint_index)
        print(f"Posição inicial do braço: {math.degrees(current_angle):.2f}° (alvo: 90°)")
        return current_angle

    def q_learning(self, episodes, angle):
        self.sim.startSimulation()
        initial_position = self.initialize_arm_position()
        time.sleep(1)
        self.start_time = datetime.datetime.now()

        for episode in range(EPISODES):
            current_position = self.get_joint_position(2)
            state_index = self.get_state_index(current_position)
            total_reward = 0
            action = None

            for _ in range(MAX_STEPS):
                action = self.choose_action(state_index)
                angle_adjustment = (action - 2) * 0.1
                next_position = current_position + angle_adjustment
                next_position = np.clip(next_position, -ANGLE_LIMIT, ANGLE_LIMIT)

                self.sim.setJointTargetPosition(self.joint_handles[2], next_position)
                self.client.step()

                target_position = math.radians(angle)
                reward = -abs(target_position - next_position)

                next_state_index = self.get_state_index(next_position)
                self.update_q_table(state_index, action, reward, next_state_index)

                state_index = next_state_index
                current_position = next_position
                total_reward += reward

            self.epsilon = max(MIN_EPSILON, self.epsilon * EPSILON_DECAY)

            np_norm = (next_position + ANGLE_LIMIT) / (2 * ANGLE_LIMIT)
            np_deg = math.degrees(next_position)
            current_time = datetime.datetime.now()
            elapsed_ms = int((current_time - self.start_time).total_seconds() * 1000)

            with open(LOG_FILENAME, 'a') as f:
                f.write(f"{episode+1},{total_reward:.2f},{np_norm:.2f},{next_position:.2f},{np_deg:.2f},{action},{elapsed_ms}\n")

            with open(QTABLE_FILENAME, 'wb') as f:
                #pickle.dump(self.q_table, f)
                #pickle.dump(self.q_table, f, protocol=2)
                np.save("qtable_nao.npy", self.q_table)

            print(f"Episode {episode + 1}/{episodes} Total Reward: {total_reward:.2f} NP: {np_norm:.2f} rad: {next_position:.2f} deg: {np_deg:.2f} reward: {reward:.2f} Action: {action} Time: {elapsed_ms}ms")

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
        time.sleep(3)
    except Exception as e:
        print(f"Erro durante a execução: {e}")
    finally:
        print("Conexão encerrada!")
        controller.close()
