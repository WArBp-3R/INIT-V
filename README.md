# INIT-V

## Download

To download the program simply do:

    $ git clone https://gitlab-ext.iosb.fraunhofer.de/pse2/ws2122-visualization-of-network-data/init-v.git

On the master branch, do the following:

    $ git submodule init && git submodule update

## Installation

INIT-V works uses Python version 3.9 and Anaconda 4.11 to install the python packages it depends on.

Install anaconda, if you do not already have it by going on:
<https://www.anaconda.com/products/individual>

Change the working directory to the git repository you just cloned:

    $ cd init-v

To create a new anaconda environment run:

    $ conda create -n init-v python==3.9

To install the dependencies run:

    $ conda install -n init-v -c conda-forge --file ./requirements.txt

## Scenario

This section contains an overview of the basic functions of the INIT-V program by describing
a simple scenario. Further functionality is mentioned briefly while going through the
steps of this scenario.

### Starting the program:

Start the anaconda shell.  
Activate the conda environment  

    $ activate init-v  

To start the program run the INITV.py file:

    $ python <Path to the project folder>/init-v/INITV.py

Afterwards open <http://127.0.0.1:8050/> in your web browser.

### Opening PCAP files:

1. In the top-bar click on the "Files" menu.
2. Click on "Open" to open a PCAP file.

The topology of the network is displayed in the Network panel. Further information on the devices
and connections appear when hovering over them. Multiple kinds of statistics concerning the PCAP can be viewed
in the Statistics panel.

In the "Files" menu, there are also items to open session files (Also done through "Open"), configuration files or to
save the session or configuration.

### Configuring the preprocessor:

The preprocessor can be configured in the Configuration panel in the top left.

All the values of the PCA and Autoencoder configuration can be set.

### Running the preprocessor:

To run the preprocessing, click on the Run button in the top-bar. The results of the PCA
and/or the autoencoding will appear in the Method Results panel after a certain time (depending on the
amount of packages in the PCAP file). An analysis of the PCA and Autoencoder performance
is displayed in the Performance panel.

Information about the packets is displayed when hovering over the points in the Method
Results panel.

### Compare results

To compare results of different preprocessor configurations, click on "Compare Runs" in the
top-bar. A window will open where the method results and performance results of runs can be 
compared side-by-side.

## Usage

### Files

If the user tries to save a configuration or session to a file while another save
operation is not completed, the program crashes in the current version.

### Network Topology

In the Protocols drop down menu, the user can select for which
protocols connections are drawn.

In the Layout drop down menu, the user can change the way the device nodes are arranged.

In the Edge Mode menu, the user can select whether to draw an edge for each connection or
an edge for each protocol on that connection.

To add a connection to the selection in the Network panel, press shift and click on the
connection.

### Method Results

To merge the PCA and Autoencoder graphs into one graph, simply click the Merge button
at the top-bar in the Method Results panel.

### Statistics

In the Stats List drop down menu, the user can select which statistic to display in
the Statistics panel.

### Exporting Images

Each graph can be exported as an image. For the network topology a button is located on
the menu bar above the Network panel. The other graphs can be saved by clicking on the
camera icon at the top right of the graph view.

## Change color scheme

Download sass and install it: <https://sass-lang.com/install> (More detailed step by step guide for
Windows: <https://stackoverflow.com/questions/51571814/how-to-install-dart-sass>).

Change sass files

Execute sass on the assets folder:

    $ sass path/assets

Reload the page

## Dash Debug mode

To (de-)activate debug mode, goto ./init-v/view/GUI_Handler.py, in method run_app, change the debug parameter in
self.app.run_server() to False/True