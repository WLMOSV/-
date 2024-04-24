import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit, QLabel, QPushButton, QTableWidget,
    QVBoxLayout, QHBoxLayout, QHeaderView, QComboBox, QMessageBox, QTabWidget,
    QTableWidgetItem
)
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# 读取数据
data_path = "HR_comma_sep.csv"  # 替换为您的数据文件路径
df = pd.read_csv(data_path, header=None)
df.columns = ["satisfaction_level", "last_evaluation", "number_project",
              "average_montly_hours", "time_spend_company", "Work_accident",
              "left", "promotion_last_5years", "sales", "salary"]


class DataAnalysisApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("数据分析")
        self.init_ui()

    def init_ui(self):
        # 创建选项卡
        tabs = QTabWidget()
        self.data_tab = QWidget()
        self.analysis_tab = QWidget()
        tabs.addTab(self.data_tab, "数据")
        tabs.addTab(self.analysis_tab, "分析")

        # 数据选项卡界面
        self.init_data_tab()

        # 分析选项卡界面
        self.init_analysis_tab()

        # 主布局
        main_layout = QVBoxLayout()
        main_layout.addWidget(tabs)
        self.setLayout(main_layout)

    def init_data_tab(self):
        # 筛选条件区域
        filter_layout = QHBoxLayout()

        # 创建下拉菜单选择列
        self.column_combobox = QComboBox()
        self.column_combobox.addItems(df.columns)
        filter_layout.addWidget(QLabel("选择列:"))
        filter_layout.addWidget(self.column_combobox)

        # 创建输入框输入筛选值
        self.filter_entry = QLineEdit()
        filter_layout.addWidget(QLabel("筛选值:"))
        filter_layout.addWidget(self.filter_entry)

        # 查询按钮
        query_button = QPushButton("查询")
        query_button.clicked.connect(self.perform_query)
        filter_layout.addWidget(query_button)

        # 数据清洗选项
        clean_label = QLabel("数据清洗:")
        clean_options = ["填充缺失值 (均值)"]
        self.clean_combobox = QComboBox()
        self.clean_combobox.addItems(clean_options)
        filter_layout.addWidget(clean_label)
        filter_layout.addWidget(self.clean_combobox)

        # 结果表格
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(len(df.columns))
        self.result_table.setHorizontalHeaderLabels(df.columns)
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.update_table(df)  # 默认显示所有数据

        # 数据选项卡布局
        data_layout = QVBoxLayout()
        data_layout.addLayout(filter_layout)
        data_layout.addWidget(self.result_table)
        self.data_tab.setLayout(data_layout)

    def init_analysis_tab(self):
        # 统计分析按钮
        analysis_button = QPushButton("描述性统计")
        analysis_button.clicked.connect(self.perform_analysis)

        # 相关性分析按钮
        correlation_button = QPushButton("相关性分析")
        correlation_button.clicked.connect(self.perform_correlation)

        # 图表显示区域
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        # 分析选项卡布局
        analysis_layout = QVBoxLayout()
        analysis_layout.addWidget(analysis_button)
        analysis_layout.addWidget(correlation_button)
        analysis_layout.addWidget(self.canvas)
        self.analysis_tab.setLayout(analysis_layout)

    def update_table(self, data):
        self.result_table.setRowCount(len(data))
        for i, row in data.iterrows():
            for j, val in enumerate(row):
                self.result_table.setItem(i, j, QTableWidgetItem(str(val)))

    def perform_query(self):
        # 获取筛选条件
        selected_column = self.column_combobox.currentText()
        value = self.filter_entry.text()

        # 应用筛选条件
        if value:
            filtered_df = df[df[selected_column] == value]
        else:
            filtered_df = df.copy()

        # 数据清洗
        clean_option = self.clean_combobox.currentText()
        if clean_option == "填充缺失值 (均值)":
            filtered_df.fillna(filtered_df.mean(), inplace=True)

        # 更新表格
        self.update_table(filtered_df)

    def perform_analysis(self):
        # 获取数值型列
        numeric_columns = df.select_dtypes(include=['number']).columns

        # 计算描述性统计信息
        descriptive_stats = df[numeric_columns].describe()

        # 显示统计结果 (使用 QMessageBox)
        stats_string = descriptive_stats.to_string()
        QMessageBox.information(self, "统计分析结果", stats_string)

    def perform_correlation(self):
        # 选择数值型列
        numeric_df = df.select_dtypes(include=['number'])

        # 计算相关系数
        corr_matrix = numeric_df.corr()

        # 绘制热力图
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    filter_app = DataAnalysisApp()
    filter_app.show()
    sys.exit(app.exec_())