import socket, math, time

class SirioAPI:
    def __init__(self, Address="raw_trinity.sirio-network.com", Port=1407, Silent=False):
        self.socket = socket.socket()
        self.socket.settimeout(1)
        self.address = Address
        self.port = Port
        self.packetsize = 8192
        self.version = "v241021"
        self.silent = False

    def log(self, Log):
        CTime = time.localtime()
        Time = f"{CTime.tm_hour:02d}:{CTime.tm_min:02d}:{CTime.tm_sec:02d}"
        Date = f"{CTime.tm_mday:02d}-{CTime.tm_mon:02d}-{CTime.tm_year}"
        if not self.silent:
            print(f"[{Date} - {Time}] {Log}")

    def connect(self, Attempts_Max=3):
        Attempts = 0
        while Attempts != Attempts_Max:
            Attempts+=1
            self.log(f"Attempt N°{Attempts} to connect to {self.address}:{self.port}...")
            try:
                Ping = time.monotonic()*1000
                self.socket.connect((self.address,self.port))
                Ping = math.floor(((time.monotonic()*1000) - Ping))
                self.log(f"Connection successful, latency: {Ping}ms.")
                return Ping
            except Exception as Error:
                self.log(f"Failed to connect to the server!\n{Error}")
        self.log(f"Reached {Attempts_Max} attempts, giving up!")
        return -1

    def receive(self, Attempts_Max=1):
        Attempts = 0
        while Attempts != Attempts_Max:
            Attempts+=1
            self.log(f"Attempt N°{Attempts} to receive data...")
            try:
                self.socket.recv(self.packetsize).decode()
                self.log(f"Received data successfully! ({Data})")
                return Data
            except Exception as Error:
                self.log(f"Failed to receive data!\n{Error}")
        self.log(f"Reached {Attempts_Max} attempts, giving up!")
        return None

    def send(self, Request, Attempts_Max=1):
        Attempts = 0
        while Attempts != Attempts_Max:
            Attempts+=1
            self.log(f"Attempt N°{Attempts} to send data...")
            try:
                self.socket.send(str(Request).encode())
                return Data
            except Exception as Error:
                self.log(f"Failed to receive data!\n{Error}")
        self.log(f"Reached {Attempts_Max} attempts, giving up!")
        return "CONNECTION_ERROR"

    def request(self, Request="Echo://shellRSC-Test", Attempts_Max=1):
        if self.send(Request, Attempts_Max) != "CONNECTION_ERROR":
            return self.receive(Request, Attempts_Max)

    def close(self):
        self.log(f"Closing the connection...")
        self.socket.close()

    def shell(self):
        def DiscardCommand(command):
            command.pop(0)
            arguments = ""
            for argument in command:
                arguments+=f"{argument} "
            return arguments

        self.log(f"Sirio Network shellRSC v{self.version}")
        if self.connect() == -1:
            self.log("Could not connect to the server ! Run the connect command to try again.")
        while True:
            Command_String = input(f"shellRSC:/{self.address}:{self.port}$ ")
            Command = Command_String.split(" ")
            match Command[0].lower():
                case "help":
                    print("shellRSC Commands\n")
                    print("exit\n     Quit shellRSC")
                    print("help\n     Print this help message")
                    print("version\n     Print the shellRSC version")
                    print("Sirio Network API Commands\n")
                    print("close\n     Close the API Connection")
                    print("connect\n     Connect to the API")
                    print("send [ Request, **Attempts_Max=1 ]\n     Send data to the server")
                    print("receive [ **Attempts_Max=1 ]\n     Receive data from the server")
                    print("request [ Request=Echo://shellRSC-Test, **Attempts_Max=1]\n     Sends and then receives data from the server")
                case "exit":
                    print("Quitting shellRSC...")
                    break
                case "version":
                    print(f"Sirio Network shellRSC v{self.version}")
                case "close":
                    self.close()
                case "connect":
                    self.connect()
                case "send":
                    if len(Command) == 3:
                        self.send(Command[1], Command[2])
                    else:
                        self.send(Command[1])
                case "receive":
                    if len(Command) == 2:
                        print(self.receive(Command[1]))
                    else:
                        print(self.receive())
                case "request":
                    if len(Command) == 3:
                        self.request(Command[1], Command[2])
                    if len(Command) == 2:
                        self.request(Command[1])
                    else:
                        self.request()
                case _:
                    print(f"shellRSC: {Command}: command not found")


if __name__ == '__main__':
    Trinity = SirioAPI()
    Trinity.shell()