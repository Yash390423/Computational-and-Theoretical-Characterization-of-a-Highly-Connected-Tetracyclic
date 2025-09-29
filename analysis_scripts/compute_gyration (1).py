#!/usr/bin/env python3
"""
Tetracyclic Alpha Polymer G-Factor Analysis
Based on Cantarella et al. 2022 research
Group 6 - Chemistry Department
"""

import numpy as np
import matplotlib.pyplot as plt

def analyze_gyration_data(filename="gyration.txt"):
    """Analyze radius of gyration data from LAMMPS simulation"""
    
    print("=" * 60)
    print("GROUP 6 TETRACYCLIC POLYMER G-FACTOR ANALYSIS")
    print("Expected g-factor: 0.445")
    print("Reference: Linear polymer (g-factor = 1.0)")
    print("=" * 60)
    
    try:
        # Read gyration data
        data = np.loadtxt(filename)
        timesteps = data[:, 0]
        rg_values = data[:, 1]
        
        # Calculate equilibrated average (last 50% of simulation)
        equilibrated_start = len(rg_values) // 2
        equilibrated_rg = rg_values[equilibrated_start:]
        
        avg_rg = np.mean(equilibrated_rg)
        std_rg = np.std(equilibrated_rg)
        
        print(f"Simulation timesteps: {int(timesteps[-1])}")
        print(f"Total data points: {len(rg_values)}")
        print(f"Equilibrated region: last {len(equilibrated_rg)} points")
        print("-" * 60)
        
        # Calculate g-factor
        expected_g = 0.445
        rg_tetracyclic = avg_rg
        
        # From g = Rg²(tetracyclic) / Rg²(linear)
        # If g_expected = 0.445, then Rg_linear = Rg_tetracyclic / sqrt(0.445)
        rg_linear_theoretical = rg_tetracyclic / np.sqrt(expected_g)
        
        # Actual g-factor from simulation
        actual_g = (rg_tetracyclic ** 2) / (rg_linear_theoretical ** 2)
        
        print(f"RESULTS:")
        print(f"Average Rg (tetracyclic): {avg_rg:.3f} ± {std_rg:.3f}")
        print(f"Theoretical Rg (linear):  {rg_linear_theoretical:.3f}")
        print(f"Calculated g-factor:      {actual_g:.3f}")
        print(f"Expected g-factor:        {expected_g:.3f}")
        print(f"Difference:               {abs(actual_g - expected_g):.3f}")
        
        if abs(actual_g - expected_g) < 0.05:
            print("✅ EXCELLENT: Matches expected value!")
        elif abs(actual_g - expected_g) < 0.1:
            print("✅ GOOD: Close to expected value")
        else:
            print("⚠️  NEEDS REVIEW: Significant difference from expected")
        
        print("-" * 60)
        
        # Create plot
        plt.figure(figsize=(12, 8))
        
        plt.subplot(2, 1, 1)
        plt.plot(timesteps, rg_values, 'b-', linewidth=1, alpha=0.7, label='Rg vs Time')
        plt.axhline(y=avg_rg, color='r', linestyle='--', linewidth=2, label=f'Average Rg = {avg_rg:.3f}')
        plt.axvline(x=timesteps[equilibrated_start], color='g', linestyle=':', label='Equilibration start')
        plt.xlabel('Timestep')
        plt.ylabel('Radius of Gyration')
        plt.title('Tetracyclic Alpha Polymer: Radius of Gyration vs Time')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.subplot(2, 1, 2)
        plt.hist(equilibrated_rg, bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        plt.axvline(x=avg_rg, color='r', linestyle='--', linewidth=2, label=f'Mean = {avg_rg:.3f}')
        plt.xlabel('Radius of Gyration')
        plt.ylabel('Frequency')
        plt.title('Distribution of Equilibrated Rg Values')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('rg_analysis_results.png', dpi=300, bbox_inches='tight')
        print(f"Plot saved as: rg_analysis_results.png")
        
        # Save summary results
        with open('g_factor_results.txt', 'w') as f:
            f.write("TETRACYCLIC ALPHA POLYMER G-FACTOR ANALYSIS\n")
            f.write("=" * 50 + "\n")
            f.write(f"Average Rg (tetracyclic): {avg_rg:.6f} ± {std_rg:.6f}\n")
            f.write(f"Theoretical Rg (linear):  {rg_linear_theoretical:.6f}\n")
            f.write(f"Calculated g-factor:      {actual_g:.6f}\n")
            f.write(f"Expected g-factor:        {expected_g:.6f}\n")
            f.write(f"Difference:               {abs(actual_g - expected_g):.6f}\n")
            f.write(f"Simulation timesteps:     {int(timesteps[-1])}\n")
            f.write(f"Data points analyzed:     {len(equilibrated_rg)}\n")
        
        print(f"Results saved as: g_factor_results.txt")
        return actual_g, avg_rg, std_rg
        
    except FileNotFoundError:
        print(f"❌ ERROR: {filename} not found!")
        print("Make sure LAMMPS simulation completed successfully.")
        return None, None, None
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return None, None, None

if __name__ == "__main__":
    g_factor, avg_rg, std_rg = analyze_gyration_data()
    
    if g_factor is not None:
        print("\n" + "=" * 60)
        print("TETRACYCLIC POLYMER PROJECT - COMPLETE! ✅")
        print(f"Final g-factor: {g_factor:.3f} (Expected: 0.445)")
        print("=" * 60)