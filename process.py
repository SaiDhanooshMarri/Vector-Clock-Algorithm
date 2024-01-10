import socket
import threading
import time
import pickle


class NewProcess:
    def __init__(self, identifier, port_num, all_identifiers, num_messages):
        self.id, self.port, self.all_ids, self.v_clo, self.num_msgs, self.re_c = (
            identifier,
            port_num,
            all_identifiers,
            [0] * len(all_identifiers),
            num_messages,
            0,
        )
        self.ser_th = threading.Thread(target=self.ss)
        self.cli_th = threading.Thread(target=self.start_client)

    def launch(self):
        self.ser_th.start()
        self.cli_th.start()

    def complete(self):
        self.ser_th.join()
        self.cli_th.join()

    def ss(self):
        s_so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_so.bind(("localhost", self.port))
        s_so.listen(5)

        print(f"ID {self.id}: Listening on port {self.port}")

        while self.re_c < self.num_msgs * (len(self.all_ids) - 1):
            connection, address = s_so.accept()
            data = connection.recv(1024)
            r_v = pickle.loads(data)
            self.u_v(r_v)
            print(f"ID {self.id}: Received clock {r_v} from {address[1]}")
            connection.close()
            self.re_c += 1
        s_so.close()

    def start_client(self):
        for _ in range(self.num_msgs):
            time.sleep(2)
            self.v_clo[self.id] += 1
            print(f"ID {self.id}: Executed local op, updated clock: {self.v_clo}")

            for i, target_id in enumerate(self.all_ids):
                if i != self.id:
                    try:
                        c_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        c_soc.connect(("localhost", target_id))
                        c_soc.send(pickle.dumps(self.v_clo))
                        c_soc.close()
                        print(f"ID {self.id}: Sent clock {self.v_clo} to {i}")
                    except ConnectionRefusedError:
                        pass

    def u_v(self, r_v):
        self.v_clo = [max(self.v_clo[i], r_v[i]) for i in range(len(self.v_clo))]