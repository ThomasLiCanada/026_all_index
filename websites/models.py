# websites/models.py

from django.db import models
import os


class IndexCategory(models.Model):
    category_name = models.CharField(max_length=1028, null=True)
    category_order_num = models.IntegerField(default=99, null=True)

    def __str__(self):
        return self.category_name


def upload_location(instance, filename):
    file_path = 'website_image/{}'.format(filename)
    return file_path


class Index(models.Model):
    key_words = models.CharField(max_length=2083, null=True)
    address = models.CharField(max_length=2083, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_click_date = models.DateTimeField(null=True, blank=True)
    click_times = models.IntegerField(default=0, null=True)

    website_image_url = models.CharField(max_length=2083, null=True, blank=True)
    website_image = models.ImageField(upload_to=upload_location, null=True, blank=True)
    website_index_position_num = models.IntegerField(default=999, null=True)

    category = models.ForeignKey(IndexCategory, on_delete=models.SET_NULL, null=True, blank=True)

    def get_fields_dict(self):
        return {field.name: getattr(self, field.name) for field in self._meta.fields}

    def delete_website_image(self):
        # Delete the associated website_image file
        if self.website_image:
            try:
                # Use the storage API to delete the file
                storage, path = self.website_image.storage, self.website_image.path
                storage.delete(path)
            except Exception as e:
                # Handle any exceptions, such as FileNotFoundError
                print(f"Error deleting website_image: {e}")

    def delete(self, *args, **kwargs):
        # Call the delete_website_image method before deleting the Index object
        self.delete_website_image()
        super(Index, self).delete(*args, **kwargs)


class ToDoTask(models.Model):
    task_name = models.CharField(max_length=2083, null=True)
    task_reminder1_date = models.DateTimeField(blank=True, null=True)
    task_reminder2_date = models.DateTimeField(blank=True, null=True)
    task_due_date = models.DateTimeField(blank=True, null=True)
    task_done = models.BooleanField(default=False)
    task_created_date = models.DateTimeField(auto_now_add=True, null=True)

    def get_fields_dict(self):
        return {field.name: getattr(self, field.name) for field in self._meta.fields}