from convert.video.videoConverter import videoConverter

class pipeline:
    def __init__(self, config):
        self.config = config
        self.model = config.model
        self.convertHandler = None

    def typeSelector(self):
        pass

    def textProcessor(self):
        pass

    def audioProcessor(self):
        pass

    def videoProcessor(self):
        self.convertHandler = videoConverter(self.config).process()

    def _process_poe(self):
        from LLMs.poe.poe import poeHandler
        poeHandler(self.config, self.convertHandler.text).sendMessage()

    def _process_chatgpt(self):
        from LLMs.chatgpt.chatgpt import chatgptHandler
        chatgptHandler(self.config, self.convertHandler.text).sendMessage()

    def process(self):
        if self.model == "poe":
            self._process_poe()
        elif self.model == "gpt-3.5-turbo":
            self._process_chatgpt()