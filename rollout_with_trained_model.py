import os
import time

from qibullet import SimulationManager
from dmpbbo.dmps.Trajectory import Trajectory



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
    path_to_costs = os.getcwd() + '/results/update00007/009_cost_vars.txt'
    
    traj_rollout = Trajectory.loadtxt(path_to_costs)    
    traj_rollout = traj_rollout.as_matrix()
    traj_rollout = Trajectory.from_matrix(traj_rollout)

    # jointNamesReplay = ["RShoulderPitch", "RElbowYaw", "RElbowRoll"]
    jointNamesReplay = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw",
                        "RElbowRoll", "RWristYaw"]
    for name, joint in pepper.joint_dict.items():
        if name in jointNamesReplay:
            print(name, joint.getLowerLimit(), joint.getUpperLimit(), )


    def replayTrajectory(_traj: Trajectory):
        times = _traj.ts
        positions = _traj.ys
        accelerations = _traj.ydds

        # go to initial position
        pepper.goToPosture("StandInit", 1)
        simulation_manager.stepSimulation(client_id)

        # delay for switching to simulator
        time.sleep(1)

        dt = times[1] - times[0]
        for (idx, position) in enumerate(positions):
            if idx != 0:
                dt = times[idx] - times[idx - 1]
            print(jointNamesReplay[:len(position)], position.tolist(), dt, accelerations[idx])
            pepper.setAngles(jointNamesReplay[:len(position)], position.tolist(), 1)
            simulation_manager.stepSimulation(client_id)


    replayTrajectory(traj_rollout)





