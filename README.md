# ⚛️ Quantum Teleportation Simulator

A Python simulation of the **quantum teleportation protocol** using IBM's Qiskit framework. The project demonstrates how a quantum state can be transmitted from one qubit (Alice) to another (Bob) using entanglement and classical communication — with an optional **depolarizing noise model** to simulate real-world quantum hardware.

---

## 📌 What It Does

- Encodes an arbitrary qubit state using a rotation gate `Ry(θ)`
- Builds a 3-qubit teleportation circuit (Alice: qubits 0 & 1, Bob: qubit 2)
- Applies the full teleportation protocol:
  - Bell pair entanglement
  - Bell measurement on Alice's side
  - Classical corrections on Bob's side
- Visualizes qubit states on the **Bloch sphere** before measurement
- Runs both an **ideal simulation** and a **noisy simulation** (5% depolarizing error)
- Prints a detailed **state-by-state comparison** table
- Plots a **bar chart** comparing ideal vs. noisy results

---

## 🔬 The Teleportation Protocol

```
Alice          Bob
──────────────────────────────────────
Qubit 0 ─[Ry(θ)]──●──[H]──────────●──
                   │               │
Qubit 1 ─[H]──────┼────────●──────┼──
              [CX]─┘        │      │
Qubit 2 ────────────────[CX]──[CZ]───  ← Bob receives the state
```

---

## 🛠️ Requirements

- Python 3.8+
- [Qiskit](https://qiskit.org/) 
- [Qiskit Aer](https://github.com/Qiskit/qiskit-aer)
- NumPy
- Matplotlib

Install dependencies:

```bash
pip install qiskit qiskit-aer numpy matplotlib
```

---

## 🚀 Usage

```bash
python quantum_teleportation.py
```

You can modify the rotation angle to teleport different quantum states:

```python
theta = np.pi / 4   # Change this to encode a different state
```

And adjust the noise level:

```python
p_error = 0.05  # 5% depolarizing error per gate
```

---

## 📊 Example Output

With `θ = π/4`, the ideal simulation yields:

| Bob's Measurement | Ideal  | With 5% Noise |
|-------------------|--------|---------------|
| Received `0`      | ~85.4% | ~75–80%       |
| Received `1`      | ~14.6% | ~20–25%       |

The noise model applies a **depolarizing error** to every `H`, `X`, `Z`, and `Ry` gate, simulating the kind of decoherence found in real quantum processors.

---

## 📁 Project Structure

```
quantum-teleportation/
│
├── quantum_teleportation.py   # Main simulation script
└── README.md
```

---

## 📚 Background

Quantum teleportation was first proposed by Bennett et al. in 1993. It does **not** transmit information faster than light — the classical correction step (2 classical bits) is required to complete the protocol. What is teleported is the **quantum state**, not matter or energy.


<img width="1433" height="546" alt="image" src="https://github.com/user-attachments/assets/5578b0f5-c747-420f-83ac-7b89a201796b" />

<img width="996" height="565" alt="image" src="https://github.com/user-attachments/assets/6d2850b1-6993-44ff-8f56-0caeae8c39cd" />




Key concepts used in this project:
- **Entanglement** — Bell state shared between Alice and Bob
- **Bell Measurement** — Projects Alice's qubits onto a Bell basis
- **Classical Communication** — 2 bits sent from Alice to Bob
- **Depolarizing Noise** — Models random Pauli errors on gates

---
