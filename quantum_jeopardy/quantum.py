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
        self.setup_game()
    
    def setup_backend(self, resource_id , backend_type = "ionq.simulator"):
        provider = AzureQuantumProvider (
            resource_id = resource_id,
            location = "eastus"
        )
        print([backend.name() for backend in provider.backends()])
        self.backend = provider.get_backend(backend_type)

    def setup_game(self):
        self.points = 0

        #Get number of rounds
        print("How many rounds? ")
        self.rounds = int(input())
        print("") #Spacing

        #List of quiz topics
        self.topicsList = ["Quantum", "Astronomy", "Math", "Geography"]

        #Print the topics
        print("The topics are: ")
        for topic in self.topicsList:
            print(topic)

        #Lists that have the questions and answers for each topic
        self.quantumQs = ["Bell states are a example of_________", "The CNOT gate is a ____ Qubit Gate"]
        self.quantumAs = ["entangled state", "2"]

        self.astronomyQs = ["A supermassive black hole that exists at the centre of the Milky Way Galaxy is _________", "The closest galaxy to the Milky Way is ___________"]
        self.astronomyAs = ["sagittarius a", "andromeda"]

        self.mathQs = ["Hilbert space is ____ Dimensional", "Complex numbers are __________ Dimensional"]
        self.mathAs = ["infinite", "2"]

        self.geographyQs = ["South Pole is situated in which continent?", "The great Barrier reef is situated in ________"]
        self.geographyAs = ["antartica", "australia"]
        
    def run(self, level = 0):
        #Start the game
        for i in range(self.rounds):
            print("Round " + str(i + 1))
            print("="*20)

            print("Here are the topics: " + str(self.topicsList))
            topic_number = self.play_round(level = level)

            #quantum pick topic
            topic = self.topicsList[topic_number]
            print("The topic is " + topic + "!")
            print("Enter your answers in lowercase letters only. For numbers, use integers only.")
            print("") #Spacing

            if(topic == "Quantum"):
                #Randomly pick question
                index = random.randint(0, len(self.quantumQs) - 1)
                question = self.quantumQs[index]
                realAns = self.quantumAs[index]

                #Ask question
                print(question)
                playerAns = input()

                #Check answer
                if(playerAns == realAns):
                    print("Correct!")
                    self.points += 1
                    print("Points: " + str(self.points))
                else:
                    print("Incorrect! The answer is " + realAns + ".")
                    self.points -= 1
                    print("Points: " + str(self.points))

            elif(topic == "Astronomy"):
                #Randomly pick question
                index = random.randint(0, len(self.astronomyQs) - 1)
                question = self.astronomyQs[index]
                realAns = self.astronomyAs[index]

                #Ask question
                print(question)
                playerAns = input()

                #Check answer
                if(playerAns == realAns):
                    print("Correct!")
                    self.points += 1
                    print("Points: " + str(self.points))
                else:
                    print("Incorrect! The answer is " + realAns + ".")
                    self.points -= 1
                    print("Points: " + str(self.points))

            elif(topic == "Math"):
                #Randomly pick question
                index = random.randint(0, len(self.mathQs) - 1)
                question = self.mathQs[index]
                realAns = self.mathAs[index]

                #Ask question
                print(question)
                playerAns = input()

                #Check answer
                if(playerAns == realAns):
                    print("Correct!")
                    self.points += 1
                    print("Points: " + str(self.points))
                else:
                    print("Incorrect! The answer is " + realAns + ".")
                    self.points -= 1
                    print("Points: " + str(self.points))

            else:
                #Randomly pick question
                index = random.randint(0, len(self.geographyQs) - 1)
                question = self.geographyQs[index]
                realAns = self.geographyAs[index]

                #Ask question
                print(question)
                playerAns = input()

                #Check answer
                if(playerAns == realAns):
                    print("Correct!")
                    self.points += 1
                    print("Points: " + str(self.points))
                else:
                    print("Incorrect! The answer is " + realAns + ".")
                    self.points -= 1
                    print("Points: " + str(self.points))

            print("") #Spacing for next round
        print("="*20)
        print("GAME OVER! Your final score is: " + str(self.points))


        
        
    def apply_gates(self, gates, qc):
        for gate in gates:
            if len(gate) < 3:
                getattr(qc,gate[0])(gate[1])
            else: 
                getattr(qc,gate[0])(gate[1],gate[2])
        return qc


    #applying user gates (the user can choose up to three gates to run)
    def get_input(self):
        gate_set = []
        for i in range(3):
            gate_type = input("What gate would you like to use? (Type None if no gate): ")
            if gate_type in ["x", "y", "z", "t", "cx", "h", "None"]:
                if gate_type != "None" and gate_type != "cx" :
                    qubit_type = int(input("Which qubit would you like to apply the gate to?: "))
                    gate_set.append((gate_type, qubit_type))
                elif gate_type == "cx":
                    qubit_type1 = int(input("Which qubit is the control?: "))
                    qubit_type2 = int(input("Which qubit is the target?: "))
                    gate_set.append((gate_type, qubit_type1, qubit_type2))
                else:
                    print("skipped code")
            else:
                raise ValueError("please input a correct gate")

        return gate_set

    def play_round(self, level = 0):
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
        
        print("These topics correspond to the following quantum states: " + str(["|00>", "|01>", "|10>", "|11>"]))
        # circuit initialization (We can set the rotation angles randomly) 
        circuit = QuantumCircuit(2, 2)
        circuit.h(0)
        circuit.cx(0,1) #this creates a bell state |00> + |11> . The qubits are maximaly entangled.

        # adding random rotations
        if level == 0: 
            pass
        elif level == 1:
            if random.random() > 0.5:
                circuit.x(0)
            if random.random() > 0.5:
                circuit.z(0)
            if random.random() > 0.5:
                circuit.x(1)
            if random.random() > 0.5:
                circuit.z(1)
        elif level == 2:
            rotations = [random.random()*2*math.pi for i in range(4)]
            circuit.rx(rotations[0],0)
            circuit.rz(rotations[1],0)
            circuit.rx(rotations[2],1)
            circuit.rz(rotations[3],1)
            

        print(circuit)
        print("A random initial quantum state has been prepared. You can add up to 3 gates to maximize the probability of measuring the quantum state corresponding to the topic of your choice. You are allowed to use the x, y, z, cx, h, and t gates.\n")
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
    
    def reset(self):
        self.setup_game()