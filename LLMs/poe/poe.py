from LLMs.LLMs import LLMs
import poe

class poeHandler(LLMs):
    def __init__(self, config, text):
        super().__init__(config, text)
        print("token: ", self.token)
        self.client = poe.Client(self.token)

    def _sendMessage(self):
        message = self.prompt + self.text
        for chunk in self.client.send_message("capybara", message):
            print(chunk["text_new"], end="", flush=True)

    def sendMessage(self):
        try:
            super().sendMessage()
        except Exception as e:
            print(f"An error occurred during sendMessage: {str(e)}")