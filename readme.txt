CounterFire Map Plotter
This script is a Python application that plots POO (point of origin) and POI (point of impact) coordinates from a CSV file on a map using the Folium library. The script allows users to visualize and analyze counterfire data in a user-friendly way.

Requirements
Python 3.6+
Folium 0.12.1
Pandas 1.3.3
MGRS 2.1.1
Tkinter (built-in)
Math (built-in)
FontAwesome (built-in)
Installation
Ensure that Python 3.6+ is installed. To check, open a terminal and enter the following command:

python3 --version

If Python 3 is not installed, install it using the following command:

sudo apt-get update
sudo apt-get install python3

Install the necessary libraries using the following command:

sudo apt-get install python3-pandas python3-tk python3-pip
sudo pip3 install folium mgrs

This will install Pandas, Tkinter, Folium, MGRS, and the necessary Python packages.

How to Use
Prepare the data file in CSV format with the following columns: POO, POI, DTG, TYPE, and SYSTEM.

Download the counterfireV2.py script and save it to your preferred directory.

Open a terminal and navigate to the directory where the script is saved.

Run the script using the following command:

python3 counterfireV2.py

A file dialog box will appear, allowing you to select the input file. Select the prepared data file in CSV format.

The script will create a new map centered on the first POO point.

The map will display different types of POOs and POIs in different colors.

The distance between the POO and POI will be displayed as a purple marker.

A layer control is added to toggle POO types and lines.

The map will be saved as an HTML file on the desktop, named CounterFire_YYYY-MM-DD_HH-MM-SS.html, where YYYY-MM-DD_HH-MM-SS is the current date and time.

The map will also be displayed in the Python environment.

Notes
The distance between POO and POI is calculated using the Haversine formula.
The icons used for POOs and POIs are from the FontAwesome library.
The map is centered on the first POO point in the input file.
The CSV file should have a header row.
The POO type is used to determine the color of the markers and the lines between the POO and POI.
The SYSTEM column is not required but can be useful to store information about the data source.
This installation guide is for Debian Linux.
