import csv
from dateutil import parser
import numpy as np
import holidays as hl
from pandas.tseries.offsets import BDay
import math 
DIRECTION_SHORT = "short"
DIRECTION_LONG = "long"


def calculateMetricsForWeek(weeklyPrices):
    drift = (weeklyPrices[-1] - weeklyPrices[0]) / weeklyPrices[0]
    vol = np.std(weeklyPrices)/weeklyPrices[0]
    return drift, vol


def isLastDayOfTheBWeek(date):
    isHoliday = False
    isFriday = date.weekday() == 4
    nextDay = date + BDay(1)
    isNextDayFRandHoliday = nextDay.weekday() == 4 and nextDay in hl.UnitedStates()
    isHoliday = isFriday or isNextDayFRandHoliday
    return isHoliday


def getCalibrationFile(ticker):
    return r"/Users/macbook/Desktop/Algorithm/Calibrations/{}_calibration.csv".format(ticker)  # load prices


def saveCalibaredDriftsAndVols(calibrationFile, drifts, vols):
    with open(calibrationFile, 'w') as fileHandler:
        for week in range(0, 51):
            line = "{},{}\n".format(drifts[week], vols[week])
            fileHandler.write(line)
    fileHandler.close()


def calibrateModelInit(ticker):
    fileName = r"/Users/macbook/Desktop/Algorithm/Prices/{}_historic.csv".format(ticker)  # load prices
    weeklyDrifts = []  # initiate list for yearly weekly drifts
    weeklyVols = []  # initiate list for yearly weekly vols
    with open(fileName, 'r') as fileHandler:
        entries = csv.reader(fileHandler)  # load csv files
        weeklyPrices = []  # initiate prices for the week
        for price in entries:  # for every entry in the list
            priceDate = parser.parse(price[0])
            usdPrice = float(price[1])
            weeklyPrices.append(usdPrice)  # add the price, second element in the list
            if isLastDayOfTheBWeek(priceDate):  # check if date, first element in the list is end of B week
                wDrift, wVol = calculateMetricsForWeek(weeklyPrices)  # calculate drift and vol for the week
                weeklyDrifts.append(wDrift)
                weeklyVols.append(wVol)
                if len(weeklyDrifts) > 52 and weeklyVols > 52:
                    break
                weeklyPrices = []  # empty the weekly prices-- reached the end of the week

    calibrationFile = getCalibrationFile(ticker)
    saveCalibaredDriftsAndVols(calibrationFile, weeklyDrifts, weeklyVols)

    return weeklyDrifts, weeklyVols


def generateRawMCValues(currPrice, scenarios, timePoints, Drift, Volatility):
    twoArray = []
    for i in range(0, scenarios): ### for 10000 times
        weeklyPrices = [currPrice]  ### | generates 5 random numbers for a normal distribution with mean of d/t and std of v/sqrt 
        dailyReturns = np.random.normal(Drift/timePoints, Volatility/math.sqrt(timePoints), timePoints)+1 
        for aReturn in dailyReturns: ### | contains average % difference and then how it differes from average
            weeklyPrices.append(weeklyPrices[-1]*(aReturn ))
        twoArray.append(weeklyPrices)
    MCMatrix = np.matrix(twoArray) ### gives 10000 arrays in from MTWThF that contain randomly selected prices multiplied by daily returns
    return (MCMatrix)


def getPercentile(MCMatrix, confidence):
    confValues = []
    for timePoint in MCMatrix.transpose():### MTWThF --> 10000mondays --> for 10000 mondays give one price
        value = np.percentile(np.array(timePoint), confidence)### returns price below which 50% of data falls
        confValues.append(value)
    return confValues   ### returns expected price for each day (day names go vertically)so 5 values vertically


def selectDriftAndVol(ticker):
    weeklyDrift, weeklyVols = loadCalibratedDriftsAndVols(ticker) ### returns two lists for dreifts and vols
    medDrift = np.median(weeklyDrift)
    medVol = np.median(weeklyVols)
    return medDrift, medVol


def getExpectedPrice(equity):
    drift, vol = selectDriftAndVol(equity.ticker) ### gets single weekly median drift and vol value
    MCMatrix = generateRawMCValues(equity.getPrices()[-1], 10000, 5, drift, vol)### gives 5*10000 matrix with returns
    confCurve = getPercentile(MCMatrix, equity.getLastSelectedPercentile())
    return confCurve[-1] ### gets friday's amount


def getDirection(equity):
    currPrice = equity.getPrices()[-1]
    expecptedPrice = equity.getLastSelectedPrice()
    if (currPrice > expecptedPrice):
       ### print(currPrice , "   exp   " , expecptedPrice)
        return DIRECTION_SHORT
    else:
       ### print(currPrice , "   exp   " , expecptedPrice)
        return DIRECTION_LONG

def loadCalibratedDriftsAndVols(ticker):
    calibrationFile = getCalibrationFile(ticker)    ### gets calculated vols and drifts
    with open(calibrationFile, 'r') as fileHandler:
        entries = csv.reader(fileHandler)
        hisotricalVols = []
        historicalDrifts = []
        prices = []
        for row in entries:
            prices.append(row)
        for week in range(1, 51):
            historicalDrifts.append(float(prices[week][0]))
            hisotricalVols.append(float(prices[week][1]))
    fileHandler.close()
    return historicalDrifts,hisotricalVols
