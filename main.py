import sys
import time
import json
import re
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import uic
from datetime import datetime

# 현재 py파일의 경로 path
path = os.path.join(os.path.dirname(__file__))

# UI 파일 연결
main_form_path = os.path.join(path, "ui", "홈화면.ui")
second_1_1_form_path = os.path.join(path, "ui", "1-1.ui")
second_1_2_form_path = os.path.join(path, "ui", "1-2.ui")
second_2_1_form_path = os.path.join(path, "ui", "2-1.ui")
second_2_2_form_path = os.path.join(path, "ui", "2-2.ui")
second_3_1_form_path = os.path.join(path, "ui", "3-1.ui")
second_3_2_form_path = os.path.join(path, "ui", "3-2.ui")
second_4_1_form_path = os.path.join(path, "ui", "4-1.ui")

main_form_class = uic.loadUiType(main_form_path)[0]
second_1_1_form_class = uic.loadUiType(second_1_1_form_path)[0]
second_1_2_form_class = uic.loadUiType(second_1_2_form_path)[0]
second_2_1_form_class = uic.loadUiType(second_2_1_form_path)[0]
second_2_2_form_class = uic.loadUiType(second_2_2_form_path)[0]
second_3_1_form_class = uic.loadUiType(second_3_1_form_path)[0]
second_3_2_form_class = uic.loadUiType(second_3_2_form_path)[0]
second_4_1_form_class = uic.loadUiType(second_4_1_form_path)[0]

class Main_UI(QMainWindow, main_form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton1.clicked.connect(self.makeFunction)
        self.pushButton2.clicked.connect(self.time_attack_Function)
        self.pushButton3.clicked.connect(self.playFunction)
        self.pushButton4.clicked.connect(self.exiteFunction)
       

    def makeFunction(self):
        self.close()
        self.new_window = Make_UI()
        self.new_window.show()

    def time_attack_Function(self) :
        self.close()
        self.new_window = Time_UI()
        self.new_window.show()

    def playFunction(self) :
        self.close()
        self.new_window = Stage_UI()
        self.new_window.show()

    def exiteFunction(self) :
        exit()

class Make_UI(QMainWindow, second_1_1_form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.backButton.clicked.connect(self.backFunction)
        self.selectbutton.clicked.connect(self.Function)
        self.select_pan = QTextEdit(self)
        self.select_pan.setText("원하는 판의 크기를 입력하시오")

    def Function(self) :
        pan = select_pan.toPlainText()
        make_grid_instance = Make_grid()  
        make_grid_instance.set_size(pan)  
        self.close()
        self.new_window = make_grid_instance
        self.new_window.show()
    
    def backFunction(self) :
        self.close()
        self.new_window = Main_UI()
        self.new_window.show()

class Make_grid(QMainWindow, second_1_2_form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.size_pan = 0  # 그리드 크기를 저장할 변수 초기화
        self.grid = []  # 그리드 데이터 초기화
        self.time = []  # 시간 데이터 초기화 (사용되지 않음)
        self.row_hint_labels = []  # 행 힌트 레이블을 저장할 리스트 초기화
        self.col_hint_labels = []  # 열 힌트 레이블을 저장할 리스트 초기화
        self.backButton.clicked.connect(self.backFunction)  # 뒤로 가기 버튼 클릭 시 처리할 함수 연결
        self.saveButton.clicked.connect(self.saveFunction)  # 저장 버튼 클릭 시 처리할 함수 연결

    def set_size(self, size):
        # 그리드 크기를 설정하고 그리드를 생성하는 함수
        self.size_pan = size  # 그리드 크기 설정
        self.create_grid(size)  # 설정된 크기로 그리드 생성

    def create_grid(self, size):
        # 그리드를 생성하는 함수
        # 기존 위젯 제거
        while self.logic_pan.count():
            child = self.logic_pan.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # 그리드 데이터 초기화
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.buttons = []  # 버튼 리스트 초기화

        # 그리드 버튼 생성 및 추가
        for i in range(size):
            row_buttons = []
            for j in range(size):
                button = QPushButton()
                button.setCheckable(True)  # 버튼을 체크 가능한 상태로 설정
                button.clicked.connect(self.create_button_handler(i, j))  # 버튼 클릭 시 이벤트 핸들러 연결
                button_size = min(600 // size, 600 // size)  # 버튼 크기 설정
                button.setFixedSize(button_size, button_size)
                self.logic_pan.addWidget(button, i, j)  # 레이아웃에 버튼 추가
                row_buttons.append(button)
            self.buttons.append(row_buttons)  # 버튼 리스트에 추가

        self.display_hints()  # 힌트 표시

    def create_button_handler(self, i, j):
        # 버튼 클릭 이벤트 핸들러 생성 함수
        def handler():
            if self.buttons[i][j].isChecked():  # 버튼이 체크된 경우
                self.grid[i][j] = 1  # 그리드 데이터 업데이트
                self.buttons[i][j].setStyleSheet('background-color: black')  # 버튼 색상 변경
            else:  # 버튼이 체크 해제된 경우
                self.grid[i][j] = 0  # 그리드 데이터 업데이트
                self.buttons[i][j].setStyleSheet('background-color: white')  # 버튼 색상 변경
            self.display_hints()  # 힌트 업데이트
        return handler

    def display_hints(self):
        # 힌트를 표시하는 함수
        # 기존 힌트 레이블 제거
        for label in self.row_hint_labels:
            self.logic_pan.removeWidget(label)
            label.deleteLater()
        self.row_hint_labels.clear()

        for label in self.col_hint_labels:
            self.logic_pan.removeWidget(label)
            label.deleteLater()
        self.col_hint_labels.clear()

        hints = self.generate_hint()  # 힌트 생성

        # 행 힌트 레이블 추가
        for i in range(len(self.grid)):
            hint_label = QLabel(' '.join(map(str, hints["rows"][i])))  # 힌트 레이블 생성
            hint_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)  # 레이블 정렬
            self.logic_pan.addWidget(hint_label, i, len(self.grid))  # 레이아웃에 레이블 추가
            self.row_hint_labels.append(hint_label)  # 리스트에 레이블 추가

        # 열 힌트 레이블 추가
        for j in range(len(self.grid)):
            hint_label = QLabel(' '.join(map(str, hints["columns"][j])))  # 힌트 레이블 생성
            self.logic_pan.addWidget(hint_label, len(self.grid), j)  # 레이아웃에 레이블 추가
            self.col_hint_labels.append(hint_label)  # 리스트에 레이블 추가

    def generate_hint(self):
        # 힌트를 생성하는 함수
        hints = {"rows": [], "columns": []}
        size = len(self.grid)

        # DFS를 이용하여 힌트 계산
        def dfs(x, y, visited, direction):
            if not (0 <= x < size and 0 <= y < size):  # 그리드 범위를 벗어난 경우
                return 0
            if visited[x][y] or self.grid[x][y] == 0:  # 이미 방문했거나 값이 0인 경우
                return 0
            visited[x][y] = True  # 방문 표시
            length = 1  # 길이 초기화
            for dx, dy in direction:  # 주어진 방향으로 이동
                nx, ny = x + dx, y + dy
                length += dfs(nx, ny, visited, direction)  # 재귀 호출
            return length

        # 행 힌트 계산
        for i in range(size):
            row_hint = []
            visited = [[False] * size for _ in range(size)]  # 방문 배열 초기화
            for j in range(size):
                if self.grid[i][j] == 1 and not visited[i][j]:  # 방문하지 않은 1인 경우
                    len_R = dfs(i, j, visited, [(0, 1), (0, -1)])  # DFS 호출
                    if len_R > 0:
                        row_hint.append(len_R)
            hints["rows"].append(row_hint if row_hint else [0])  # 힌트 추가

        # 열 힌트 계산
        for j in range(size):
            col_hint = []
            visited = [[False] * size for _ in range(size)]  # 방문 배열 초기화
            for i in range(size):
                if self.grid[i][j] == 1 and not visited[i][j]:  # 방문하지 않은 1인 경우
                    len_C = dfs(i, j, visited, [(1, 0), (-1, 0)])  # DFS 호출
                    if len_C > 0:
                        col_hint.append(len_C)
            hints["columns"].append(col_hint if col_hint else [0])  # 힌트 추가

        return hints
    
    def saveFunction(self):

        puzzle_directory = os.path.join(path, "puzzle")
        time_directory = os.path.join(path, "time")

        # 'puzzle' 디렉토리가 없으면 생성
        if not os.path.exists(puzzle_directory):
            os.makedirs(puzzle_directory)
        if not os.path.exists(time_directory):
            os.makedirs(time_directory)

        # 고유 이름의 파일
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        current_time_2 = datetime.now().strftime("%Y%m%d_%H%M%S")
        # 파일 경로 지정
        file_path = os.path.join(puzzle_directory, f"puzzle_{current_time}.txt")
        time_path = os.path.join(time_directory, f"time_{current_time_2}.txt")

        puzzle_data = {
            'grid': self.grid,
            'hints': self.generate_hint()
        }
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(puzzle_data, f, ensure_ascii=False, indent=4)
        open(time_path, 'w').close()

    def backFunction(self) :
        self.close()
        self.new_window = Make_UI()
        self.new_window.show()

class Time_UI(QMainWindow, second_2_1_form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.backButton.clicked.connect(self.backFunction)

    def backFunction(self) :
        self.close()
        self.new_window = Main_UI()
        self.new_window.show()
    
class Stage_UI(QMainWindow, second_3_1_form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.backButton.clicked.connect(self.backFunction)

    def backFunction(self) :
        self.close()
        self.new_window = Main_UI()
        self.new_window.show()

if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    widget = QStackedWidget()

    # WindowClass의 인스턴스 생성
    myWindow = Main_UI()

    # 프로그램 화면을 보여주는 코드
    myWindow.show()
    
    # 프로그램을 이벤트 루프로 진입시키는(프로그램을 작동시키는) 코드
    sys.exit(app.exec_())
    
