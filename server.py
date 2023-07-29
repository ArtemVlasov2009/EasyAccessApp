import os # Взаємодія з операційною та файловою системою. Приклади застосування: запуск, створення файлів, отримання шляхів системи.
import sys # цей модуль надає доступ до деяких змінних, будемо застосовувати для роботи з додатком
import time # повертає час в секундах з початку епохи як число з плаваючею точкою
import json # робота з файлами де зберігаються дані (числа, строки (рядки), списки...) і обмін цими даними
import socket # використовуються для надсилання повідомлень через мережу. Модуль забезпечуює форму міжпроцесного зв'язку.
import base64 # кодує двійкові дані у друковані символи ASCII та декодує такі кодування назад у двійкові дані
import glob # Повертає список імен шляхів, які знаходяться в каталозі pythname
# import PIL
import pygame
pygame.init()
import pyautogui # імітація дій користувача

from PyQt5 import (
        QtCore, # Дозволяє зареєструвати тип події. Метод повертає ідентифікатор зареєстрованої події.
        QtGui, # Компоненти графічного інтерфейсу (елементу управління), що грунтуються на візуальном поданні.                          
        QtWidgets # Модуль з бібліотеки "QT" з набором графічних "віджетів" (компонентів користувацького інтерфейсу) для створення додатків із графічним інтерфейсом.
    )
# from PyQt5.QtWidgets import QApplication
from des import * # Використовується для шифрування даних

# Створюємо клас(інструкцію) My_Thread
class My_Thread(QtCore.QThread):
    my_signal = QtCore.pyqtSignal(list)# Змінна що зберігає список сигналів
    # Створюємо метод конструктор, щоб описати характеристики класу
    def __init__(self, ip = None, port = None, parent = None):
        QtCore.QThread.__init__(self, parent) # сповіщаємо батьківському класу QtThread, про наявність точного такого параметра у класа нащадка
        #
        self.IP = ip # особиста адреса пристрою в інтернеті
        self.PORT = port # номер (ключ) по якому можна підключитись до серверу 
        self.ACTIVE_SOCKET = None # 
        self.COMMAND = "screen" # 
        #
        self.SERVER = socket.socket(
            socket.AF_INET, # застосовується для використання мережевих протоколів IPV-4
            socket.SOCK_STREAM # константа яка забезпечує стабільний зв'язок між сервером та клієнтом
        ) 
        self.SERVER.setsockopt(
            socket.SOL_SOCKET, # повертає значення, яке вказує, чи знаходиться сокет у режимі прослуховування 
            socket.SO_REUSEADDR, # допомагає функції bind здійснити підключення до IP та Port повторно 
            1
        ) #
        self.SERVER.bind((self.IP, self.PORT)) #
        self.SERVER.listen(0) # 
        
    # Метод, що приймає та обробляє дані
    def run(self):
        # Приймаємо вхідне з'єднання
        self.DATA_CONNECTION, ADDRESS = self.SERVER.accept()
        self.ACTIVE_SOCKET = self.DATA_CONNECTION
        #
        while True:
            self.send_json(self.COMMAND.split(' '))
            response = self.receive_json()
            self.my_signal.emit([response])
            if self.COMMAND.split(" ")[0] != "screen":
                # self.send_json(self.COMMAND.split(' '))
                # response = self.receive_json()
                # self.my_signal.emit([response])
                self.COMMAND = 'screen'
            # if self.COMMAND.split(' ')[0] == 'screen':
                # self.send_json(self.COMMAND.split(' '))
                # response = self.receive_json()
                # self.my_signal.emit([response])

    # Відправка даних клієнту
    def send_json(self, data):
        # обробляємо бінарні дані, з 0 та 1 переводимо до символьної строки
        try:
            json_data = json.dumps(data.decode("utf-8"))
        except:
            json_data = json.dumps(data)
        # у випадку, якщо клієнт розірве з'єднання, але сервер все ще відправляє команди
        try:
            self.ACTIVE_SOCKET.send(json_data.encode('utf-8'))
        except ConnectionResetError:
            # переводимо ACTIVE_SOCKET в початковий стан, з'єднання розірвано
            self.ACTIVE_SOCKET = None    
    
    # отримуємо дані від користувача та зберігаємо їх у json файлах
    def receive_json(self):
        json_data = ""
        while True:
            try:
                # якщо є з'єднання з клієнтом
                if self.ACTIVE_SOCKET != None:
                    # Отримувати дані від кліента та декодувати їх зберігаючи у json файлі
                    json_data += self.ACTIVE_SOCKET.recv(1024).decode('utf-8')
                    # json_data = json_data + self.ACTIVE_SOCKET.recv(1024).decode('utf-8')
                    return json.loads(json_data)
            except ValueError:
                pass   
#
class VNC_Server:
    def __init__(self, ip = None, port = None):
        # Вказуються висота та ширина вікна та зображення.
        self.WIN_WIDTH, self.WIN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.FILE_IMAGE = "2.png"
        self.TEXT_EXСEPT = ""

        # створюємо додаток my_app
        self.MY_APP = QtWidgets.QApplication(sys.argv)
        # створюємо вікно додатку
        self.APP_WINDOW = QtWidgets.QWidget()
        # задаємо розміри  вікна додатку
        self.APP_WINDOW.setFixedSize(self.WIN_WIDTH, self.WIN_HEIGHT)
        # Відповідає за створення об'єкта (текст) який буде відображений на екрані в додатку 
        self.TEXT = QtWidgets.QLabel(self.TEXT_EXСEPT)
        # Створюємо об'єкт вертикального layout, на якому будемо розміщувати текст
        self.VERTICAL_LAYOUT = QtWidgets.QVBoxLayout()
        # додаемо текст до вертекального лейауту
        self.VERTICAL_LAYOUT.addWidget(self.TEXT)
        # встановлюємо вертикальний layout до вікна додатку
        self.APP_WINDOW.setLayout(self.VERTICAL_LAYOUT)
        # Задаємо ім'я додатку 
        self.APP_WINDOW.setWindowTitle("Вікно додатка")

        self.IP = "localhost"
        self.PORT = 4445
        self.THREAD_HANDLER = My_Thread(self.IP, self.PORT)
        self.THREAD_HANDLER.start()

        self.THREAD_HANDLER.my_signal.connect(self.screen_handler) # 

        # self.show_image_in_window()
    #
    def show_image_in_window(self):
        # Завантажуємо зображення з папки до програми
        try:
            file_image = pygame.image.load(self.FILE_IMAGE)
            # Змінюємо розміри зображення
            file_image = pygame.transform.scale(file_image, (self.WIN_WIDTH, self.WIN_HEIGHT))
            # зберігаємо редаговане зображення в папці проекту
            pygame.image.save(file_image, "2.png")
        except:
            self.TEXT_EXСEPT = "image doesnt exist"
            self.TEXT.setText(self.TEXT_EXСEPT)
            self.TEXT.setStyleSheet(
                '''
                    font-size: 100px;
                    qproperty-alignment: "AlignCenter";
                    color: red;
                '''
            )
        self.APP_WINDOW.setStyleSheet(
            f'''
                background-color: rgb(80,80,80);
                background-image: url({self.FILE_IMAGE});
                background-repeat: no-repeat;
            ''' 
        )
    # Обробка івентів
    def events(self, event):
        # Обробка лкм та пкм
        if event.type() == QtCore.QEvent.MouseButtonPress:
            current_button = event.button() # З'ясовуємо нажату кнопку миші
            if current_button == 1: 
                self.THREAD_HANDLER.COMMAND = f"mouse_left_click {event.x()} {event.y()}"
            elif current_button == 2:
                self.THREAD_HANDLER.COMMAND = f"mouse_right_click {event.x()} {event.y()}"
        # Обробка double-кліка
        elif event.type() == QtCore.QEvent.MouseButtonDblClick:
            self.THREAD_HANDLER.COMMAND = f"mouse_double_left_click {event.x()} {event.y()}"
        return QtWidgets.QWidget.event(self, event)
    
    #
    def screen_handler(self, screen_value):
        data = ["mouse_left_click", "mouse_right_click", "mouse_double_left_click"]
        # Якщо було отримано не скрін екрану
        if screen_value[0] not in data:
            decrypt_image = base64.b64decode(screen_value[0])
            with open('2.png', 'wb') as file:
                file.write(decrypt_image)
            #
        self.show_image_in_window()

# умова __name__  == '__main__' виконує код що написаний нижче тільки в модулі server.py
if __name__  == '__main__':
    
    vnc_server = VNC_Server()
    # Відображає вікно додатка
    vnc_server.APP_WINDOW.show()
    # Робе так щоб вікно не закривалось вікно додатку
    vnc_server.MY_APP.exec_()
    

    
