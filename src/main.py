from src.node import Node
from src.node import netlist


def main():
    #Syntax Node(name,type, propagation_delay, setup_time, hold_time, is input or not)
    node1=Node('FF1', 'FF', 0.5, 5, 1, True)
    node2=Node('FF2', 'FF', 0.5, 5, 1, True)
    node3=Node('FF3', 'FF', 0.5,5,1, True)
    node4=Node('N1', 'GATE', 2)
    node5=Node('N2', 'GATE', 2)
    node6=Node('N3', 'GATE', 2)
    node7=Node('N4', 'GATE', 2)
    node8=Node('FF4', 'FF', 0.5, 5, 1)
    node9=Node('FF5', 'FF', 0.5, 5, 1)

    myCircuit=netlist()
    myCircuit.add(node4, node1, node2)
    myCircuit.add(node5, node2, node3)
    myCircuit.add(node6, node4, node5)
    myCircuit.add(node7, node3, node5)
    myCircuit.add(node9, node7)
    myCircuit.add(node8, node6)
    myCircuit.timingAnalyze()

if __name__ == '__main__':
    main()
    input('\nPress enter to exit...')
