import sys
sys.path.append("..")

from config.ProgramConfig import ProgramConfig
import flet as ft
import os

class GUI:

    modelDropdown = None
    urlTXT = None
    page = None
    outputTXT = None

    def __init__(self, config):
        self.config = config

    def window(self, page: ft.Page):
        self.page = page
        self.page.title = "CyberReader"
        self.page.horizontal_alignment = "center"

        tokenTXT = ft.Text(value="Token: %s" % (self.config.token), color="black")

        self.modelDropdown = ft.Dropdown(
            options=[
                ft.dropdown.Option("gpt-3.5-turbo"),
                ft.dropdown.Option("gpt-3.5-turbo-16k"),
                ft.dropdown.Option("gpt-4"),
            ],
        )

        self.urlTXT = ft.TextField(label="URL")

        submitBTN = ft.ElevatedButton(text="Submit", on_click=self.submitCallback)

        self.outputTXT = ft.Text()

        self.page.add(tokenTXT, self.modelDropdown, self.urlTXT, submitBTN, self.outputTXT)

    def submitCallback(self, event):
        self.config.model = self.modelDropdown.value
        self.config.content = self.urlTXT.value
        self.outputTXT.value = "Model: %s\nURL: %s" % (self.config.model, self.config.content)
        self.page.update()

    def run(self):
        ft.app(target=self.window)

if __name__ == "__main__":
    config = ProgramConfig(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../config.yaml'))
    gui = GUI(config)
    gui.run()