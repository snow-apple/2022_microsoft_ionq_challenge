from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
from qiskit.tools.monitor import job_monitor
from azure.quantum.qiskit import AzureQuantumProvider
import random
import matplotlib.pyplot as plt 
import math

class QuantumJeopardy:
    def __init__(self):
        self.backend = None
    
    def setup_backend(self, resource_id , backend_type = "ionq.simulator"):
        provider = AzureQuantumProvider (
            resource_id = resource_id,
            location = "eastus"
        )
        print([backend.name() for backend in provider.backends()])
        self.backend = provider.get_backend(backend_type)


    def apply_gates(self, gates, qc):
        for gate in gates:
            getattr(qc,gate[0])(gate[1])
        return qc


    #applying user gates (the user can choose up to three gates to run)
    def get_input(self):
        gate_set = []
        for i in range(3):
            gate_type = input("What gate would you like to use? (Type None if no gate): ")
            if gate_type in ["x", "y", "z", "t", "None"]:
                if gate_type != "None":
                    qubit_type = int(input("Which qubit would you like to apply the gate to?: "))
                    gate_set.append((gate_type, qubit_type))
                else:
                    print("skipped code")
            else:
                raise ValueError("please input a correct gate")

        return gate_set

    def play_round(self, make_random = True):
        """
        1. It initializes the circuit in a random state
        2. It calls get_input() to let the user choose which gates they want to apply to the circuit. The user's
        goal is to maximize the probability of choosing a certain topic, represented by a quantum state 
        (|00> -> 0, |01> -> 1, |10> -> 2, |11> -> 3).
        3. The final circuit is run by run_result using either the simulator or quantum hardware
        4. The results are parsed.
        5. The most common measurment is converted into a choice. (|00> -> 0, |01> -> 1, |10> -> 2, |11> -> 3) 
        """
        
        if self.backend is None:
            raise ValueError("please setup backend first ")
            
        # circuit initialization (We can set the rotation angles randomly) 
        circuit = QuantumCircuit(2, 2)
        circuit.h(0)
        circuit.cx(0,1) #this creates a bell state |00> + |11> . The qubits are maximaly entangled.

        # adding random rotations
        if make_random:
            rotations = [random.random()*2*math.pi for i in range(4)]
            circuit.rx(rotations[0],0)
            circuit.rz(rotations[1],0)
            circuit.rx(rotations[2],1)
            circuit.rz(rotations[3],1)

        print(circuit)
        gate_set = self.get_input()           
        circuit = self.apply_gates(gate_set, circuit)
        circuit.measure([0, 1], [0, 1])
        print(circuit)

        result = self.run_result(circuit)

        # parsing results
        counts = {format(n, "02b"): 0 for n in range(4)}
        counts.update(result.get_counts(circuit))
        print(counts)

        # finding which measurment was measured the most amount of times
        max_counts = 0
        max_key = None
        for key,count in counts.items():
            if count > max_counts:
                max_counts = count
                max_key = key
        max_key = max_key[::-1] # reversing string since qiskit represents |01> as "10"
        choice = int(max_key, 2)
        return choice


    def run_result(self, qc):
        job = self.backend.run(qc, shots=100)
        job_id = job.id()
        print("Job id", job_id)
        job_monitor(job)
        result = job.result()
        return result