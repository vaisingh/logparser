import sys
from apachelogs import LogParser
from tabulate import tabulate
from pandas import DataFrame

def Top_10_requests(df):
    """ 
    Function for top 10 requested pages and the number of requests made for each
    Params:
        df: Dataframe with valid log entries
        
    """
    df.drop(columns=['host', 'status'], inplace=True)
    df["count"] = ""
    data = df.groupby("url", as_index=False).count().nlargest(10, "count")
    print("Below is the tabular report:")
    tb = data.reset_index()[['url', 'count']]
    del(data)
    tb.index += 1
    tabularized_report = tabulate(tb, headers=[
                                      "Sl.No", "URL", "Number of times requested"])
    print(tabularized_report)


def Percent_success(df):
    """ 
    Function to identify percentage of successfull request
    Params:
        df: Dataframe with valid log entries
    """
    dt = df.sort_values("status")["status"]
    filter1 = dt >= 200
    filter2 = dt < 400
    success_percent = (dt.where(filter1 & filter2).count()/dt.count())*100
    print("Total success percent is: {0}%".format(
        format(success_percent, '.2f')))


def Percent_failed(df):
    """ 
    Function to identify percentage of unsuccessful request
    Params:
        df: Dataframe with valid log entries
    """
    dt = df.sort_values("status")["status"]
    filter1 = dt < 200
    filter2 = dt >= 400
    fail_percent = (dt.where(filter1 | filter2).count()/dt.count())*100
    print("Total fail percent is: {0}%".format(format(fail_percent, '.2f')))


def Top_10_failed(df_in):
    """ 
    Function to identify top 10 failed requests
    Params:
        df_in: Dataframe with valid log entries
        
    """
    df_in.drop(columns=['host'], inplace=True)
    df_in["count"] = ""
    df = df_in.groupby(["url", "status"], as_index=False).count()
    del(df_in)
    df.set_index('url', inplace=True)
    filter1 = df["status"] < 200
    filter2 = df["status"] >= 400
    dt = df.where(filter1 | filter2).dropna()
    del(df)
    dt.drop(columns=["status"], inplace=True)
    de = dt.sort_values(["count"], ascending=False).nlargest(10, "count")
    print("Below is the tabular report:")
    tb = de.reset_index()[['url', 'count']]
    del(de)
    tb.index += 1
    tabularized_report = tabulate(tb, headers=[
                                      "Sl.No", "URL", "Number of times request failed"])
    print(tabularized_report)


def Top_10_host(df):
    """ 
    Function to identify top 10 host making maximum request
    Params:
        df_in: Dataframe with valid log entries
    """
    df.drop(columns=['url', 'status'], inplace=True)
    df["count"] = ""
    data = df.groupby("host").count().nlargest(10, "count")
    print("Below is the tabular report:")
    tb = data.reset_index()[['host', 'count']]
    del(data)
    tb.index += 1
    tabularized_report = tabulate(tb, headers=[
                                      "Sl.No", "HOST", "Number of times requested"])
    print(tabularized_report)


def Parsing_logs(filepath, option):
    """ 
    Function to import log file and perform further tasks
    Params:
        filepath: Path to the log file
        option: Which type of analysis needs to be done
    """
    parser = LogParser(
        "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\" \"-\"")
    requests = []
    # count = 0
    with open(filepath, 'r') as f:
        lines = f.readlines()
        for line in lines:
            try:
                entry = parser.parse(line)
                request = {
                    "url": entry.request_line,
                    "status": entry.final_status,
                    "host": entry.remote_host
                }
                requests.append(request)
                # count += 1
                # if count > 6:
                #     break
            except Exception as e:
                continue
    df = DataFrame(requests, columns=['url', 'status', 'host'])
    if option == 1:
        Top_10_requests(df)
    if option == 2:
        Percent_success(df)
    if option == 3:
        Percent_failed(df)
    if option == 4:
        Top_10_failed(df)
    if option == 5:
        Top_10_host(df)


if __name__ == "__main__":
    """ 
    Entry point
    """
    try:

        print("""
                This program is to analyze the log files generated by apache server.  
                Please choose:
                1 - for Top 10 requested pages and the number of requests made for each.
                2 - for Percentage of successful requests (anything in the 200s and 300s range).
                3 - for Percentage of unsuccessful requests (anything that is not in the 200s or 300s range).
                4 - for Top 10 unsuccessful page requests.
                5 - for Top 10 hosts making the most requests, displaying the IP address and number of requests made.
               """)

        option = int(input("Enter your option:"))   
        print(" Printing the values please wait")
        Parsing_logs(sys.argv[1], option)
    except Exception as e:
        print(e)
