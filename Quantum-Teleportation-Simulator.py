import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector
import matplotlib.pyplot as plt
from qiskit_aer.noise import NoiseModel, depolarizing_error

# --- Parameters ---
theta = np.pi / 4
p_error = 0.05
num_shots = 1000

# --- Prepare the message qubit (Alice's qubit) ---
msg_circ = QuantumCircuit(1)
msg_circ.ry(theta, 0)

# --- Main teleportation circuit ---
qc = QuantumCircuit(3, 3)
qc.compose(msg_circ, [0], inplace=True)
qc.barrier()

# Create entanglement (Bell pair) between qubits 1 & 2
qc.h(1)
qc.cx(1, 2)
qc.barrier()

# Bell measurement on Alice's side
qc.cx(0, 1)
qc.h(0)
qc.barrier()

# Classical corrections on Bob's side
qc.cx(1, 2)
qc.cz(0, 2)
qc.barrier()

# --- Visualize Bloch sphere before measurement ---
final_state = Statevector(qc)
plot_bloch_multivector(final_state)
plt.title("Qubit States (before measurement)")
plt.show()

# --- Measurement ---
qc.measure([0, 1, 2], [0, 1, 2])
print(qc.draw())

# --- Ideal simulation ---
simulator = AerSimulator()
ideal_counts = simulator.run(qc, shots=num_shots).result().get_counts(qc)
print(f"\nIdeal results ({num_shots} shots): {ideal_counts}")

# --- Noise model ---
error_1q = depolarizing_error(p_error, 1)
noise_model = NoiseModel()
noise_model.add_all_qubit_quantum_error(error_1q, ['h', 'x', 'z', 'ry'])

# --- Noisy simulation ---
noisy_simulator = AerSimulator(noise_model=noise_model)
noisy_counts = noisy_simulator.run(qc, shots=num_shots).result().get_counts(qc)
print(f"\nResults with {p_error*100:.0f}% noise: {noisy_counts}")

# --- Detailed state comparison ---
total_ideal = sum(ideal_counts.values())
total_noisy = sum(noisy_counts.values())

print("\n--- DETAILED STATE COMPARISON ---")
print(f"{'State':<12} | {'Ideal (%)':<12} | {'With 5% Noise (%)':<12}")
print("-" * 46)

all_states = [format(i, '03b') for i in range(8)]
for state in all_states:
    ideal_pct = (ideal_counts.get(state, 0) / total_ideal) * 100
    noisy_pct = (noisy_counts.get(state, 0) / total_noisy) * 100
    print(f"   {state:<9} |    {ideal_pct:>5.1f}%     |      {noisy_pct:>5.1f}%")

# --- Bob's qubit analysis (qubit 2 = leftmost bit in the string) ---
bob_ideal = {
    '0': sum(c for s, c in ideal_counts.items() if s[0] == '0'),
    '1': sum(c for s, c in ideal_counts.items() if s[0] == '1'),
}
bob_noisy = {
    '0': sum(c for s, c in noisy_counts.items() if s[0] == '0'),
    '1': sum(c for s, c in noisy_counts.items() if s[0] == '1'),
}

print("\n--- BOB'S RECEIVED MESSAGE (Qubit 2) ---")
print(f"{'Measurement':<12} | {'Ideal (%)':<12} | {'With 5% Noise (%)':<12}")
print("-" * 46)
for bit in ['0', '1']:
    ideal_pct = (bob_ideal[bit] / total_ideal) * 100
    noisy_pct = (bob_noisy[bit] / total_noisy) * 100
    print(f"Received '{bit}'  |    {ideal_pct:>5.1f}%     |      {noisy_pct:>5.1f}%")
print("-" * 46)

# --- Bar chart comparison ---
fig, ax = plt.subplots(figsize=(10, 5))
x = np.arange(len(all_states))
width = 0.35

ideal_vals = [(ideal_counts.get(s, 0) / total_ideal) * 100 for s in all_states]
noisy_vals = [(noisy_counts.get(s, 0) / total_noisy) * 100 for s in all_states]

ax.bar(x - width/2, ideal_vals, width, label='Ideal', color='steelblue')
ax.bar(x + width/2, noisy_vals, width, label=f'With {p_error*100:.0f}% Noise', color='tomato')
ax.set_xticks(x)
ax.set_xticklabels(all_states)
ax.set_xlabel('State')
ax.set_ylabel('Probability (%)')
ax.set_title('Ideal vs Noisy Simulation Comparison')
ax.legend()
plt.tight_layout()
plt.show()
