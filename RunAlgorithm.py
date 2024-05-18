from Algorithm.Objects.Equity import Stock as eqClass
import Algorithm.libs.LIB_SFQ_Vanilla_MC_Fns as lib
from dateutil import parser
import matplotlib.pyplot as mp
import csv

def setCycle(ticker, currentPrice):
    equity = eqClass(ticker)        ### initializes class with a "DOW" ticker name
    lib.calibrateModelInit(ticker)  ### opens dow_historic.csv with last year prices
                                    ### splits data to data and price
                                    ### loads weekly prices till encounters the last day of the week
                                    ### then calculates weekly drift and volatility and stores in respective lists
                                    ### then stores those lists in dow_calibrations_csv
                                    
    equity.setTodayPrice(currentPrice)          ### adds the last price of 2015 to be acting as a price to get first calculations on
    equity.setLastSelectedPercentile(50)        ### sets percentile field to 50
    expectedPrice = lib.getExpectedPrice(equity)### gets expected price for a current friday
    equity.setLastSelectedPrice(expectedPrice)  ### records new calculated price of friday
    direction = lib.getDirection(equity)        ### returns SHORT or LONG if previos price is higher/lower than the new calculated price
    equity.setLastDirection(direction)          ### records direction in the equity object
    equity.setLastPurchasedPrice(currentPrice)  ### records previous price
    equity.saveObject()                         ### stores all info in DOW.csv(the one inb Object folder)

def runCycle(ticker, currentPrice,currentDate):
    equity = eqClass(ticker)
    equity.loadObject()
    equity.setTodayPrice(currentPrice)  ### = append to the price list

    if not lib.isLastDayOfTheBWeek(currentDate):### keep adding prices to the list till we encounter last day of the week
        equity.saveObject()
        return equity.getLastSelectedPrice()

    equity.setLastSelectedPercentile(50)
    expectedPrice = lib.getExpectedPrice(equity)### got the predicted amount for friday
    equity.setLastSelectedPrice(expectedPrice)
    direction = lib.getDirection(equity)    
    equity.setLastDirection(direction)
    equity.setLastPurchasedPrice(currentPrice)### what was the last friday
    ###(equity.getLastPurchasedPrice() - equity.getLastSelectedPrice())
    equity.emptyThisWeekPrices()
    equity.saveObject()
    
    return equity.getLastSelectedPrice()

def getExpectedvsActual(ticker,lastPrice):
    fileName = r"/Users/macbook/Desktop/Algorithm/Prices/{}.csv".format(ticker)  # load prices
    with open(fileName, 'r') as fileHandler:
        entries = csv.reader(fileHandler)  # load csv files
        weeklyDates = []
        ActualPrices = []
        PredictedPrices = [lastPrice]
        i = 0
        for prices in entries:
            date = parser.parse(prices[0])
            aPrice = float(prices[1])       ### actual price
            ePrice = runCycle(ticker, aPrice, date) ### gives the new predicted price for current week
            if lib.isLastDayOfTheBWeek(date):       
                i += 1
                weeklyDates.append(date)
                PredictedPrices.append(ePrice)
                ActualPrices.append(aPrice)
    return ActualPrices, PredictedPrices, weeklyDates

ticker = "DOW"
lastPrice = 49.716367
setCycle(ticker, lastPrice)
aPrices, pPrices, dates = getExpectedvsActual(ticker,lastPrice)

balance = 1000000
flag = ''
bought = []
longEntranceDates=[]

for i in range (2, len(aPrices) - 1): 
    if (flag == 'purchased'):
            balance += 1000 * aPrices[i]
            flag = ''
            print('balance is', balance)
            print('Income is: ', 1000*(aPrices[i] - aPrices[i-1]))
            print('-----------')
            
    if (aPrices[i] > aPrices[i-1] and aPrices[i] > aPrices[i-2]):
        if (aPrices[i] < pPrices[i+1]):
            print('purchased at', aPrices[i])
            buy = 1000 * aPrices[i]
            balance -= buy
            flag = 'purchased'
            longEntranceDates.append(dates[i])
            bought.append(aPrices[i])
            
balance += 1000 * aPrices[-1] ### close the last unaccounted purchase

print('Closing Balance ', balance, 'flag is: ', flag)
print('Total Income ' , (balance - 1000000), '. In %: ', (balance - 1000000)/1000000*100,'%')
    
del pPrices[-1]
mp.plot(dates, aPrices, 'o', color = 'grey', label='Actual prices')  # Blue dots for aPrices
###mp.plot(dates, pPrices, 'ro', label='Predicted prices')
mp.plot(longEntranceDates, bought, 'go', label = 'Bought here')
mp.legend()
mp.show()
