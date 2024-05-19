import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton

class PageSimulation(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("页面调度模拟")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.number_layout = QHBoxLayout()
        self.page_labels = []
        for i in range(32):
            label = QLabel(str(i + 1))
            label.setFixedSize(40, 40)
            label.setStyleSheet("background-color: red; color: white")
            self.page_labels.append(label)
            self.number_layout.addWidget(label)

        self.start_button = QPushButton("一次执行")
        self.start_button.clicked.connect(self.run_simulation)

        self.step_button = QPushButton("逐步执行")
        self.step_button.clicked.connect(self.step_execution)

        self.layout.addLayout(self.number_layout)

        self.page_fault_label = QLabel("缺页次数: 0")
        self.page_fault_rate_label = QLabel("缺页率: 0%")
        self.layout.addWidget(self.page_fault_label)
        self.layout.addWidget(self.page_fault_rate_label)

        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.step_button)

        self.memory_blocks = [-1, -1, -1, -1]  # 内存块，初始值为-1表示未调入
        self.page_fault_count = 0  # 缺页次数
        self.instruction_count = 0  # 调用的指令数
        self.pages_in_memory = 0


    def generate_next_instruction(self):
        m = random.randint(1, 318)
        m1 = random.randint(0, m - 1)
        m2 = random.randint(m1 + 2, 319)
        if m2<=319:
            return [m, m + 1, m1,  m1 + 1 , m2, m2 + 1]
        else:
            return [m, m + 1, m1,  m1 + 1 , m2, 0]

    def run_simulation(self):
        self.instruction_count = 0  # 初始化指令计数器
        self.page_fault_count = 0
        while self.instruction_count < 320:
            instructions = self.generate_next_instruction()
            for instruction_number in instructions:
                if self.instruction_count < 320:
                    self.instruction_count += 1
                    print(f"指令号：{instruction_number}")

                    page = (instruction_number - 1) // 10  # 计算所属页号

                    if self.pages_in_memory < 4:
                        if page not in self.memory_blocks:
                            self.page_fault_count += 1
                            self.memory_blocks[self.pages_in_memory] = page
                            self.page_labels[page].setStyleSheet("background-color: green; color: black")
                            self.pages_in_memory += 1
                    else:
                        if page not in self.memory_blocks:
                            # 发生缺页
                            self.page_fault_count += 1
                            page_to_replace = self.memory_blocks.pop(0)
                            self.memory_blocks.append(page)
                            self.page_labels[page].setStyleSheet("background-color: green; color: black")
                            self.page_labels[page_to_replace].setStyleSheet("background-color: red; color: white")

        self.page_fault_label.setText(f"缺页次数: {self.page_fault_count}")
        page_fault_rate = self.page_fault_count / 320 * 100
        self.page_fault_rate_label.setText(f"缺页率: {page_fault_rate:.2f}%")
        print(f"指令数目: {self.instruction_count}")
        self.instruction_count = 0  # 初始化指令计数器
        self.page_fault_count = 0

    def step_execution(self):
        if self.instruction_count < 320:
            instructions = self.generate_next_instruction()
            for instruction_number in instructions:
                if self.instruction_count < 320:
                    self.instruction_count += 1
                    print(f"指令号：{instruction_number}")

                    page = (instruction_number - 1) // 10  # 计算所属页号

                    if self.pages_in_memory < 4:
                        if page not in self.memory_blocks:
                            self.page_fault_count += 1
                            self.memory_blocks[self.pages_in_memory] = page
                            self.page_labels[page].setStyleSheet("background-color: green; color: black")
                            self.pages_in_memory += 1
                    else:
                        if page not in self.memory_blocks:
                            # 发生缺页
                            self.page_fault_count += 1
                            page_to_replace = self.memory_blocks.pop(0)
                            self.memory_blocks.append(page)
                            self.page_labels[page].setStyleSheet("background-color: green; color: black")
                            self.page_labels[page_to_replace].setStyleSheet("background-color: red; color: white")

            if self.instruction_count == 320:
                self.page_fault_label.setText(f"缺页次数: {self.page_fault_count}")
                page_fault_rate = self.page_fault_count / self.instruction_count * 100
                self.page_fault_rate_label.setText(f"缺页率: {page_fault_rate:.2f}%")
                print(f"指令数目: {self.instruction_count}")
            else:
                self.page_fault_label.setText(f"缺页次数: {self.page_fault_count}")
                self.page_fault_rate_label.setText("缺页率: 正在计算...")
                print(f"指令数目: {self.instruction_count}")

        else:
            self.instruction_count = 0  # 初始化指令计数器
            self.page_fault_count = 0
            self.step_button.setEnabled(False)


app = QApplication(sys.argv)
window = PageSimulation()
window.show()
sys.exit(app.exec_())
