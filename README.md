# MIT iQuHACK 2022 Project

Project coming soon...
##The Quantum Quiz Game...........(Just a bad name :))
Greatly based on ur quizlet model,and using Lana's cloumns as the visual effects. Say we use this game in a competition. Participants are shown 4 columns representing 4 topics representing 4  Quantum states.They have a favourite topic in one of them,they want to increase the probability of finding that particular state representing their favorite topic. For that they need to design a circuit (a few qubits) to get the desired out put. this is based on my understanding -please point out the drawbacks

 there are 4 options essentially(each option is a quantum state using a few qubits). And the participants have to create a quantum circuit that would get them to that state which increases the prob amplitude of the state representing their prefered topic
 
 Imagine that the game is kind of like jeopardy and the participants want to select a topic that they know best. Then we would implement the Whack-a-Mole type of idea so that they would have a greater chance at selecting that topic. From that topic, we could either have the computer completely randomly select a question or we could implement the same idea from before.

 I think that we can just print a list of the topics where their order represents the column that they are in
 ##But I'll still find the code for visuals for our presentation

1. Need a list of 4 topics
  a) List of topics are printed
  b) Players can manipulate circuits to increase the chance of picking a topic
  c) Can add a maximum of 3 gates

2. Each topic has 4 questions (for now)
  a) Questions are randomly chosen by computer (possibly by player)
  b) If answered correctly, points go up
  c) Return to topic choosing phase

3. Repeat for the specified amount of rounds
