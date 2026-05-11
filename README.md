
# Q-Learning for NAO Robot Joint Control

This project uses the **Q-Learning** algorithm to train the NAO robot to adjust a specific joint angle (by default, `LShoulderPitch`) until it reaches a target value. The training involves real interactions with the robot, applying discrete actions and evaluating the reward based on how close the reached angle is to the target.

## 🚀 Technologies Used

* Python 2.7
* Naoqi SDK
* NumPy
* NAO Robot (physical)
* IP-based communication

## 🧠 Algorithm Description

The agent uses **Q-Learning**, a reinforcement learning technique that aims to learn an optimal policy through exploration and updating of a Q-table.
During the process:

1. The joint starts at a current angle.
2. The agent chooses an action (movement) based on ε-greedy strategy.
3. The action is applied to the robot, moving the joint.
4. The new position is evaluated and a reward is assigned.
5. The Q-table is updated based on the reward and the best estimated future value.

## ⚙️ Parameters

* `alpha`: Learning rate (0.2)
* `gamma`: Discount factor (0.9)
* `epsilon`: Exploration probability (0.2)
* `n_actions`: Number of possible actions (5)
* `n_states`: Discretization of the state space (100)
* `ANGLE_LIMIT`: Joint movement limit in radians (±90°)
* `EPISODES`: Number of training episodes (100)
* `MAX_STEPS`: Steps per episode (1)

## 📁 Files

* `main.py`: Main script with connection, execution, and learning logic.
* `qlearning_log_NAO.csv`: Log of each episode (reward, position, etc.).
* `q_table.txt`: File where the Q-table can be saved (currently disabled).

## 📝 How to Use

1. Connect the NAO robot to the same network as your computer.

2. Install the `naoqi` SDK compatible with Python 2.7.

3. Edit the line with your robot's IP:

   ```python
   robot_ip = "172.15.0.136"
   ```

4. Run the script:

   ```bash
   python main.py
   ```

5. Monitor the log in `qlearning_log_NAO.csv`.

## 📊 Expected Output

During training, the terminal will display:

* Current episode
* Total reward
* Normalized and radian position
* Angle in degrees
* Step reward
* Alert if the target is reached

## ✅ Stopping Criterion

Training automatically stops if the joint angle reaches the target value within a tolerance of `±0.05 rad`.

## 📌 Notes

* Adjust the joint name (`joint_name`) if you want to train a different part of the robot.
* Angle limits can be refined based on the physical constraints of the NAO.
* The code has been tested with the `LShoulderPitch` joint.


