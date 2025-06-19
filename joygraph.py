import pygame
import matplotlib.pyplot as plt
from typing import List

class Joystick:
    def __init__(self, index: int):
        self.index = index
        self.joystick = pygame.joystick.Joystick(index)
        self.joystick.init()

    def get_joystick_index(self) -> int:
        return self.index
    
    def get_axis(self, axis_index: int) -> float:
        return self.joystick.get_axis(axis_index)
    
    def get_button(self, button_index: int) -> int:
        return self.joystick.get_button(button_index)
    
    def get_name(self) -> str:
        return self.joystick.get_name()
    
    def get_index(self) -> int:
        return self.index
    
class Graph:

    def __init__(self, labels: List[str], min_raw_value: float = -1.0, max_raw_value: float = 1.0, factor: float = 1.0, yLabel: str = "", graph_name: str = ""):
        plt.ion()
        self.fig, self.ax = plt.subplots()
        self.labels = labels
        self.label_number = len(self.labels)
        self.bar_container = self.ax.bar(self.labels, [0, 0, 0, 0])

        x = list(range(self.label_number))

        self.bars_real = []
        self.bars_target = []

        for i in x:
            real = self.ax.bar(i - 0.15, 0, width=0.3, color='deepskyblue', label='Current' if i == 0 else "")
            target = self.ax.bar(i + 0.15, 0, width=0.3, color='red', label='Target' if i == 0 else "")
            self.bars_real.append(real[0])
            self.bars_target.append(target[0])

        self.ax.set_xticks(x)
        self.ax.set_xticklabels(self.labels, color='black')

        min_value = min_raw_value * factor
        max_value = max_raw_value * factor
        self.ax.set_ylim(min_value, max_value)

        self.ax.set_ylabel(yLabel)
        self.ax.set_title(graph_name)

    def update_chart(self, real_values: List[float], target_values: List[float]):
        for bar, val in zip(self.bars_real, real_values):
            bar.set_height(val)
        for bar, val in zip(self.bars_target, target_values):
            bar.set_height(val)

        plt.pause(0.01) 


class JoyGraph:
    
    def __init__(self):
        pygame.init()
        pygame.joystick.init()

        if self.joystick_count() == 0:
            print('No joystick plugged. Quitting program...')
            exit()


    def joystick_count(self) -> int:
        return pygame.joystick.get_count()
    
    def create_joystick(self, joystick_index: int) -> Joystick:
        return Joystick(joystick_index)
    
    def create_graph(self, labels: List[str], min_raw_value: float = -1.0, max_raw_value: float = 1.0, factor: float = 1.0, yLabel: str = "", graph_name: str = "") -> Graph:
        return Graph(labels,
                    min_raw_value=min_raw_value,
                    max_raw_value=max_raw_value,
                    factor=factor,
                    yLabel=yLabel,
                    graph_name=graph_name
                    )


    
    

