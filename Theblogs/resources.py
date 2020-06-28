from import_export import resources
from .models import Categories 
from django.db import IntegrityError

class CategoryResource(resources.ModelResource):
	class Meta:
		model=Categories
		skip_unchanged=True 
		report_skipped=True

	def save_instance(self, instance, using_transactions=True, dry_run=False):
		try:
			super(CategoryResource,self).save_instance(instance, using_transactions, dry_run)
		except:
			print('e')