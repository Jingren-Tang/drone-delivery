
import bus
class BusSystem:
    def __init__(self, time_per_station=10):

        self.time_per_station = time_per_station  # 每经过一个巴士站增加的时间
        self.tasks_transported = 0  # 统计巴士运输的次数
        self.buses = []  # 公交车列表
        self.bus_id_counter = 0  # 用来给每辆公交车分配唯一ID
        self.time = 0  # 系统的全局时间

    def initialize_buses(self, bus_lines, bus_stations_df):
        """初始化每条线路的公交车，每次调用时新增公交车"""
        for line in bus_lines:
            route_stations = [station for station in bus_stations_df.to_dict('records') if station['line'] == line]
            print(f"route station 是 {route_stations} ")
            # 为该线路添加新的公交车
            
            self.buses.append(Bus(self.bus_id_counter, route_stations, start_station_index = 0, direction=1))
            self.bus_id_counter += 1
            self.buses.append(Bus(self.bus_id_counter, route_stations, start_station_index = len(route_stations) - 1, direction=-1))
            self.bus_id_counter += 1

    def update_buses(self):
        """更新所有公交车的位置"""
        for bus in self.buses:
            bus.move()
            # print(f"Bus {bus.bus_id} at ({bus.x}, {bus.y}), Status: {bus.status}, Direction: {bus.direction}")

    def simulate(self, bus_lines, bus_stations_df):
        """每隔50个时间单位发车一次，并更新公交车的位置"""
        # 每隔50个时间单位添加新的公交车
        if self.time % 50 == 0 and self.time <= 100:
            # print(f"Starting new buses on all lines at time {self.time}.")
            self.initialize_buses(bus_lines, bus_stations_df)

        # 更新所有公交车的位置
        self.update_buses()
        self.time += 1  # 时间步长

    


    def check_buses_at_station_for_pickup(self, x, y, tolerance=0.1):
        """检查某个站点是否有公交车到达以便接客（允许一定容差，避免浮点误差）。
        此函数不要求提供公交车ID。
        """
        for bus in self.buses:
            # 检查公交车是否在指定位置（使用容差）
            if math.isclose(bus.x, x, abs_tol=tolerance) and math.isclose(bus.y, y, abs_tol=tolerance):
                # print(f"Bus {bus.bus_id} found at station ({x}, {y}), Status: {bus.status}")
                return bus
        # print(f"No bus found at station ({x}, {y}) for pickup.")
        return None

    def check_buses_at_station_for_delivery(self, x, y, bus_id, tolerance=0.1):
        """检查某个站点是否有指定ID的公交车到达以便送达（允许一定容差，避免浮点误差）。
        此函数需要提供公交车ID。
        """
        for bus in self.buses:
            # 检查公交车位置和ID是否匹配
            if (math.isclose(bus.x, x, abs_tol=tolerance) and 
                math.isclose(bus.y, y, abs_tol=tolerance) and 
                bus.bus_id == bus_id):
                # print(f"Bus {bus.bus_id} found at station ({x}, {y}) for delivery.")
                return bus
        # print(f"No matching bus found at station ({x}, {y}) for delivery with bus_id: {bus_id}")
        return None