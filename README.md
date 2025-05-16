# YOLO_Robot



## 요구 사항

- Python 3.8 이상
- PyQt5
- pyserial

## 실행 화면
![Image](https://github.com/user-attachments/assets/b9ea69c6-b2c9-4399-a505-8159505a4900)


 - 캠을 통해서 아무것도 인식 되지 않을경우 로봇은 가만히 대기
 - 캠을 통해서 포트홀을 인식할 경우 아래의 코드를 통해서 동작
# 
 
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

# 시리얼 포트를 지정하지 않는 경우
 - 포트를 지정하지 않아도 프로그램을 실행하여 선택 가능
![Image](https://github.com/user-attachments/assets/a9a52cb8-158d-4fd4-a054-15251777a092)
![Image](https://github.com/user-attachments/assets/cf9b51f7-c989-402f-8683-c07dddf900d0)

## 예외 처리

시리얼 포트 오류가 발생하면 경고 메시지가 출력됩니다:
- GUI 환경에서는 `QMessageBox`로 경고를 표시합니다.
- CLI 환경에서는 오류 메시지를 출력합니다.

## 학습 결과

### 1. 주요 지표

* **mAP@0.5:** 0.571 [cite: 6]
* **Precision (Confidence 0.788):** 1.00 [cite: 5]
* **Recall (Confidence 0.000):** 0.90 [cite: 7]
* **F1 Score (at Confidence 0.340):** 0.57 [cite: 2]

### 2. 성능 분석

* **Precision-Recall Curve:**
    * 전반적으로 우하향하는 경향을 보이며, 이는 Recall을 높이려고 할 때 Precision이 급격히 감소함을 의미합니다.  
    * 초반 Recall이 낮을 때는 Precision이 높지만, Recall이 증가함에 따라 Precision이 빠르게 감소하여 오탐이 증가하는 경향을 나타냅니다. [cite: 6]
* **Precision-Confidence Curve:**
    * Confidence가 높아질수록 Precision이 증가하지만, 특정 Confidence 이상에서는 Precision이 1.0에 도달합니다. [cite: 5]
* **Recall-Confidence Curve:**
    * Confidence가 낮아질수록 Recall이 증가하는 일반적인 경향을 보입니다. [cite: 7]
* **F1-Confidence Curve:**
    * F1 Score는 특정 Confidence 값에서 최대값을 가지며, Confidence가 너무 높거나 낮으면 성능이 저하됩니다. [cite: 2]

### 3. 혼동 행렬 (Confusion Matrix)

* 포트홀로 예측한 결과 중 62%가 실제 포트홀이었고, 38%는 배경으로 잘못 예측했습니다. [cite: 1]
* 배경으로 예측한 결과는 100%가 실제 배경이었습니다. [cite: 1]

### 4. 학습 과정

* **손실(Loss):**
    * `train/box_loss` 및 `val/box_loss`는 감소하는 경향을 보이며, 학습이 진행됨에 따라 bounding box 예측 성능이 향상됨을 나타냅니다. [cite: 8]
    * `train/obj_loss` 및 `val/obj_loss`는 objectness loss로, 물체가 있는지 없는지를 예측하는 손실입니다. [cite: 8]
* **지표(Metrics):**
    * `metrics/precision`, `metrics/recall`, `metrics/mAP_0.5`, `metrics/mAP_0.5:0.95`는 학습이 진행됨에 따라 증가하는 경향을 보이며, 모델의 성능이 향상됨을 나타냅니다. [cite: 8]

### 5. 레이블 분석

* 데이터셋의 레이블 분포 및 bounding box의 위치, 크기 등에 대한 분석 결과는 다음과 같습니다. [cite: 3, 4]

    * (레이블 분포, bounding box 위치/크기 관련 이미지 삽입 또는 분석 내용 요약)

### 6.  종합 의견 및 개선 방향

* 모델의 전반적인 성능은 mAP@0.5 = 0.571로, 개선의 여지가 있습니다.
* Precision과 Recall 간의 균형을 맞추는 것이 중요하며, 특히 오탐을 줄여 Precision을 높이는 방향으로 모델을 개선할 필요가 있습니다.
* 다양한 환경 조건에서의 데이터를 추가하여 모델의 일반화 성능을 향상시키는 것이 좋습니다.
