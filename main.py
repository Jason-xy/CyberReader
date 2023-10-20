#!/usr/bin/env python3
from config.ProgramConfig import ProgramConfig
from pipeline.pipeline import pipeline
from gui.MainGUI import MainGUI
import argparse
import sys
import os

def argsParser(argv):
    parser = argparse.ArgumentParser(description='CyberReader')
    parser.add_argument('--auto_test', action='store_true', help='auto_test without GUI')
    args = parser.parse_args(argv)
    return args

def auto_test():
    config = ProgramConfig(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.yaml'))
    pipeline(config).process()

def main(argv):
    args = argsParser(argv)
    if args.auto_test:
        auto_test()
    else:
        config = ProgramConfig(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.yaml'))
        pipe = pipeline(config)
        gui = MainGUI(pipe)
        gui.run()

if __name__ == "__main__":
    main(sys.argv[1:])