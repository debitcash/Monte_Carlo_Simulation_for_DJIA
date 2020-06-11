from Objects.Equity import Stock as eqClass
import libs.LIB_SFQ_Vanilla_MC_Fns as lib
from dateutil import parser
import matplotlib.pyplot as mp
import csv

def setCycle(ticker, currentPrice):
    equity = eqClass(ticker) #making our ticker(DOW) a member of the class "Stock"
    lib.calibrateModelInit(ticker) #gives weekly drifts and vols
    equity.setTodayPrice(currentPrice) #
    equity.setLastSelectedPercentile(50)
    expectedPrice = lib.getExpectedPrice(equity)
    equity.setLastSelectedPrice(expectedPrice)
    direction = lib.getDirection(equity)
    equity.setLastDirection(direction)
    equity.setLastPurchasedPrice(currentPrice)
    equity.saveObject()

def runCycle(ticker, currentPrice,currentDate):
    equity = eqClass(ticker)
    equity.loadObject()
    equity.setTodayPrice(currentPrice)

    if not lib.isLastDayOfTheBWeek(currentDate):
        equity.saveObject()
        return equity.getLastSelectedPrice()

    equity.setLastSelectedPercentile(50)
    expectedPrice = lib.getExpectedPrice(equity)
    equity.setLastSelectedPrice(expectedPrice)
    direction = lib.getDirection(equity)
    equity.setLastDirection(direction)
    equity.setLastPurchasedPrice(currentPrice)
    equity.emptyThisWeekPrices()
    equity.saveObject()
    return equity.getLastSelectedPrice()

def getExpectedvsActual(ticker,lastPrice):
    fileName = r"..\Prices\{}.csv".format(ticker)  # load prices
    with open(fileName, 'r') as fileHandler:
        entries = csv.reader(fileHandler)  # load csv files
        weeklyDates = []
        ActualPrices = []
        PredictedPrices = [lastPrice]
        i = 0
        for prices in entries:
            date = parser.parse(prices[0])
            aPrice = float(prices[1])
            ePrice = runCycle(ticker, aPrice, date)
            if lib.isLastDayOfTheBWeek(date):
                i += 1
                print("Doing week {}".format(i))
                weeklyDates.append(date)
                PredictedPrices.append(ePrice)
                ActualPrices.append(aPrice)

    return ActualPrices, PredictedPrices, weeklyDates


ticker = "DOW"
lastPrice = 49.716367
setCycle(ticker, lastPrice)
aPrices, pPrices, dates = getExpectedvsActual(ticker,lastPrice)
del pPrices[-1]
mp.plot(dates, aPrices, dates, pPrices,'r--')
mp.show()