import os
import random
import time
from qibullet import SimulationManager
from dmpbbo.bbo_of_dmps.Task import Task
from dmpbbo.dmps.Trajectory import Trajectory
from optimizer import run_optimization

if __name__ == "__main__":
    simulation_manager = SimulationManager()

    # Launch a simulation instances, with using a graphical interface.
    # Please note that only one graphical interface can be launched at a time
    client_id = simulation_manager.launchSimulation(gui=True)

    # Spawning a virtual Pepper robot, at the origin of the WORLD frame, and a
    # ground plane
    pepper = simulation_manager.spawnPepper(
        client_id,
        translation=[0, 0, 0],
        quaternion=[0, 0, 0, 1],
        spawn_ground_plane=True)

    # load trajectory
    traj = Trajectory.loadtxt(os.getcwd() + "/trajectories/angels.txt")

    jointNames = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand"]

    """ Run one demo for Trajectory and userFeedback

    @param traj: Trajectory that should be replayed using the robot
    """

    # jointNamesReplay = ["RShoulderPitch", "RElbowYaw", "RElbowRoll"]
    jointNamesReplay = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw",
                        "RElbowRoll", "RWristYaw"]

    for name, joint in pepper.joint_dict.items():
        if name in jointNamesReplay:
            print(name, joint.getLowerLimit(), joint.getUpperLimit(), )


    def replayTrajectory(_traj: Trajectory):
        times = _traj.ts
        positions = _traj.ys
        velocities = _traj.yds
        accelerations = _traj.ydds
        jerks = _traj.yddds

        # go to initial position
        pepper.goToPosture("StandInit", 1)
        simulation_manager.stepSimulation(client_id)

        # delay for switching to simulator
        time.sleep(1)

        dt = times[1] - times[0]
        for (idx, position) in enumerate(positions):
            if idx != 0:
                dt = times[idx] - times[idx - 1]
            #TODO replay angles relative to offset in trajectory
            pepper.setAngles(jointNamesReplay[:len(position)], position.tolist(), 1)
            simulation_manager.stepSimulation(client_id)


    replayTrajectory(traj)


    class TaskUserFeedback(Task):
        def evaluate_rollout(cost_vars, sample):
            # return random.randint(1,5) # TODO for quickly testing plotting
            traj_rollout = Trajectory.from_matrix(cost_vars)
            replayTrajectory(traj_rollout)

            evaluation = -1
            while evaluation not in [1, 2, 3, 4, 5]:
                input_string = input(
                    "Rate rollout with a number from 1 to 5 (1: not good at all, 2: not so good, 3: average, 4: good, 5: very good) or \"r\" for replay \n")
                if input_string.isnumeric():
                    evaluation = int(input_string)
                elif input_string == "r":
                    replayTrajectory(traj_rollout)
            print("Rated rollout as ", evaluation)
            return 6 - evaluation  # invert scale


    session = run_optimization(
        directory=os.getcwd() + "/results/",
        traj=traj,
        task=TaskUserFeedback,
    )

    input("Press a key to end the simulation ")

    # Stop the simulation
    simulation_manager.stopSimulation(client_id)
