# This file is part of DmpBbo, a set of libraries and programs for the
# black-box optimization of dynamical movement primitives.
# Copyright (C) 2022 Freek Stulp
#
# DmpBbo is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# DmpBbo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with DmpBbo.  If not, see <http://www.gnu.org/licenses/>.
"""Script for bbo_of_dmps demo."""
import argparse
import tempfile
from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt
import os

from dmpbbo.bbo.DistributionGaussian import DistributionGaussian
from dmpbbo.bbo.updaters import UpdaterCovarAdaptation
from dmpbbo.bbo_of_dmps.run_optimization_task import run_optimization_task
from dmpbbo.bbo_of_dmps.TaskSolverDmp import TaskSolverDmp
from dmpbbo.dmps.Dmp import Dmp
from dmpbbo.dmps.Trajectory import Trajectory
from dmpbbo.functionapproximators.FunctionApproximatorLWR import FunctionApproximatorLWR
from dmpbbo.functionapproximators.FunctionApproximatorRBFN import FunctionApproximatorRBFN
from dmpbbo.dynamicalsystems.SpringDamperSystem import SpringDamperSystem


def run_optimization(directory, traj, task):
    """ Run one demo for bbo_of_dmps (with single updates)

    @param directory: Directory to save results to
    @param traj: Initial trajectory
    @param task: Task
    """

    n_dims = traj.dim
    n_bfs_per_dim = 30
    intersection_height = 0.9
    function_apps = [FunctionApproximatorRBFN(n_bfs_per_dim, intersection_height) for _ in range(n_dims)]
    # function_apps = [FunctionApproximatorLWR(n_bfs_per_dim, intersection_height) for _ in range(n_dims)]

    # initialize damper system
    positions = traj.ys
    tau = 0.5
    y_init = positions[0]
    y_attr = positions[len(positions) - 1]
    damping_coefficient = 12.0
    print("damper", y_init, y_attr)

    dmp = Dmp.from_traj(
        traj,
        function_apps,
        transformation_system=SpringDamperSystem(tau, y_init, y_attr, damping_coefficient),
        forcing_term_scaling="G_MINUS_Y0_SCALING",
        dmp_type="KULVICIUS_2012_JOINING"
    )
    dmp.set_selected_param_names("weights")
    # dmp.set_selected_param_names(['goal','weights'])

    # Make task solver, based on a Dmp
    dt = 0.01
    integrate_dmp_beyond_tau_factor = 1.5
    task_solver = TaskSolverDmp(dmp, dt, integrate_dmp_beyond_tau_factor)

    n_search = dmp.get_param_vector_size()

    mean_init = np.full(n_search, 0.0)
    covar_init = 1000.0 * np.eye(n_search)
    distribution = DistributionGaussian(mean_init, covar_init)

    updater = UpdaterCovarAdaptation()

    n_samples_per_update = 10
    n_updates = 8

    session = run_optimization_task(
        task, task_solver, distribution, updater, n_updates, n_samples_per_update, directory
    )
    #TODO fix issue with plotting
    session.plot()
    plt.savefig(os.getcwd() + "/figures/distr_rollouts_explor_lc__2B",)


def main():
    """ Main function of the script. """
    default_dir = Path(tempfile.gettempdir(), "dmpbbo", "demo_bbo_of_dmps")

    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=str, help="dir to write results to", default=default_dir)
    parser.add_argument("--traj", type=str, help="optional init trajectory file")
    args = parser.parse_args()

    if args.traj:
        traj = Trajectory.loadtxt(args.traj)
        # traj.plot # Check if trajectory loaded correctly.
        run_optimization(args.dir, traj)

    else:
        # Some DMP parameters
        for n_dims in [1, 2]:
            tau = 0.5
            dt = 0.005
            ts = np.linspace(0.0, tau, int(tau / dt) + 1)
            y_init = np.linspace(1.8, 2.0, n_dims)
            y_attr = np.linspace(4.0, 3.0, n_dims)
            traj = Trajectory.from_min_jerk(ts, y_init, y_attr)
            run_optimization(args.dir, traj)

    plt.show()


if __name__ == "__main__":
    main()
