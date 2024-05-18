def saveObjectToStorage(aStock):
    fileName = r"/Users/macbook/Desktop/Algorithm/Objects/Storage/{}.csv".format(aStock.ticker)
    with open(fileName, 'w') as fileHandler:
        dataLine = 'Data:,{},{},{},{}\n'
        fDL = dataLine.format(aStock.lastSelectedPrice, aStock.lastPurchasedPrice,
                              aStock.lastDirection,aStock.lastSelectedPercentile)
        fileHandler.write(fDL)
        pricesLine = 'Prices:'
        for price in aStock.prices:
            pricesLine = pricesLine+',{}'.format(price)
        fileHandler.write(pricesLine)
    fileHandler.close()

def loadObjectFromStorage(aStock):
    fileName = r"/Users/macbook/Desktop/Algorithm/Objects/Storage/{}.csv".format(aStock.ticker)
    fileHandler = open(fileName,'r')
    values = fileHandler.readlines()
    data = values[0].split(',')
    prices = values[1].split(',')
    return data, prices


class Stock(object):

    def __init__(self, aTicker):
        self.ticker = aTicker
        self.lastSelectedPrice = 0
        self.lastPurchasedPrice = 0
        self.prices = []

    def getLastSelectedPrice(self):
        return self.lastSelectedPrice

    def setLastSelectedPrice(self, price):
        self.lastSelectedPrice = price
    
    def getLastDirection(self):
        return self.lastDirection

    def setLastDirection(self, direction):
        self.lastDirection = direction

    def getLastSelectedPercentile(self):
        return self.lastSelectedPercentile

    def setLastSelectedPercentile(self, percentile):
        self.lastSelectedPercentile = percentile

    def getLastPurchasedPrice(self):
        return self.lastPurchasedPrice
    
    def setLastPurchasedPrice(self, price):
        self.lastPurchasedPrice = price

    def setTodayPrice(self, price):
        self.prices.append(price)

    def getPrices(self):
        return self.prices

    def saveObject(self):
        saveObjectToStorage(self)

    def loadObject(self):
        data,loadedPrices = loadObjectFromStorage(self)
        self.lastSelectedPrice = float(data[1])
        self.lastPurchasedPrice = float(data[2])
        self.lastDirection = data[3]
        self.lastSelectedPercentile = float(data[4])
        self.prices = []
        for column in range(1,len(loadedPrices)):
            loadedPrice = float(loadedPrices[column])
            self.prices.append(loadedPrice)

    def emptyThisWeekPrices(self):
        self.prices = []
