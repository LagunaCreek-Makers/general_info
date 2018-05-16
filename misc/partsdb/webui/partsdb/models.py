from django.db import models


class AssetType(models.Model):
    type = models.CharField(unique=True, max_length=45)
    description = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'asset_type'
        verbose_name = 'Asset Type'
        verbose_name_plural = 'Asset Types'


class Category(models.Model):
    category = models.CharField(max_length=55)
    parent_id = models.IntegerField(blank=True, null=True)
    list = models.CharField(max_length=65)
    breadcrumb = models.CharField(max_length=175)

    def __str__(self):
        return self.breadcrumb

    class Meta:
        managed = False
        db_table = 'category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class CategoryAsset(models.Model):
    asset = models.TextField()
    metadata = models.TextField(blank=True, null=True)
    asset_type = models.ForeignKey(AssetType, models.DO_NOTHING)
    category = models.ForeignKey(Category, models.DO_NOTHING)
    filename = models.CharField(max_length=255)
    size = models.IntegerField()
    md5 = models.CharField(unique=True, max_length=16)
    entry_created = models.DateTimeField()
    entry_modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'category_asset'
        verbose_name = 'Category Asset'
        verbose_name_plural = 'Category Assets'


class Manufacturer(models.Model):
    manufacturer = models.CharField(unique=True, max_length=45)
    homepage_url = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.manufacturer

    class Meta:
        managed = False
        db_table = 'manufacturer'
        verbose_name = 'Manufacturer'
        verbose_name_plural = 'Manufacturers'


class OrderAsset(models.Model):
    asset = models.TextField()
    metadata = models.TextField(blank=True, null=True)
    asset_type = models.ForeignKey(AssetType, models.DO_NOTHING)
    order_number = models.CharField(max_length=45)
    filename = models.CharField(max_length=255)
    size = models.IntegerField()
    md5 = models.CharField(unique=True, max_length=16)
    entry_created = models.DateTimeField()
    entry_modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'order_asset'
        verbose_name = 'Order Asset'
        verbose_name_plural = 'Order Assets'


class Orders(models.Model):
    order_number = models.CharField(max_length=45, blank=True, null=True)
    part = models.ForeignKey('Part', models.DO_NOTHING)
    supplier = models.ForeignKey('Supplier', models.DO_NOTHING)
    quantity = models.IntegerField()
    price = models.FloatField(blank=True, null=True)
    order_asset = models.ForeignKey(OrderAsset, models.DO_NOTHING, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    entry_created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orders'
        verbose_name = 'Orders'
        verbose_name_plural = 'Orders'


class PackageClassification(models.Model):
    type = models.CharField(max_length=45)
    abbreviation = models.CharField(max_length=15,unique=True,null=False)
    classification = models.CharField(max_length=200,unique=True,null=False)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return "{0} - {1}:{2}".format(self.type,self.abbreviation, self.classification)

    class Meta:
        managed = False
        db_table = 'package_classification'
        verbose_name = 'Package Classification'
        verbose_name_plural = 'Package Classifications'


class Packaging(models.Model):
    packaging = models.CharField(unique=True, max_length=45)
    classification = models.ForeignKey(PackageClassification, models.DO_NOTHING)
    description = models.TextField(blank=True, null=True)
    num_pins = models.SmallIntegerField(blank=True, null=True)

    def __str__(self):
        return self.packaging

    class Meta:
        managed = False
        db_table = 'packaging'
        verbose_name = 'Packaging'
        verbose_name_plural = 'Packaging'


class Part(models.Model):
    category = models.ForeignKey(Category, models.DO_NOTHING)
    mpn = models.CharField(max_length=45)
    manufacturer = models.ForeignKey(Manufacturer, models.DO_NOTHING)
    description = models.TextField(blank=True, null=True)
    short_description = models.CharField(max_length=255, blank=True, null=True)
    storage = models.ForeignKey('StorageLocation', models.DO_NOTHING)
    comments = models.TextField(blank=True, null=True)
    packaging = models.ForeignKey(Packaging, models.DO_NOTHING, blank=True, null=True)
    stock_level = models.SmallIntegerField(blank=True, null=True)
    supplier = models.ForeignKey('Supplier', models.DO_NOTHING, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    entry_created = models.DateTimeField(blank=True, null=True)
    entry_modified = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "{0} - {1}".format(self.mpn,self.short_description)

    class Meta:
        managed = False
        db_table = 'part'
        verbose_name = 'Part'
        verbose_name_plural = 'Parts'


class PartAsset(models.Model):
    title = models.CharField(max_length=45, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    asset_type = models.ForeignKey(AssetType, models.DO_NOTHING)
    part = models.ForeignKey(Part, models.DO_NOTHING)
    asset = models.TextField(blank=True, null=True)
    metadata = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    attribution = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    subtype = models.CharField(max_length=255, blank=True, null=True)
    filename = models.CharField(max_length=255)
    size = models.IntegerField()
    md5 = models.CharField(unique=True, max_length=16)
    entry_created = models.DateTimeField()
    entry_modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'part_asset'
        verbose_name = 'Part Asset'
        verbose_name_plural = 'Part Assets'


class PartParameter(models.Model):
    part = models.ForeignKey(Part, models.DO_NOTHING)
    parameter = models.CharField(max_length=45)
    value = models.CharField(max_length=45)
    min = models.CharField(max_length=45, blank=True, null=True)
    max = models.CharField(max_length=45, blank=True, null=True)
    unit = models.ForeignKey('UnitOfMeasurement', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'part_parameter'
        verbose_name = 'Part Parameter'
        verbose_name_plural = 'Part Parameters'


class StorageLocation(models.Model):
    storage_location = models.CharField(unique=True, max_length=45)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.storage_location

    class Meta:
        managed = False
        db_table = 'storage_location'
        verbose_name = 'Storage Location'
        verbose_name_plural = 'Storage Locations'


class Supplier(models.Model):
    name = models.CharField(unique=True, max_length=45)
    url = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'supplier'
        verbose_name_plural = 'Suppliers'


class UnitOfMeasurement(models.Model):
    name = models.CharField(unique=True, max_length=45)
    abbreviation = models.CharField(max_length=45, blank=True, null=True)
    symbol = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'unit_of_measurement'
        verbose_name = 'Unit of Measurement'
        verbose_name_plural = 'Units of Measurement'
