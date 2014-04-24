from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from os.path import basename
from ...models import Photo

class Command(BaseCommand):
    args = 'IMAGEFILE [IMAGEFILE..]'
    help = 'import photo from disk'

    def handle(self, *args, **options):
        for filename in args:
            with open(filename, 'rb') as f:
                photo = Photo()
                photo.image.save(basename(filename), File(f))
                photo.save()
                self.stdout.write('Imported {0}'.format(filename))
