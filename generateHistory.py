import os
import requests
import plistlib as pll
import webbrowser
from datetime import datetime
import argparse
import ntpath

# Require an argument with the path to the file
parser = argparse.ArgumentParser(description='Visualize playlist over time')
parser.add_argument('file', nargs='+', help='Path to the XML file')
args = parser.parse_args()

path, file = os.path.split(args.file[0])

# Save the current directory and move into the git repo
owd = os.getcwd()
os.chdir(path)

# Get a list of commits from git
output = os.popen('git log --pretty=format:%h').read()
hashes = output.splitlines()

data = {}

# Loop through each commit (oldest first)
for hash in reversed(hashes):
    # Extract the raw XML into a Plist then into workable data
    xml = os.popen('git show ' + hash + ':' + file).read()
    text_file = open("tmp", "wt")
    n = text_file.write(xml)
    text_file.close()
    try:
        plist = pll.load(open("tmp", "rb"))
    except pll.InvalidFileException:
        os.remove("tmp")
        continue
    os.remove("tmp")

    # Get the commit date
    date = os.popen(" git show --no-patch --no-notes --pretty='%cd' " + hash).read()

    # Save the track data
    order = plist['Playlists'][0]['Playlist Items']
    output = []
    for item in order:
        output.append(plist['Tracks'][str(item['Track ID'])]['Name'])

    data[date] = output

maxLength = 0

# Setup HTML output file
html = '<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">'
html += "<script src='https://ajax.googleapis.com/ajax/libs/jquery/2.0.0/jquery.min.js'></script><script src='svgDraw.js'></script>"
html += '<div id="svgContainer" style="z-index: -10; position:absolute;"><svg id="svg1">'

# Create a bunch of SVG paths
count = 0
for i in range(len(hashes)):
    html += '''
    <path
        id="path''' + str(i) + '''"
        d="M0 0"
        stroke="#000"
        opacity="0.9"
        fill="none"
        stroke-width="6px";/>'''

html += "</svg></div><table class='table'><thead class='thead-dark'>"

# Data headers
for revision in data:
    date = datetime.strptime(revision.rstrip(), '%a %b %d %H:%M:%S %Y %z')

    html += "<th style='min-width: 300px'>" + date.strftime("%m/%d/%Y") + "</th>"

    if len(data[revision]) > maxLength:
        maxLength = len(data[revision])
html += "</thead>"

# Display the data
row = 1
for i in range(maxLength):
    html += "<tr>"
    col = 0
    for revision in data:
        col += 1
        try:
            html += "<td id='" + str(col) + "-" + str(row) + "'>" + data[revision][i] + "</td>"
        except IndexError:
            html += "<td>&nbsp;</td>"

    html += "</tr>"
    row += 1

html += "</table>"

# Save the output HTML and open it
os.chdir(owd)
text_file = open("output.html", "wt")
n = text_file.write(html)
text_file.close()
webbrowser.open_new_tab('file:///' + owd + '/output.html')
