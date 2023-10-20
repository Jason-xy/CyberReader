import flet as ft
import os

class MainGUI:

    page = None
    currentRoute = None

    MAIN_NAVIGATION = {
        'Home': {
            'nav_index': 0,
            'route': '/CyberReader/home',
        },
        'Settings': {
            'nav_index': 1,
            'route': '/CyberReader/settings',
        },
    }

    def __init__(self, pipeline):
        self.pipeline = pipeline
        self.config = pipeline.config

        self.appIcon = ft.Image(
            src=os.path.join(os.path.dirname(__file__), '../icon/CyberReader.png'),
            width=200,
            height=200,
            scale=0.5,
        )
        self.tokenTXT = ft.TextField(
            label="Token (openai | poe)", password=True, can_reveal_password=True,
            hint_text="Input your token here to replace the default token in config.yaml",
        )
        self.urlTXT = ft.TextField(label="URL")
        self.inputLanguageDropdown = ft.Dropdown(
            hint_text="Select input language",
            options=[
                ft.dropdown.Option("English"),
                ft.dropdown.Option("Chinese"),
                ft.dropdown.Option("Japanese"),
                ft.dropdown.Option("Russian"),
            ],
        )
        self.outputLanguageDropdown = ft.Dropdown(
            hint_text="Select output language",
            options=[
                ft.dropdown.Option("English"),
                ft.dropdown.Option("Chinese"),
                ft.dropdown.Option("Japanese"),
                ft.dropdown.Option("Russian"),
            ],
        )
        self.whisperModelDropdown = ft.Dropdown(
            hint_text="Select whisper model",
            options=[
                ft.dropdown.Option("base"),
                ft.dropdown.Option("small"),
                ft.dropdown.Option("medium"),
                ft.dropdown.Option("large"),
            ],
        )
        self.gpuSwitch = ft.Switch(label="Enable GPU", value=False)
        self.outputTXT = ft.Markdown(
            expand=True,
            selectable=True,
            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
        )
        self.originTXT = ft.Markdown(
            expand=True,
            selectable=True,
            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
        )
        self.modelDropdown = ft.Dropdown(
            hint_text="Select a model",
            options=[
                ft.dropdown.Option("gpt-3.5-turbo"),
                ft.dropdown.Option("gpt-3.5-turbo-16k"),
                ft.dropdown.Option("gpt-4"),
            ],
        )
        self.outPutRow = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        ft.Text(
                            "Origin",
                            size=30,
                            weight=ft.FontWeight.W_700,
                        ),
                        ft.Container(
                            margin=10,
                            padding=10,
                            border_radius=10,
                            content=ft.Column(
                                horizontal_alignment=ft.CrossAxisAlignment.START,
                                expand=True,
                                scroll="AUTO",
                                controls=[
                                    self.originTXT
                                ],
                            ),
                            expand=True,
                        ),
                    ],
                    expand=True,
                ),
                ft.VerticalDivider(width=1),
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        ft.Text(
                            "Summary",
                            size=30,
                            weight=ft.FontWeight.W_700,
                        ),
                        ft.Container(
                            margin=10,
                            padding=10,
                            border_radius=10,
                            content=ft.Column(
                                horizontal_alignment=ft.CrossAxisAlignment.START,
                                expand=True,
                                scroll="AUTO",
                                controls=[
                                    self.outputTXT,
                                ],
                            ),
                            expand=True,
                        ),
                    ],
                    expand=True,
                ),
            ],
            expand=True,
        )
        self.mainRail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            leading=ft.FloatingActionButton(icon=ft.icons.FILE_UPLOAD_ROUNDED , text="Submit", on_click=self.submitCallback),
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.icons.HOME_OUTLINED,
                    selected_icon_content=ft.Icon(ft.icons.HOME_ROUNDED),
                    label_content=ft.Text("Home"),
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.SETTINGS_OUTLINED,
                    selected_icon_content=ft.Icon(ft.icons.SETTINGS),
                    label_content=ft.Text("Settings"),
                ),
            ],
            on_change=None,
        )
        self.homeView = ft.View(
            route='/CyberReader/home',
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    [
                        self.mainRail,
                        ft.VerticalDivider(width=1),

                        ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls = [
                                self.appIcon,
                                self.urlTXT,
                                self.outPutRow,
                            ],
                            expand=True,
                        ),
                    ],
                    expand=True,
                )
            ],
        )
        self.settingsView = ft.View(
            route='/CyberReader/settings',
            horizontal_alignment=ft.CrossAxisAlignment.START,
            controls=[
                ft.Row(
                    [
                        self.mainRail,
                        ft.VerticalDivider(width=1),

                        ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=10,
                            controls = [
                                self.tokenTXT,
                                self.modelDropdown,
                                self.inputLanguageDropdown,
                                self.outputLanguageDropdown,
                                self.whisperModelDropdown,
                                self.gpuSwitch,
                            ],
                            expand=True,
                        ),
                    ],
                    expand=True,
                )
            ],
        )

        self.NAV_INDEX_TO_ROUTE = {}
        for view in self.MAIN_NAVIGATION.values():
            self.NAV_INDEX_TO_ROUTE[view['nav_index']] = view['route']

        self.ROUTE_TO_VIEW = {
            '/CyberReader/home': self.homeView,
            '/CyberReader/settings': self.settingsView,
        }

    def window(self, page: ft.Page):
        self.page = page
        self.page.scroll="AUTO"
        self.page.title = "CyberReader"
        self.page.horizontal_alignment = "center"

        self.mainRail.on_change = lambda event: self.page.go(self.NAV_INDEX_TO_ROUTE[event.control.selected_index])
        self.page.on_route_change = self.onRouteChange
        self.page.go('/CyberReader/home')

    def onRouteChange(self, route):
            self.page.views.clear()
            self.page.views.append(self.ROUTE_TO_VIEW[self.page.route])
            self.page.update()

    def reWriteConfig(self):
        if self.tokenTXT.value:
            self.config.token = self.tokenTXT.value
        if self.gpuSwitch.value:
            self.config.withGPU = self.gpuSwitch.value
        if self.modelDropdown.value:
            self.config.model = self.modelDropdown.value
        if self.inputLanguageDropdown.value:
            self.config.inputLaguage = self.inputLanguageDropdown.value
        if self.outputLanguageDropdown.value:
            self.config.outputLaguage = self.outputLanguageDropdown.value
        if self.whisperModelDropdown.value:
            self.config.whisperModel = self.whisperModelDropdown.value
        if self.urlTXT.value:
            self.config.content = self.urlTXT.value
        else:
            raise Exception("Please input URL")

        self.outputTXT.value = "Please wait..."
        self.originTXT.value = "Please wait..."

    def getOutput(self):
        self.outputTXT.value = self.pipeline.LLMsHandler.summary
        self.originTXT.value = self.pipeline.LLMsHandler.text

    def submitCallback(self, event):
        # rewrite config
        self.reWriteConfig()

        # wait animation
        self.page.update()

        # main logic of CyberReader
        self.CyberReader()

        # show result to GUI
        self.getOutput()

        self.page.update()

    def CyberReader(self):
        self.pipeline.process()

    def run(self):
        ft.app(target=self.window)