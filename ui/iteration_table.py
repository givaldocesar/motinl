from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTableWidget, 
                             QTableWidgetItem, QHeaderView)

class TableArea(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setLayout(QVBoxLayout(self))

        label_table = QLabel("Histórico de iterações: ")
        self.layout().addWidget(label_table)

        self.table = QTableWidget(parent=self)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.layout().addWidget(self.table)

    def update_table_headers(self, method):
        if method:
            self.table.clearContents()
            self.table.setRowCount(0)
            self.table.setColumnCount(method.num_colunas)
            self.table.setHorizontalHeaderLabels(method.headers)  

    def insert_row(self, data):
        row_idx = self.table.rowCount()
        self.table.insertRow(row_idx)

        #Adiciona os texto a coluna
        for column_idx, value in enumerate(data):
            self.table.setItem(row_idx, column_idx, QTableWidgetItem(value))
        
        return row_idx