#!/bin/bash
#SBATCH --job-name=tetracyclic_md
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#SBATCH --time=24:00:00
#SBATCH --memory=16GB
#SBATCH --output=tetracyclic_%j.out
#SBATCH --error=tetracyclic_%j.err

# Load modules (adjust for your cluster)
module load lammps/latest
module load python/3.8

# Set environment
export OMP_NUM_THREADS=1

echo "Starting Group 6 Tetracyclic Polymer MD Simulation"
echo "Expected g-factor: 0.445"
echo "Date: $(date)"
echo "=========================================="

# Run LAMMPS simulation
echo "Running LAMMPS..."
mpirun -np 16 lmp_mpi -in alpha_polymer.in

# Check simulation success
if [ $? -eq 0 ]; then
    echo "SUCCESS: LAMMPS simulation completed!"

    # Run analysis
    echo "Running post-processing analysis..."
    python3 ../analysis_scripts/compute_gyration.py

    echo "Analysis completed successfully!"
    echo "Check gyration_data.txt for results"
else
    echo "ERROR: LAMMPS simulation failed!"
    exit 1
fi

echo "Job completed at: $(date)"
