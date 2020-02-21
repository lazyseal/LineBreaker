import sys, time, serial, datetime
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QMainWindow, QLCDNumber, QFileDialog, QTextEdit, QGridLayout
from PyQt5.QtCore import QCoreApplication
from grid3 import Ui_MainWindow

text1 = '''
Версия 0.90
Всё начато с чистого листа. Да пребудет с нами Кот
Исправлено открытие COM-порта
(В работе)Обновлён алгоритм работы кнопки "Начать запись" - теперь её нажатие обнуляет сохранённые ранее данные

Параметры соединения указываются через "-" 
Например:
COM1-9600
Пока что поддерживается только имя порта и скорость
остальные параметры -N-8-1 заданы по умолчанию
После этого нужно нажать "Начать запись". Когда будет накоплено достаточно информации, нужно нажать "Остановить запись".

Кнопка "Сохранить в файл" сохраняет все данные, полученные между нажатиями кнопки "Начать запись" и нажатием "Остановить запись" в сыром виде

Кнопка "Выбрать файл" позволяет выбрать файл с данными и сразу же переводит данные
из выбранного файла в отдельные строки в файл output.txt
и конвертирует их в десятичную систему в файл output_decimal.txt
Проверки формата входных данных пока что нет, если загрузить что-то не то - программа упадёт 😄

Кнопка "Построить график" строит график на основании записанных данных или данных из файла

Кнопка "Выход" позволяет выйти из программы
'''

testBytes = b'\xd0\x91\xd0\xb0\xd0\xb9\xd1\x82\xd1\x8b'
testIndexes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
testValues = [2, 0, 2, 5, 4, 3, 0, 2, 5, 4, 3]
testMin = 0
testMinIndex = 1

def count(numbers):
    n = len(numbers)
    return n

def binToHexConvert(bin):
    hex = bin
    return hex

def hexToDecConvert(hex):
    dec = hex
    return dec

def binToDecConvert(bin):
    dec = []
    for i in range(0, len(bin)):
        word = bin[i:i + 2]
        decword = int.from_bytes(word, byteorder='big')
        dec.append(decword)
    return dec


def detect_com_parameters(line):
    dash = line.find('-')
    com_line = line[0: dash]
    com_line = com_line.upper()
    com_speed = line[dash+1:]
    return com_line, com_speed


def open_com_port(com_number, com_speed):
    com = serial.Serial(com_number, com_speed)
    com.close()
    com.open()
    print(com_number + ' @ ' + com_speed + 'Открыт успешно. Запись начата')
    return com


def close_com_port(com_number):
    com = serial.Serial(com_number)
    com.close()
    print(com_number + ' Закрыт успешно. Запись остановлена')


def readraw(raw):
    print('Input size = ' + str(int(len(raw)/4)) + ' words \n')
    out = open('output.txt', 'w')
    outdec = open('output_decimal.txt', 'w')
    i = int(0)
    while i <= len(raw):
        word = raw[i:i+4]
        out.write(word + '\n')
        if word != '':
            decword = int(word, 16)
            decword = decword/8
            if  int(decword) > 8:
                outdec.write(str(decword) + '\n')
        i += 4
    outdec.write('\n')
    out.close()
    outdec.close()
    strings = int(len(raw)/4)
    return strings


class Files:
    def __init__(self, *args, **kwargs):
        self.rawString = ''


class Serial:
    def __init__(self, *args, **kwargs):
        self.rawConnectionString='COM4-38400-N-1'
        self.comNumber = '4'
        self.speed = '38400'
        self.parity = 'None'

class Calculations:
    def __init__(self, *args, **kwargs):
        print('Calc')

    def findMax(self, data, param):
        newMax = 0
        maxIndexes = []
        for i in range(0, len(data)):
            if data[i] > newMax:
                newMax = data[i]
        for i in range(0, len(data)):
            if data[i] == newMax:
                maxIndexes.append(i)
        if param == 'number':
            return newMax
        elif param == 'index':
            return maxIndexes[0]
        elif param == 'all_indexes':
            return maxIndexes
        else:
            return newMax, maxIndexes




class Data:
    def __init__(self, *args, **kwargs):
        self.rawString = ''
        self.binary = ''
        self.decimals = []
        self.heximals = []
        self.ammount = 0
        self.innocence = True

    def post(self):
        nextdec = 1
        while nextdec != '0':
            nextdec = int(input('Enter next Decimal = '))
            self.decimals.append(nextdec)

    def get(self):
        print(self.decimals)


class Plot:
    def __init__(self, *args, **kwargs):
        self.indexes = []
        self.dataValues = []
        self.averageValues = []
        self.maximumValue = ''
        self.maximumValueIndex = ''
        self.minimumValue = ''
        self.minimumValueIndex = ''


    def plot(self,indexes, dataValues, averageValues, maximumValue, maximumValueIndex, minimumValue, minimumValueIndex):
        plt.ylabel('Длина импульса, $\mu$сек')
        plt.xlabel('Отсчёты таймера')
        plt.grid(True)
        plt.plot(indexes, dataValues)
        plt.plot(maximumValueIndex, maximumValue, 'ro')
        plt.plot(minimumValueIndex, minimumValue, 'ro')
        plt.annotate('Минимальная длина импульса = ' + str(minimumValue) + ' $\mu$сек', xy=(minimumValueIndex, minimumValue))
        plt.annotate('Максимальная длина импульса = ' + str(maximumValue) + ' $\mu$сек', xy=(maximumValueIndex, maximumValue))
        plt.show()


class ReadingThread(QtCore.QThread):

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)

    def run(self):
        com_line = window.com_line.text()
        print(com_line)
        com, speed = detect_com_parameters(com_line)
        ser = open_com_port(com, speed)
        outdec = open('output_decimal.txt', 'w')
        raw_data = ''
        raw_data_file = open('temp_raw.txt', 'w')
        window.textBrowser.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Запись начата из порта ' + com + ' На скорости ' + speed)
        self.running = True
        while self.running:
            try:
                for i in range(0, 31536000):
                    if self.running is True:
                        word = ser.read(2)
                        window.lcdNumber.display(i)

                    else:

                        outdec.close()
                        window.textBrowser.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Запись остановлена')
                        raw_data_file.write(raw_data)
                        raw_data_file.close()
                        return

            except Exception as err:
                print(err)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.plot_button.clicked.connect(self.plotClicked)
        self.file_button.clicked.connect(self.openfileclicked)
        self.start_button.clicked.connect(self.startclicked)
        self.stop_button.clicked.connect(self.stopclicked)
        self.save_button.clicked.connect(self.savefileclicked)

        self.statusBar().showMessage('Ready')
        self.show()
        self.pause = False

    def showFileDialog(self):
        rawfilename = QFileDialog.getOpenFileName(self, 'Open File')[0]
        f = open(rawfilename, 'r')
        temp_raw_file = open('temp_raw.txt', 'w')
        raw = f.read()
        tempraw = f.read()
        self.textBrowser.append(str(rawfilename)+' Прочитан успешно')
        strings = readraw(raw)
        self.textBrowser.append(str(strings)+' Строк конвертировано')
        dec = open('output_decimal.txt')
        nextline = ''
        while nextline != '\n':
            nextline = dec.readline()
            if len(nextline) > 2:
                nextdec = float(nextline)
                decimals.append(nextdec)
        window.lcdNumber.display(strings)
        temp_raw_file.write(str(tempraw))
        temp_raw_file.close()


    def saveFileDialog(self):
        rawfilename = QFileDialog.getSaveFileName(self, 'Save')[0]
        f = open(rawfilename, 'w')
        df = open('temp_raw.txt', 'r')
        data = df.read()
        f.write(data)
        window.textBrowser.append('Сохранено в файл ' + str(rawfilename))
        df.close()
        f.close()


    def plotClicked(self):
        self.textBrowser.append('Построение графика')
        calc = Calculations()
        plot = Plot()
        plot.plot(testIndexes, testValues, testValues, calc.findMax(testValues, 'number'), calc.findMax(testValues, 'index'), testMin, testMinIndex)
        self.textBrowser.append('Окно графика закрыто')

    def openfileclicked(self):
        try:
            self.showFileDialog()
        except:
            pass

    def savefileclicked(self):
        try:
            self.saveFileDialog()
        except:
            pass

    def startclicked(self):
        try:
            self.thread1 = ReadingThread()
            self.thread1.start()
        except:
            pass

    def stopclicked(self):
        try:
            self.thread1.running = False
        except:
            pass


# Основная функция
if __name__ == '__main__':
    app = QApplication([])
    app.setApplicationName("LineBreaker 0.90")
    window = MainWindow()
    window.label.setFont(QtGui.QFont('Calibri', 9))
    window.label.setText(text1)
    window.quit_button.clicked.connect(QCoreApplication.instance().quit)
    app.exec_()
