import numpy

import libs.LIB_SFQ_Vanilla_MC_Fns as lib
from dateutil import parser


def testCalculateMetricsForWeek():
    weeklyPrices = [1,2,3,4,5]
    drift, vol = lib.calculateMetricsForWeek(weeklyPrices)
    print("Drift for the numbers is: {}".format(drift))
    print("Volatility for the numbers is: {}".format(vol))

def testIsLastDayOfTheBWeek():
    friday = parser.parse("3/03/2017",dayfirst=True)
    thursday = parser.parse("4/3/2017",dayfirst=True)
    thursBeforeHoliday =parser.parse("3/07/2014",dayfirst=True)
    print("Is thursday last day of the week: {}".format(lib.isLastDayOfTheBWeek(thursday)))
    print("Is friday last day of the week: {}".format(lib.isLastDayOfTheBWeek(friday)))
    print("Is thursday before 4th of  July that is Friday last day of the week: {}".format(lib.isLastDayOfTheBWeek(thursBeforeHoliday)))

def testCalibrateModel():
    lib.calibrateModelInit("DOW")

def testgenerateRawMCValues():
    print("Our curve looks like: {}".format(lib.generateRawMCValues(50,10,10,0.5,0.5)))

def testGetPercentile():
    dayOne = range(1,100)
    dayTwo = range(10,1000,10)
    Matrix = numpy.matrix([dayOne,dayTwo])
    Matrix = Matrix.transpose()
    print("Confidence matrix is: {}".format(lib.getPercentile(Matrix,95)))


testCalculateMetricsForWeek()
testIsLastDayOfTheBWeek()
testCalibrateModel()
testgenerateRawMCValues()
testGetPercentile()