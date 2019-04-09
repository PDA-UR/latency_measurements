#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from matplotlib import pyplot as plt
import seaborn as sns


class Constants:
    CSV_DELIMITER = ';'
    PLOT_X_MIN = 0
    PLOT_X_MAX = 50
    PLOT_WIDTH = 16
    PLOT_HEIGHT = 4
    PLOT_OUTPUT_DPI = 600


class ProcessingPipeline:

    def __init__(self):
        try:
            filename = sys.argv[1]
        except IndexError:
            sys.exit("No .csv file handed over. The name of the .csv file needs to be passed as an argument")

        print(filename)
        self.read_csv_data(filename)

    def read_csv_data(self, filename):
        try:
            current_file = open(filename, 'r').readlines()  # Open the csv File
        except:
            sys.exit("file missing: " + filename)

        comment_lines = []  # All lines containing a comment (==> Metadata about the measurement)
        measurement_rows = []  # All lines containing actual measurement data

        for i in range(len(current_file)):
            if current_file[i][0] is '#':  # If row is a comment
                comment_lines.append(current_file[i])
            elif current_file[i] == 'counter;latency;delayTime\n':  # If row is header of measurements
                measurement_rows = current_file[i + 1:len(
                    current_file)]  # Take all rows of the file starting by the first line after the header
                break  # No need to continue the loop

        latencies = self.parse_measurements(measurement_rows)
        self.parse_comments(comment_lines)

        self.generate_plot(filename, latencies)

    def parse_measurements(self, measurement_rows):
        latencies = []

        for i in range(len(measurement_rows)):
            row_values = measurement_rows[i].split(Constants.CSV_DELIMITER)
            latencies.append(float(row_values[1]) / 1000)  # Divide by 1000 to get ms

        return latencies

    def parse_comments(self, comment_lines):
        print("Comments:")
        for comment_line in comment_lines:
            print(comment_line.split(';')[0].replace('#', '') + " " + comment_line.split(';')[1])

    # Get a name for the plot that will be saved as an image at the end
    def get_image_filename(self, filename):
        return filename.replace('.csv', '.png')

    def generate_plot(self, filename, latencies):
        plt.figure(figsize=[Constants.PLOT_WIDTH, Constants.PLOT_HEIGHT])

        # ax = sns.pointplot((values["latency"]), values["polling"], join=False, palette="dark", markers="D", scale=.75, ci="sd", zorder=1, errwidth=0.5, capsize=.2, ax =axes)
        # ax = sns.swarmplot((values["latency"]), values["polling"], hue=None, palette="colorblind", size=1, dodge=True, marker="H",orient="h", alpha=1, zorder=0)
        ax = sns.swarmplot(x=latencies, hue=None, palette="colorblind", dodge=True, marker="H", orient="h", alpha=1,
                           zorder=0)

        # plt.title("TEST")
        plt.xlabel("latency (ms)")
        plt.xlim(Constants.PLOT_X_MIN, Constants.PLOT_X_MAX)

        axes = plt.gca()

        plt.savefig(self.get_image_filename(filename), dpi=Constants.PLOT_OUTPUT_DPI)
        print("Plot created successfully")


def main():
    processingPipeline = ProcessingPipeline()
    sys.exit()


if __name__ == '__main__':
    main()
