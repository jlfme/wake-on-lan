#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# ---------------------------------------
# Created by: Jlfme<jlfgeek@gmail.com>
# Created on: 2015-04-09 20:48:18
# ---------------------------------------


import struct
import socket


def wake_on_lan(mac, options='local'):

    mac = mac.replace(':', '').replace('-', '')  # mac地址格式化
    print(mac)

    # Magic Packet开头是6个FF
    packet_header = struct.pack('!B', 0xFF) * 6

    # 存储mac地址，每2位十六进制为一组
    mac_packet = []
    for i in range(0, 12, 2):
        mac_packet.append(int(mac[i:i+2], 16))

    # Magic Packet结尾是16个MAC地址
    packet_end = struct.pack('!BBBBBB', *mac_packet) * 16

    # 要发送的完整Magic Packet
    magic_packet = packet_header + packet_end

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if options == 'local':
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        address = ('255.255.255.255', 7)
    elif options == 'internet':
        address = ('118.114.208.186', 4343)
    else:
        address = ('255.255.255.255', 7)

    try:
        s.sendto(magic_packet, address)
        print("唤醒数据包发送完成", address, mac)
    except Exception as e:
        print("发送数据出错!", e)
    finally:
        s.close()


if __name__ == '__main__':
    wake_on_lan('AC-9E-17-81-34-32', options='internet')
