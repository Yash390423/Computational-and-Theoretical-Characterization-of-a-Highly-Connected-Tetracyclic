#!/usr/bin/env python3
"""
Radius of Gyration Analysis for Group 6 Tetracyclic Polymer
Expected g-factor: 0.445 from Cantarella et al. (2022)
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
import os

def analyze_gyration_data(filename='gyration_data.txt'):
    """Analyze radius of gyration from LAMMPS output"""

    print("="*60)
    print("GROUP 6 TETRACYCLIC POLYMER ANALYSIS")
    print("Expected g-factor: 0.445")
    print("="*60)

    try:
        # Load data
        data = np.loadtxt(filename, comments='#')
        timesteps = data[:, 0]
        rg_values = data[:, 1]

        print(f"Loaded {len(rg_values)} data points")

        # Calculate statistics
        mean_rg = np.mean(rg_values)
        std_rg = np.std(rg_values)
        min_rg = np.min(rg_values)
        max_rg = np.max(rg_values)

        # Confidence interval
        n = len(rg_values)
        conf_int = stats.t.interval(0.95, n-1, loc=mean_rg, scale=std_rg/np.sqrt(n))

        print(f"\nRadius of Gyration Results:")
        print(f"Mean R_g:     {mean_rg:.4f} ± {std_rg:.4f} Å")
        print(f"Min R_g:      {min_rg:.4f} Å")
        print(f"Max R_g:      {max_rg:.4f} Å")
        print(f"95% CI:       [{conf_int[0]:.4f}, {conf_int[1]:.4f}] Å")
        print(f"Samples:      {n}")

        # Create plots
        plt.figure(figsize=(15, 5))

        # Time series
        plt.subplot(1, 3, 1)
        plt.plot(timesteps, rg_values, 'b-', alpha=0.7)
        plt.axhline(mean_rg, color='r', linestyle='--', label=f'Mean = {mean_rg:.3f}')
        plt.xlabel('Time Step')
        plt.ylabel('Radius of Gyration (Å)')
        plt.title('R_g vs Time')
        plt.legend()
        plt.grid(True, alpha=0.3)

        # Distribution
        plt.subplot(1, 3, 2)
        plt.hist(rg_values, bins=50, alpha=0.7, color='skyblue', density=True)
        plt.axvline(mean_rg, color='r', linestyle='--', label=f'Mean = {mean_rg:.3f}')
        plt.xlabel('Radius of Gyration (Å)')
        plt.ylabel('Probability Density')
        plt.title('R_g Distribution')
        plt.legend()
        plt.grid(True, alpha=0.3)

        # Running average
        plt.subplot(1, 3, 3)
        running_avg = np.cumsum(rg_values) / np.arange(1, len(rg_values) + 1)
        plt.plot(timesteps, running_avg, 'g-', linewidth=2)
        plt.axhline(mean_rg, color='r', linestyle='--', label=f'Final Mean = {mean_rg:.3f}')
        plt.xlabel('Time Step')
        plt.ylabel('Running Average R_g (Å)')
        plt.title('Convergence Check')
        plt.legend()
        plt.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig('rg_analysis_results.png', dpi=300, bbox_inches='tight')
        plt.show()

        # Save results
        with open('simulation_results.txt', 'w') as f:
            f.write("GROUP 6 TETRACYCLIC POLYMER - SIMULATION RESULTS\n")
            f.write("="*50 + "\n")
            f.write(f"Expected g-factor from paper: 0.445\n")
            f.write(f"Mean radius of gyration: {mean_rg:.6f} ± {std_rg:.6f} Å\n")
            f.write(f"95% confidence interval: [{conf_int[0]:.6f}, {conf_int[1]:.6f}] Å\n")
            f.write(f"Number of samples: {n}\n")
            f.write(f"Minimum R_g: {min_rg:.6f} Å\n")
            f.write(f"Maximum R_g: {max_rg:.6f} Å\n")
            f.write("\nNote: Compare with theoretical calculation from graph theory\n")

        print("\nResults saved to: simulation_results.txt")
        print("Plots saved to: rg_analysis_results.png")

        return {
            'mean_rg': mean_rg,
            'std_rg': std_rg,
            'conf_int': conf_int,
            'n_samples': n
        }

    except FileNotFoundError:
        print(f"Error: {filename} not found!")
        print("Make sure LAMMPS simulation completed successfully.")
        return None
    except Exception as e:
        print(f"Error analyzing data: {e}")
        return None

if __name__ == "__main__":
    results = analyze_gyration_data()
    if results:
        print("\n🎯 Analysis completed successfully!")
        print("Compare these results with theoretical predictions!")
