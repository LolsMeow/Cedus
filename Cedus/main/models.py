from django.db import models
import datetime
class Patient(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	name = models.CharField(max_length=50)
	email = models.EmailField(unique=True)
	password = models.CharField(max_length=200)

	birth_date = models.DateField(default=datetime.date.today)
	phone_number = models.CharField(max_length=50)
	street_address = models.CharField(max_length=50)
	apt = models.CharField(max_length=50)
	city = models.CharField(max_length=50)
	state = models.CharField(max_length=50)
	zip_code = models.IntegerField()

	provider_name = models.CharField(max_length=50)
	plan_name = models.CharField(max_length=50)
	rx_bin = models.IntegerField()
	id_number = models.IntegerField()
	rx_pcn = models.IntegerField()
	rx_group = models.CharField(max_length=50)

	def __str__(self):
		return self.name