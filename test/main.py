import sys
import json
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
second_4_2_form_path = os.path.join(path, "ui", "4-2.ui")

main_form_class = uic.loadUiType(main_form_path)[0]
second_1_1_form_class = uic.loadUiType(second_1_1_form_path)[0]
second_1_2_form_class = uic.loadUiType(second_1_2_form_path)[0]
second_2_1_form_class = uic.loadUiType(second_2_1_form_path)[0]
second_2_2_form_class = uic.loadUiType(second_2_2_form_path)[0]
second_3_1_form_class = uic.loadUiType(second_3_1_form_path)[0]
second_3_2_form_class = uic.loadUiType(second_3_2_form_path)[0]
second_4_1_form_class = uic.loadUiType(second_4_1_form_path)[0]
second_4_2_form_class = uic.loadUiType(second_4_2_form_path)[0]

class Main_UI(QMainWindow, main_form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton1.clicked.connect(self.makeFunction)
        self.pushButton2.clicked.connect(self.time_attack_Function)
        self.pushButton3.clicked.connect(self.playFunction)
        self.pushButton4.clicked.connect(self.aiFunction)
        self.pushButton5.clicked.connect(self.exiteFunction)

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
    
    def aiFunction(self) :
        self.close()
        self.new_window = Ai_UI()
        self.new_window.show()

    def exiteFunction(self) :
        exit()

class Make_UI(QMainWindow, second_1_1_form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.backButton.clicked.connect(self.backFunction)
        self.selectbutton.clicked.connect(self.Function)
        self.select_pan.returnPressed.connect(self.Function)

    def Function(self) :
        # 크기 값을 입력받음
        try :
            text = int(self.select_pan.text())
            if text >=1 and text <= 20 :
                make_grid_instance = Make_grid()  # Make_grid 클래스의 인스턴스 생성
                make_grid_instance.set_size(text)  # set_size 메서드 호출
                self.close()
                self.new_window = make_grid_instance
                self.new_window.show()
            else :                
                QMessageBox.information(self, "오류!", "값 입력에 실패했습니다.\n숫자가 제대로 입력되었는지 확인해주세요.\n1~20까지의 수만 입력이 가능합니다.")
        except :
            QMessageBox.information(self, "오류!", "값 입력에 실패했습니다.\n숫자가 제대로 입력되었는지 확인해주세요.\n1~20까지의 수만 입력이 가능합니다.")


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
                button.setStyleSheet('background-color: white')
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
        # 이중 for문을 통해 힌트 계산

        # 힌트를 생성하는 함수
        hints = {"rows": [], "columns": []}
        size = len(self.grid)

        # 행 힌트 계산
        for i in range(size):
            row_hint = []
            count = 0
            for j in range(size):
                if self.grid[i][j] == 1:
                    count += 1
                elif count > 0:
                    row_hint.append(count)
                    count = 0
            if count > 0:
                row_hint.append(count)
            hints["rows"].append(row_hint if row_hint else [0])

        # 열 힌트 계산
        for j in range(size):
            col_hint = []
            count = 0
            for i in range(size):
                if self.grid[i][j] == 1:
                    count += 1
                elif count > 0:
                    col_hint.append(count)
                    count = 0
            if count > 0:
                col_hint.append(count)
            hints["columns"].append(col_hint if col_hint else [0])

        return hints
    
    def saveFunction(self):

        puzzle_directory = os.path.join(path, "puzzle")
        time_directory = os.path.join(path, "time")
        hint_directory = os.path.join(path, "hint")

        # 해당 디렉토리가 없으면 생성
        if not os.path.exists(puzzle_directory):
            os.makedirs(puzzle_directory)
        if not os.path.exists(time_directory):
            os.makedirs(time_directory)
        if not os.path.exists(hint_directory):
            os.makedirs(hint_directory)

        # 고유 이름의 파일
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        # 파일 경로 지정
        file_path = os.path.join(puzzle_directory, f"puzzle_{current_time}.txt")
        hint_path = os.path.join(hint_directory, f"hint_{current_time}.txt")

        puzzle_data = {
            'grid': self.grid,
        }
        hint_data = {
            'hints': self.generate_hint()
        }
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(puzzle_data, f, ensure_ascii=False, indent=4)
        with open(hint_path, 'w', encoding='utf-8') as f:
            json.dump(hint_data, f, ensure_ascii=False, indent=4)
        self.close()
        self.new_window = Main_UI()
        self.new_window.show()

    def backFunction(self) :
        self.close()
        self.new_window = Make_UI()
        self.new_window.show()


class Time_UI(QMainWindow, second_2_1_form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.backButton.clicked.connect(self.backFunction)
        self.time_attack() # 생성자에서 time_attack 메서드 호출

    def time_attack(self):
        file_count = count_puzzle_files()

        layout = QGridLayout()  # 버튼을 배치할 그리드 레이아웃 생성

        # 버튼을 2개씩 생성하여 배치
        for i in range(file_count):
            row = i // 2  # 행 계산 (나누기 2)
            col = (i % 2) * 2  # 열 계산 (0 또는 2)
            
            button1 = QPushButton(f"Puzzle{i+1}", self)
            button1.clicked.connect(lambda _, x=2*i: self.puzzle_button_clicked(x))
            layout.addWidget(button1, row, col)  # 첫 번째 버튼 추가

            # 다음 열에 두 번째 버튼 추가
            button2 = QPushButton(f"Puzzle{i+1} Ranking", self)
            button2.clicked.connect(lambda _, x=2*i + 1: self.puzzle_button_clicked(x))
            layout.addWidget(button2, row, col + 1)

        # 기존 레이아웃 제거 및 새로운 레이아웃 설정
        if self.scrollAreaWidgetContents.layout():
            QWidget().setLayout(self.scrollAreaWidgetContents.layout())
        self.scrollAreaWidgetContents.setLayout(layout)

    def puzzle_button_clicked(self, index):
        puzzle_files = index_puzzle_files()  # 퍼즐 파일 목록을 불러옵니다.
        puzzle_directory = os.path.join(path, "puzzle")
        time_files = index_time_files()
        time_directory = os.path.join(path, "time")
        hint_files = index_hint_files()
        hint_directory = os.path.join(path, "hint")
        print(f"Puzzle Button {index + 1} clicked.")  # 버튼 클릭 이벤트 핸들러 구현
        if (index + 1) % 2:
            selected_puzzle_file = puzzle_files[(index // 2)]  # 선택된 퍼즐 파일
            selected_hint_file = hint_files[(index // 2)]  # 선택된 힌트 파일
            selected_puzzle_path = os.path.join(puzzle_directory, selected_puzzle_file)
            selected_hint_path = os.path.join(hint_directory, selected_hint_file)
            self.close()
            self.new_window = make_Time(selected_puzzle_path, selected_puzzle_file, selected_hint_path)  # selected_puzzle_file을 전달합니다.
            self.new_window.show()
        else:
            selected_puzzle_file = puzzle_files[(index // 2)]  # 선택된 퍼즐 파일에 해당하는 타임 파일을 매칭
            time_file_name = os.path.splitext(selected_puzzle_file)[0] + "_time.txt"  # 타임 파일 이름 생성
            selected_time_path = os.path.join(time_directory, time_file_name)
            if os.path.exists(selected_time_path):
                with open(selected_time_path, 'r') as file:
                    ranking_data = file.readlines()  # 파일의 각 줄을 리스트로 읽기
                    if ranking_data:  # 빈 파일이 아닌 경우
                        time = []
                        for time_line in ranking_data:
                            start_time = time_line.index(":") + 1
                            end_time = time_line.index("}")
                            time_value = float(time_line[start_time:end_time].strip())
                            time.append(time_value)
                        ranking_data = [(time.strip()) for time in ranking_data]
                        # 리스트를 정렬
                        sorted_ranking = sorted(time)
                        # 순위와 시간을 함께 출력
                        ranking_str = '\n'.join([f"{idx + 1}. {time} sec" for idx, time in enumerate(sorted_ranking)])
                        QMessageBox.information(self, f"{(index // 2) + 1} Ranking", ranking_str)
            else:
                QMessageBox.information(self, f"{(index // 2) + 1} Ranking", "No ranking data available.")

    def backFunction(self):
        self.close()
        self.new_window = Main_UI()
        self.new_window.show()


class make_Time(QMainWindow, second_2_2_form_class):
    def __init__(self, selected_puzzle_path, selected_puzzle_file, selected_hint_path):
        super().__init__()
        self.setupUi(self)
        self.backButton.clicked.connect(self.backFunction)
        self.life = 3
        self.set_timer = 600        # 10분 타이머 설정
        self.load_puzzle(selected_puzzle_path, selected_hint_path)
        self.selected_puzzle_file = selected_puzzle_file

    def load_puzzle(self, selected_puzzle_path, selected_hint_path):
        with open(selected_puzzle_path, 'r') as file:
            self.current_puzzle = json.load(file)
        with open(selected_hint_path, 'r') as file:
            self.hints = json.load(file)["hints"]
        self.life = 3
        self.update_life()
        self.game_grid = self.current_puzzle['grid']
        size = len(self.game_grid)
        self.game_buttons = []
        self.real_time = self.set_timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(10)  

        for i in reversed(range(self.logic_pan.count())):  # 퍼즐 그리드 초기화
            widget = self.logic_pan.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        self.display_hints(size)
        self.create_puzzle_grid(size)

    def display_hints(self, size):
        row_hints = self.hints["rows"]
        col_hints = self.hints["columns"]

        for i in range(size):
            hint_label = QLabel(' '.join(map(str, row_hints[i])))
            self.logic_pan.addWidget(hint_label, i + 1, 0)

        for j in range(size):
            hint_label = QLabel(' '.join(map(str, col_hints[j])))
            self.logic_pan.addWidget(hint_label, 0, j + 1)

    def create_puzzle_grid(self, size):
        for i in range(size):
            row_buttons = []
            for j in range(size):
                button = QPushButton()
                button.setCheckable(True)
                button.setStyleSheet('background-color: white')
                button.clicked.connect(self.create_button_handler(i, j))
                button_size = min(600 // size, 600 // size)  # 퍼즐 크기에 따라 버튼 크기 조정
                button.setFixedSize(button_size, button_size)
                self.logic_pan.addWidget(button, i + 1, j + 1)
                row_buttons.append(button)
            self.game_buttons.append(row_buttons)

    def create_button_handler(self, x, y):
        def handler():
            self.check_answer(x, y)
        return handler
    
    def update_time(self):
        self.real_time -= 0.01  # real_time 값을 1씩 감소시킵니다.
        minutes, seconds = divmod(self.real_time, 60)
        time_text = f"{minutes:02.0f}:{seconds:02.2f}"
        self.time.setText(f"time: {time_text}")
        if self.real_time <= 0:
            self.timer.stop()
            QMessageBox.information(self, "!시간종료!", "문제 풀이에 실패했습니다.")
            self.close()
            self.new_window = Time_UI()
            self.new_window.show()

    def check_answer(self, x, y):
        if self.game_grid[x][y] == 1:
            self.game_buttons[x][y].setStyleSheet('background-color: black')
        else:
            self.life -= 1
            self.update_life()
            if self.life == 0:
                self.fail()
            return

        if check_clear(self.game_grid, self.game_buttons):
            self.time_save_file('time')
            QMessageBox.information(self, "Clear!", "정답입니다")
            self.close()
            self.new_window = Time_UI()
            self.new_window.show()

    def update_life(self):
        self.heart.setText(f"life: {self.life}")

    def fail(self):
        QMessageBox.information(self, "Game Over", "체력이 없습니다.")
        self.close()
        self.new_window = Time_UI()
        self.new_window.show()

    def backFunction(self):
        self.close()
        self.new_window = Main_UI()
        self.new_window.show()

    def time_save_file(self, index):
        time_path = os.path.join(path, "time")

        # time 디렉토리가 없는 경우 생성, 디렉토리 파일이 이미 존재해도 오류 발생하지 않음
        if not os.path.exists(time_path):
            os.makedirs(time_path)

        # index 사용하여 고유한 파일 이름 생성
        # file_name, file_extension 분리 ex) a.json 파일에 index 1인 경우 a.1.json 저장
        file_name, file_extension = os.path.splitext(self.selected_puzzle_file)
        indexed_file_name = f"{file_name}_{index}{file_extension}"
        
        selected_time_path = os.path.join(time_path, indexed_file_name)
        #소수점 반올림
        r_time = round(self.set_timer - self.real_time, 2)
        time_data = {"real_time": r_time}

        # 파일에 새로운 줄로 추가 (append)
        with open(selected_time_path, "a") as file:
            file.write(json.dumps(time_data) + "\n")


class Stage_UI(QMainWindow, second_3_1_form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.backButton.clicked.connect(self.backFunction)
        self.stage_button()

    def stage_button(self):
        file_count = count_puzzle_files()

        layout = QGridLayout()  # 버튼을 배치할 그리드 레이아웃 생성

        for i in range(file_count):
            row = i // 3  # 행 계산
            col = i % 3   # 열 계산
            button = QPushButton(f"Puzzle {i + 1}", self)
            button.clicked.connect(lambda _, x=i: self.puzzle_button_clicked(x))
            layout.addWidget(button, row, col)  # 그리드 레이아웃에 버튼 추가

        # 기존 레이아웃 제거 및 새로운 레이아웃 설정
        if self.scrollAreaWidgetContents.layout():
            QWidget().setLayout(self.scrollAreaWidgetContents.layout())
        self.scrollAreaWidgetContents.setLayout(layout)

    def puzzle_button_clicked(self, index):
        # 퍼즐 파일 목록을 가져옴
        puzzle_files = index_puzzle_files()
        puzzle_directory = os.path.join(path, "puzzle") # 퍼즐 파일이 위치한 디렉토리
        hint_files = index_hint_files()
        hint_directory = os.path.join(path, "hint") #힌트 파일 디렉토리
        
        # 인덱스가 퍼즐 파일 개수 이내에 있는지 확인
        if 0 <= index < len(puzzle_files):
            selected_puzzle_file = puzzle_files[index]  # 선택된 퍼즐 파일
            selected_hint_file = hint_files[index]  #선택된 힌트 파일

            # 선택된 퍼즐 파일 경로
            selected_puzzle_path = os.path.join(puzzle_directory, selected_puzzle_file)
            selected_hint_path = os.path.join(hint_directory, selected_hint_file)

            # 선택된 퍼즐 파일을 불러오는 함수 호출 (예시로 print 함수를 사용)
            print("Selected puzzle file:", selected_puzzle_path)
            self.close()
            self.new_window = make_stage(selected_puzzle_path, selected_hint_path)
            self.new_window.show()
            
        else:
            print("Invalid puzzle index")

    def backFunction(self):
        self.close()
        self.new_window = Main_UI()
        self.new_window.show()

class make_stage(QMainWindow, second_3_2_form_class):
    def __init__(self, selected_puzzle_path, selected_hint_path):
        super().__init__()
        self.setupUi(self)
        self.backButton.clicked.connect(self.backFunction)
        self.life = 3
        self.load_puzzle(selected_puzzle_path, selected_hint_path)

    def load_puzzle(self, selected_puzzle_path, selected_hint_path):
        with open(selected_puzzle_path, 'r') as file:
            self.current_puzzle = json.load(file)
        with open(selected_hint_path, 'r') as file:
            self.hints = json.load(file)["hints"]
        self.life = 3
        self.update_life()
        self.game_grid = self.current_puzzle['grid']
        size = len(self.game_grid)
        self.game_buttons = []

        for i in reversed(range(self.logic_pan.count())):  # 퍼즐 그리드 초기화
            widget = self.logic_pan.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        self.display_hints(size)
        self.create_puzzle_grid(size)

    def display_hints(self, size):
        row_hints = self.hints["rows"]
        col_hints = self.hints["columns"]  # Transpose for column hints

        for i in range(size):
            hint_label = QLabel(' '.join(map(str, row_hints[i])))
            self.logic_pan.addWidget(hint_label, i + 1, 0)

        for j in range(size):
            hint_label = QLabel(' '.join(map(str, col_hints[j])))
            self.logic_pan.addWidget(hint_label, 0, j + 1)

    def create_puzzle_grid(self, size):
        for i in range(size):
            row_buttons = []
            for j in range(size):
                button = QPushButton()
                button.setCheckable(True)
                button.setStyleSheet('background-color: white')
                button.clicked.connect(self.create_button_handler(i, j))
                button_size = min(600 // size, 600 // size)  # 퍼즐 크기에 따라 버튼 크기 조정
                button.setFixedSize(button_size, button_size)
                self.logic_pan.addWidget(button, i + 1, j + 1)
                row_buttons.append(button)
            self.game_buttons.append(row_buttons)

    def create_button_handler(self, x, y):
        def handler():
            self.check_answer(x, y)
        return handler

    def check_answer(self, x, y):
        if self.game_grid[x][y] == 1:
            self.game_buttons[x][y].setStyleSheet('background-color: black')
        else:
            self.life -= 1
            self.update_life()
            if self.life == 0:
                self.fail()
            return

        if check_clear(self.game_grid, self.game_buttons):
            QMessageBox.information(self, "Clear!", "정답입니다")
            self.close()
            self.new_window = Stage_UI()
            self.new_window.show()

    def update_life(self):
        self.heart.setText(f"life: {self.life}")

    def fail(self):
        QMessageBox.information(self, "Game Over", "체력이 없습니다.")
        self.close()
        self.new_window = Stage_UI()
        self.new_window.show()

    def backFunction(self):
        self.close()
        self.new_window = Main_UI()
        self.new_window.show()

class Ai_UI(QMainWindow, second_4_1_form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.backButton.clicked.connect(self.backFunction)
        self.stage_button()

    def stage_button(self):
        file_count = count_puzzle_files()
        layout = QGridLayout()  # 버튼을 배치할 그리드 레이아웃 생성

        for i in range(file_count):
            row = i // 3  # 행 계산
            col = i % 3   # 열 계산
            button = QPushButton(f"Puzzle {i + 1}", self)
            button.clicked.connect(lambda _, x=i: self.puzzle_button_clicked(x))
            layout.addWidget(button, row, col)  # 그리드 레이아웃에 버튼 추가

        # 기존 레이아웃 제거 및 새로운 레이아웃 설정
        if self.scrollAreaWidgetContents.layout():
            QWidget().setLayout(self.scrollAreaWidgetContents.layout())
        self.scrollAreaWidgetContents.setLayout(layout)

    def puzzle_button_clicked(self, index):
        # 퍼즐 파일 목록을 가져옴
        puzzle_files = index_puzzle_files()
        
        # 인덱스가 퍼즐 파일 개수 이내에 있는지 확인
        if 0 <= index < len(puzzle_files):
            selected_puzzle_file = puzzle_files[index]  # 선택된 퍼즐 파일
            puzzle_directory = os.path.join(path, "puzzle")  # 퍼즐 파일이 위치한 디렉토리

            # 선택된 퍼즐 파일 경로
            selected_puzzle_path = os.path.join(puzzle_directory, selected_puzzle_file)

            # 선택된 퍼즐 파일을 불러오는 함수 호출 (예시로 print 함수를 사용)
            print("Selected puzzle file:", selected_puzzle_path)
            self.close()
            self.new_window = ai_stage(selected_puzzle_path)
            self.new_window.show()
            
        else:
            print("Invalid puzzle index")

    def backFunction(self):
        self.close()
        self.new_window = Main_UI()
        self.new_window.show()

class ai_stage(QMainWindow, second_4_2_form_class):
    def __init__(self, selected_puzzle_path):
        super().__init__()
        self.setupUi(self)
        self.backButton.clicked.connect(self.backFunction)
        self.load_puzzle(selected_puzzle_path)

    def load_puzzle(self, selected_puzzle_path):
        with open(selected_puzzle_path, 'r') as file:
            self.current_puzzle = json.load(file)
        self.game_grid = self.current_puzzle['grid']  # 퍼즐 그리드
        size = len(self.game_grid)
        self.game_buttons = []

        for i in reversed(range(self.logic_pan.count())):  # 퍼즐 그리드 초기화
            widget = self.logic_pan.itemAt(i).widget()
            if widget:
                widget.setParent(None)
                
        self.display_hints(size)
        self.create_puzzle_grid(size)
        self.search_graph(size)

    def display_hints(self, size):
        hints = self.generate_hint()  # DFS 방식으로 힌트 생성
        row_hints = hints["rows"]
        col_hints = hints["columns"]

        for i in range(size):
            hint_label = QLabel(' '.join(map(str, row_hints[i])))
            self.logic_pan.addWidget(hint_label, i + 1, 0)

        for j in range(size):
            hint_label = QLabel(' '.join(map(str, col_hints[j])))
            self.logic_pan.addWidget(hint_label, 0, j + 1)

    def generate_hint(self):
        # 힌트를 생성하는 함수
        hints = {"rows": [], "columns": []}
        size = len(self.game_grid)

        # DFS를 이용하여 힌트 계산
        def dfs(x, y, visited, direction):
            if not (0 <= x < size and 0 <= y < size):  # 그리드 범위를 벗어난 경우
                return 0
            if visited[x][y] or self.game_grid[x][y] == 0:  # 이미 방문했거나 값이 0인 경우
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
                if self.game_grid[i][j] == 1 and not visited[i][j]:  # 방문하지 않은 1인 경우
                    len_R = dfs(i, j, visited, [(0, 1), (0, -1)])  # DFS 호출
                    if len_R > 0:
                        row_hint.append(len_R)
            hints["rows"].append(row_hint if row_hint else [0])  # 힌트 추가

        # 열 힌트 계산
        for j in range(size):
            col_hint = []
            visited = [[False] * size for _ in range(size)]  # 방문 배열 초기화
            for i in range(size):
                if self.game_grid[i][j] == 1 and not visited[i][j]:  # 방문하지 않은 1인 경우
                    len_C = dfs(i, j, visited, [(1, 0), (-1, 0)])  # DFS 호출
                    if len_C > 0:
                        col_hint.append(len_C)
            hints["columns"].append(col_hint if col_hint else [0])  # 힌트 추가

        return hints

    def create_puzzle_grid(self, size):
        self.game_buttons = []  # 게임 버튼 초기화
        for i in range(size):
            row_buttons = []
            for j in range(size):
                button = QPushButton()
                button.setCheckable(True)
                button.setStyleSheet('background-color: white')
                button.clicked.connect(self.create_button_handler(i, j))
                button_size = min(600 // size, 600 // size)  # 퍼즐 크기에 따라 버튼 크기 조정
                button.setFixedSize(button_size, button_size)
                self.logic_pan.addWidget(button, i + 1, j + 1)
                row_buttons.append(button)
            self.game_buttons.append(row_buttons)

    def create_button_handler(self, x, y):
        def handler():
            self.check(x, y)
        return handler

    def search_graph(self, size):
        for i in range(size):
            for j in range(size):
                self.check(i, j)
                
    def check(self, x, y):
        if x < 0 or x >= len(self.game_grid) or y < 0 or y >= len(self.game_grid):
            return  # 범위를 벗어나는 경우

        if self.game_grid[x][y] == 1:  # 체크되어 있다면
            self.game_buttons[x][y].setStyleSheet('background-color: black')

        if check_clear(self.game_grid, self.game_buttons):
            QMessageBox.information(self, "Clear!", "자동풀이 완료")
            self.close()
            self.new_window = Ai_UI()
            self.new_window.show()
    
    def backFunction(self):
        self.close()
        self.new_window = Main_UI()
        self.new_window.show()

def check_clear(game_grid, game_buttons):
    for i in range(len(game_grid)):
        for j in range(len(game_grid[i])):
            if game_grid[i][j] == 1 and not game_buttons[i][j].isChecked():
                return False
    return True

def count_puzzle_files(): # 퍼즐 파일 개수 세는 함수
        
        puzzle_directory = os.path.join(path, "puzzle")
        if not os.path.exists(puzzle_directory):
            return 0

        # puzzle 디렉토리 내의 파일 목록을 가져와서 ".txt" 확장자를 가진 파일 개수를 셈
        puzzle_files = [f for f in os.listdir(puzzle_directory) if f.endswith(".txt")]
        return len(puzzle_files)

def index_puzzle_files() :

    puzzle_dir = os.path.join(path, "puzzle")

    # puzzle_dir 디렉토리에 있는 파일과 디렉토리 목록을 가져옵니다.
    puzzle_files = os.listdir(puzzle_dir)

    # 파일 목록(files) 중에서 확장자가 '.txt'인 파일들만 필터링하여 txt_file 리스트에 저장합니다.
    puzzle_txt_file = [f for f in puzzle_files if f.endswith('.txt')]

    # txt_file 리스트에 있는 파일들을 수정된 시간을 기준으로 내림차순으로 정렬합니다.
    # 정렬 기준은 파일의 수정 시간(os.path.getmtime)을 사용합니다.
    # reverse=True 옵션을 통해 내림차순으로 정렬합니다.
    puzzle_txt_file.sort(key=lambda x: os.path.getmtime(os.path.join(puzzle_dir, x)), reverse=True)

    # 정렬된 파일 리스트를 반환합니다.
    return puzzle_txt_file

def index_time_files() :

    time_dir = os.path.join(path, "time")

    time_files = os.listdir(time_dir)

    time_txt_file = [f for f in time_files if f.endswith('.txt')]
    time_txt_file.sort(key=lambda x: os.path.getmtime(os.path.join(time_dir, x)), reverse=True)

    return time_txt_file

def index_hint_files() :

    hint_dir = os.path.join(path, "hint")

    hint_files = os.listdir(hint_dir)

    hint_txt_file = [f for f in hint_files if f.endswith('.txt')]
    hint_txt_file.sort(key=lambda x: os.path.getmtime(os.path.join(hint_dir, x)), reverse=True)

    return hint_txt_file


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
