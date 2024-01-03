from src.model.config import Config

from src.view.advanced_setting import AdvancedSettingView


class AdvancedSettingController:
    def __init__(self, view: AdvancedSettingView):
        # view
        self.view = view
        # model
        self.config = Config()

        # bind
        self.view.save_button.clicked.connect(self.save_settings)
        self.view.close_button.clicked.connect(self.close_event)

        self.load_settings()

    def load_settings(self):
        if self.config.edge_package_size:
            self.view.package_size_entry.setText(str(self.config.edge_package_size))

        if self.config.edge_description:
            self.view.package_size_entry.setText(self.config.edge_description)

        if self.config.edge_etc_args:
            self.view.edge_etc_args_entry.setText("\n".join(self.config.edge_etc_args))

    def save_settings(self):
        self.config.edge_package_size = self.view.package_size_entry.text()
        self.config.edge_description = self.view.edge_description_entry.text()
        self.config.edge_etc_args = self.view.edge_etc_args_entry.toPlainText().split("\n")
        self.view.close()

    def show_event(self):
        self.view.show()

    def close_event(self):
        self.view.close()
