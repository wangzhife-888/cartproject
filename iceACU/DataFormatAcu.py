# -*- coding: utf-8 -*-
"""
@Time: 2023/12/6 22:01
@Author: liucong
@File: DataFormatAcu.py
@IDE: PyCharm
@Description: 
"""

import ctypes
import sys


class header_t(ctypes.Structure):
    '''
    在 ctypes 中，_pack_ 属性用于控制结构体的字节对齐。它的值是一个整数，表示结构体字段之间的最小字节间隔。
    通常情况下，ctypes 会根据平台和硬件架构自动选择一个合适的字节对齐方式。然而，如果你希望自定义字节对齐方式，可以设置 _pack_ 属性来指定它。
    当你将 _pack_ 设置为 1 时，意味着你要求每个字段之间只有一个字节的间隔。这有助于确保数据按照字节顺序准确地存储和解析，特别是在处理不同字节序的数据时。
    '''
    _pack_ = 1
    _fields_ = [
        ("frame_header", ctypes.c_uint8),
        ("frame_count", ctypes.c_uint16),
        ("time_hour", ctypes.c_uint8),
        ("time_minute", ctypes.c_uint8),
        ("time_second", ctypes.c_uint8),
        ("time_millisecond", ctypes.c_uint8 * 2),
        ("frame_length", ctypes.c_uint16),
        ("category_code", ctypes.c_uint8),
    ]


class ending_t(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("frame_end", ctypes.c_uint8),
    ]


class high_rate_status_t(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("header", header_t),
        ("real_az_angle", ctypes.c_double),
        ("real_az_position", ctypes.c_bool),
        ("real_el_angle", ctypes.c_double),
        ("target_az_angle", ctypes.c_double),
        ("target_az_position", ctypes.c_bool),
        ("target_el_angle", ctypes.c_double),
        ("deviation_az", ctypes.c_double),
        ("deviation_el", ctypes.c_double),
        ("status", ctypes.c_bool),
        ("ending", ending_t),
    ]








class acu_status_t(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("cw_final_limit", ctypes.c_uint8, 1),
        ("cw_ahead_limit", ctypes.c_uint8, 1),
        ("cw_software_limit", ctypes.c_uint8, 1),
        ("ccw_final_limit", ctypes.c_uint8, 1),
        ("ccw_ahead_limit", ctypes.c_uint8, 1),
        ("ccw_software_limit", ctypes.c_uint8, 1),
        ("zero_crossing_swtich", ctypes.c_uint8, 1),
        ("up_final_limit", ctypes.c_uint8, 1),
        ("up_ahead_limit", ctypes.c_uint8, 1),
        ("up_software_limit", ctypes.c_uint8, 1),
        ("emergency_stop", ctypes.c_uint8, 1),
        ("el_central_door", ctypes.c_uint8, 1),
        ("el_mortise_lock", ctypes.c_uint8, 1),
        ("el_pull_lock", ctypes.c_uint8, 1),
        ("adu_control_mode", ctypes.c_uint8, 1),
        ("az_break", ctypes.c_uint8, 1),
        ("el_break", ctypes.c_uint8, 1),
        ("az1_motor_power", ctypes.c_uint8, 1),
        ("az2_motor_power", ctypes.c_uint8, 1),
        ("el1_motor_power", ctypes.c_uint8, 1),
        ("el2_motor_power", ctypes.c_uint8, 1),
        ("el_lockmotor_power", ctypes.c_uint8, 1),
        ("az_move_direction", ctypes.c_uint8, 1),
        ("el_move_direction", ctypes.c_uint8, 1),
        ("az_mortise_lock", ctypes.c_uint8, 1),
        ("az_pull_lock", ctypes.c_uint8, 1),
        ("az_lockmotor_power", ctypes.c_uint8, 1),
        ("az_surface_door", ctypes.c_uint8, 1),
    ]




class ant_abnormal_status_t(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("adu_power", ctypes.c_uint8, 1),
        ("adu_control_mode", ctypes.c_uint8, 1),
        ("acu_control_mode", ctypes.c_uint8, 1),
        ("az_encoder_state", ctypes.c_uint8, 1),
        ("el_encoder_state", ctypes.c_uint8, 1),
        ("adu_control_status", ctypes.c_uint8, 1),
        ("time_code_status", ctypes.c_uint8, 1),
        ("serial_communication_status", ctypes.c_uint8, 1),
        ("az_drive_status", ctypes.c_uint8, 1),
        ("el_drive_status", ctypes.c_uint8, 1),
        ("feed_status", ctypes.c_uint8, 1),
    ]


class feed_status_t(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("cw_final_limit", ctypes.c_uint8, 1),
        ("cw_ahead_limit", ctypes.c_uint8, 1),
        ("cw_software_limit", ctypes.c_uint8, 1),
        ("ccw_final_limit", ctypes.c_uint8, 1),
        ("ccw_ahead_limit", ctypes.c_uint8, 1),
        ("ccw_software_limit", ctypes.c_uint8, 1),
        ("feed1_break", ctypes.c_uint8, 1),
        ("feed2_break", ctypes.c_uint8, 1),
        ("emergency_stop", ctypes.c_uint8, 1),
        ("feed1_motor", ctypes.c_uint8, 1),
        ("feed2_motor", ctypes.c_uint8, 1),
        ("remote_control", ctypes.c_uint8, 1),
    ]


# 定义normal_status_t结构体
class normal_status_t(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("header", header_t),
        ("ACU_status", ctypes.c_uint32), #4 个字节
        ("antenna_problem_status", ctypes.c_uint16),
        ("mode", ctypes.c_uint8),
        ("az_speed", ctypes.c_double),
        ("el_speed", ctypes.c_double),
        ("feedback", ctypes.c_uint8),
        ("feed_status", ctypes.c_uint16),
        ("feed_real_angle", ctypes.c_double),
        ("feed_speed", ctypes.c_double),
        ("ending", ending_t),
    ]


# 定义ant_control_command_t结构体
class ant_control_command_t(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("header", header_t),
        ("mode", ctypes.c_uint8),
        ("childmode", ctypes.c_uint8),
        ("param", ctypes.c_double * 2),  # az, el
        ("cw_ccw", ctypes.c_uint8),
        ("ending", ending_t),
    ]


# 定义ant_control_command_t2结构体（注意：这里结构体名称与上一个重复，可能需要更改）
class ant_control_command_t2(ctypes.Structure):
    _pack_ = 1 # 这里的1表示字节对齐方式为1字节
    _fields_ = [
        ("header", header_t),
        ("mode", ctypes.c_uint8),
        ("childmode", ctypes.c_uint8),
        ("az", ctypes.c_double * 3),  # p, v, a (position, velocity, acceleration) 8字节*3=24字节
        ("el", ctypes.c_double * 3),  # p, v, a
        ("cw_ccw", ctypes.c_uint8),
        ("ending", ending_t),
    ]




# 定义feed_control_command_t结构体
class feed_control_command_t(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("header", header_t),
        ("move_command", ctypes.c_uint8),
        ("move_position", ctypes.c_double),
        ("ending", ending_t),
    ]


# 定义rejection_frame_t结构体
class rejection_frame_t(ctypes.Structure):
    _fields_ = [
        ("header", header_t),
        ("rejection_category_code", ctypes.c_uint8),
        ("rejection_code", ctypes.c_uint8),
        ("ending", ending_t),
    ]

# 定义response_frame_t结构体（注意：这个结构体没有额外的字段，只有header和ending）
class response_frame_t(ctypes.Structure):
    _fields_ = [
        ("header", header_t),
        ("ending", ending_t),
    ]






# class ACUDriver(ctypes.Structure):
#     _fields_ = [
#         ("m_addr", ctypes.c_char * 128),
#         ("m_remote_port", ctypes.c_ushort),
#         ("m_local_port", ctypes.c_ushort),
#         ("high_rate_status", ctypes.POINTER(high_rate_status_t)),
#         ("normal_status", ctypes.POINTER(normal_status_t)),
#         ("rejection_frame", ctypes.POINTER(rejection_frame_t)),
#         ("response_frame", ctypes.POINTER(response_frame_t)),
#         ("ant_control_command", ctypes.POINTER(ant_control_command_t)),
#         ("ant_control_command2", ctypes.POINTER(ant_control_command_t2)),
#         ("feed_control_command", ctypes.POINTER(feed_control_command_t)),
#         ("thread_read", ctypes.c_void_p),
#     ]
#
#     def __init__(self, addr, remoteport, localport):
#         self.m_addr = addr.encode()
#         self.m_remote_port = remoteport
#         self.m_local_port = localport
#         self.high_rate_status = None
#         self.normal_status = None
#         self.rejection_frame = None
#         self.response_frame = None
#         self.ant_control_command = None
#         self.ant_control_command2 = None
#         self.feed_control_command = None
#         self.thread_read = None
#
#     def getStatus_50ms(self, statusvalues, error):
#         pass
#
#     def getStatus_50ms(self, HRS, error):
#         pass
#
#     def getStatus_1s(self, acustatus, error):
#         pass
#
#     def getStatus_1s(self, AS, error):
#         pass
#
#     def setAntCon(self, mode, childmode, control, azcir, error):
#         pass
#
#     def setAntCon2(self, mode, childmode, control, azcir, error):
#         pass
#
#     def setFeed(self, command, angle, error):
#         pass
#
#     def getRejection(self, rejectionstatus, error):
#         pass
#
#     def getRejection(self, RF, error):
#         pass
#
#     def setStandBy(self, error):
#         pass
#
#     def moveToAccessPosition(self, error):
#         pass
#
#     def setAzElCmd_azel(self, az, el, azcir, error):
#         pass
#
#     def setAzElPVA(self, azp, azv, aza, elp, elv, ela, azcir, error):
#         pass



# # 定义所需的C数据类型
# c_char_p = ctypes.POINTER(ctypes.c_char)
# c_double_p = ctypes.POINTER(ctypes.c_double)
# c_ushort = ctypes.c_uint16
#
#
# class Mutex:
#     pass  # 这里留空，因为具体的Mutex实现取决于你的环境或库
#
#
# class UDPClient:
#     pass  # 这里留空，因为具体的UDPClient实现需要在别的地方定义
#
#
# class ACUDriver:
#     def __init__(self, addr: str, remoteport: int, localport: int):
#         self._mutex_50ms = Mutex()
#         self._mutex_1s = Mutex()
#         self._mutex_command = Mutex()
#         self.client = UDPClient()
#         self.m_addr = ctypes.create_string_buffer(addr.encode())
#         self.high_rate_status = ctypes.pointer(high_rate_status_t())
#         self.normal_status = ctypes.pointer(normal_status_t())
#         self.rejection_frame = ctypes.pointer(rejection_frame_t())
#         self.response_frame = ctypes.pointer(response_frame_t())
#         self.ant_control_command = ctypes.pointer(ant_control_command_t())
#         self.ant_control_command2 = ctypes.pointer(ant_control_command_t2())
#         self.feed_control_command = ctypes.pointer(feed_control_command_t())
#         self.m_remote_port = remoteport
#         self.m_local_port = localport
#         self.thread_read = Thread(target=self.loop)  # 假设你有一个Thread类可用
#
#     def loop(self):
#         pass  # 实现循环逻辑
#
#     def getStatus_50ms(self, statusvalues: dict, error: str):
#         pass  # 实现getStatus_50ms逻辑
#
#     def getStatus_50ms(self, HRS: ctypes.POINTER(high_rate_status_t), error: str):
#         pass  # 实现getStatus_50ms逻辑
#
#     # 类似的，为其他函数添加Python包装器...
#
#     def setAntCon(self, mode: int, childmode: int, control: list, azcir: int, error: str):
#         control_array = (ctypes.c_double * len(control))(*control)
#         pass  # 实现setAntCon逻辑
#
#     def setAntCon2(self, mode: int, childmode: int, control: list, azcir: int, error: str):
#         control_array = (ctypes.c_double * len(control))(*control)
#         pass  # 实现setAntCon2逻辑