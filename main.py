#!/usr/bin/env python3
from config.ProgramConfig import ProgramConfig
from convert.video.videoConverter import videoConverter
import os

def main():
    config = ProgramConfig(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.yaml'))
    videoHandler = videoConverter(config)
    videoHandler.process()

if __name__ == "__main__":
    main()