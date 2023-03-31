"""
This module uses 'matplotlib.pyplot' and 'numpy' libraries to create a line chart.
'matplotlib' is a plotting library for creating static, animated, and interactive
visualizations in Python. It allows you to create a wide variety of plots and charts,
such as line plots, scatter plots, bar plots, histograms, 3D plots, etc.
'numpy' is a library for scientific computing in Python, it provides support for large
multidimensional arrays and matrices of numerical data and a large library of high-level
mathematical functions to operate on these arrays. It is widely used in scientific and
engineering fields, data science and machine learning.
"""
import matplotlib.pyplot as plt
import numpy as np


def create_line_chart(year, exports, imports):
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

    # Plot the line chart for imports
    plt.plot(year, imports, color='#FE420F', label='Imports')
    plt.legend()
    plt.xlabel('Year', fontsize=7)
    plt.ylabel('Euro in Million', fontsize=7)
    # plt.show()
    # plt.savefig('/website/static/images/line-import-chart.png')

    # Clear the figure for the next chart
    plt.clf()

    # Set the x-axis values to the years with 3 years gap
    plt.xticks(year[::3], rotation=45, fontsize=8)

    # Set the y-axis values to start from 0 and increase by 200000
    plt.yticks(y_values, y_values, fontsize=8)

    # Plot the line chart for exports
    plt.plot(year, exports, color='#069AF3', label='Exports')
    plt.legend()
    plt.xlabel('Year', fontsize=7)
    plt.ylabel('Euro in Million', fontsize=7)
    # plt.show()
    # plt.savefig('/website/static/images/line-export-chart.png')

    # Clear the figure for the next chart
    plt.clf()

    # Set the x-axis values to the years with 3 years gap
    plt.xticks(year[::3], rotation=45, fontsize=8)

    # Set the y-axis values to start from 0 and increase by 200000
    plt.yticks(y_values, y_values, fontsize=8)

    # Plot the line chart for both imports and exports
    plt.plot(year, exports, color='#069AF3', label='Exports')
    plt.plot(year, imports, color='#FE420F', label='Imports')
    plt.legend()
    plt.xlabel('Year', fontsize=7)
    plt.ylabel('Euro in Million', fontsize=7)
    # plt.show()
    # plt.savefig('/website/static/images/line-export-import-chart.png')
