import csv    
import pandas as pd
from pprint import pprint
from pytrends.request import TrendReq

SPREADSHEET_URL = '1022_ufEh0V2xeSGDa1CWgRP70q6WfNX9HF7VN6CrBAE'
CLIENT_NAME = '[GUMTREE]'
GEO = 'AU'


def exportToCSV(source,name):
    """
        Takes in a dictionary as a source and the proposed name for the csv file
        The output will be a CSV file with the proposed name
    """
    with open(name, mode ='w',newline='') as finalOutput:
        outputWriter = csv.writer(finalOutput,delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
        for row in source:
            outputWriter.writerow(row)

def readCSV(CSVName):
    """
        Takes in a name of a CSV file to read
        The output will be a dictionary
    """
    input = csv.reader(open(CSVName))  
    result = []
    for row in input: 
        result.append(row)
    return result


def getTrendData(df,geo):
    """
        Take a dataframe which will be used as a keyword list
        Process the interest over time data
        Format it into a accessible, ready-to-upload table to Google Sheets

    """
    pytrend = TrendReq()
    finalResults = []
    
    for each in df:
        pytrend.build_payload(kw_list = [each[0]], timeframe='today 3-m', geo=geo)
        results = pytrend.interest_over_time()

        if not results.empty:
            results = results.drop(['isPartial'], axis = 1)
            allRows = list(results.index.values)
            for row in allRows:
                smallArray = []
                dt = pd.to_datetime(str(row))
                dt = dt.strftime('%d/%m/%Y')
                smallArray.append(dt)
                smallArray.append(each[0])
                smallArray.append(int(results.loc[row,:]))
                smallArray.append(each[1])
                finalResults.append(smallArray)
            
    finalResults.insert(0,["date","keyword","trend","category"])
    exportToCSV(finalResults,CLIENT_NAME+"-"+geo+".csv")
    finalResults.clear()
    
    
def getRelatedData(keywords,geo):
    """
        Takes in a dictinary of dataframe from Google Trends API
        Format it into a accessible, ready-to-upload table to Google Sheets
    """
    pytrend = TrendReq()
    results = [["keyword","type","query","value"]]
   
    for keyword in keywords:
        pytrend.build_payload(kw_list = [keyword[0]], timeframe='now 7-d', geo=geo)
        df = pytrend.related_queries()
        
        if df:
            if df[keyword[0]]["top"] is not None:
                for each in range(len(df[keyword[0]]["top"])):
                    results.append([keyword[0],"top",df[keyword[0]]["top"].iloc[each,0],int(df[keyword[0]]["top"].iloc[each,1])])
            if df[keyword[0]]["rising"] is not None:
                for each in range(len(df[keyword[0]]["rising"])):
                    results.append([keyword[0],"rising",df[keyword[0]]["rising"].iloc[each,0],int(df[keyword[0]]["rising"].iloc[each,1])])
    exportToCSV(results,CLIENT_NAME+"-"+geo+"-TopOrRising.csv")
    

if __name__ == "__main__":
    getRelatedData(["dress","mini dress","midi dress","party dress","formal dress","maxi dress","cocktail dress"],'AU')
    


