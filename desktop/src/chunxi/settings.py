import copy
from PySide6.QtCore import Qt, Signal
from .config import MIN_SCALE, MAX_SCALE
from PySide6.QtWidgets import QCheckBox, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QHBoxLayout, QLabel, QSlider, QSpinBox, QWidget


class SizeControl(QWidget):
    valueChanged = Signal(int)

    def __init__(self, percent, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.spin = QSpinBox(self)
        for control in (self.slider, self.spin):
            control.setRange(round(MIN_SCALE * 100), round(MAX_SCALE * 100))
            control.setSingleStep(5)
        self.slider.setPageStep(25)
        self.spin.setSuffix(" %")
        self.spin.setValue(percent)
        self.slider.setValue(percent)
        self.slider.valueChanged.connect(self.spin.setValue)
        self.spin.valueChanged.connect(self.slider.setValue)
        self.spin.valueChanged.connect(self.valueChanged.emit)
        layout.addWidget(self.slider, 1)
        layout.addWidget(self.spin)

    def value(self):
        return self.spin.value()

    def setValue(self, value):
        self.spin.setValue(value)


class SizeDialog(QDialog):
    def __init__(self, scale, parent=None):
        super().__init__(parent)
        self.setWindowTitle("春喜 · 调节大小")
        self.setMinimumWidth(400)
        layout = QFormLayout(self)
        self.size = SizeControl(round(scale * 100), self)
        layout.addRow("宠物大小", self.size)
        layout.addRow(QLabel("拖动滑块可实时预览；保存后记住大小，取消则恢复。", self))
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel, self)
        buttons.button(QDialogButtonBox.StandardButton.Save).setText('保存')
        buttons.button(QDialogButtonBox.StandardButton.Cancel).setText('取消')
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)


class SettingsDialog(QDialog):
    def __init__(self, config: dict, startup_enabled: bool, parent=None):
        super().__init__(parent)
        self.config = copy.deepcopy(config)
        self.setWindowTitle("春喜 · 设置")
        self.setMinimumWidth(360)
        layout = QFormLayout(self)
        self.size = SizeControl(round(config['window']['scale']*100), self)
        layout.addRow("宠物大小", self.size)
        self.topmost = QCheckBox("始终置顶", self)
        self.topmost.setChecked(config['window']['always_on_top'])
        layout.addRow(self.topmost)
        self.frequency = QComboBox(self)
        for label, key in [('更安静','quiet'),('默认','normal'),('稍多一些','more')]:
            self.frequency.addItem(label,key)
        self.frequency.setCurrentIndex(max(0,self.frequency.findData(config['preferences']['frequency'])))
        layout.addRow("行为频率",self.frequency)
        self.startup = QCheckBox("登录 Windows 后启动春喜", self)
        self.startup.setChecked(startup_enabled)
        layout.addRow(self.startup)
        note = QLabel("点击保存后生效。开机启动默认关闭，只在你勾选并保存后启用。",self)
        note.setWordWrap(True)
        layout.addRow(note)
        buttons=QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel,self)
        buttons.button(QDialogButtonBox.StandardButton.Save).setText('保存')
        buttons.button(QDialogButtonBox.StandardButton.Cancel).setText('取消')
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def selected_config(self):
        result=copy.deepcopy(self.config)
        result['window']['scale']=self.size.value()/100
        result['window']['always_on_top']=self.topmost.isChecked()
        result['preferences']['frequency']=self.frequency.currentData()
        return result
