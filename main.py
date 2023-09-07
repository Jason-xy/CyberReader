#!/usr/bin/env python3
from config.ProgramConfig import ProgramConfig
from pipeline.pipeline import pipeline
import os

def main():
    config = ProgramConfig(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.yaml'))
    pipeline(config).process()

if __name__ == "__main__":
    main()