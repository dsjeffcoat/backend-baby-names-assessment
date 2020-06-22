#!/usr/bin/env python
# -*- coding: utf-8 -*-

# BabyNames python coding exercise.

# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

__author__ = "Diarte Jeffcoat w/help from Kyle Negley, Randy Charity, and Yale University Lecture(https://zoo.cs.yale.edu/classes/cs200/lectures/google-python-exercises/babynames/solution/babynames.py)"

"""
Define the extract_names() function below and change main()
to call it.

For writing regex, it's nice to include a copy of the target
text for inspiration. Here's what the HTML looks like in the
baby.html files:
...
<h3 align="center">Popularity in 1990</h3>
....
<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
<tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
<tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
...

Suggested milestones for incremental development:
 - Extract all the text from the file and print it
 - Find and extract the year and print it
 - Extract the names and rank numbers and print them
 - Get the names data into a dict and print it
 - Build the [year, 'name rank', ... ] list and print it
 - Fix main() to use the extracted_names list
"""

import sys
import re
import argparse


def extract_names(filename):
    """
    Given a single file name for babyXXXX.html, returns a
    single list starting with the year string followed by
    the name-rank strings in alphabetical order.
    ['2006', 'Aaliyah 91', 'Aaron 57', 'Abagail 895', ...]
    """

    names = []

    # First, open file and read the content within it
    file = open(filename, 'rU')
    text = file.read()
    # print(text)

    # Match the year in question
    match_year = re.search(r'Popularity\sin\s(\d\d\d\d)', text)
    if not match_year:
        sys.stderr.write('Year not found in directory!\n')
        sys.exit(1)
    year = match_year.group(1)
    names.append(year)

    # Find all tuples within the specified file.
    nametuples = re.findall(
        r'<td>(\d+)</td><td>(\w+)</td>\<td>(\w+)</td>', text)
    # print(nametuples)

    # Store into a dictionary using each name as a key and the rank number as the value
    name_rankings = {}
    for rank, boyname, girlname in nametuples:
        if boyname not in name_rankings:
            name_rankings[boyname] = rank
        if girlname not in name_rankings:
            name_rankings[girlname] = rank

    # Sort the names in the order needed
    sorted_names = sorted(name_rankings.keys())
    for name in sorted_names:
        names.append(name + " " + name_rankings[name])
    return names


def create_parser():
    """Create a command line parser object with 2 argument definitions."""
    parser = argparse.ArgumentParser(
        description="Extracts and alphabetizes baby names from html.")
    parser.add_argument(
        '--summaryfile', help='creates a summary file', action='store_true')
    # The nargs option instructs the parser to expect 1 or more
    # filenames. It will also expand wildcards just like the shell.
    # e.g. 'baby*.html' will work.
    parser.add_argument('files', help='filename(s) to parse', nargs='+')
    return parser


def main(args):
    # Create a command line parser object with parsing rules
    parser = create_parser()
    # Run the parser to collect command line arguments into a
    # NAMESPACE called 'ns'
    ns = parser.parse_args(args)
    # print(ns)

    if not ns:
        parser.print_usage()
        sys.exit(1)

    file_list = ns.files

    # option flag
    create_summary = ns.summaryfile

    # For each filename, call `extract_names()` with that single file.
    # Format the resulting list as a vertical list (separated by newline \n).
    # Use the create_summary flag to decide whether to print the list
    # or to write the list to a summary file (e.g. `baby1990.html.summary`).

    for file in file_list:
        if create_summary:
            with open(file + '.summary', 'w') as ofile:
                for name in '\n'.join(extract_names(file)):
                    ofile.write(name)
        elif file_list:
            for file in file_list:
                print('\n'.join(extract_names(file)))


if __name__ == '__main__':
    main(sys.argv[1:])
