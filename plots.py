import matplotlib.pyplot as plt


def plot_pdu_vs_simulation_time(simulation_time, pdu_count, filename='pdu_vs_simulation_time.jpg'):
    plt.figure(figsize=(10, 5))
    plt.plot(range(simulation_time + 1), pdu_count, label='PDU count')
    plt.xlabel('Simulation Time')
    plt.ylabel('PDU Count')
    plt.title('PDU vs Simulation Time')
    plt.legend()
    plt.grid(True)
    plt.savefig(filename)
    plt.show()


def plot_upf_vs_simulation_time(simulation_time, upf_count, filename='upf_vs_simulation_time.jpg'):
    plt.figure(figsize=(10, 5))
    plt.plot(range(simulation_time + 1), upf_count, label='UPF count')
    plt.xlabel('Simulation Time')
    plt.ylabel('UPF Count')
    plt.title('UPF vs Simulation Time')
    plt.legend()
    plt.grid(True)
    plt.savefig(filename)
    plt.show()
