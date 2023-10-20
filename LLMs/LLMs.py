class LLMs:

    def __init__(self, config, text):
        self.model = config.model
        self.token = config.token
        self.prompt = 'Summarize the following text into 150 words, making it easy to read and comprehend. The summary should be concise, clear, and capture the main points of the text. Avoid using complex sentence structures or technical jargon. Respond in %s. Please begin by editing the following text: ' % (config.outputLaguage)
        self.text = text
        self.summary = None

    def _sendMessage(self):
        # Subclasses should override this method
        raise NotImplementedError("Subclasses must implement _sendMessage() method.")

    def sendMessage(self):
        # before sending the message
        self._sendMessage()

