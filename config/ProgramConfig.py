import yaml

class ProgramConfig:
    def __init__(self, yamlPath):
        self.startTime = None
        self.yamlPath = yamlPath
        self.config = None
        self.token = None
        self.tmpDir = None
        self.resultDir = None
        self.content = None
        self.model = None
        self.inputLaguage = None
        self.outputLaguage = 'Chinese'
        self.whisperModel = 'base'
        self.withGPU = False

        self.load()

    def load(self):
        try:
            with open(self.yamlPath, 'r') as f:
                self.config = yaml.safe_load(f)
                self.token = self.config.get('TOKEN', '')
                self.tmpDir = self.config.get('TMP_DIR', '')
                self.resultDir = self.config.get('RESULT_DIR', '')
                self.content = self.config.get('CONTENTS', '')
                self.model = self.config.get('MODEL', '')
        except Exception as e:
            print(f"Error loading config file: {str(e)}")
            raise e