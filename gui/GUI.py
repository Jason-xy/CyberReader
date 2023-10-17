import flet as ft

class GUI:

    modelDropdown = None
    urlTXT = None
    page = None
    outputTXT = None

    def __init__(self, pipeline):
        self.pipeline = pipeline
        self.config = pipeline.config

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

        # main logic of CyberReader
        self.CyberReader()

        # show result to GUI
        self.outputTXT.value = "Summary: %s\n" % (self.pipeline.LLMsHandler.summary)

        self.page.update()

    def CyberReader(self):
        self.pipeline.process()

    def run(self):
        ft.app(target=self.window)