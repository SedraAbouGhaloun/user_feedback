#!/usr/bin/env python
# coding: utf-8

import sys
import time
import pybullet as p
from qibullet import SimulationManager
from qibullet import PepperVirtual
from qibullet import NaoVirtual
from qibullet import RomeoVirtual
import numpy as np

if __name__ == "__main__":
    simulation_manager = SimulationManager()

    rob = "pepper"
    # if (sys.version_info > (3, 0)):
    #     rob = input("Which robot should be spawned? (pepper/nao/romeo): ")
    # else:
    #     rob = raw_input("Which robot should be spawned? (pepper/nao/romeo): ")

    # Auto stepping set to False, the user has to manually step the simulation
    client = simulation_manager.launchSimulation(gui=True, auto_step=False)

    if rob.lower() == "nao":
        robot = simulation_manager.spawnNao(client, spawn_ground_plane=True)
    elif rob.lower() == "pepper":
        robot = simulation_manager.spawnPepper(client, spawn_ground_plane=True)
    elif rob.lower() == "romeo":
        robot = simulation_manager.spawnRomeo(client, spawn_ground_plane=True)
    else:
        print("You have to specify a robot, pepper, nao or romeo.")
        simulation_manager.stopSimulation(client)
        sys.exit(1)

    time.sleep(1.0)
    # lshoulderpitch_values = []  # List to store the joint values
    
    joint_parameters = list()

    ball_joint_parameters = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", 
                             "RElbowRoll", "RWristYaw"]
    
    n_ball_joint_parameters = len(ball_joint_parameters)
    
    for name, joint in robot.joint_dict.items():
        # if "Finger" not in name and "Thumb" not in name:
        if name in ball_joint_parameters:
            joint_parameters.append((
                p.addUserDebugParameter(
                    name,
                    joint.getLowerLimit(),
                    joint.getUpperLimit(),
                    robot.getAnglesPosition(name)),
                name))
    
    # name = "LShoulderPitch"
    # joint = robot.joint_dict.get(name)
    # joint_param = p.addUserDebugParameter(name,
    #                                       joint.getLowerLimit(),
    #                                       joint.getUpperLimit(),
    #                                       robot.getAnglesPosition(name))
    angels = np.ones((10000, 1 + n_ball_joint_parameters*3))
    
    print("jetzt inside try:")
    try:
        i = 0
        while True:
            joints_list = []
            for joint_parameter in joint_parameters:
                                
                new_angle = p.readUserDebugParameter(joint_parameter[0])
                robot.setAngles(
                    joint_parameter[1],
                    new_angle,
                    1.0)
                
                joints_list.append(new_angle)
            
            joints_list.insert(0, i)
            angels[i, 0:1+n_ball_joint_parameters] = joints_list
            # new_angle = p.readUserDebugParameter(joint_param)
            
            # robot.setAngles(name, new_angle, 1.0)
            
            # angels.append(new_angle)  # Append the new angle to the list
            # Step the simulation
            simulation_manager.stepSimulation(client)

            # print(i)
            i += 1
            np.savetxt("angels.txt", angels)
    except KeyboardInterrupt:
        # pass
        # print("Simulation stopped. Final joint values:", lshoulderpitch_values)
        # np.savetxt("lshoulderpitch_values.txt", lshoulderpitch_values)
        simulation_manager.stopSimulation(client)
        
    finally:
        # np.savetxt("lshoulderpitch_values.txt", lshoulderpitch_values)
        simulation_manager.stopSimulation(client)
