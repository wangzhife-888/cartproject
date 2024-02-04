# -*- coding: utf-8 -*-
"""
@Time: 2023/12/6 22:48
@Author: liucong
@File: ACUCMD.py
@IDE: PyCharm
@Description: 
"""

from DataFormatAcu import *

import ctypes
import socket
import struct
import time
import threading

from datetime import datetime


# # Define some constants
TIMEOUT = 2
# RECALL_FRAME_LEN = 15
# BUFFER_MAX_LEN = 1024


class UDPClient:
    def __init__(self, local_addr, local_port,dev_add,dev_port):
        self.local_addr = local_addr
        self.local_port = local_port
        self.dev_port = dev_port

        self.dev_add = dev_add

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.local_addr, self.local_port))
        self.sock.settimeout(TIMEOUT)


    def connect(self):
        self.sock= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.local_addr, self.local_port))
        pass  # In UDP, connect is not needed, it's a dummy method

    def close(self):
        self.sock.close()
    #
    def read(self, size):
        data, addr = self.sock.recvfrom(size)
        return data, addr
    #
    def write(self,data):
        import binascii
        print(data)
        print(type(data))

        rt = self.sock.sendto(data,(self.dev_add,self.dev_port))

        '''
        mock 
        '''
        # # hex_data = '7b ca 1e 00 00 1b 00 00 3f 00 42 32 56 8a 15 a1 03 d2 af 4c 40 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 4b bb 5f 47 3a 83 3c 40 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 7d'
        # hex_data = '7b ca 1e 01 2a 1b 00 00 3f 00 42 32 56 8a 15 a1 03 d2 af 4c 40 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 4b bb 5f 47 3a 83 3c 40 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 7d'
        # # 将十六进制数据转换为 bytes
        # byte_data = binascii.unhexlify(hex_data.replace(' ', ''))
        # print(byte_data)
        # rt = self.sock.sendto(byte_data, self.dev_add)


        return rt







count = 0

class ACUDriver():
    def __init__(self, local_addr, local_port, acu_add,acu_port):
        self.local_addr = local_addr
        self.local_port = local_port
        self.acu_add = acu_add
        self.acu_port = acu_port

        self.statusvalues = {"AzIndicated":'',
                             "ElIndicated":'',
                             "AzWrap": '',
                             "AzCommanded": '',
                             "ElCommanded": '',
                             "AzWrapCommanded": '',
                             "AzDifference": '',
                             "ElDifference": '',
                             "Status": '',
                             "FrameCount": '',
                             "Hour": '',
                             "Minute": '',
                             "Second": '',
                             "Millisecond": '',
                             "FrameLength": '',
                             }


        self.acustatus = {}


        self.high_rate_status = high_rate_status_t()
        # 使用 memset() 函数将结构体中的所有字节设置为 0
        ctypes.memset(ctypes.addressof(self.high_rate_status), 0, ctypes.sizeof(high_rate_status_t))

        self.normal_status = normal_status_t()
        ctypes.memset(ctypes.addressof(self.normal_status), 0, ctypes.sizeof(normal_status_t))

        self.rejection_frame = rejection_frame_t()
        ctypes.memset(ctypes.addressof(self.rejection_frame), 0, ctypes.sizeof(rejection_frame_t))

        self.response_frame = response_frame_t()
        ctypes.memset(ctypes.addressof(self.response_frame), 0, ctypes.sizeof(response_frame_t))

        self.ant_control_command = ant_control_command_t()
        self.ant_control_command2 = ant_control_command_t2()
        self.feed_control_command = feed_control_command_t()

        self.client = UDPClient(self.local_addr,self.local_port,self.acu_add,self.acu_port)


        self._mutex_50ms = threading.Lock()  # 定义互斥锁

        self._mutex_1s = threading.Lock()
        self._mutex_command = threading.Lock()



        # self.ant_control_command = ctypes.pointer(DataFormatAcu.ant_control_command_t())



        self.read_thread = threading.Thread(target=self.loop)
        self.read_thread.start()

    def __del__(self):
        pass
        # if self.client is not None:
        #     print("Cleaning up the client...")
        #
        #     self.client.close()
        #     # 这里可以添加你的清理代码，例如关闭连接、删除文件等。

    def loop(self):
        RCV_LEN = 1024
        rcv_buf = bytearray(RCV_LEN)

        while True:
            rcv_buf[:] = b'\0' * RCV_LEN  # Clear the buffer
            try:
                data, addr = self.client.read(RCV_LEN)

                if not data:
                    continue
                rcv_buf[:len(data)] = data
                rcv_buf[len(data):] = b''
                # rcv_buf = rcv_buf[:len(data)]

            except Exception as e:
                print(f"Exception occurred: {e}")
                self.client.close()
                time.sleep(1)
                self.client.connect()
                continue

            if len(rcv_buf) > 11 and bytes([rcv_buf[0]]) == b'\x7b' and bytes([rcv_buf[-1]]) == b'\x7d' :
                with self._mutex_50ms:  # 使用互斥锁保护共享资源的访问
                    if bytes([rcv_buf[10]]) == b'\x31':
                        ctypes.memmove(ctypes.addressof(self.high_rate_status), bytes(rcv_buf), len(rcv_buf))
                        # print(self.high_rate_status.real_az_angle)
                        # print(self.high_rate_status.real_az_position)
                        # print(self.high_rate_status.real_el_angle)
                        # print(self.high_rate_status.target_az_angle)
                        # print(self.high_rate_status.target_az_position)
                        # print(self.high_rate_status.target_el_angle)
                        # print(self.high_rate_status.deviation_az)
                        # print(self.high_rate_status.deviation_el)
                        # print(self.high_rate_status.header.time_hour)
                        # print(self.high_rate_status.header.time_minute)
                        # print(self.high_rate_status.header.time_second)
                        # print(self.high_rate_status.header.time_millisecond)
                    elif bytes([rcv_buf[10]]) == b'\x32':
                        ctypes.memmove(ctypes.addressof(self.normal_status), bytes(rcv_buf), len(rcv_buf))
                    elif bytes([rcv_buf[10]]) == b'\x7f':
                        ctypes.memmove(ctypes.addressof(self.rejection_frame), bytes(rcv_buf), len(rcv_buf))
                    else:
                        print("read flag other")
                        self.rejection_frame[:] = b'\0' * ctypes.sizeof(self.rejection_frame)
                        ctypes.memmove(ctypes.addressof(self.response_frame), bytes(rcv_buf), len(rcv_buf))
            else:
                print("Error received data from ACU ,the frame header is unmatch")



    # BCD码转换为十进制
    def bcd2int(self,bcd_byte):
        return (bcd_byte >> 4) * 10 + (bcd_byte & 0x0F)


    #毫秒，BCD码转换为十进制
    def bcd2int_ms(self,bcd_array):
        result = 0
        for byte in bcd_array:
            result *= 100
            result += (byte >> 4) * 10 + (byte & 0x0F)
        return result

    def getStatus_50ms(self):
        with self._mutex_50ms:
            temp = "%.4lf" % self.high_rate_status.real_az_angle
            self.statusvalues["AzIndicated"] = temp
            temp = "%.4lf" % self.high_rate_status.real_el_angle
            self.statusvalues["ElIndicated"] = temp
            temp = "%d" % self.high_rate_status.real_az_position
            self.statusvalues["AzWrap"] = temp
            temp = "%.4lf" % self.high_rate_status.target_az_angle
            self.statusvalues["AzCommanded"] = temp
            temp = "%.4lf" % self.high_rate_status.target_el_angle
            self.statusvalues["ElCommanded"] = temp
            temp = "%d" % self.high_rate_status.target_az_position
            self.statusvalues["AzWrapCommanded"] = temp
            temp = "%.4lf" % self.high_rate_status.deviation_az
            self.statusvalues["AzDifference"] = temp
            temp = "%.4lf" % self.high_rate_status.deviation_el
            self.statusvalues["ElDifference"] = temp
            temp = "%d" % self.high_rate_status.status
            self.statusvalues["Status"] = temp
            temp = "%d" % self.high_rate_status.header.frame_count
            self.statusvalues["FrameCount"] = temp

            temp = "%d" % self.bcd2int(self.high_rate_status.header.time_hour)
            self.statusvalues["Hour"] = temp
            temp = "%d" % self.bcd2int(self.high_rate_status.header.time_minute)
            self.statusvalues["Minute"] = temp
            temp = "%d" % self.bcd2int(self.high_rate_status.header.time_second)
            self.statusvalues["Second"] = temp

            temp = "%d" % self.bcd2int_ms(self.high_rate_status.header.time_millisecond)
            self.statusvalues["Millisecond"] = temp

            temp = "%d" % self.high_rate_status.header.frame_length
            self.statusvalues["FrameLength"] = temp

        return self.statusvalues
    #
    #
    def getStatus_1s(self):
        with self._mutex_50ms:
            ACUStatus = ["CWF", "CWP", "CWS", "CCWF", "CCWP", "CCWS", "ZS", "UPF", "UPP", "UPS", "DOWNF", "DOWNP",
                         "DOWNS", "ES", "ELCD", "ELI", "ELP", "ADUCM", "AZB", "ELB", "AZ1P", "AZ2P", "EL1P", "EL2P",
                         "ELLP", "AZD", "ELD", "AZI", "AZP", "AZLP", "ASD"]

            ACUPStatus = ["ADUP", "ADUWM", "ACUMM", "AZCS", "ELZS", "ADUCS", "TS", "SCS", "AZMS", "ELMS", "FUS"]

            FUStatus = ["FCWF", "FCWP", "FCWS", "FCCWF", "FCCWP", "FCCWS", "FB1", "FB2", "FES", "FM1P", "FM2P", "FCM"]

            for i in range(31):
                temp = format((self.normal_status.ACU_status >> i) & 1, "d")
                self.acustatus[ACUStatus[i]] = temp

            for i in range(11):
                temp = format((self.normal_status.antenna_problem_status >> i) & 1, "d")
                self.acustatus[ACUPStatus[i]] = temp

            for i in range(12):
                temp = format((self.normal_status.feed_status >> i) & 1, "d")
                self.acustatus[FUStatus[i]] = temp

            temp = format(self.normal_status.mode, "x").zfill(2)
            self.acustatus["MODE"] = f"0x{temp}"


            temp = format(self.normal_status.az_speed, ".3f")
            self.acustatus["AzRate"] = temp

            temp = format(self.normal_status.el_speed, ".3f")
            self.acustatus["ElRate"] = temp

            temp = format(self.normal_status.feedback, "x").zfill(2)
            self.acustatus["FEED"] = f"0x{temp}"

            temp = format(self.normal_status.feed_real_angle, ".3f")
            self.acustatus["feed_real_angle"] = temp

            temp = format(self.normal_status.feed_speed, ".3f")
            self.acustatus["feed_speed"] = temp

            temp = "%x" % self.normal_status.header.frame_header
            self.acustatus["frame_header"] = temp

            temp = "%d" % self.normal_status.header.frame_count
            self.acustatus["frame_count"] = temp

            temp = "%d" % self.bcd2int(self.normal_status.header.time_hour)
            self.acustatus["time_hour"] = temp
            temp = "%d" % self.bcd2int(self.normal_status.header.time_minute)
            self.acustatus["time_minute"] = temp
            temp = "%d" % self.bcd2int(self.normal_status.header.time_second)
            self.acustatus["time_second"] = temp

            temp = "%d" % self.bcd2int_ms(self.normal_status.header.time_millisecond)
            self.acustatus["time_millisecond"] = temp

            temp = "%d" % self.normal_status.header.frame_length
            self.acustatus["frame_length"] = temp

        return self.acustatus

    def setAntCom(self, mode, childmode, control, azcir):
        global count
        time = datetime.now()
        hour, min, sec, milisec = time.hour, time.minute, time.second, time.microsecond // 1000
        print(hour, min, sec, milisec)

        with self._mutex_command:
            self.ant_control_command.header.frame_header = 0x7b
            self.ant_control_command.header.frame_count = count
            self.ant_control_command.header.time_hour = hour
            self.ant_control_command.header.time_minute = min
            self.ant_control_command.header.time_second = sec

            self.ant_control_command.header.time_millisecond[0] = ctypes.c_uint8(milisec & 0xFF)
            self.ant_control_command.header.time_millisecond[1] = ctypes.c_uint8((milisec >> 8) & 0xFF)

            self.ant_control_command.header.frame_length = ctypes.sizeof(self.ant_control_command)
            self.ant_control_command.header.category_code = 0x42
            self.ant_control_command.ending.frame_end = 0x7d
            self.ant_control_command.mode = mode

        if mode == 0x30:
            self.ant_control_command.childmode = 0x0
            self.ant_control_command.param[0] = 0
            self.ant_control_command.param[1] = 0
            self.ant_control_command.cw_ccw = 0
        elif mode == 0x32:
            self.ant_control_command.childmode = childmode
            if childmode == 0x31:
                self.ant_control_command.param[0] = control[0]
                self.ant_control_command.param[1] = control[1]
                self.ant_control_command.cw_ccw = azcir
            else:
                raise ValueError("mode 0x32, childmode parameter error, should be 0x31 or 0x32 or 0x33")
        elif mode == 0x36:
            self.ant_control_command.param[0] = control[0]
            self.ant_control_command.param[1] = control[1]
            self.ant_control_command.cw_ccw = azcir
        else:
            raise ValueError("mode parameter is error, check it, should be 0x30 0x32 0x34 0x36")

        try:
            rt = self.client.write(ctypes.string_at(ctypes.addressof(self.ant_control_command), ctypes.sizeof(self.ant_control_command)))

            self.count = (count + 1) % 10000
        except Exception as e:
            return -1
        return 0
    #
    def setAntComPVA(self, mode, childmode, control, azcir):
        global count
        time = datetime.now()
        hour, min, sec, milisec = time.hour, time.minute, time.second, time.microsecond // 1000
        print(hour,min,sec,milisec)
        with self._mutex_command:

            self.ant_control_command2.header.frame_header = 0x7b
            self.ant_control_command2.header.frame_count = count

            self.ant_control_command2.header.time_hour = hour
            self.ant_control_command2.header.time_minute = min
            self.ant_control_command2.header.time_second = sec

            self.ant_control_command2.header.time_millisecond[0] = ctypes.c_uint8(milisec & 0xFF)
            self.ant_control_command2.header.time_millisecond[1] = ctypes.c_uint8((milisec >> 8) & 0xFF)

            self.ant_control_command2.header.frame_length = ctypes.sizeof(self.ant_control_command2)
            self.ant_control_command2.header.category_code = 0x42
            self.ant_control_command2.ending.frame_end = 0x7d
            self.ant_control_command2.mode = mode

        if mode == 0x30: # 待机
            self.ant_control_command2.childmode = 0x00
            self.ant_control_command2.az[0] = ctypes.c_double(0.0)
            self.ant_control_command2.az[1] = ctypes.c_double(0.0)
            self.ant_control_command2.az[2] = ctypes.c_double(0.0)

            self.ant_control_command2.el[0] = ctypes.c_double(0.0)
            self.ant_control_command2.el[1] = ctypes.c_double(0.0)
            self.ant_control_command2.el[2] = ctypes.c_double(0.0)

            self.ant_control_command2.cw_ccw = 0
        elif mode == 0x32: # 命令位置
            print('here')
            self.ant_control_command2.childmode = childmode

            if childmode == 0x31: #直接命令角

                # self.ant_control_command2.az[0] = ctypes.c_double(control[0])
                # self.ant_control_command2.az[1] = ctypes.c_double(control[1])
                # self.ant_control_command2.az[2] = ctypes.c_double(control[2])
                # self.ant_control_command2.el[0] = ctypes.c_double(control[3])
                # self.ant_control_command2.el[1] = ctypes.c_double(control[4])
                # self.ant_control_command2.el[2] = ctypes.c_double(control[5])
                self.ant_control_command2.az[0] = control[0]
                self.ant_control_command2.az[1] = control[1]
                self.ant_control_command2.az[2] = control[2]
                self.ant_control_command2.el[0] = control[3]
                self.ant_control_command2.el[1] = control[4]
                self.ant_control_command2.el[2] = control[5]
                self.ant_control_command2.cw_ccw = azcir
                print('here2')
            else:
                error = "mode 0x32 ,childmode parameter error,should be 0x31 or 0x 32 or 0x33"
                return -1
        elif mode == 0x36: # 收藏
            self.ant_control_command2.az[0] = ctypes.c_double(control[0])
            self.ant_control_command2.az[1] = ctypes.c_double(control[1])
            self.ant_control_command2.az[2] = ctypes.c_double(control[2])
            self.ant_control_command2.el[0] = ctypes.c_double(control[3])
            self.ant_control_command2.el[1] = ctypes.c_double(control[4])
            self.ant_control_command2.el[2] = ctypes.c_double(control[5])
            self.ant_control_command2.cw_ccw = azcir
        else:
            error = "mode parameter is error,check it,should is 0x30 0x32 0x34 0x36"
            return -1
        try:
            rt = self.client.write(ctypes.string_at(ctypes.addressof(self.ant_control_command2), ctypes.sizeof(self.ant_control_command2)))

            # print(self.ant_control_command2.header.frame_header)
            # print(self.ant_control_command2.az[0], self.ant_control_command2.az[1], self.ant_control_command2.az[2])
            # print(self.ant_control_command2.el[0], self.ant_control_command2.el[1], self.ant_control_command2.el[2])

            count = (count + 1) % 10000
        except Exception as e:
            print(e)
            return -1
        return 0
    #
    #
    def setAntCon3(self, mode, childmode, control, azcir):
        global count
        time = datetime.now()
        hour, min, sec, milisec = time.hour, time.minute, time.second, time.microsecond // 1000
        print(hour,min,sec,milisec)


        self.ant_control_command2.header.frame_header = 0x7b
        self.ant_control_command2.header.frame_count = 7882

        self.ant_control_command2.header.time_hour = 0
        self.ant_control_command2.header.time_minute = 0
        self.ant_control_command2.header.time_second = 0
        # self.ant_control_command2.header.time_hour = hour
        # self.ant_control_command2.header.time_minute = min
        # self.ant_control_command2.header.time_second = sec

        # self.ant_control_command2.header.time_millisecond = milisec
        self.ant_control_command2.header.time_millisecond[0]= ctypes.c_uint8(0)
        self.ant_control_command2.header.time_millisecond[1] = ctypes.c_uint8(0)
        # self.ant_control_command2.header.frame_length = ctypes.c_uint16(63)
        # self.ant_control_command2.header.frame_length = 0x003F
        self.ant_control_command2.header.frame_length = ctypes.sizeof(self.ant_control_command2)
        self.ant_control_command2.header.category_code = 0x42
        self.ant_control_command2.ending.frame_end = 0x7d
        self.ant_control_command2.mode = 0x32

        self.ant_control_command2.childmode = 0x31  #0x56
        #
        hex_data = '7b ca 1e 00 00 1b 00 00 3f 00 42 32 56 8a 15 a1 03 d2 af 4c 40 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 4b bb 5f 47 3a 83 3c 40 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 7d'
        #
        # self.ant_control_command2.az[0] = ctypes.c_double(control[0])
        # self.ant_control_command2.az[1] = ctypes.c_double(control[1])
        # self.ant_control_command2.az[2] = ctypes.c_double(control[2])
        # self.ant_control_command2.el[0] = ctypes.c_double(control[3])
        # self.ant_control_command2.el[1] = ctypes.c_double(control[4])
        # self.ant_control_command2.el[2] = ctypes.c_double(control[5])
        self.ant_control_command2.az[0] = 46 #57.373596624044765
        self.ant_control_command2.az[1] = ctypes.c_double(0)
        self.ant_control_command2.az[2] = ctypes.c_double(0)
        self.ant_control_command2.el[0] = ctypes.c_double(46)
        self.ant_control_command2.el[1] = ctypes.c_double(0)
        self.ant_control_command2.el[2] = ctypes.c_double(0)
        self.ant_control_command2.cw_ccw = ctypes.c_uint8(0)

        # self.ant_control_command2.az[0] = 180.0
        # self.ant_control_command2.az[1] = 0.0
        # self.ant_control_command2.az[2] = 0.0
        # self.ant_control_command2.el[0] = 45.0
        # self.ant_control_command2.el[1] = 0.0
        # self.ant_control_command2.el[2] = 0.0
        # self.ant_control_command2.cw_ccw = 1
        rt = self.client.write(
            ctypes.string_at(ctypes.addressof(self.ant_control_command2), ctypes.sizeof(self.ant_control_command2)))
        # rt = self.client.write(bytes(self.ant_control_command2))

        # print(self.ant_control_command2.header.frame_length)
        # rt = self.client.write(
        #     ctypes.string_at(ctypes.addressof(self.ant_control_command2), 58))
        # rt1 = self.client.write(ctypes.cast(self.ant_control_command2, ctypes.POINTER(ctypes.c_char)))
        #     print(self.ant_control_command2.header.time_millisecond)
        #     # print(self.ant_control_command2.header.frame_header)
        #     # print(self.ant_control_command2.az[0], self.ant_control_command2.az[1], self.ant_control_command2.az[2])
        #     # print(self.ant_control_command2.el[0], self.ant_control_command2.el[1], self.ant_control_command2.el[2])
        return 0

        # with self._mutex_command:
        #
        #
        #     self.ant_control_command2.header.frame_header = 0x7b
        #
        #     self.ant_control_command2.header.frame_count = count
        #
        #     self.ant_control_command2.header.time_hour = hour
        #     self.ant_control_command2.header.time_minute = min
        #     self.ant_control_command2.header.time_second = sec
        #
        #     # self.ant_control_command2.header.time_millisecond = milisec
        #     # #
        #     # # self.ant_control_command2.header.time_millisecond[1] = ctypes.c_uint8(0)
        #     self.ant_control_command2.header.frame_length = ctypes.sizeof(self.ant_control_command2)
        #     self.ant_control_command2.header.category_code = 0x42
        #     self.ant_control_command2.ending.frame_end = 0x7d
        #     self.ant_control_command2.mode = mode
        # if mode == 0x30: # 待机
        #     self.ant_control_command2.childmode = 0x00
        #     self.ant_control_command2.az[0] = ctypes.c_double(0.0)
        #     self.ant_control_command2.az[1] = ctypes.c_double(0.0)
        #     self.ant_control_command2.az[2] = ctypes.c_double(0.0)
        #
        #     self.ant_control_command2.el[0] = ctypes.c_double(0.0)
        #     self.ant_control_command2.el[1] = ctypes.c_double(0.0)
        #     self.ant_control_command2.el[2] = ctypes.c_double(0.0)
        #
        #     self.ant_control_command2.cw_ccw = 0
        # elif mode == 0x32: # 命令位置
        #     print('here')
        #     self.ant_control_command2.childmode = childmode
        #
        #     if self.ant_control_command2.childmode == 0x31: #直接命令角
        #
        #         # self.ant_control_command2.az[0] = ctypes.c_double(control[0])
        #         # self.ant_control_command2.az[1] = ctypes.c_double(control[1])
        #         # self.ant_control_command2.az[2] = ctypes.c_double(control[2])
        #         # self.ant_control_command2.el[0] = ctypes.c_double(control[3])
        #         # self.ant_control_command2.el[1] = ctypes.c_double(control[4])
        #         # self.ant_control_command2.el[2] = ctypes.c_double(control[5])
        #         self.ant_control_command2.az[0] = control[0]
        #         self.ant_control_command2.az[1] = control[1]
        #         self.ant_control_command2.az[2] = control[2]
        #         self.ant_control_command2.el[0] = control[3]
        #         self.ant_control_command2.el[1] = control[4]
        #         self.ant_control_command2.el[2] = control[5]
        #         self.ant_control_command2.cw_ccw = azcir
        #         print('here2')
        #     else:
        #         error = "mode 0x32 ,childmode parameter error,should be 0x31 or 0x 32 or 0x33"
        #         return -1
        # elif mode == 0x36: # 收藏
        #     self.ant_control_command2.az[0] = ctypes.c_double(control[0])
        #     self.ant_control_command2.az[1] = ctypes.c_double(control[1])
        #     self.ant_control_command2.az[2] = ctypes.c_double(control[2])
        #     self.ant_control_command2.el[0] = ctypes.c_double(control[3])
        #     self.ant_control_command2.el[1] = ctypes.c_double(control[4])
        #     self.ant_control_command2.el[2] = ctypes.c_double(control[5])
        #     self.ant_control_command2.cw_ccw = azcir
        # else:
        #     error = "mode parameter is error,check it,should is 0x30 0x32 0x34 0x36"
        #     return -1
        # try:
        #     rt = self.client.write(ctypes.string_at(ctypes.addressof(self.ant_control_command2), ctypes.sizeof(self.ant_control_command2)))
        #     print(self.ant_control_command2.header.time_millisecond)
        #     # print(self.ant_control_command2.header.frame_header)
        #     # print(self.ant_control_command2.az[0], self.ant_control_command2.az[1], self.ant_control_command2.az[2])
        #     # print(self.ant_control_command2.el[0], self.ant_control_command2.el[1], self.ant_control_command2.el[2])
        #
        #     count = (count + 1) % 10000
        # except Exception as e:
        #     print(e)
        #     return -1
        # return 0

    #
    #
    def setFeed(self, command, angle):
        global count
        # print(angle)
        time = datetime.now()
        hour, min, sec, milisec = time.hour, time.minute, time.second, time.microsecond // 1000
        with self._mutex_command:
            self.feed_control_command.header.frame_header = 0x7b
            self.feed_control_command.header.frame_count = count
            self.feed_control_command.header.time_hour = hour
            self.feed_control_command.header.time_minute = min
            self.feed_control_command.header.time_second = sec
            # feed_control_command->header.time_millisecond = milisec
            self.feed_control_command.header.frame_length = ctypes.sizeof(self.feed_control_command)
            self.feed_control_command.header.category_code = 0x43
            self.feed_control_command.ending.frame_end = 0x7d
            if command == True:
                self.feed_control_command.move_command = 0x31
            elif command == False:
                self.feed_control_command.move_command = 0x30
            else:
                error = "setFeed parameter error"
                return -1
            self.feed_control_command.move_position = angle
            if angle < 0 or angle > 360:
                error = "setFeed parameter error"
                return -1
        try:
            rt = self.client.write(ctypes.string_at(ctypes.addressof(self.feed_control_command), ctypes.sizeof(self.feed_control_command)))

            count += 1
        except Exception as e:
            return -1
        if count == 10000:
            count = 0
        return 0
    #
    #
    #
    # def getRejection(self, rejectionstatus, error):
    #     temp = b""
    #     out = ""
    #     rejectionstatus["frame_count"] = str(rejection_frame.header.frame_count)
    #     rejectionstatus["time_hour"] = str(rejection_frame.header.time_hour)
    #     rejectionstatus["time_minute"] = str(rejection_frame.header.time_minute)
    #     rejectionstatus["time_second"] = str(rejection_frame.header.time_second)
    #     rejectionstatus["time_millisecond"] = str(rejection_frame.header.time_millisecond[0])
    #     rejectionstatus["frame_length"] = str(rejection_frame.header.frame_length)
    #     rejectionstatus["rejection_category_code"] = "0x" + hex(rejection_frame.rejection_category_code)[2:]
    #     if rejection_frame.rejection_code == 0:
    #         rejectionstatus["rejection_mean"] = "receive ok"
    #     elif rejection_frame.rejection_code == 1:
    #         rejectionstatus["rejection_mean"] = "adu can not operate"
    #     elif rejection_frame.rejection_code == 2:
    #         rejectionstatus["rejection_mean"] = "parameter over limit"
    #     elif rejection_frame.rejection_code == 3:
    #         rejectionstatus["rejection_mean"] = "condition need"
    #     elif rejection_frame.rejection_code == 4:
    #         rejectionstatus["rejection_mean"] = "command not pair"
    #     elif rejection_frame.rejection_code == 5:
    #         rejectionstatus["rejection_mean"] = "category_code error"
    #     elif rejection_frame.rejection_code == 6:
    #         rejectionstatus["rejection_mean"] = "other problem"
    #     else:
    #         error = "unknow rejection_code"
    #         return -1
    #     return 0
    #

    #
    # def getStatus_50ms(self, HRS):
    #     HRS[0] = self.high_rate_status
    #     return 0
    #
    # def getStatus_1s(self, AS):
    #     AS[0] = self.normal_status
    #     return 0
    #
    # def getRejection(self, RF):
    #     RF[0] = self.rejection_frame
    #     return 0
    #
    # def setStandBy(self):
    #     self.mode = 0x30
    #     self.con = [0.0, 0.0]
    #     self.childmode = 0
    #     self.azcir = 0
    #     self.err = ""
    #     return self.setAntCon()
    #
    # def moveToAccessPosition(self):
    #     self.mode = 0x36
    #     self.con = [0.0, 0.0]
    #     self.childmode = 0
    #     self.azcir = 0
    #     self.err = ""
    #     return self.setAntCon()
    #
    # def setAzElCmd_azel(self, az, el, azcir):
    #     self.mode = 0x32
    #     self.con = [az, el]
    #     self.childmode = 0x31
    #     self.azc = azcir
    #     self.err = ""
    #     return self.setAntCon()
    #



    def setAzElPVA(self, azp, azv, aza, elp, elv, ela, azcir):

        mode = 0x32
        con = [azp, azv, aza, elp, elv, ela]
        childmode = 0x31
        azc = azcir
        err = ""
        print(type(mode))
        try:
            self.rt = self.setAntComPVA(mode,childmode,con,azc)
        except Exception as e:
            pass
            return -1

        return self.rt



if __name__ == '__main__':
    # local_host = '127.0.0.1'
    local_host = '192.168.100.120'
    local_port = 8090
    acu_add = '192.168.100.10'
    acu_port = 8091

    a= ACUDriver(local_host,local_port,acu_add,acu_port)

    az = [60, 70,80,230]
    el = [88.9,87,86,85]
    for i,j in enumerate(az):
        # print(j,el[i])
        a.setAzElPVA(azp=j, azv=0, aza=0, elp=el[i], elv=0, ela=0,azcir=0)


    # while True:
    #
    #     a.setAzElPVA(azp=az, azv=0, aza=0, elp=el, elv=0, ela=0, azcir=0)
    #     time.sleep(1)
        # a.setFeed(True,20)
    #     info_50ms = a.getStatus_50ms()
    #     info_1s = a.getStatus_1s()
    #
    #     print(info_50ms)
    #     print(info_1s)
        time.sleep(1)


