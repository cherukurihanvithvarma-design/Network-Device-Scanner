import sys
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QMessageBox
)
from PyQt5.QtCore import Qt

from scanner import scan_network
from database import init_db, upsert_device
from event import add_event 


class ScanThread(QThread):
    finished = pyqtSignal(list)

    def run(self):
        devices = scan_network()
        self.finished.emit(devices)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        init_db()

        self.setWindowTitle("WIFI Scanner")
        self.setGeometry(300, 200, 700, 400)

        layout = QVBoxLayout()

        self.scan_button = QPushButton("Scan Network")
        self.scan_button.clicked.connect(self.start_scan)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ["IP Address", "MAC Address", "Vendor", "OS"]
        )

        layout.addWidget(self.scan_button)
        layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.start_periodic_scan()

    def start_scan(self):
        if hasattr(self, "scan_thread") and self.scan_thread.isRunning():
            return

        self.scan_button.setEnabled(False)
        self.scan_button.setText("Scanning...")
        self.table.setRowCount(0)

        self.scan_thread = ScanThread()
        self.scan_thread.finished.connect(self.update_table)
        self.scan_thread.start()

    def start_periodic_scan(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.start_scan)
        self.timer.start(60000) 

    def update_table(self, devices):
        for row, device in enumerate(devices):
            is_new = upsert_device(device)

            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(device["ip"]))
            self.table.setItem(row, 1, QTableWidgetItem(device["mac"]))
            self.table.setItem(row, 2, QTableWidgetItem(device["vendor"]))
            self.table.setItem(row, 3, QTableWidgetItem(device["os"]))

            add_event(
                mac=device["mac"],
                ip=device["ip"],
                network_id="ROOM_A" 
            )

            if is_new:
                for col in range(4):
                    self.table.item(row, col).setBackground(Qt.yellow)

                QMessageBox.information(
                    self,
                    "New Device Detected",
                    f"New device detected:\nIP: {device['ip']}\nMAC: {device['mac']}"
                )

        self.scan_button.setEnabled(True)
        self.scan_button.setText("Scan Network")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
