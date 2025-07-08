from PySide6.QtCore import QPoint
from PySide6.QtGui import QColor, QFont
import json


class Configuration:
    def __init__(self):
        self.__bgColor = QColor(255, 255, 255)
        self.__fontColor = QColor(0, 0, 0)
        self.__font = QFont('Arial')
        self.__fontSize = 12
        self.__windowPos = QPoint(400, 400)
        self.__windowWidth = 400
        self.__scroll_forward_speed = 10
        self.__scroll_backward_speed = 5

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
                self.__windowWidth = configs.get('windowWidth', 400)
                self.__scroll_forward_speed = configs.get('scrollForwardSpeed', 10)
                self.__scroll_backward_speed = configs.get('scrollBackwardSpeed', 5)

        except FileNotFoundError:
            print('未找到配置文件')

    def save_config(self):
        configs = {
            'bgColor': self.__bgColor.name(),
            'fontColor': self.__fontColor.name(),
            'font': self.__font.family(),
            'fontSize': self.__fontSize,
            'windowPosX': self.__windowPos.x(),
            'windowPosY': self.__windowPos.y(),
            'windowWidth': self.__windowWidth,
            'scrollForwardSpeed': self.__scroll_forward_speed,
            'scrollBackwardSpeed': self.__scroll_backward_speed
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

    def set_window_width(self, width):
        self.__windowWidth = width

    def get_window_width(self):
        return self.__windowWidth

    def get_scroll_forward_speed(self):
        return self.__scroll_forward_speed

    def get_scroll_backward_speed(self):
        return self.__scroll_backward_speed

    def set_scroll_forward_speed(self, speed):
        self.__scroll_forward_speed = speed

    def set_scroll_backward_speed(self, speed):
        self.__scroll_backward_speed = speed


config = Configuration()
