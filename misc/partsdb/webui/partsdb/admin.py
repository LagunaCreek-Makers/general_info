from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(AssetType)
admin.site.register(Category)
admin.site.register(CategoryAsset)
admin.site.register(Manufacturer)
admin.site.register(OrderAsset)
admin.site.register(Orders)
admin.site.register(PackageClassification)
admin.site.register(Packaging)
admin.site.register(Part)
admin.site.register(PartAsset)
admin.site.register(PartParameter)
admin.site.register(StorageLocation)
admin.site.register(Supplier)
admin.site.register(UnitOfMeasurement)
