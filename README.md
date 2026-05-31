# Computational and Theoretical Characterization of a Highly Connected Tetracyclic Polymer

## Polymer Topology Analysis with LAMMPS

This project uses **Molecular Dynamics (MD)** simulations with **LAMMPS** to analyze and compare the conformational properties of two different polymer topologies through their **Radius of Gyration ($R_g$)**.

---

## Polymer Systems

1. **Alpha Polymer** — A three-dimensional tetracyclic (knotted) polymer structure.
2. **Tree Polymer** — A two-dimensional highly branched dendrimer-like polymer structure.

The workflow is fully automated through a Bash script that:

1. Runs separate LAMMPS simulations for both polymer topologies.
2. Extracts the radius of gyration data.
3. Performs a comparative analysis using Python.
4. Computes the ratio:

$$\frac{\langle R_g^2 \rangle_{\text{alpha}}}{\langle R_g^2 \rangle_{\text{tree}}}$$

The framework can also be adapted to calculate the standard **g-factor** by comparing a branched polymer with a linear polymer of equal molecular weight.

---

## Project Structure

```text
.
├── documentation/
│   ├── mathematical_derivation.tex
│   └── derivation.pdf
│
├── lammps_files/
│   ├── alpha_polymer.data          # Alpha polymer geometry
│   ├── tree_polymer.data           # Tree polymer geometry
│   │
│   ├── alpha_polymer.in            # LAMMPS input script for alpha polymer
│   ├── tree_polymer.in             # LAMMPS input script for tree polymer
│   │
│   ├── run_simulation.sh           # Main SLURM batch script
│   └── compute_gyration.py         # Analysis script
│
├── results/
│   └──                             # Simulation outputs
│
└── README.md
```

---

## Dependencies

### Simulation Software

- LAMMPS
- OpenMPI (or another MPI implementation compatible with your LAMMPS build)
- SLURM Workload Manager

### Python Requirements

- Python 3.x
- NumPy
- Matplotlib

Install Python dependencies using:

```bash
pip install numpy matplotlib
```

---

## Running the Project

### Step 1: Prepare Input Files

The repository already contains the required polymer structures:

- `alpha_polymer.data`
- `tree_polymer.data`

If you wish to generate new structures (e.g., different polymer sizes), use the original generator scripts:

| Output File          | Generator Script                 |
| -------------------- | -------------------------------- |
| `alpha_polymer.data` | `alpha_graph_3D_alpha_like_*.py` |
| `tree_polymer.data`  | `generate_from_coords_2D.py`     |

---

### Step 2: Run Simulations and Analysis

Navigate to the LAMMPS directory and submit the SLURM job:

```bash
cd lammps_files/
sbatch run_simulation.sh
```

The script will:

1. Run the Alpha Polymer simulation.
2. Run the Tree Polymer simulation.
3. Collect gyration data.
4. Execute the Python analysis script.
5. Generate plots and summary statistics.

---

### Step 3: View Results

After completion, the following files will be generated:

| File                            | Description                               |
| ------------------------------- | ----------------------------------------- |
| `gyration.alpha_polymer.txt`    | Radius of gyration data for Alpha Polymer |
| `gyration.tree_polymer.txt`     | Radius of gyration data for Tree Polymer  |
| `g_factor_analysis_results.png` | Comparative plots of both simulations     |
| `g_factor_results.txt`          | Final calculated statistics and ratio     |

---

## Output Metrics

The analysis computes the following for each polymer.

### Mean-Square Radius of Gyration

$$\langle R_g^2 \rangle$$

### Comparative Ratio

$$\frac{\langle R_g^2 \rangle_{\text{alpha}}}{\langle R_g^2 \rangle_{\text{tree}}}$$

> Only the equilibrated portion of the simulation (last 25%) is used in the calculation.

---

## Key File Descriptions

### `run_simulation.sh`

Main execution script for the project. Responsibilities:

- Defines the polymer systems to simulate.
- Executes LAMMPS using MPI.
- Passes the appropriate `.data` and `.in` files.
- Runs simulations sequentially.
- Launches the Python analysis script after all simulations finish.

**Workflow:**

```
Alpha Polymer Simulation
        ↓
Tree Polymer Simulation
        ↓
Compute Gyration Statistics
        ↓
Generate Plots & Results
```

---

### `alpha_polymer.in` and `tree_polymer.in`

LAMMPS input templates defining the simulation protocol.

**Simulation Settings:**

| Parameter     | Value                        |
| ------------- | ---------------------------- |
| Units         | `real`                       |
| Pair Potential| Lennard-Jones (`lj/cut`)     |
| Bond Potential| FENE                         |
| Ensemble      | NVT with Langevin thermostat |
| Temperature   | 300 K                        |

**Simulation Procedure:**

1. Read polymer topology.
2. Perform multi-stage energy minimization.
3. Equilibrate the structure.
4. Run production dynamics.
5. Compute and save radius of gyration data.

**Radius of Gyration Calculation:**

```lammps
compute myRg all gyration
```

---

### `compute_gyration.py`

Post-processing and analysis script.

**Functionality:**

1. Loads gyration data from both simulations.
2. Discards the first 75% of frames as equilibration.
3. Computes $\langle R_g^2 \rangle_{\text{alpha}}$ and $\langle R_g^2 \rangle_{\text{tree}}$.
4. Calculates the final ratio:

$$\frac{\langle R_g^2 \rangle_{\text{alpha}}}{\langle R_g^2 \rangle_{\text{tree}}}$$

5. Generates comparative time-series plots and distribution plots.
6. Saves `g_factor_analysis_results.png` and `g_factor_results.txt`.

---

## Research Objective

This project investigates how polymer topology influences conformational size and compactness. By comparing a highly connected tetracyclic polymer with a branched tree-like polymer, the study quantifies topology-dependent scaling behavior through the radius of gyration and related shape descriptors.
