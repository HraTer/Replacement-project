from django.db import models

class Brand(models.Model):
    brand_name = models.CharField(max_length=100)

    def __str__(self):
        return self.brand_name

class Hardware(models.Model):
    brand_name = models.ForeignKey(Brand, on_delete=models.CASCADE)
    hw_name = models.CharField(max_length=100)
    hw_price = models.IntegerField()
    write_off_length = models.IntegerField()


    def __str__(self):
        write_off_text = f"{self.write_off_length} roky" if self.write_off_length == 3 else f"{self.write_off_length} let"
        return f"{self.hw_name} | Pořizovací cena: {self.hw_price} | Délka odpisu: {write_off_text}"
