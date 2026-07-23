from apps.jobs.models.company import Company
from apps.jobs.models.location import Location
from apps.jobs.models.technology import Technology
from apps.jobs.models.user import User
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction


class Command(BaseCommand):
  help = 'Poblar base de datos con datos iniciales'

  @transaction.atomic
  def handle(self, *args, **options):
    admin = User.objects.filter(is_superuser=True).first()
    if admin is None:
      raise CommandError('No existe un superusuario')

    companies = ['GLOBANT', 'MERCADO LIBRE', 'RAPPI', 'NTT DATA']
    for name in companies:
      Company.objects.get_or_create(
        name=name,
        defaults={'creator_id': admin.id, 'modifier_id': admin.id},
      )

    locations = [
      'LIMA, PERÚ',
      'BUENOS AIRES, ARGENTINA',
      'BOGOTÁ, COLOMBIA',
    ]
    for name in locations:
      Location.objects.get_or_create(
        name=name,
        defaults={'creator_id': admin.id, 'modifier_id': admin.id},
      )

    technologies = ['PYTHON', 'DJANGO', 'REACT', 'TYPESCRIPT', 'POSTGRESQL']
    for name in technologies:
      Technology.objects.get_or_create(
        name=name,
        defaults={'creator_id': admin.id, 'modifier_id': admin.id},
      )

    self.stdout.write(self.style.SUCCESS('Seed ejecutado con éxito'))
