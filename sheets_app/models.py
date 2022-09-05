from django.db import models

class SheetInfo (models.Model):
    id = models.AutoField(primary_key=True, db_column='№')
    order_number = models.IntegerField(db_column='заказ №')
    cost = models.IntegerField(db_column='стоимость,$')
    delivery_time = models.CharField(max_length=10, db_column='срок поставки', help_text='Expiration date')
    cost_roubles = models.IntegerField(db_column='стоимость,₽')

    class Meta :
        db_table = 'goog_sheet_table'

    # def __str__(self):
    #     return self.order_number
