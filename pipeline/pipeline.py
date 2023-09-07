from convert.video.videoConverter import videoConverter

class pipeline:
    def __init__(self, config):
        self.config = config
        self.model = config.model

    def _process_poe(self):
        from LLMs.poe.poe import poeHandler
        videoHandler = videoConverter(self.config)
        videoHandler.process()
        poeHandler(self.config, videoHandler.text).sendMessage()

    def _process_chatgpt(self):
        from LLMs.chatgpt.chatgpt import chatgptHandler
        videoHandler = videoConverter(self.config)
        videoHandler.process()
        chatgptHandler(self.config, videoHandler.text).sendMessage()

    def process(self):
        if self.model == "poe":
            self._process_poe()
        elif self.model == "gpt-3.5-turbo":
            self._process_chatgpt()