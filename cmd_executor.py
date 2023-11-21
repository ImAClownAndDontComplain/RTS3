import os
from threading import Thread


class ConsumerD(Thread):
    def __init__(self, pipe_connection):
        super().__init__()
        self.pipe_connection = pipe_connection

    def run(self) -> None:
        for _ in range(40):
            # waiting for command from pipe
            response = self.pipe_connection.recv()

            # putting command into cmd
            stream = os.popen(response)

            # reading result
            output = stream.read().encode('cp1251').decode('cp866')

            # sending result via pipe
            self.pipe_connection.send(output)


if __name__ == "__main__":
    cmd = 'cmd.exe /c dir'
    stream = os.popen(cmd)
    output = stream.read()
    output = output.encode('cp1251').decode('cp866')
    print(output)