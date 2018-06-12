# oop-data-script

The goal of this repo is to showcase an example of how I have utilized python to enhance my data analysis capabilities.
To give some background, I built these scripts two summers ago when I was doing data analysis on the US stock market.
The goal for me was to create an easy and quick way to load derived data factors. When I state derived data factors, what
I mean our any set of time series data which can be constructed from a set of stocks daily adjusted open/close/high/low
prices. All of my factors (at their base level) use these as inputs. 

Scripting Logic:

(1)  Main Script here is DerivedDataCollector_V8.py
(2) The main script utilizes DataCollection.py, Regression.py, SimBase.py, InputFields.py, and TradeDataFormatting.py. Each
of these modules provide different levels of classes to help build out the script.
(3) Data is originated from the stock_data.csv. The file is in format Date,Symbol,Open,High,Low,Close,Adj Close,Volume.
(4) The idea behind this script is that any factor of interest has specific properties to it (time length, input data fields, field name,
etc). I define different potential types of Fields in the InputFields.py file. In all the class definitions you will notice a similar
pattern - a constructor to define the class and a 'createField' function to actually give add the parameter to the dataset.
(5) Classes are as simple as basic column/field operations (add, diff, divide, multiply) to SD, SMAs, Retracement Pcnt. The key
to see here is that all of the fields defined for the most part, can take other defined fields as inputs. Using this relationship,
You can start defining your own classes such as SMA_PREMIUM.

SMA_PREMIUM = DivideField( Divide( Diff( AdjClose, SMA )), AdjClose) , SD). Simply Current Price - Moving Average in SDs.

(6). The process to add all these fields is a recursive one and is innitiated by the call to initializeCollectionFields. This function
takes in the base data from stock_data.csv and takes each constructed data field one at a time and goes over what inputs are
needed to create the data field. If a field is not available in the constructed data set, it calls the same create field function
on the required input. The process is continued until a primary data field (Open,High,Low,Close,Adj Close,Volume) or a already
created data field is there in the date. What this does is it allows for no duplication of data and faster processing time.

While this script is only about 80 lines long, it constructs over 200 data fields that the user can potentially investigate. An
example of the output can be seen in 'dd_collector_V8_20180612-120906.csv' file.

