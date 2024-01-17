# csvTool

A small tool written in Python to parse csv files

# Usage

This tool was created to ingest a csv and search for matching criteria between 2 columns. You can then decide which columns information to display in the output window.

When you start the program you will be presented with a Load CSV button at the top. Navigate to your CSV and load it into the program.

The csvTool will show you which columns are available for searching in the Available Columns window

Criteria 1 and Criteria 2 are the criteria associated with the columns you select from the Available Columns window. There is currently a bug that deselects the columns from the Available Columns window if you select them before entering the criteria, so make sure to enter your criteria ahead of time.

You can select which columns you want to output for the results window, and only that information will show for columns that are matching.

# Requirements

requires pandas 

To install:

pip install pandas

**Data Types**:

You can search for boolean, interger, and strings. Additionally you can use * as a wildcard to search for any data in a column, or leave a criteria blank to search for blank cells in a column.

## Example

For example, if you have a CSV of customer data and you want to find customers that match a pair of criteria, but do not want to output all the data about those customers. 

Lets say your CSV contains data for Name, Date, City, Country, Email, Phone Number, and Age. You may want to look up which customers match the criteria of City + Country and then output only the name and email of those customers. 

You can then copy the data from the output window.

## Development Queue

- Save function to save the filtered data to a separate CSV. 
- Option to select more than 2 columns to search by
