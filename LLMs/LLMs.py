class LLMs:

    prompt = 'Your previous explanation was accurate and comprehensive, but hard to remember. Can you provide a rough, less precise, but still generally correct and easy-to-understand summary?'

    def __init__(self, config, text):
        self.model = config.model
        self.token = config.token
        self.text = text
        self.summary = None

    def _sendMessage(self):
        # Subclasses should override this method
        raise NotImplementedError("Subclasses must implement _sendMessage() method.")

    def sendMessage(self):
        # before sending the message
        self._sendMessage()

