from django.db import models


class Revenue(models.Model):
    revenue_name=models.CharField(max_length=50, unique=True)
    revenue_amount=models.IntegerField(default=0)
    year=models.IntegerField()
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  str(self.revenue_name)
    class Meta:
            verbose_name = ('Revenue ')
            verbose_name_plural = ('Revenues' )

class Taxrate (models.Model):
    tax_rate=models.FloatField(default=0)
    year=models.IntegerField()
    active_rate=models.BooleanField(default=False)
    year=models.IntegerField()
   # date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  'Tax Rate ' +  str(self.tax_rate)
    class Meta:
            verbose_name = ('Taxrate ')
            verbose_name_plural = ('Taxrate' )

class Expenses (models.Model):
    expenses_name=models.CharField(max_length=50,unique=True)
    expenses_amount=models.IntegerField(default=0)
    year=models.IntegerField()
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  str(self.expenses_name)
    class Meta:
            verbose_name = ('Expense ')
            verbose_name_plural = ('Expenses' )

class Assets (models.Model):
    asset_name=models.CharField(max_length=50,unique=True)
    asset_amount=models.IntegerField(default=0)
    year=models.IntegerField()
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  str(self.asset_name)
    class Meta:
            verbose_name = ('Asset ')
            verbose_name_plural = ('Assets' )
 

class Liabilities (models.Model):
    Liabilities_name=models.CharField(max_length=50 , unique=True)
    Liabilities_amount=models.IntegerField(default=0)
    year=models.IntegerField()
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  str(self.Liabilities_name)
    class Meta:
            verbose_name = ('Liabilitie ')
            verbose_name_plural = ('Liabilities' )