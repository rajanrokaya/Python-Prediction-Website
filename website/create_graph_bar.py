"""
This module uses 'matplotlib.pyplot' and 'numpy' libraries to create a bar chart.
"""
import matplotlib.pyplot as plt
import numpy as np


def create_bar_chart(year, exports, imports):
    """
        :param year: Takes the year
        :param exports: Export Data for certain year
        :param imports: Import Data for certain year
        """
    # Convert the year, exports, and imports lists to numpy arrays
    year = np.array(year, dtype=int)
    exports = np.array(exports, dtype=int)
    imports = np.array(imports, dtype=int)

    # Set the x-axis values to the years with 3 years gap
    plt.xticks(year[::3], rotation=45, fontsize=8)

    # Set the y-axis values to start from 0 and increase by 200000
    max_value = max(max(exports), max(imports))
    y_values = np.arange(0, max_value + 200000, 200000)
    plt.yticks(y_values, y_values, fontsize=8)

    # Plot the bar chart for imports
    plt.bar(year, imports, color='#FE420F', label='Imports')
    plt.legend()
    plt.xlabel('Year', fontsize=7)
    plt.ylabel('Euro in Million', fontsize=7)
    # plt.show()
    # plt.savefig('/website/static/images/bar-import-chart.png')

    # Clear the figure for the next chart
    plt.clf()

    # Set the x-axis values to the years with 3 years gap
    plt.xticks(year[::3], rotation=45, fontsize=8)

    # Set the y-axis values to start from 0 and increase by 200000
    plt.yticks(y_values, y_values, fontsize=8)

    # Plot the bar chart for exports
    plt.bar(year, exports, color='#069AF3', label='Exports')
    plt.legend()
    plt.xlabel('Year', fontsize=7)
    plt.ylabel('Euro in Million', fontsize=7)
    # plt.show()
    # plt.savefig('/website/static/images/bar-export-chart.png')

    # Clear the figure for the next chart
    plt.clf()

    # Set the x-axis values to the years with 3 years gap
    plt.xticks(year[::3], rotation=45, fontsize=8)

    # Set the y-axis values to start from 0 and increase by 50000
    plt.yticks(y_values, y_values, fontsize=8)

    # Plot the bar chart for both imports and exports
    bar_width = 0.4
    plt.bar(year, exports, bar_width, color='#069AF3', label='Exports')
    plt.bar(year + bar_width, imports, bar_width, color='#FE420F', label='Imports')
    plt.legend()
    plt.xlabel('Year', fontsize=7)
    plt.ylabel('Euro in Million', fontsize=7)
    # plt.show()
    # plt.savefig('/website/static/images/bar-export-import-chart.png')
