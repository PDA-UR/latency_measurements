#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import mysql.connector
from datetime import datetime


# All Constants are placed in their own class to find them more easily
class Constants:
    CSV_DELIMITER = ';'
    PLOT_X_MIN = 0  # Minimum x value of the plot
    PLOT_X_MAX = 100  # Maximum x value of the plot
    PLOT_WIDTH = 16
    PLOT_HEIGHT = 4
    PLOT_OUTPUT_DPI = 600

    DATABASE_HOST = 'localhost'
    DATABASE_USER = 'root'
    DATABASE_PASSWORD = ''
    DATABASE_NAME = 'lagbox_db'


class Result:

    def __init__(self):
        self.name = 'D'
        self.minDelay = 100
        self.maxDelay = 10000
        self.iterations = 1000
        self.authors = 'A'
        self.vendorID = 'A'
        self.productID = 'A'
        self.date = datetime.now().strftime('%Y-%m-%d')  # TODO: Check what date format to use for a MySQL Database
        self.bIntervall = 1000
        self.deviceType = 'Mouse'
        self.mean = 0.0
        self.median = 0.0
        self.min = 0.0
        self.max = 0.0
        self.standardDeviation = 0.0
        self.deviceImage = 'A'
        self.plotImage = 'A'


class ProcessingPipeline:

    result = Result()

    def __init__(self):
        try:
            filename = sys.argv[1]  # The filename needs to be passed over as an argument when starting the script
        except IndexError:
            sys.exit("No .csv file handed over. The name of the .csv file needs to be passed as an argument.")

        print(filename + " will be processed.")
        self.read_csv_data(filename)

    # Reads in a csv file and hands the data over at the end
    def read_csv_data(self, filename):
        try:
            current_file = open(filename, 'r').readlines()  # Open the csv File
        except:
            sys.exit("file missing: " + filename)

        comment_lines = []  # All lines containing a comment (==> Metadata about the measurement)
        measurement_rows = []  # All lines containing actual measurement data

        # TODO:  Check loop performance
        for i in range(len(current_file)):
            if current_file[i][0] is '#':  # If row is a comment
                comment_lines.append(current_file[i])
            elif current_file[i] == 'counter;latency;delayTime\n':  # If row is header of measurements
                measurement_rows = current_file[i + 1:len(current_file)]  # Take all rows of the file starting by the first line after the header
                break  # No need to continue the loop

        # The csv file is now read in and relevant parts are extracted. Now the data needs to be processed further
        latencies = self.parse_measurements(measurement_rows)

        self.parse_comments(comment_lines)
        self.get_stats_about_data(latencies)
        self.generate_plot(filename, latencies)

    # Parse the bare rows from the .csv file and extract only the relevant data
    def parse_measurements(self, measurement_rows):
        latencies = []

        for i in range(len(measurement_rows)):
            row_values = measurement_rows[i].split(Constants.CSV_DELIMITER)
            latencies.append(float(row_values[1]) / 1000)  # Divide by 1000 to get ms

        for i in range(len(latencies)):
            if latencies[i] > Constants.PLOT_X_MAX:  # Check if values will get clipped
                print("WARNING: One or more measured latencies exceed the defined limit of the plots x-axis and will not be displayed!")
                break

        return latencies

    # Interpret the comment lines of the .csv file. They contain relevant metadata about the measurement
    def parse_comments(self, comment_lines):
        print("Comments:")
        for comment_line in comment_lines:
            print(comment_line.split(';')[0].replace('#', '') + " " + comment_line.split(';')[1])

    def get_stats_about_data(self, latencies):
        mean = np.mean(latencies)
        median = np.median(latencies)
        minimum = min(latencies)
        maximum = max(latencies)
        standard_deviation = np.std(latencies)

        self.result.mean = mean
        self.result.median = median
        self.result.min = minimum
        self.result.max = maximum
        self.result.standardDeviation = standard_deviation

        print("Mean: ", mean, "Median: ", median, "Minimum: ", minimum, "Maximum", maximum, "Standard Deviation: ", standard_deviation)

    # Get a name for the plot that will be saved as an image at the end
    def get_image_filename(self, filename):
        return filename.replace('.csv', '.png')

    # Generate a plot from the extracted latencies
    def generate_plot(self, filename, latencies):
        plt.figure(figsize=[Constants.PLOT_WIDTH, Constants.PLOT_HEIGHT])

        # ax = sns.pointplot((values["latency"]), values["polling"], join=False, palette="dark", markers="D", scale=.75,
        # ci="sd", zorder=1, errwidth=0.5, capsize=.2, ax =axes)
        # ax = sns.swarmplot((values["latency"]), values["polling"], hue=None, palette="colorblind", size=1, dodge=True,
        # marker="H",orient="h", alpha=1, zorder=0)

        ax = sns.swarmplot(x=latencies, hue=None, palette="colorblind", dodge=True, marker="H", orient="h", alpha=1,
                           zorder=0)

        # plt.title("TEST")
        plt.xlabel("latency (ms)")
        plt.xlim(Constants.PLOT_X_MIN, Constants.PLOT_X_MAX)

        axes = plt.gca()

        plt.savefig(self.get_image_filename(filename), dpi=Constants.PLOT_OUTPUT_DPI)
        print("Plot created successfully")

        self.write_to_database()

    def write_to_database(self):

        print('Connecting to Database', Constants.DATABASE_NAME)

        database = mysql.connector.connect(
            host=Constants.DATABASE_HOST,
            user=Constants.DATABASE_USER,
            passwd=Constants.DATABASE_PASSWORD,
            database=Constants.DATABASE_NAME
        )

        sql = "INSERT INTO `measurements` (`name`, `minDelay`, `maxDelay`, `iterations`, `authors`, `vendorID`, " \
              "`productID`, `date`, `bIntervall`, `deviceType`, `mean`, `median`, `min`, `max`, `standardDeviation`, " \
              "`deviceImage`, `plotImage`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        values = (self.result.name, str(self.result.minDelay), str(self.result.maxDelay),  str(self.result.iterations),
                  self.result.authors, self.result.vendorID, self.result.productID, self.result.date,
                  str(self.result.bIntervall), self.result.deviceType, str(self.result.mean), str(self.result.median),
                  str(self.result.min), str(self.result.max), str(self.result.standardDeviation),
                  self.result.deviceImage, self.result.plotImage)

        database.cursor().execute(sql, values)
        database.commit()

        print("Values inserted into database", Constants.DATABASE_NAME)


def main():
    processingPipeline = ProcessingPipeline()
    sys.exit()


if __name__ == '__main__':
    main()
