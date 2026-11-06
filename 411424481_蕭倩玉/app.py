from collections import deque

class SmartParkingLot:
    def __init__(self, total_spots=3):
        self.total_spots = total_spots
        # 車位狀態：陣列紀錄每個車位是否被佔用 (None 代表空，否則放車牌)
        self.spots = [None] * total_spots
        # Hash Table (Python dict)：快速查詢車牌目前停在哪一個車位
        self.active_cars = {} 
        # Queue：滿位時的等待佇列
        self.waiting_queue = deque()

    def display_status(self):
        print("\n--- 停車場即時狀態 ---")
        print(f"車位狀態: {self.spots}")
        print(f"停放中的車輛 (Hash Table): {self.active_cars}")
        print(f"等待佇列 (Queue): {list(self.waiting_queue)}")
        print("----------------------\n")

    def check_in(self, plate):
        if plate in self.active_cars:
            print(f"❌ 錯誤：車牌 {plate} 已經在停車場內了！")
            return

        # 尋找第一個空車位
        empty_spot = -1
        for i in range(self.total_spots):
            if self.spots[i] is None:
                empty_spot = i
                break

        if empty_spot != -1:
            # 有空位，直接停車
            self.spots[empty_spot] = plate
            self.active_cars[plate] = empty_spot
            print(f"✅ 車輛 {plate} 成功停入第 {empty_spot} 號車位。")
        else:
            # 沒空位，進入等待佇列
            self.waiting_queue.append(plate)
            print(f"⚠️ 停車場已滿！車輛 {plate} 已加入等待佇列（目前排第 {len(self.waiting_queue)} 位）。")

    def check_out(self, plate):
        if plate not in self.active_cars:
            print(f"❌ 錯誤：找不到車牌 {plate} 的停車紀錄！")
            return

        # 釋放車位
        spot_index = self.active_cars[plate]
        del self.active_cars[plate]
        self.spots[spot_index] = None
        print(f"🚗 車輛 {plate} 已出場，釋放第 {spot_index} 號車位。")

        # 檢查等待佇列是否有車要遞補
        if self.waiting_queue:
            next_plate = self.waiting_queue.popleft()
            self.spots[spot_index] = next_plate
            self.active_cars[next_plate] = spot_index
            print(f"🔄 遞補機制啟動：等待中的車輛 {next_plate} 自動停入第 {spot_index} 號車位。")

# === 測試與 Demo 執行範例 ===
if __name__ == "__main__":
    # 建立一個只有 2 個車位的測試停車場
    lot = SmartParkingLot(total_spots=2)

    # 1. 車輛陸續入場
    lot.check_in("ABC-1234")
    lot.check_in("XYZ-5678")
    lot.display_status()

    # 2. 停車場滿位，測試排隊機制
    lot.check_in("HELLO-999")
    lot.display_status()

    # 3. 車輛出場，測試自動遞補與 Hash Table/Queue 運作
    lot.check_out("ABC-1234")
    lot.display_status()