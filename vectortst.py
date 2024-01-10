
import random
from process import NewProcess 


if __name__ == "__main__":
    start_port = 5000 + random.randint(0, 1000)
    port_list = [i for i in range(start_port, start_port + 4)]
    num_messages = 4

    new_processes = [NewProcess(i, port_list[i], port_list, num_messages) for i in range(4)]

    for process in new_processes:
        process.launch()

    for process in new_processes:
        process.complete()

    print("All processes finished")

    for i, process in enumerate(new_processes):
        print(f"ID {i}: {process.v_clo}")
