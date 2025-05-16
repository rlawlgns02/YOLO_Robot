# YOLO_Robot

## 요구 사항

- Python 3.8 이상
- PyQt5
- pyserial

## 설치

필요한 패키지를 설치하려면 아래 명령어를 실행하세요:

```bash
pip install pyqt5 pyserial
```

## 사용법

`motion_controller.py`를 사용하여 특정 모션 ID를 실행하려면 다음과 같이 호출하세요:

```python
from motion_controller import execute_motion

# 시리얼 포트와 모션 ID를 지정하여 실행
execute_motion("COM3", 1)
```

- `port`: 로봇이 연결된 시리얼 포트 (예: "COM3").
- `motion_id`: 실행할 모션의 ID (정수).

## 예외 처리

시리얼 포트 오류가 발생하면 경고 메시지가 출력됩니다:
- GUI 환경에서는 `QMessageBox`로 경고를 표시합니다.
- CLI 환경에서는 오류 메시지를 출력합니다.
