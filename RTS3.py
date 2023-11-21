import sys

from multiprocessing import Process, Pipe
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from cmd_executor import ConsumerD

# init pyqt app
app = QApplication(sys.argv)


class APP(QWidget):
    def __init__(self, pipe_part):
        super().__init__()
        self.pipe_part = pipe_part
        
        # window
        self.setWindowTitle("RTS-3")
        self.move(300, 300) 
        self.resize(800, 500) 
        self.setStyleSheet('QWidget {background-color: #A3C1DA}')
        
        #  button
        self.button = QPushButton("Send", self)
        self.button.setStyleSheet('QPushButton {color: rgb(255, 255, 255); background-color: rgb(38,56,76);}');
        self.button.setFont(QFont('Times', 14))
        self.button.move(350, 400)
        self.button.clicked.connect(self.clicked)

        #  text label
        self.label = QLabel("", self)
        self.label.setFont(QFont('Times', 11))
        self.label.move(250,150)
        self.label.resize(300,200)
        
        self.Line_edit()

    def Line_edit(self):
        # input 
        self.input_text = QLineEdit(self)
        self.input_text.setStyleSheet('QLineEdit {color: rgb(0, 0, 0); background-color: rgb(200, 200, 200);}');
        self.input_text.move(280,50)
        self.input_text.setFont(QFont('Times', 14))
        self.input_text.setPlaceholderText("Command")

    def clicked(self):
        if self.input_text.text():
            
            # send input value via pipe
            text = self.input_text.text()
            self.pipe_part.send(text)

            # waiting for response from another end of pipe
            recv_text = self.pipe_part.recv()
            print(recv_text)
            print(type(recv_text))
            if recv_text is None:
                self.label.setText('error')
            self.label.setText(recv_text)


if __name__ == '__main__':
    parent_conn, child_conn = Pipe()

    ConsumerD(child_conn).start()

    window = APP(parent_conn)
    window.show()
    sys.exit(app.exec_())