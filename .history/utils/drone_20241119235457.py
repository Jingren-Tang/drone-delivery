import numpy as np
from scipy.spatial.distance import cdist
from collections import deque

# 无人机类，负责区域内的取货和将物品送至巴士站
class Drone:
    def __init__(self, drone_id, region, x, y, speed = 5):
        self.drone_id = drone_id
        self.region = region  # 无人机负责的区域编号
        self.x = x
        self.y = y
        self.status = 'idle'  # 初始状态为空闲
        self.current_task = None  # 当前任务
        self.target_x = None
        self.target_y = None
        self.time_until_idle = 0  # 剩余时间
        self.delivery_tasks_completed = 0  # 统计无人机完成的送货任务数
        self.pickup_tasks_completed = 0  # 统计无人机完成的取货任务数
        self.bus_id = None  # 记录携带任务包裹的巴士ID
        self.speed = speed


    def assign_pickup_task(self, task, target_x, target_y):
        """分配取货任务，并设置目标位置"""
        self.current_task = task
        self.status = 'moving_to_pickup'  # 状态设置为前往取货点
        self.target_x = target_x
        self.target_y = target_y
        # 计算欧拉距离并考虑速度，向上取整移动所需的时间
        distance_to_target = np.sqrt((self.target_x - self.x)**2 + (self.target_y - self.y)**2)
        self.time_until_idle = int(np.ceil(distance_to_target / self.speed))  # 向上取整后的移动时间

    def assign_delivery_task(self, task, target_x, target_y):
        """分配送货任务，设置目标位置为离送货点最近的巴士站"""
        self.current_task = task
        self.status = 'moving_to_bus_station_for_delivery'  # 状态设置为前往送货巴士站
        self.target_x = target_x
        self.target_y = target_y
        # 计算欧拉距离并考虑速度，向上取整移动所需的时间
        distance_to_target = np.sqrt((self.target_x - self.x)**2 + (self.target_y - self.y)**2)
        self.time_until_idle = int(np.ceil(distance_to_target / self.speed))  # 向上取整后的移动时间


    def move(self):
        """Drone's movement logic to fly directly towards the target using Euclidean distance."""
        if self.status == 'idle' or self.time_until_idle <= 0:
            return

        # Calculate Euclidean distance to target
        distance_to_target = np.sqrt((self.target_x - self.x)**2 + (self.target_y - self.y)**2)
        
        if distance_to_target <= self.speed:
            # Move directly to target if within one speed unit
            self.x = self.target_x
            self.y = self.target_y
        else:
            # Move proportionally towards the target based on speed
            move_ratio = self.speed / distance_to_target
            self.x += move_ratio * (self.target_x - self.x)
            self.y += move_ratio * (self.target_y - self.y)

        # Decrement time_until_idle each move
        self.time_until_idle = max(self.time_until_idle - 1, 0)

        # Check if drone has arrived at target
        if self.x == self.target_x and self.y == self.target_y:

            if self.status == 'moving_to_pickup':
                # Check if the pickup point is at a bus station
                nearest_bus_station = find_nearest_bus_station(self.current_task['pickup_x'], self.current_task['pickup_y'], bus_stations)
                if (self.current_task['pickup_x'] == nearest_bus_station.x and 
                    self.current_task['pickup_y'] == nearest_bus_station.y):
                    # If pickup point is at the bus station, go directly to waiting for bus
                    self.status = 'waiting_at_bus_station_for_pickup_bus'
                    self.current_task['pickup_status'] = 'waiting_for_bus'
                    # print(f"Drone {self.drone_id} is now waiting at the bus station ({self.x}, {self.y}) for the pickup bus.")
                else:
                    # Move to nearest bus station after pickup
                    self.status = 'moving_to_bus_station_finish_pickup'
                    self.target_x, self.target_y = nearest_bus_station.x, nearest_bus_station.y
                    distance_to_target = np.sqrt((self.target_x - self.x)**2 + (self.target_y - self.y)**2)
                    self.time_until_idle = int(np.ceil(distance_to_target / self.speed))
                    # print(f"Drone {self.drone_id} has picked up the package and is heading to the bus station ({self.target_x}, {self.target_y}).")

            elif self.status == 'moving_to_bus_station_finish_pickup':
                # Arrived at bus station after pickup, set status to waiting
                self.status = 'waiting_at_bus_station_for_pickup_bus'
                self.current_task['pickup_status'] = 'waiting_for_bus'
                print(f"Drone {self.drone_id} is now waiting at the bus station ({self.x}, {self.y}) for the pickup bus.")

            elif self.status == 'moving_to_bus_station_for_delivery':
                # Check if the delivery point is at a bus station
                nearest_bus_station = find_nearest_bus_station(self.current_task['delivery_x'], self.current_task['delivery_y'], bus_stations)
                if (self.current_task['delivery_x'] == nearest_bus_station.x and 
                    self.current_task['delivery_y'] == nearest_bus_station.y):
                    # If delivery point is at the bus station, go directly to idle
                    self.status = 'idle'
                    self.delivery_tasks_completed += 1
                    self.current_task['delivery_status'] = 'completed'
                    # print(f"Drone {self.drone_id} has delivered the package to the bus station at the delivery location and is now idle.")
                    self.current_task = None
                    self.target_x = None
                    self.target_y = None
                else:
                    # Reached delivery bus station, set waiting status
                    self.current_task['delivery_status'] = 'waiting_for_bus'
                    self.status = 'waiting_at_bus_station_for_delivery'
                    # print(f"Drone {self.drone_id} is now waiting at the bus station ({self.x}, {self.y}) for the delivery.")

            elif self.status == 'waiting_at_bus_station_for_pickup_bus':
                # Waiting at bus station for package arrival
                pass

            elif self.status == 'waiting_at_bus_station_for_delivery':
                # Waiting at bus station for package arrival
                pass

            elif self.status == 'moving_to_delivery':
                # Reached final destination
                self.status = 'idle'
                self.delivery_tasks_completed += 1
                self.current_task['delivery_status'] = 'completed'
                print(f"Drone {self.drone_id} has delivered the package to the final destination.")
                self.current_task = None
                self.target_x = None
                self.target_y = None
