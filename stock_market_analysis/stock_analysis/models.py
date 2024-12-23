from django.db import models

class StockData(models.Model):
    symbol = models.CharField(max_length=100)
    opening_price = models.FloatField()
    closing_price = models.FloatField()
    highest_price = models.FloatField()
    lowest_price = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return self.symbol


class StockAnalysis(models.Model):
    stock = models.ForeignKey(StockData, on_delete=models.CASCADE)
    moving_average = models.FloatField()
    volatility = models.FloatField()

    def __str__(self):
        return f'{self.stock.symbol} Analysis'
