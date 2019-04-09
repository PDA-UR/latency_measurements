#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys


class ProcessingPipeline:

    def __init__(self):
        try:
            filename = sys.argv[1]
        except IndexError:
            sys.exit("No .csv file handed over. The name of the .csv file needs to be passed as an argument")

        print(filename)


def main():
    processingPipeline = ProcessingPipeline()
    sys.exit()


if __name__ == '__main__':
    main()
