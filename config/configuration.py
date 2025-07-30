from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QColor, QFont
from utils.key_utils import KeyUtils
import json


class Configuration:
    def __init__(self):
        # styles
        self.__bgColor = QColor(255, 255, 255)
        self.__fontColor = QColor(0, 0, 0)
        self.__font = QFont('Arial')
        self.__fontSize = 12
        # reader_configs
        self.__windowPos = QPoint(400, 400)
        self.__windowWidth = 400
        self.__scroll_forward_speed = 10
        self.__scroll_backward_speed = 5
        self.__last_opened_file = ""
        self.__scroll_to_new_disable_gap = 500
        self.__scroll_after_new_disable_gap = 500
        # keys
        self.__previous_line_key = Qt.Key.Key_Up
        self.__next_line_key = Qt.Key.Key_Down
        self.__move_backward_key = Qt.Key.Key_Left
        self.__move_forward_key = Qt.Key.Key_Right

        self.load_config()

    def load_config(self):
        try:
            with open('config.json', 'r') as f:
                configs = json.load(f)
                self.load_styles(configs)
                self.load_reader_configs(configs)
                self.load_short_cut_keys(configs)

        except FileNotFoundError:
            print('未找到配置文件')

    def load_styles(self, configs):
        self.__bgColor = QColor(configs.get('bgColor', '#FFFFFF'))
        self.__fontColor = QColor(configs.get('fontColor', '#000000'))
        self.__font = QFont(configs.get('font', 'Arial'))
        self.__fontSize = configs.get('fontSize', 12)

    def load_reader_configs(self, configs):
        window_pos_x = configs.get('windowPosX', 400)
        window_pos_y = configs.get('windowPosY', 400)
        self.__windowPos = QPoint(window_pos_x, window_pos_y)
        self.__windowWidth = configs.get('windowWidth', 400)
        self.__scroll_forward_speed = configs.get('scrollForwardSpeed', 10)
        self.__scroll_backward_speed = configs.get('scrollBackwardSpeed', 5)
        self.__last_opened_file = configs.get('lastOpenedFile', '')
        self.__scroll_to_new_disable_gap = configs.get('scrollToNewDisableGap', 500)
        self.__scroll_after_new_disable_gap = configs.get('scrollAfterNewDisableGap', 500)

    def load_short_cut_keys(self, configs):
        self.__previous_line_key = KeyUtils.get_key_enum(configs.get('previousLineKey', 'Up'))
        self.__next_line_key = KeyUtils.get_key_enum(configs.get('nextLineKey', 'Down'))
        self.__move_backward_key = KeyUtils.get_key_enum(configs.get('moveBackwardKey', 'Left'))
        self.__move_forward_key = KeyUtils.get_key_enum(configs.get('moveForwardKey', 'Right'))

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
            'scrollBackwardSpeed': self.__scroll_backward_speed,
            'lastOpenedFile': self.__last_opened_file,
            'scrollToNewDisableGap': self.__scroll_to_new_disable_gap,
            'scrollAfterNewDisableGap': self.__scroll_after_new_disable_gap,

            'previousLineKey': KeyUtils.get_key_description(self.__previous_line_key),
            'nextLineKey': KeyUtils.get_key_description(self.__next_line_key),
            'moveBackwardKey': KeyUtils.get_key_description(self.__move_backward_key),
            'moveForwardKey': KeyUtils.get_key_description(self.__move_forward_key)
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

    def get_last_opened_file(self):
        return self.__last_opened_file

    def set_last_opened_file(self, file_path):
        self.__last_opened_file = file_path

    def get_scroll_to_new_disable_gap(self):
        return self.__scroll_to_new_disable_gap

    def set_scroll_to_new_disable_gap(self, gap):
        self.__scroll_to_new_disable_gap = gap

    def get_scroll_after_new_disable_gap(self):
        return self.__scroll_after_new_disable_gap

    def set_scroll_after_new_disable_gap(self, gap):
        self.__scroll_after_new_disable_gap = gap

    def get_previous_line_key(self):
        return self.__previous_line_key

    def get_next_line_key(self):
        return self.__next_line_key

    def get_move_backward_key(self):
        return self.__move_backward_key

    def get_move_forward_key(self):
        return self.__move_forward_key

    def set_previous_line_key(self, key):
        self.__previous_line_key = key

    def set_next_line_key(self, key):
        self.__next_line_key = key

    def set_move_backward_key(self, key):
        self.__move_backward_key = key

    def set_move_forward_key(self, key):
        self.__move_forward_key = key


config = Configuration()
