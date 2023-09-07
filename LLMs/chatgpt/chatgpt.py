from LLMs.LLMs import LLMs
import openai

class chatgptHandler(LLMs):
    def __init__(self, config, text):
        super().__init__(config, text)
        openai.api_key = self.token

    def _sendMessage(self):
        message = self.prompt + self.text
        completion = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "user", "content": message}
            ]
        )
        print(completion.choices[0].message.content)

    def sendMessage(self):
        try:
            super().sendMessage()
        except Exception as e:
            print(f"An error occurred during sendMessage: {str(e)}")