from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QColor, QFont
import json


class Configuration:
    def __init__(self):
        self.__bgColor = QColor(255, 255, 255)
        self.__fontColor = QColor(0, 0, 0)
        self.__font = QFont('Arial')
        self.__fontSize = 12
        self.__windowPos = QPoint(400, 400)

        self.load_config()

    def load_config(self):
        try:
            with open('config.json', 'r') as f:
                configs = json.load(f)
                self.__bgColor = QColor(configs.get('bgColor', '#FFFFFF'))
                self.__fontColor = QColor(configs.get('fontColor', '#000000'))
                self.__font = QFont(configs.get('font', 'Arial'))
                self.__fontSize = configs.get('fontSize', 12)
                window_pos_x = configs.get('windowPosX', 400)
                window_pos_y = configs.get('windowPosY', 400)
                self.__windowPos = QPoint(window_pos_x, window_pos_y)
        except FileNotFoundError:
            print('未找到配置文件')


    def save_config(self):
        configs = {
            'bgColor': self.__bgColor.name(),
            'fontColor': self.__fontColor.name(),
            'font': self.__font.family(),
            'fontSize': self.__fontSize,
            'windowPosX': self.__windowPos.x(),
            'windowPosY': self.__windowPos.y()
        }

        with open('config.json', 'w') as f:
            json.dump(configs, f, indent=4)

    def get_bg_color(self):
        return self.__bgColor

    def get_font_color(self):
        return self.__fontColor

    def get_font(self):
        return self.__font

    def get_font_size(self):
        return self.__fontSize

    def get_window_pos(self):
        return self.__windowPos

    def set_bg_color(self, color):
        self.__bgColor = color

    def set_font_color(self, color):
        self.__fontColor = color

    def set_font(self, font):
        self.__font = font

    def set_font_size(self, size):
        self.__fontSize = size

    def set_window_pos(self, pos):
        self.__windowPos = pos


config = Configuration()
