import os
import socket
import time
import base64
import pyautogui
import json
from PIL import ImageGrab
import pygame

pygame.init()

class VNC_Client:
    #
    def __init__(self, ip, port):
        
        self.CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        while True:
            try:
                self.CLIENT.connect((ip, port))
                break
            except:
                time.sleep(5)
                
    # Задаємо напрямок миші по координатам
    def mouse_active(self, mouse_flag, x, y):
        if mouse_flag == "mouse_right_click":
            pyautogui.rightClick(int(x), int(y))
            return "mouse_right_click"
        elif mouse_flag == "mouse_left_click":
            pyautogui.leftClick(int(x), int(y))
            return "mouse_left_click"
        elif mouse_flag == "mouse_double_left_click":
            pyautogui.doubleClick(int(x), int(y))
            return "mouse_double_left_click"
        
    # задаємо метод обробки зображення з екрану
    def screen_handler(self):
        # win = pygame.display.get_desktop_sizes()
        # a = (0, 0, win[0][0], win[0][1])
        screenshot = ImageGrab.grab(all_screens= True)
        screenshot.save('1.png')
        with open("1.png", "rb") as file:
            data = base64.b64encode(file.read())
        os.remove("1.png")
        return data
    
    # Відправка json даних на сервер
    def send_json(self, data):
        try:
            json_data = json.dumps(data.decode("utf-8"))
        except:
            json_data = json.dumps(data)
        self.CLIENT.send(json_data.encode('utf-8'))

    # Отримуємо дані від сервера
    def receive_json(self):
        json_data = ""
        while True:
            try:
                json_data += self.CLIENT.recv(1024).decode("utf-8")
                return json.loads(json_data)
            except ValueError:
                pass
    # Обробка всіх вхідних команд
    def execute_handler(self):
        while True:
            # response - відповідь 
            response = self.receive_json()
            if response[0] == "screen": # response = "screen"
                result = self.screen_handler()
            elif "mouse" in response[0]:
                result = self.mouse_active(response[0], response[1], response[2]) # response = "mouse_right_click 12 15"
            self.send_json(result)
        
my_client = VNC_Client(ip = "localhost", port = 4445)
my_client.execute_handler()           

# my_client.screen_handler()