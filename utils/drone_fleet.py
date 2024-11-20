import drone
import numpy as np
from scipy.spatial.distance import cdist
from collections import deque


class DroneFleet:
    def __init__(self, initial_drone_count=1):
        self.drones = [Drone(i, 'pickup', 35, 35) for i in range(initial_drone_count)]
        self.drone_count = initial_drone_count
        self.pickup_task_queue = deque()
        self.delivery_task_queue = deque()

    def get_idle_drone(self, target_x, target_y):
        """查找距离目标位置最近的空闲无人机"""
        nearest_drone = None
        min_distance = float('inf')
        
        for drone in self.drones:
            if drone.status == 'idle':
                distance = self.calculate_distance(drone, target_x, target_y)
                if distance < min_distance:
                    min_distance = distance
                    nearest_drone = drone

        return nearest_drone

    def create_new_drone(self):
        """创建一个新的无人机并返回它"""
        new_drone = Drone(self.drone_count, 'pickup', 35, 35)  # 假设新无人机从(35,35)出发
        self.drones.append(new_drone)
        self.drone_count += 1
        print(f"Created new drone with ID {new_drone.drone_id}.")
        return new_drone

    def ensure_delivery_drone_availability(self, task, target_x, target_y):
        """
        如果没有空闲的无人机可用，创建一个新的无人机来处理任务。
        """
        # 创建一个新的无人机
        new_drone = self.create_new_drone()
        # 找到最近的巴士站，并分配送货任务
        nearest_station = self.find_nearest_bus_station(target_x, target_y)
        new_drone.assign_delivery_task(task, nearest_station.x, nearest_station.y)
        print(f"No available drones. Created new Drone {new_drone.drone_id} and assigned delivery task {task['pickup_task']} at nearest bus station ({nearest_station.x}, {nearest_station.y})")

    def calculate_distance(self, drone, x, y):
        """计算无人机与目标点之间的欧式距离"""
        return ((drone.x - x) ** 2 + (drone.y - y) ** 2) ** 0.5

    def allocate_pickup_task(self, task, target_x, target_y):
        """分配取货任务，直接寻找离目标位置最近的空闲无人机"""
        
        nearest_station = find_nearest_bus_station(target_x, target_y, bus_stations)
        nearest_drone = self.get_idle_drone(target_x, target_y)
        
        # 检查是否找到空闲无人机
        if nearest_drone is None:
            # 没有空闲的无人机，将任务加入等待队列
            self.pickup_task_queue.append((task, target_x, target_y))
            print(f"No available drone for pickup task {task['pickup_task']} - task added to the queue.")
            return

        # 如果取货点位于巴士站，直接标记任务完成
        if nearest_station.x == target_x and nearest_station.y == target_y:
            task['pickup_status'] = 'completed'
            nearest_drone.pickup_tasks_completed += 1
            
            print(f"Pickup task {task['pickup_task']} completed directly at the bus station ({target_x}, {target_y}).")
            return

        # 分配取货任务到无人机
        nearest_drone.assign_pickup_task(task, target_x, target_y)
        task['pickup_status'] = 'assigned'
        print(f"Assigned pickup task {task['pickup_task']} to Drone {nearest_drone.drone_id} at ({target_x}, {target_y})")

        # 从取货任务队列中移除已分配的任务（确保是正确的任务）
        if (task, target_x, target_y) in self.pickup_task_queue:
            self.pickup_task_queue.remove((task, target_x, target_y))
            print(f"Removed task {task['pickup_task']} from the queue.")



    def allocate_delivery_task(self, task, target_x, target_y, auto_create_drone=False):
        """分配送货任务，直接寻找离目标位置最近的空闲无人机"""
        nearest_drone = self.get_idle_drone(target_x, target_y)
        nearest_station = find_nearest_bus_station(target_x, target_y, bus_stations)
        
        # 检查是否找到了空闲无人机
        if nearest_drone is None:
            if auto_create_drone:
                # 如果允许自动创建无人机，确保有足够的无人机来处理任务
                self.ensure_delivery_drone_availability(task, target_x, target_y)
            else:
                # 没有可用无人机且不允许创建新无人机，将任务加入等待队列
                self.delivery_task_queue.append((task, target_x, target_y))
                print(f"No available drone for delivery task {task['pickup_task']} - task added to the queue.")
            return

        # 如果送货点位于巴士站，则直接标记任务完成
        if nearest_station.x == target_x and nearest_station.y == target_y:
            task['delivery_status'] = 'completed'
            nearest_drone.delivery_tasks_completed += 1
            print(f"Delivery task {task['pickup_task']} completed directly at the bus station ({target_x}, {target_y}).")
            return

        # 分配送货任务到无人机
        nearest_drone.assign_delivery_task(task, nearest_station.x, nearest_station.y)
        task['delivery_status'] = 'assigned'
        print(f"Assigned delivery task {task['pickup_task']} to Drone {nearest_drone.drone_id} at nearest bus station ({nearest_station.x}, {nearest_station.y}).")
        
        # 移除送货任务队列中的任务

        if (task, target_x, target_y) in self.delivery_task_queue:
            self.delivery_task_queue.remove((task, target_x, target_y))
            print(f"Removed delivery task {task['pickup_task']} from the queue.")


    def add_pickup_task_to_queue(self, task, target_x, target_y):
        """Add a pickup task to the queue."""
        self.pickup_task_queue.append((task, target_x, target_y))

    def add_delivery_task_to_queue(self, task, target_x, target_y):
        """Add a delivery task to the queue."""
        self.delivery_task_queue.append((task, target_x, target_y))

    def get_pickup_queue(self):
        """Return the pickup task queue."""
        return list(self.pickup_task_queue)

    def get_delivery_queue(self):
        """Return the delivery task queue."""
        return list(self.delivery_task_queue)




    def move_all_drones(self):

        
        for drone in self.drones:
            drone.move()

            # 如果无人机空闲且有等待的取货任务，分配任务
        if drone.status == 'idle' and self.pickup_task_queue:
            task, target_x, target_y = self.pickup_task_queue.popleft()
            print(f"Assigning queued pickup task {task['pickup_task']} to Drone {drone.drone_id} at ({target_x}, {target_y})")
            drone.assign_pickup_task(task, target_x, target_y)

        # 如果无人机空闲且有等待的送货任务，分配任务
        if drone.status == 'idle' and self.delivery_task_queue:
            task, target_x, target_y = self.delivery_task_queue.popleft()
            print(f"Assigning queued delivery task {task['pickup_task']} to Drone {drone.drone_id} at ({target_x}, {target_y})")
            drone.assign_delivery_task(task, target_x, target_y)
                

