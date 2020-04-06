# Get Metrics

This program creates an API endpoint that gets the following information from a set of doucments in the 'data' directory:

* Total number of customers that mande an order that day
* Total number of items sold on that day
* The total amount of discount given that day
* The average discount rate applied to the items sold that day
* The average order total for that day
* The total amount of commissions generated that day
* The average amount of commissions per order for that day
* The total amount of commissions earned per promotion that day

## Getting Started

### Prerequisites 

Apart from the standard libraries, you will need to install, 'nltk', 'bs4' and 'pandas'. If you don't have them already you can simply use pip install in your command prompt.

To run this file on your machine you will need to install 'pandas' and 'flask'. In the unlikely event you don't have them already you can simply use pip install in your command prompt.

```
pip install pandas
pip install flask
```
## Program Spesifics

The approach is pretty straight forward, the files are set up in dataframes which are then used to sort and extract the information needed to collect the above listed metrics.

The metrics are collected in order of simplicity, the metric requiring the least amount of calculations and code first, with the most complex coming last.

All the metrics are collected in one function; `get_metrics`, given the time pressure I did not write out unit-tests for that function, I just used print statements as I coded down the function to make sure I am on the right track.

From a user perspective, getting the metrics report is very easy; simply write out the URL endpoint into a browser (or program) followed by the spesific date in format `YYYY-MM-DD`, for example: `http://127.0.0.1:5000/get_metrics/2019-08-02` (obviously replacing the localhost with the published URL once deployed).

The file that is returned is a csv file with the first column the metric description and the second its value.

## What could/should be improved...

Given the time pressure on this project (spend 2-3 hours coding and return within a 24 hour time period), there are a lot of improvements that can and should be made.

The biggest and most obvious is that (pretty much) all calculations and functionality happens in one function, potentially causing problems where a bug in a single line may cause a crash or more faulty/incorrect values than if a different approach was taken.

A more sensible approach would be to use classes, starting with dataframes and data needed for each metric in the top class, branching out into sub-classes for metrics requiring additional data and then bringing it all together with a final result class that inherits from all of the others, having the resulting metrics as instance attributes.
