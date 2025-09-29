#!/bin/bash
#SBATCH --job-name=tetracyclic_md
#SBATCH --output=tetracyclic_%j.out
#SBATCH --error=tetracyclic_%j.err
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --time=00:30:00
#SBATCH --partition=phd_student
#SBATCH --qos=phd_student

module load openmpi-4.1.5
module load lammps-openmpi
module load anaconda3

export OMP_NUM_THREADS=1

echo "Starting Group 6 Tetracyclic Polymer MD Simulation"
echo "Expected g-factor: 0.445"
echo "Date: $(date)"
echo "=========================================="

echo "Running LAMMPS..."
mpirun -np 1 lmp -in alpha_polymer.in

if [ $? -eq 0 ]; then
    echo "SUCCESS: LAMMPS simulation completed!"
    echo "Running post-processing analysis..."
    python3 ../analysis_scripts/compute_gyration.py
    echo "Analysis completed successfully!"
    echo "Check gyration_data.txt for results"
else
    echo "ERROR: LAMMPS simulation failed!"
    exit 1
fi

echo "Job completed at: $(date)"
