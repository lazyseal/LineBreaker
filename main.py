import sys, time, serial, datetime
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QMainWindow, QLCDNumber, QFileDialog, QTextEdit, QGridLayout
from PyQt5.QtCore import QCoreApplication

from grid3 import Ui_MainWindow

text1 = '''
Версия 0.80
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
strings = 0
decimals = []



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
                        decword = int.from_bytes(word, byteorder='big')
                        hexword = str(hex(decword))
                        hexword = hexword[2:].upper()
                        print(hexword)
                        raw_data += hexword
                        decword = float(decword)
                        if int(decword) > 8:
                            decimals.append(decword/8)
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

        self.plot_button.clicked.connect(self.runclicked)
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




    def runclicked(self):
        self.textBrowser.append('Построение графика')
        plot(decimals)
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




    def read_com_port_parameters(self):
        com_number = 'COM4'
        com_speed = '9600'
        return com_number, com_speed




#Функции вычисления минимума, максимума, отклонения
def maxdeviation(data, value, n):
    maximum = data[0]
    minimum = data[0]
    for i in range(0, n):
        if data[i] > maximum:
            maximum = data[i]
        if data[i] < minimum:
            minimum = data[i]
    if (maximum - value) > (value - minimum):
        return maximum - value
    else:
        return -(value - minimum)


def plotmax(data, n):
    maximum = data[0]
    minimum = data[0]
    maxi = 0
    for i in range(0, n):
        if data[i] > maximum:
            maximum = data[i]
            maxi = i
        if data[i] < minimum:
            minimum = data[i]
            mini = i

    window.textBrowser.append('Максимальная длина импульса = ' + str(maximum) + ' мксек')
    return maximum, maxi


def plotmin(data, n):
    minimum = data[64]
    mini = 64
    for i in range(64, n):
        if data[i] < minimum:
            minimum = data[i]
            mini = i
    window.textBrowser.append('Минимальная длина импульса = ' + str(minimum) + ' мксек')
    return mini, minimum


# Функция построения чертежа

def plot(decimals):
    axisx = []
    values = []
    approximateValues = []
 #   approximateValues[1] = values[1]
 #   approximateValues[-1] = values[-1]
    medium = 0
    statistic = 0
    i = int(1)
    for i in range (0, len(decimals)):
        print(i)
        values.append(decimals[i])
        axisx.append(i)
 #       if i > 1 and i < len(decimals):
 #           approxi = (decimals[i-1] + decimals[i+1]) /2
 #           approximateValues.append(approxi)

#    ApproxValue = float(decimals[0])
    maximum, maxi = plotmax(values, i)
    mini, minimum = plotmin(values, i)
#    plt.annotate(
#        'Среднее значение = ' + str('%.2f' % float(medium / i)) + ' $\mu$сек, \nМаксимальное отклонение = ' + str(
#            '%.2f' % maxdeviation(values, medium / i, i)) + ' $\mu$сек', xy=(0, ApproxValue))
    plt.ylabel('Длина импульса, $\mu$сек')
    plt.xlabel('Отсчёты таймера')
    plt.grid(True)
    plt.plot(axisx, values)
 #   plt.plot(axisx, approximateValues)
    plt.plot(maxi, maximum, 'ro')
    plt.plot(mini, minimum, 'ro')
    plt.annotate('Минимальная длина импульса = ' + str(minimum) + ' $\mu$сек', xy=(mini, (minimum)))
    plt.annotate('Максимальная длина импульса = ' + str(maximum) + ' $\mu$сек', xy=(maxi, (maximum)))
    plt.show()




# Основная функция
if __name__ == '__main__':
    app = QApplication([])
    app.setApplicationName("LineBreaker 0.80")
    window = MainWindow()
    window.label.setFont(QtGui.QFont('Calibri', 9))
    window.label.setText(text1)
    window.quit_button.clicked.connect(QCoreApplication.instance().quit)

    app.exec_()
