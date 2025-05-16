# YOLO_Robot



## 요구 사항

- Python 3.8 이상
- PyQt5
- pyserial

## 실행 화면
![Image](https://github.com/user-attachments/assets/b9ea69c6-b2c9-4399-a505-8159505a4900)


 - 캠을 통해서 아무것도 인식 되지 않을경우 로봇은 가만히 대기
 - 캠을 통해서 포트홀을 인식할 경우 아래의 코드를 통해서 움직인다
`motion_controller.py`에 있는 `handle_pothole_detected` 함수를 이용해서 포트홀 감지시에 움직일 동작을 설정하세요:
```python
def handle_pothole_detected(self):
    print("포트홀 감지됨! 모션 실행")
    self.reset_timer.stop()
    self.exeHumanoidMotion(19) #감지 시에 동작할 모션 설정
```
## 설치

필요한 패키지를 설치하려면 아래 명령어를 실행하세요:

```bash
pip install -r requirements.txt
```
만약 설치가 안된다면 현재 경로와 requirements.txt 파일의 위치를 확인하고 이동해주세요


## 사용법

`motion_controller.py`를 사용하여 특정 모션 ID를 실행하려면 다음과 같이 호출하세요:

```python
from motion_controller import execute_motion

# 시리얼 포트와 모션 ID를 지정하여 실행
execute_motion("COM3", 1)
```

- `port`: 로봇이 연결된 시리얼 포트 (예: "COM3").
- `motion_id`: 실행할 모션의 ID (정수).

#시리얼 포트를 지정하지 않는 경우
-포트를 지정하지 않아도 프로그램을 실행하여 선택 가능
![Image](https://github.com/user-attachments/assets/a9a52cb8-158d-4fd4-a054-15251777a092)
![Image](https://github.com/user-attachments/assets/cf9b51f7-c989-402f-8683-c07dddf900d0)

## 예외 처리

시리얼 포트 오류가 발생하면 경고 메시지가 출력됩니다:
- GUI 환경에서는 `QMessageBox`로 경고를 표시합니다.
- CLI 환경에서는 오류 메시지를 출력합니다.
