import serial
from PyQt5.QtWidgets import QMessageBox

def execute_motion(port, motion_id, parent=None):
    # 모션 제어 패킷 생성
    packet_buff = [0xff, 0xff, 0x4c, 0x53,  # 헤더
                   0x00, 0x00, 0x00, 0x00,  # Destination ADD, Source ADD
                   0x30, 0x0c, 0x03,        # 명령어, 모션 실행, 파라미터 길이
                   motion_id, 0x00, 0x64,   # 모션 ID, 반복, 속도
                   0x00]                    # 체크섬

    # 체크섬 계산
    checksum = sum(packet_buff[6:14])
    packet_buff[14] = checksum

    # 시리얼 포트 열기 및 패킷 전송
    try:
        ser = serial.Serial(port, 115200, timeout=1)
        if ser.is_open:
            ser.write(packet_buff)
        else:
            raise serial.SerialException(f"Failed to open serial port {port}.")
    except serial.SerialException as e:
        if parent:
            QMessageBox.warning(parent, "Serial Port Error", str(e))
        else:
            print(f"Serial Port Error: {e}")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()