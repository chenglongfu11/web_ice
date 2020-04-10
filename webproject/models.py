# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class BuildingInfo(models.Model):
    building_name = models.CharField(unique=True, max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'building_info'


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
        managed = False
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
        managed = False
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
        managed = False
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
        managed = False
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
        managed = False
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
        managed = False
        db_table = 'consump_lighting_facility'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class PkPowerDomesticHotWater(models.Model):
    sid = models.IntegerField(blank=True, null=True)
    bid = models.IntegerField(blank=True, null=True)
    pk_power = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pk_power_domestic_hot_water'


class PkPowerElectricCooling(models.Model):
    sid = models.IntegerField(blank=True, null=True)
    bid = models.IntegerField(blank=True, null=True)
    pk_power = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pk_power_electric_cooling'


class PkPowerEquipmentTenant(models.Model):
    sid = models.IntegerField(blank=True, null=True)
    bid = models.IntegerField(blank=True, null=True)
    pk_power = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pk_power_equipment_tenant'


class PkPowerFuelHeating(models.Model):
    sid = models.IntegerField(blank=True, null=True)
    bid = models.IntegerField(blank=True, null=True)
    pk_power = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pk_power_fuel_heating'


class PkPowerHvac(models.Model):
    sid = models.IntegerField(blank=True, null=True)
    bid = models.IntegerField(blank=True, null=True)
    pk_power = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pk_power_hvac'


class PkPowerLightingFacility(models.Model):
    sid = models.IntegerField(blank=True, null=True)
    bid = models.IntegerField(blank=True, null=True)
    pk_power = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pk_power_lighting_facility'


class Questions(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'questions'


class SimulationInfo(models.Model):
    bid = models.IntegerField(blank=True, null=True)
    simulation_option = models.CharField(max_length=45, blank=True, null=True)
    simu_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'simulation_info'


class WebapplicationChoice(models.Model):
    choice_text = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'webapplication_choice'
