import numpy as np
from matplotlib.colors import Normalize
import os

from dmpbbo.dmps.Trajectory import Trajectory


from matplotlib import pyplot as plt

def plot_trajectory_data(trajectory):

    _, axs = plt.subplots(3, 1, figsize=(8, 8))
    num_dims = trajectory.ys.shape[1] if len(trajectory.ys.shape) > 1 else 1
    dimension_labels = ['X', 'Y', 'Z'][:num_dims]  

    for i, label in enumerate(dimension_labels):
        axs[0].plot(trajectory.ts, trajectory.ys[:, i], label=f'Position {label}')
        axs[1].plot(trajectory.ts, trajectory.yds[:, i], label=f'Velocity {label}')
        axs[2].plot(trajectory.ts, trajectory.ydds[:, i], label=f'Acceleration {label}')

    axs[0].set_title('Trajectory Data')
    axs[0].set_ylabel('Position')
    axs[1].set_ylabel('Velocity')
    axs[2].set_ylabel('Acceleration')
    axs[2].set_xlabel('Time')

    axs[0].legend()
    axs[1].legend()
    axs[2].legend()

    plt.tight_layout()

    if not os.path.exists("figures"):
        os.makedirs("figures")
    file_path = os.path.join("figures", f"{num_dims}D_init_traj.png")
    
    plt.savefig(file_path)

    plt.show()


def plot_position_trajectory(trajectory, plot_type):
    """
    Plots the position trajectory in 2D or 3D based on the specified type.

    Args:
        trajectory: A trajectory object containing time steps `ts` and position data `ys`.
        plot_type (str): "2D" or "3D" indicating the type of plot.
    """
    ts = trajectory.ts  # Time steps
    norm = Normalize(vmin=np.min(ts), vmax=np.max(ts))

    if plot_type == "3D":
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        xs = trajectory.ys[:, 0]  # X coordinates
        ys = trajectory.ys[:, 1]  # Y coordinates
        zs = trajectory.ys[:, 2]  # Z coordinates
        scatter = ax.scatter(xs, ys, zs, c=ts, cmap='viridis', s=20)
        ax.set_zlabel('Z Position')
    
    elif plot_type == "2D":
        fig, ax = plt.subplots()
        xs = trajectory.ys[:, 0]  # X coordinates
        ys = trajectory.ys[:, 1]  # Y coordinates
        scatter = ax.scatter(xs, ys, c=ts, cmap='viridis', s=20)

    cbar = fig.colorbar(scatter, ax=ax, shrink=0.5, aspect=5)
    cbar.set_label('Time')

    ax.set_xlabel('X Position')
    ax.set_ylabel('Y Position')
    ax.set_title(f'{plot_type} Position Trajectories')

    os.makedirs("figures", exist_ok=True)
    file_path = os.path.join("figures", f"{plot_type}_init_pos_traj.png")

    
    plt.savefig(file_path)
    print(f"Figure saved to {file_path}")
    
    plt.show()



def main():

    start_time = 0  # starts at time 0
    end_time = 1    # ends at time 1

    # Number of discrete time steps for the trajectory
    n_time_steps = 100  # Total of number of time steps from start to end

    # Generate linearly spaced time steps between start and end times
    ts = np.linspace(start_time, end_time, n_time_steps)

    # Choose y_from and y_to with values matching the following constrains
    # RShoulderPitch min: -2.08567 max: 2.08567
    # RElbowYaw min: -2.08567 max: 2.08567
    # RElbowRoll min: 0.00872665 max: 1.56207

    y_from = np.array([1.5799891550618397, 1.2256556824604095, 0.5184863658529284])  # Starting position in 3D space (x=0, y=0, z=0)
    yd_from = np.array([0, 0, 0])  # Starting velocity in 3D space (vx=0, vy=0, vz=0)
    ydd_from = np.array([0, 0, 0])  # Starting acceleration in 3D space (ax=0, ay=0, az=0)

    y_to = np.array([-0.3, 1, 0])  # Target position in 3D space (x=1, y=1, z=1)
    yd_to = np.array([1, 1, 1])  # Target velocity in 3D space (vx=3, vy=2, vz=1)
    ydd_to = np.array([0, 0, 0])  # Target acceleration in 3D space (ax=0, ay=0, az=0)


    trajectory = Trajectory.from_polynomial(ts, y_from, yd_from, ydd_from, y_to, yd_to, ydd_to)

    # positions = trajectory.ys
    # velocities = trajectory.yds
    # accelerations = trajectory.ydds

    type="3D" # oder "2D"
    
    plot_trajectory_data(trajectory)
    plot_position_trajectory(trajectory, plot_type=type)
    
    if not os.path.exists("trajectories"):
        os.makedirs("trajectories")
    file_path = os.path.join("trajectories", f"{type}_init_traj.txt")
    
    trajectory.savetxt(file_path)
    print(f"Trajectory data saved to '{file_path}'")

if __name__ == "__main__":
    main()