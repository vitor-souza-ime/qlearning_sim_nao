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


