import numpy as np
from pyModbusTCP.client import ModbusClient
import time



class ModbusFuzzer:
    def __init__(self):
        self.debug = True
        self.clients={}
    
    def connection(self):
        ips = input('Enter IP List: ').split(',')
        counter = 0
        for ip in ips:
            counter += 1
            self.clients[counter] = ip
            print(f"[INFO] Client No {counter} IP: {self.clients[counter]}")
            
            try:
                cl=ModbusClient(self.clients[counter], port=502, auto_close=True)
                cl.open()
                time.sleep(3)
                if cl.is_open == True:
                   print(f"[OK] Connection Successful {self.clients[counter]}")
                   print(f"[INFO] Setting Up {self.clients[counter]}")
                   choice = int(input("1) Coil 2) Holding Register: "))
                   size = int(input("How many bits to write ?:  "))
                   if size >= 0 or size <= 65535:
                      size = size
                   else:
                        size = 5
                   p_times = int(input("How many times do you want the payload to execute ? "))
                   if p_times > 9999 or p_times <= 0:
                       p_times = 10
                   else:
                       p_times = p_times
                       
                   if choice == 1:
                      print(f"[OK] Trying payload to coil with {self.clients[counter]}")
                      for timing in range(0, p_times):
                          payload=self.generate_payload('coil', size)
                          time.sleep(1)
                          cl.write_multiple_coils(0, payload)
                          print(f'[OK] Sent payload: {payload}')
                   if choice == 2:
                      print(f"[OK] Trying payload to holding register with {self.clients[counter]}")
                      for timing in range(0, p_times):
                          payload = self.generate_payload('holding_register', size)
                          time.sleep(1)
                          cl.write_multiple_registers(0, payload)
                          print(f'[OK] Sent payload: {payload}')
                else:
                     print(f"[ERROR] Connection NOT Successful IP: {self.clients[counter]}")
                     print(f"[INFO] Send payload manually: {self.generate_payload('holding_register', size)}")
            except Exception as e:
                   print(e)
                   exit()
                    
    def generate_payload(self,choice, size):
        if choice == "coil":
            rn = np.random.uniform(low=0, high=2, size=size).astype(np.int32)
            return list(rn)
        
        if choice == "holding_register":
            rn = np.random.uniform(low=0, high=65536, size=size).astype(np.int32)
            return list(rn)
print("""
#     #               #######                                    
##   ##  ####  #####  #       #    # ###### ###### ###### #####  
# # # # #    # #    # #       #    #     #      #  #      #    # 
#  #  # #    # #    # #####   #    #    #      #   #####  #    # 
#     # #    # #    # #       #    #   #      #    #      #####  
#     # #    # #    # #       #    #  #      #     #      #   #  
#     #  ####  #####  #        ####  ###### ###### ###### #    # 
""")

fuzzer = ModbusFuzzer()
while True:
    option = int(input('1) Fuzz IP\n2) Generate Payloads\n3) Exit'))
    if option == 1:
        fuzzer.connection()
    if option == 2:
        print(f'''Coil Payload {fuzzer.generate_payload('coil', 10)}\nHolding Register {fuzzer.generate_payload('holding_register', 10)}''')
    if option == 3:
        exit()
