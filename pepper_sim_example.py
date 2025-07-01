import time
from qibullet import SimulationManager

def perform_throw(pepper, manager, client):
    """
    Perform the throwing motion.
    """
    # Set initial posture
    pepper.goToPosture("StandInit", 1.0)
    manager.stepSimulation(client)

    time.sleep(1)

    initial = pepper.getAnglesPosition(["RShoulderPitch", "RElbowYaw", "RElbowRoll"])
    print(initial)

    input("show position 1 \n")
    
    initial_joint_values = [1.5799891550618397, 1.2256556824604095, 0.5184863658529284]
    pepper.setAngles(["RShoulderPitch", "RElbowYaw", "RElbowRoll"], initial_joint_values, 0.1)
    manager.stepSimulation(client)

    input("show position 2 \n")

    throwing_joint_values = [1.9, -0.5, 0.5184863658529284]
    pepper.setAngles(["RShoulderPitch", "RElbowYaw", "RElbowRoll"], throwing_joint_values, 0.1)
    manager.stepSimulation(client)

    input("show position 3\n")

    extended_front_joint_values = [-0.6, 1, 0.5184863658529284]
    pepper.setAngles(["RShoulderPitch", "RElbowYaw", "RElbowRoll"], extended_front_joint_values, 0.1)
    manager.stepSimulation(client)

    time.sleep(1)

    # Return to initial posture (extended front)
    pepper.goToPosture("StandInit", 1.0)
    manager.stepSimulation(client)


    # Set initial arm position (normal)
    normal_joint_values = [0.0, 1.0, 0.0]  
    pepper.setAngles(["RShoulderPitch", "RElbowYaw", "RElbowRoll"], normal_joint_values, 0.3)
    manager.stepSimulation(client)

    time.sleep(2.0)  

def main():
    # Launch the simulation
    simulation_manager = SimulationManager()
    client = simulation_manager.launchSimulation(gui=True)
    pepper = simulation_manager.spawnPepper(client, spawn_ground_plane=True)

    while True:
        try:
            # Simulate throwing motion
            perform_throw(pepper, simulation_manager, client)

            # Get user feedback
            feedback_input = float(input("Enter feedback value (-5 to 5, 0 to exit): "))
            
            if feedback_input == 0:
                break
            
            if -5 <= feedback_input <= 5:
                
                print(f"Received feedback: {feedback_input}")
            else:
                print("Feedback value must be between -5 and 5.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

    # Stop the simulation
    simulation_manager.stopSimulation(client)

if __name__ == "__main__":
    main()
