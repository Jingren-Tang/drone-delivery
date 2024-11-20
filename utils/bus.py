# 巴士站类，记录位置
import numpy as np
from scipy.spatial.distance import cdist
from collections import deque
class BusStation:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Bus:
    def __init__(self, bus_id, route, start_station_index, direction=1, speed=5, stop_time=10):
        """
        Initializes a bus with specified attributes.
        - bus_id: Unique identifier for the bus
        - route: List of stations along the bus route
        - start_station_index: Index of the starting station
        - direction: Travel direction (1 for forward, -1 for reverse)
        - speed: Distance moved per unit time
        - stop_time: Time to wait at each station
        """
        self.bus_id = bus_id
        self.route = route
        self.station_index = start_station_index
        self.direction = direction
        
        # Initialize position using x and y attributes
        self.x = self.route[self.station_index]['x']
        self.y = self.route[self.station_index]['y']
        
        self.speed = speed  # Distance moved per unit time
        self.time_at_station = 0  # Time spent at station
        self.stop_time = stop_time  # Time to stop at each station
        self.status = 'moving'  # Bus status (moving, at_station, etc.)




    def move(self):
        """Defines the movement logic of the bus."""
        # if self.status == 'at_station':
        #     # Bus is waiting at the station
        #     self.time_at_station += 1
        #     if self.time_at_station >= self.stop_time:
        #         # Time to leave the station
        #         self.status = 'moving'
        #         self.time_at_station = 0
        # else:  # status is 'moving'
        #     # Bus is moving towards the next station
        #     next_station_index = self.station_index + self.direction
        #     if 0 <= next_station_index < len(self.route):
        #         next_station = self.route[next_station_index]
        #         # Calculate the Euclidean distance to the next station
        #         distance_to_next_station = math.sqrt(
        #             (self.x - next_station['x']) ** 2 + (self.y - next_station['y']) ** 2
        #         )

        #         # Check if bus has reached the next station
        #         if distance_to_next_station <= self.speed:
        #             self.x = next_station['x']
        #             self.y = next_station['y']
        #             self.station_index += self.direction
        #             self.status = 'at_station'
        #             # Reverse direction if at route endpoints
        #             if self.station_index == 0 or self.station_index == len(self.route) - 1:
        #                 self.direction *= -1
        #         else:
        #             # Move towards the target proportionally to avoid overshooting
        #             move_ratio = self.speed / distance_to_next_station
        #             self.x += move_ratio * (next_station['x'] - self.x)
        #             self.y += move_ratio * (next_station['y'] - self.y)
        if self.status == 'at_station':
            # Bus is waiting at the station
            self.time_at_station += 1
            if self.time_at_station >= self.stop_time:
                # Time to leave the station
                self.status = 'moving'
                self.time_at_station = 0
        else:  # status is 'moving'
            next_station_index = self.station_index + self.direction
            if 0 <= next_station_index < len(self.route):
                next_station = self.route[next_station_index]
                distance_to_next_station = math.sqrt(
                    (self.x - next_station['x']) ** 2 + (self.y - next_station['y']) ** 2
                )

                if distance_to_next_station <= self.speed:
                    self.x = next_station['x']
                    self.y = next_station['y']
                    self.station_index += self.direction
                    self.status = 'at_station'

                    # **Only reverse direction if at endpoints**
                    if self.station_index == 0:
                        self.direction = 1
                    elif self.station_index == len(self.route) - 1:
                        self.direction = -1
                else:
                    move_ratio = self.speed / distance_to_next_station
                    self.x += move_ratio * (next_station['x'] - self.x)
                    self.y += move_ratio * (next_station['y'] - self.y)




    # def is_going_to(self, target_x, target_y):
    #     """
    #     检查公交车是否能够按照当前行驶方向到达指定目标站点。直接用遍历的方法
    #     - target_x, target_y: 目标站点的坐标
    #     返回值:
    #     - 如果公交车可以在当前方向上到达目标站点，返回 True；否则返回 False。
    #     """
    #     try:
    #         # 获取目标站点在路线中的索引
    #         target_station_index = next(
    #             i for i, station in enumerate(self.route)
    #             if station['x'] == target_x and station['y'] == target_y
    #         )
    #         # 判断当前方向是否可以到达目标站点
    #         if (self.direction == 1 and target_station_index > self.station_index) or \
    #            (self.direction == -1 and target_station_index < self.station_index):
    #             return True  # 当前方向可以到达目标站点
    #         return False  # 当前方向无法到达目标站点
    #     except StopIteration:
    #         # 如果目标站点不在公交车的路线中，返回 False
    #         return False
