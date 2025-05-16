import os
import sys
import cv2
import torch
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5 import uic
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from serial_port_selector import SerialPortSelector
from motion_controller import execute_motion

# UI 파일 경로 설정
ui_file_path = os.path.join(os.path.dirname(__file__), "res", "mainWindow.ui")

try:
    form_mainWin = uic.loadUiType(ui_file_path)[0]
except FileNotFoundError:
    print(f"Error: UI file not found at {ui_file_path}")
    sys.exit(1)

class YOLOThread(QThread):
    pothole_detected = pyqtSignal()  # 포트홀 감지 시 신호
    no_pothole_detected = pyqtSignal()  # 포트홀이 감지되지 않을 때 신호
    frame_ready = pyqtSignal(QImage)  # 웹캠 프레임 신호

    def __init__(self, model_path, parent=None):
        super().__init__(parent)
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)
        self.running = True

    def run(self):
        cap = cv2.VideoCapture(0)  # 웹캠 열기
        while self.running:
            ret, frame = cap.read()
            if not ret:
                break

            # YOLOv5로 감지
            results = self.model(frame)
            detections = results.xyxy[0].cpu().numpy()

            # 포트홀 감지 여부 확인
            pothole_found = False
            for *box, conf, cls in detections:
                if int(cls) == 0:  # 포트홀 클래스 ID (YOLOv5 학습 시 설정한 ID)
                    pothole_found = True
                    self.pothole_detected.emit()  # 신호 발생
                    break

            if not pothole_found:
                self.no_pothole_detected.emit()  # 포트홀이 없을 때 신호

            # 프레임을 QImage로 변환하여 신호로 보냄
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_frame.shape
            qimg = QImage(rgb_frame.data, w, h, ch * w, QImage.Format_RGB888)
            self.frame_ready.emit(qimg)

        cap.release()

    def stop(self):
        self.running = False
        self.wait()
class MyWindow(QMainWindow, form_mainWin):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 실행 플래그 초기화
        self.motion_ready = False

        # YOLO 스레드 초기화
        model_path = r"best.pt"
        self.yolo_thread = YOLOThread(model_path)
        self.yolo_thread.pothole_detected.connect(self.handle_pothole_detected)
        self.yolo_thread.no_pothole_detected.connect(self.handle_no_pothole_detected)
        self.yolo_thread.frame_ready.connect(self.update_webcam_view)
        self.yolo_thread.start()

        # 기본 자세로 돌아가기 타이머
        self.reset_timer = QTimer(self)
        self.reset_timer.setInterval(3000)  # 3초 후 기본 자세로 복귀
        self.reset_timer.timeout.connect(self.reset_to_default_pose)

        # 포트찾기 버튼 클릭 이벤트 연결
        self.pushButton_6.clicked.connect(self.open_port_selector)

    def exeHumanoidMotion(self, motion_id):
        if not self.motion_ready:
            QMessageBox.warning(self, "Motion Error", "Motion is not ready. Please select a port first.")
            return

        # 모션 실행
        execute_motion(self.lblPort.text(), motion_id, self)

    def open_port_selector(self):
        # 포트 선택기 실행
        selected_port = SerialPortSelector.launch(self)
        if selected_port:
            print("선택한 포트:", selected_port)
            self.lblPort.setText(selected_port)
            # 포트가 선택되면 플래그 활성화
            self.motion_ready = True

    def handle_pothole_detected(self):
        print("포트홀 감지됨! 모션 실행")
        self.reset_timer.stop()  # 기본 자세 복귀 타이머 중지
        self.exeHumanoidMotion(19)

    def handle_no_pothole_detected(self):
        print("포트홀이 감지되지 않음. 기본 자세로 복귀 준비")
        self.reset_timer.start()  # 기본 자세 복귀 타이머 시작

    def reset_to_default_pose(self):
        print("기본 자세로 복귀")
        self.exeHumanoidMotion(0)  # 기본 자세 모션 ID

    def update_webcam_view(self, qimg):
        self.webcamLabel.setPixmap(QPixmap.fromImage(qimg))

    def closeEvent(self, event):
        # 창 닫힐 때 YOLO 스레드 종료
        self.yolo_thread.stop()
        event.accept()

# PyQt 애플리케이션 초기화
app = QApplication(sys.argv)

# 메인 윈도우 생성
window = MyWindow()
window.show()

# 애플리케이션 실행
sys.exit(app.exec_())