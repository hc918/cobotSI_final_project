import socket

# 리프트가 C# 기반의 코드를 사용하기 때문에 C# 프로그램과 통신하는 클래스 구성
class LiftConnect:

    def __init__(self, HOST='192.168.1.2', PORT=9999):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((HOST, PORT))

    def sendData(self, up_down_value, time):
        for i in range(1, 10):
            msg = f"{up_down_value}-{time}"
            data = msg.encode()
            length = len(data)
            self.client_socket.sendall(length.to_bytes(4, byteorder="big"))
            self.client_socket.sendall(data)

            data = self.client_socket.recv(4)
            length = int.from_bytes(data, "big")
            data = self.client_socket.recv(length)
            if data.decode() == "1":
                return True
            else:
                return False

    def Disconnect(self):
        self.client_socket.close()
