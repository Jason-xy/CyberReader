from convert.video.videoConverter import videoConverter
import datetime
import shutil
import os

class pipeline:
    def __init__(self, config):
        self.config = config
        self.model = config.model
        self.convertHandler = None
        self.LLMsHandler = None

    def typeSelector(self):
        pass

    def textProcessor(self):
        pass

    def audioProcessor(self):
        pass

    def videoProcessor(self):
        self.convertHandler = videoConverter(self.config)

    def _process_poe(self):
        from LLMs.poe.poe import poeHandler
        self.LLMsHandler = poeHandler(self.config, self.convertHandler.text)

    def _process_chatgpt(self):
        from LLMs.chatgpt.chatgpt import chatgptHandler
        self.LLMsHandler = chatgptHandler(self.config, self.convertHandler.text)

    def postProcessor(self):
        resultDir = os.path.join(os.path.abspath(self.config.resultDir), self.config.startTime)
        os.makedirs(resultDir)

        with open(os.path.join(resultDir, 'original.txt'), 'w') as f:
            f.write(self.convertHandler.text)
        with open(os.path.join(resultDir, 'result.txt'), 'w') as f:
            f.write(self.LLMsHandler.summary)

        print("Result has been saved to ", resultDir)

        if os.path.exists(self.config.tmpDir):
            shutil.rmtree(self.config.tmpDir)

    def process(self):
        self.config.startTime = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S")
        # find out the type of the input
        self.videoProcessor()

        # convert the input to text
        self.convertHandler.process()

        # find out the type of the model
        if "poe" in self.model:
            self._process_poe()
        elif "gpt" in self.model:
            self._process_chatgpt()

        # send the text to the model
        self.LLMsHandler.sendMessage()

        self.postProcessor()