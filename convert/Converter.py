import os

class Converter:
    def __init__(self, config):
        self.path = config.content
        self.config = config
        self.localPath = None
        self.text = None

    def download(self):
        # Create temporary download directory
        temp_dir = self.config.tmpDir
        os.makedirs(temp_dir, exist_ok=True)

        try:
            # Call the subclass-specific download function
            self._download()

            # Perform post-download operations

            # Placeholder: Move the downloaded video to the desired location

            print("Download completed successfully.")

        except Exception as e:
            print(f"An error occurred during download: {str(e)}")
            # Clean up the temporary download directory
            if os.path.exists(temp_dir):
                os.rmdir(temp_dir)

        finally:
            pass

    def convert(self):
        # Placeholder implementation
        self._convert()

    def process(self):
        # Placeholder implementation
        self._process()

    def _download(self):
        # Subclasses should override this method
        raise NotImplementedError("Subclasses must implement _download() method.")

    def _convert(self):
        # Subclasses should override this method
        raise NotImplementedError("Subclasses must implement _convert() method.")

    def _process(self):
        # Subclasses should override this method
        raise NotImplementedError("Subclasses must implement _process() method.")
