import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import pandas as pd
import matplotlib.pyplot as plt
import os

# Create output directories if they don't exist
os.makedirs('data', exist_ok=True)
os.makedirs('screenshots', exist_ok=True)

# Define fuzzy variables
voltage_dev = ctrl.Antecedent(np.arange(0, 11, 0.1), 'voltage_deviation')
freq_var = ctrl.Antecedent(np.arange(0, 6, 0.1), 'frequency_variation')
load_imb = ctrl.Antecedent(np.arange(0, 101, 1), 'load_imbalance')
anomaly = ctrl.Consequent(np.arange(0, 101, 1), 'anomaly_score')
action = ctrl.Consequent(np.arange(0, 101, 1), 'action_output')

# Fuzzification: Define membership functions
voltage_dev['low'] = fuzz.trimf(voltage_dev.universe, [0, 0, 5])
voltage_dev['medium'] = fuzz.trimf(voltage_dev.universe, [2, 5, 8])
voltage_dev['high'] = fuzz.trimf(voltage_dev.universe, [5, 10, 10])

freq_var['stable'] = fuzz.trimf(freq_var.universe, [0, 0, 2])
freq_var['unstable'] = fuzz.trimf(freq_var.universe, [1.5, 3, 5])

load_imb['balanced'] = fuzz.trimf(load_imb.universe, [0, 0, 50])
load_imb['unbalanced'] = fuzz.trimf(load_imb.universe, [40, 70, 100])

anomaly['normal'] = fuzz.trimf(anomaly.universe, [0, 0, 30])
anomaly['warning'] = fuzz.trimf(anomaly.universe, [20, 50, 80])
anomaly['critical'] = fuzz.trimf(anomaly.universe, [70, 100, 100])

action['none'] = fuzz.trimf(action.universe, [0, 0, 20])
action['load_balancing'] = fuzz.trimf(action.universe, [15, 30, 45])
action['power_factor_correction'] = fuzz.trimf(action.universe, [40, 55, 70])
action['frequency_regulation'] = fuzz.trimf(action.universe, [65, 80, 95])
action['shutdown'] = fuzz.trimf(action.universe, [90, 100, 100])

# Fuzzy Rules
rules = [
    # Normal conditions
    ctrl.Rule(voltage_dev['low'] & freq_var['stable'] & load_imb['balanced'], 
              (anomaly['normal'], action['none'])),
    # Warning conditions
    ctrl.Rule(voltage_dev['medium'] | freq_var['unstable'] | load_imb['unbalanced'], 
              (anomaly['warning'], action['load_balancing'])),
    ctrl.Rule(voltage_dev['medium'] & freq_var['unstable'], 
              (anomaly['warning'], action['power_factor_correction'])),
    # Critical conditions
    ctrl.Rule(voltage_dev['high'] & freq_var['unstable'] & load_imb['unbalanced'], 
              (anomaly['critical'], action['shutdown'])),
    ctrl.Rule(voltage_dev['high'] | (freq_var['unstable'] & load_imb['unbalanced']), 
              (anomaly['critical'], action['frequency_regulation'])),
    # Edge case to reduce false negatives
    ctrl.Rule(voltage_dev['low'] & freq_var['unstable'], 
              (anomaly['warning'], action['power_factor_correction']))
]

# Create control system
anomaly_ctrl = ctrl.ControlSystem(rules)
anomaly_sim = ctrl.ControlSystemSimulation(anomaly_ctrl)

# Simulated test cases
test_data = {
    'voltage_deviation': [1, 4, 8, 9.5, 3, 6],
    'frequency_variation': [0.5, 2, 4, 4.5, 1.5, 3.5],
    'load_imbalance': [20, 50, 80, 90, 40, 70]
}
df = pd.DataFrame(test_data)
df.to_csv('data/sample_data.csv', index=False)

# Process test cases
results = []
for index, row in df.iterrows():
    anomaly_sim.input['voltage_deviation'] = row['voltage_deviation']
    anomaly_sim.input['frequency_variation'] = row['frequency_variation']
    anomaly_sim.input['load_imbalance'] = row['load_imbalance']
    
    try:
        anomaly_sim.compute()
        anomaly_score = anomaly_sim.output['anomaly_score']
        action_output = anomaly_sim.output['action_output']
        
        # Interpret action output
        if action_output <= 20:
            action_desc = 'None'
        elif action_output <= 45:
            action_desc = 'Load Balancing'
        elif action_output <= 70:
            action_desc = 'Power Factor Correction'
        elif action_output <= 95:
            action_desc = 'Frequency Regulation'
        else:
            action_desc = 'Shutdown'
        
        results.append({
            'voltage_deviation': row['voltage_deviation'],
            'frequency_variation': row['frequency_variation'],
            'load_imbalance': row['load_imbalance'],
            'anomaly_score': round(anomaly_score, 2),
            'action_output': round(action_output, 2),
            'action_description': action_desc
        })
    except KeyError as e:
        print(f"Error processing row {index}: {e}")
        results.append({
            'voltage_deviation': row['voltage_deviation'],
            'frequency_variation': row['frequency_variation'],
            'load_imbalance': row['load_imbalance'],
            'anomaly_score': None,
            'action_output': None,
            'action_description': 'Error'
        })

# Save results
results_df = pd.DataFrame(results)
results_df.to_csv('data/results.csv', index=False)

# Visualize results
plt.figure(figsize=(10, 6))
plt.plot(results_df['anomaly_score'], label='Anomaly Score', marker='o')
plt.plot(results_df['action_output'], label='Action Output', marker='x')
plt.title('Fuzzy Logic Anomaly Detection and Correction Results')
plt.xlabel('Test Case Index')
plt.ylabel('Score')
plt.legend()
plt.grid(True)
plt.savefig('screenshots/anomaly_output.png')
plt.close()

# Print summary
print("Test cases processed. Results saved to data/results.csv")
print("Visualization saved to screenshots/anomaly_output.png")
print("\nSummary of Results:")
print(results_df)

# Optimization: Evaluate false positives/negatives
false_positives = len(results_df[(results_df['anomaly_score'] > 50) & (results_df['voltage_deviation'] < 2)])
false_negatives = len(results_df[(results_df['anomaly_score'] < 50) & (results_df['voltage_deviation'] > 8)])
print(f"\nOptimization Metrics:")
print(f"False Positives: {false_positives}")
print(f"False Negatives: {false_negatives}")