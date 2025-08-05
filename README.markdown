# Fuzzy Logic-Based Anomaly Detection and Correction in Smart Grid Systems

## Overview
This project implements a fuzzy logic-based system for detecting and mitigating anomalies in a smart grid. The system monitors voltage deviation, frequency variation, and load imbalance to detect anomalies and suggests mitigation actions like load balancing, power factor correction, frequency regulation, or shutdown.

## Features
- **Fuzzification**: Converts real-time grid data into fuzzy linguistic variables (e.g., Voltage Deviation: Low, Medium, High).
- **Fuzzy Rules**: Infers anomaly severity (Normal, Warning, Critical) and mitigation actions.
- **Defuzzification**: Uses centroid method to compute anomaly scores and action outputs.
- **Testing**: Includes simulated test cases with anomalies (voltage drops, frequency spikes, load imbalances).
- **Optimization**: Minimizes false positives/negatives through comprehensive rule coverage.
- **Visualization**: Generates plots of anomaly scores and actions.

## Fuzzy Sets
- **Voltage Deviation** (0–10):
  - Low: [0, 0, 5]
  - Medium: [2, 5, 8]
  - High: [5, 10, 10]
- **Frequency Variation** (0–5):
  - Stable: [0, 0, 2]
  - Unstable: [1.5, 3, 5]
- **Load Imbalance** (0–100):
  - Balanced: [0, 0, 50]
  - Unbalanced: [40, 70, 100]
- **Anomaly Score** (0–100):
  - Normal: [0, 0, 30]
  - Warning: [20, 50, 80]
  - Critical: [70, 100, 100]
- **Action Output** (0–100):
  - None: [0, 0, 20]
  - Load Balancing: [15, 30, 45]
  - Power Factor Correction: [40, 55, 70]
  - Frequency Regulation: [65, 80, 95]
  - Shutdown: [90, 100, 100]

## Fuzzy Rules
1. IF Voltage Deviation is Low AND Frequency Variation is Stable AND Load Imbalance is Balanced, THEN Anomaly is Normal AND Action is None.
2. IF Voltage Deviation is Medium OR Frequency Variation is Unstable OR Load Imbalance is Unbalanced, THEN Anomaly is Warning AND Action is Load Balancing.
3. IF Voltage Deviation is Medium AND Frequency Variation is Unstable, THEN Anomaly is Warning AND Action is Power Factor Correction.
4. IF Voltage Deviation is High AND Frequency Variation is Unstable AND Load Imbalance is Unbalanced, THEN Anomaly is Critical AND Action is Shutdown.
5. IF Voltage Deviation is High OR (Frequency Variation is Unstable AND Load Imbalance is Unbalanced), THEN Anomaly is Critical AND Action is Frequency Regulation.
6. IF Voltage Deviation is Low AND Frequency Variation is Unstable, THEN Anomaly is Warning AND Action is Power Factor Correction (reduces false negatives).

## Decision-Making Process
1. **Input**: Real-time grid data (voltage deviation, frequency variation, load imbalance).
2. **Fuzzification**: Map inputs to fuzzy sets using triangular membership functions.
3. **Inference**: Apply fuzzy rules to determine anomaly severity and mitigation action.
4. **Defuzzification**: Compute crisp outputs (anomaly score, action score) using centroid method.
5. **Action**: Interpret action score to select mitigation (e.g., Load Balancing for scores 15–45).

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/fuzzy_anomaly_detection.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the script:
   ```bash
   python main.py
   ```

## Directory Structure
- `main.py`: Core fuzzy logic implementation.
- `data/data.csv`: Simulated test data.
- `data/results.csv`: Output with anomaly scores and actions.
- `screenshots/anomaly_output.png`: Visualization of results.
- `requirements.txt`: Project dependencies.

## Usage
- Update `data/data.csv` with your grid data.
- Run `main.py` to process data and generate results.
- Check `data/results.csv` for outputs and `screenshots/anomaly_output.png` for visualization.

## Test Cases
The included `data.csv` contains 6 test cases simulating:
- Normal conditions (low voltage deviation, stable frequency, balanced load).
- Warning conditions (medium/unstable/unbalanced inputs).
- Critical conditions (high voltage deviation, unstable frequency, unbalanced load).

## Optimization
- **False Positives**: Minimized by requiring multiple high inputs for critical anomalies.
- **False Negatives**: Reduced by including edge-case rules.
- **Grid Stability**: Actions prioritize load balancing and frequency regulation for moderate anomalies, reserving shutdown for critical cases.

## Screenshots
![Anomaly Detection Output](screenshots/anomaly_output.png)
