from django.db import models
import datetime
from django.utils import timezone
# Create your models here. Django creates database by default

#Question.objects.all()   Questions.objects.order_by('pub_date'[:5]
#Question.objects.get(pk=id)
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=timezone.now())
    # To identiy string
    def __str__(self):
        return self.question_text
    # A specific function to check date time
    def was_published_recently(self):
        now =timezone.now()
        return now >= self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    class Meta:
        # define name of the table
        db_table = 'questions'


class Choice(models.Model):
    # question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    def __str__(self):
        return self.choice_text


class BuildingInfo(models.Model):
    building_name = models.CharField(unique=True, max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'building_info'


class SimulationInfo(models.Model):
    bid = models.IntegerField(blank=True, null=True)
    simulation_option = models.CharField(max_length=45, blank=True, null=True)
    simu_time = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'simulation_info'

class ConsumpDomesticHotWater(models.Model):
    sid = models.IntegerField()
    bid = models.IntegerField(blank=True, null=True)
    month1 = models.FloatField(blank=True, null=True)
    month2 = models.FloatField(blank=True, null=True)
    month3 = models.FloatField(blank=True, null=True)
    month4 = models.FloatField(blank=True, null=True)
    month5 = models.FloatField(blank=True, null=True)
    month6 = models.FloatField(blank=True, null=True)
    month7 = models.FloatField(blank=True, null=True)
    month8 = models.FloatField(blank=True, null=True)
    month9 = models.FloatField(blank=True, null=True)
    month10 = models.FloatField(blank=True, null=True)
    month11 = models.FloatField(blank=True, null=True)
    month12 = models.FloatField(blank=True, null=True)

    class Meta:

        db_table = 'consump_domestic_hot_water'

class ConsumpElectricCooling(models.Model):
    sid = models.IntegerField()
    bid = models.IntegerField(blank=True, null=True)
    month1 = models.FloatField(blank=True, null=True)
    month2 = models.FloatField(blank=True, null=True)
    month3 = models.FloatField(blank=True, null=True)
    month4 = models.FloatField(blank=True, null=True)
    month5 = models.FloatField(blank=True, null=True)
    month6 = models.FloatField(blank=True, null=True)
    month7 = models.FloatField(blank=True, null=True)
    month8 = models.FloatField(blank=True, null=True)
    month9 = models.FloatField(blank=True, null=True)
    month10 = models.FloatField(blank=True, null=True)
    month11 = models.FloatField(blank=True, null=True)
    month12 = models.FloatField(blank=True, null=True)

    class Meta:

        db_table = 'consump_electric_cooling'

class ConsumpEquipmentTenant(models.Model):
    sid = models.IntegerField()
    bid = models.IntegerField(blank=True, null=True)
    month1 = models.FloatField(blank=True, null=True)
    month2 = models.FloatField(blank=True, null=True)
    month3 = models.FloatField(blank=True, null=True)
    month4 = models.FloatField(blank=True, null=True)
    month5 = models.FloatField(blank=True, null=True)
    month6 = models.FloatField(blank=True, null=True)
    month7 = models.FloatField(blank=True, null=True)
    month8 = models.FloatField(blank=True, null=True)
    month9 = models.FloatField(blank=True, null=True)
    month10 = models.FloatField(blank=True, null=True)
    month11 = models.FloatField(blank=True, null=True)
    month12 = models.FloatField(blank=True, null=True)

    class Meta:

        db_table = 'consump_equipment_tenant'

class ConsumpFuelHeating(models.Model):
    sid = models.IntegerField()
    bid = models.IntegerField(blank=True, null=True)
    month1 = models.FloatField(blank=True, null=True)
    month2 = models.FloatField(blank=True, null=True)
    month3 = models.FloatField(blank=True, null=True)
    month4 = models.FloatField(blank=True, null=True)
    month5 = models.FloatField(blank=True, null=True)
    month6 = models.FloatField(blank=True, null=True)
    month7 = models.FloatField(blank=True, null=True)
    month8 = models.FloatField(blank=True, null=True)
    month9 = models.FloatField(blank=True, null=True)
    month10 = models.FloatField(blank=True, null=True)
    month11 = models.FloatField(blank=True, null=True)
    month12 = models.FloatField(blank=True, null=True)

    class Meta:

        db_table = 'consump_fuel_heating'

class ConsumpHvac(models.Model):
    sid = models.IntegerField()
    bid = models.IntegerField(blank=True, null=True)
    month1 = models.FloatField(blank=True, null=True)
    month2 = models.FloatField(blank=True, null=True)
    month3 = models.FloatField(blank=True, null=True)
    month4 = models.FloatField(blank=True, null=True)
    month5 = models.FloatField(blank=True, null=True)
    month6 = models.FloatField(blank=True, null=True)
    month7 = models.FloatField(blank=True, null=True)
    month8 = models.FloatField(blank=True, null=True)
    month9 = models.FloatField(blank=True, null=True)
    month10 = models.FloatField(blank=True, null=True)
    month11 = models.FloatField(blank=True, null=True)
    month12 = models.FloatField(blank=True, null=True)

    class Meta:

        db_table = 'consump_hvac'

class ConsumpLightingFacility(models.Model):
    sid = models.IntegerField()
    bid = models.IntegerField(blank=True, null=True)
    month1 = models.IntegerField(blank=True, null=True)
    month2 = models.IntegerField(blank=True, null=True)
    month3 = models.IntegerField(blank=True, null=True)
    month4 = models.IntegerField(blank=True, null=True)
    month5 = models.IntegerField(blank=True, null=True)
    month6 = models.IntegerField(blank=True, null=True)
    month7 = models.IntegerField(blank=True, null=True)
    month8 = models.IntegerField(blank=True, null=True)
    month9 = models.IntegerField(blank=True, null=True)
    month10 = models.IntegerField(blank=True, null=True)
    month11 = models.IntegerField(blank=True, null=True)
    month12 = models.IntegerField(blank=True, null=True)

    class Meta:

        db_table = 'consump_lighting_facility'

class PkPowerDomesticHotWater(models.Model):
    sid = models.IntegerField(blank=True, null=True)
    bid = models.IntegerField(blank=True, null=True)
    pk_power = models.FloatField(blank=True, null=True)

    class Meta:

        db_table = 'pk_power_domestic_hot_water'

class PkPowerElectricCooling(models.Model):
    sid = models.IntegerField(blank=True, null=True)
    bid = models.IntegerField(blank=True, null=True)
    pk_power = models.FloatField(blank=True, null=True)

    class Meta:

        db_table = 'pk_power_electric_cooling'

class PkPowerEquipmentTenant(models.Model):
    sid = models.IntegerField(blank=True, null=True)
    bid = models.IntegerField(blank=True, null=True)
    pk_power = models.FloatField(blank=True, null=True)

    class Meta:

        db_table = 'pk_power_equipment_tenant'

class PkPowerFuelHeating(models.Model):
    sid = models.IntegerField(blank=True, null=True)
    bid = models.IntegerField(blank=True, null=True)
    pk_power = models.FloatField(blank=True, null=True)

    class Meta:

        db_table = 'pk_power_fuel_heating'

class PkPowerHvac(models.Model):
    sid = models.IntegerField(blank=True, null=True)
    bid = models.IntegerField(blank=True, null=True)
    pk_power = models.FloatField(blank=True, null=True)

    class Meta:

        db_table = 'pk_power_hvac'

class PkPowerLightingFacility(models.Model):
    sid = models.IntegerField(blank=True, null=True)
    bid = models.IntegerField(blank=True, null=True)
    pk_power = models.FloatField(blank=True, null=True)

    class Meta:

        db_table = 'pk_power_lighting_facility'