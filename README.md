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

## Objectives

1. **MD Simulation** — Use LAMMPS to simulate the alpha graph polymer and compute radius of gyration.
2. **Analytical Calculation** — Apply graph theory to calculate the theoretical radius of gyration using the Kirchhoff index.
3. **Comparison** — Compare simulation results with analytical predictions.
4. **Validation** — Verify results against Figure 4 values from Cantarella et al. (2022).

---

## Alpha Graph Structure

The alpha graph (Group 6) is one of six topological polymer architectures studied in the paper. It represents a specific graph topology with:

- Multiple vertices (junction points)
- Interconnecting edges (polymer chains)
- Unique topological constraints

---

## Project Structure

```text
.
├── documentation/
│   ├── README.md
│   ├── derivation.pdf
│   └── mathematical_derivation.tex
│
├── lammps_files/
│   ├── alpha_polymer.data          # Alpha polymer geometry
│   ├── tree_polymer.data           # Tree polymer geometry
│   ├── alpha_polymer.in            # LAMMPS input script for alpha polymer
│   ├── run_simulation.sh           # Main SLURM batch script
│   ├── compute_gyration.py         # MD analysis
│   └── tetracyclic_analysis.py     # Tetracyclic-specific analysis
│
├── results/
│   ├── g_factor_analysis_results.png
│   ├── g_factor_results.txt
│   ├── tetracyclic_4225.out
│   ├── traj.alpha_polymer.prod.lammpstrj
│   ├── traj.alpha_polymer.relax.lammpstrj
│   ├── traj.tree_polymer.prod.lammpstrj
│   └── traj.tree_polymer.relax.lammpstrj
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

For local execution:

```bash
lmp_serial -in alpha_polymer.in
```

The script will:

1. Run the Alpha Polymer simulation.
2. Run the Tree Polymer simulation.
3. Collect gyration data.
4. Execute the Python analysis script.
5. Generate plots and summary statistics.

### Step 3: Run Analytical Calculations

```bash
# Tetracyclic-specific analysis and comparison
python3 lammps_files/tetracyclic_analysis.py
```

---

### Step 4: View Results

After completion, the following files will be generated:

| File                                    | Description                               |
| --------------------------------------- | ----------------------------------------- |
| `g_factor_analysis_results.png`         | Comparative plots of both simulations     |
| `g_factor_results.txt`                  | Final calculated statistics and ratio     |
| `tetracyclic_4225.out`                  | LAMMPS simulation log output              |
| `traj.alpha_polymer.prod.lammpstrj`     | Alpha polymer production trajectory       |
| `traj.alpha_polymer.relax.lammpstrj`    | Alpha polymer relaxation trajectory       |
| `traj.tree_polymer.prod.lammpstrj`      | Tree polymer production trajectory        |
| `traj.tree_polymer.relax.lammpstrj`     | Tree polymer relaxation trajectory        |

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

### `alpha_polymer.in`

LAMMPS input template defining the simulation protocol.

**Simulation Settings:**

| Parameter      | Value                        |
| -------------- | ---------------------------- |
| Units          | `real`                       |
| Force Field    | Kremer-Grest with FENE bonds |
| Pair Potential | Lennard-Jones (`lj/cut`)     |
| Bond Potential | FENE                         |
| Ensemble       | NVT with Langevin thermostat |
| Temperature    | 300 K                        |
| Duration       | 1,000,000 time steps (~1 ns) |

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

### `tetracyclic_analysis.py`

Performs tetracyclic-specific post-processing and analytical calculations.

**Procedure:**

1. Compute the graph Laplacian matrix $L$.
2. Calculate the Moore-Penrose pseudoinverse $L^{+}$.
3. Determine resistance distances $r_{ij}$.
4. Sum over all vertex pairs: $Kf(G) = \sum_{i<j} r_{ij}$.

**Key equations (from Cantarella et al., 2022):**

Expected radius of gyration (Theorem 9):

$$E(R_g^2;\, G) = \frac{d}{v^2} \times Kf(G)$$

where $d$ is the spatial dimension and $v$ is the number of vertices.

Kirchhoff index:

$$Kf(G) = \sum_{i<j} r_{ij} = \frac{v}{2} \cdot \mathrm{Tr}(L^{+})$$

Resistance distance:

$$r_{ij} = L^{+}_{ii} + L^{+}_{jj} - L^{+}_{ij} - L^{+}_{ji}$$

Contraction factor (Theorem 5, asymptotic limit):

$$g(G_\infty) = \frac{3}{e^2} \left[\text{Tr}\,L^{+}(G) + \frac{1}{3}\text{Loops}(G) - \frac{1}{6}\right]$$

---

## Key Equations Summary

| Quantity | Formula |
| -------- | ------- |
| Radius of gyration | $R_g^2 = \frac{1}{2v^2} \sum_{i,j} \|x_i - x_j\|^2$ |
| Kirchhoff index | $Kf(G) = \sum_{i<j} r_{ij} = \frac{v}{2} \cdot \text{Tr}(L^{+})$ |
| Resistance distance | $r_{ij} = L^{+}_{ii} + L^{+}_{jj} - L^{+}_{ij} - L^{+}_{ji}$ |
| Expected $R_g^2$ | $E(R_g^2; G) = \frac{d}{v^2} \times Kf(G)$ |

---

## Expected Results

Based on the research paper, we expect:

1. **Radius of Gyration** — Specific value from Figure 4 table (column 2).
2. **Contraction Factor** — Theoretical g-factor (column 3).
3. **Agreement** — MD simulation should match analytical predictions within ~5%.

---

## Research Objective

This project investigates how polymer topology influences conformational size and compactness. By comparing a highly connected tetracyclic polymer with a branched tree-like polymer, the study quantifies topology-dependent scaling behavior through the radius of gyration and related shape descriptors.

---

## Project Timeline

| Phase | Description |
| ----- | ----------- |
| Setup | Create LAMMPS input files and structure |
| Simulation | Run MD simulations (24–48 hours on cluster) |
| Analysis | Process results and perform graph theory calculations |
| Comparison | Validate against theoretical predictions |
| Documentation | Prepare final report and presentation |

---

## References

1. Cantarella, J., Deguchi, T., Shonkwiler, C., & Uehara, E. (2022). Radius of gyration, contraction factors, and subdivisions of topological polymers. *Journal of Physics A: Mathematical and Theoretical*, 55(47), 475202.

2. Plimpton, S. (1995). Fast parallel algorithms for short-range molecular dynamics. *Journal of Computational Physics*, 117(1), 1–19.

---



