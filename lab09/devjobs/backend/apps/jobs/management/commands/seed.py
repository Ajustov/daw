from apps.jobs.models.company import Company
from apps.jobs.models.location import Location
from apps.jobs.models.technology import Technology
from apps.jobs.models.user import User
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
  help = 'Poblar base de datos con datos iniciales'

  @transaction.atomic
  def handle(self, *args, **options):
    admin, created = User.objects.get_or_create(
      username='luisg',
      defaults={
        'email': 'luisgardaz13@gmail.com',
        'is_staff': True,
        'is_superuser': True, 
      },
    )
    if created:
      admin.set_password('1234')
      admin.creator_id = admin.id  # type: ignore
      admin.modifier_id = admin.id  # type: ignore
      admin.save()

    companies = ['Globant', 'Mercado Libre', 'Rappi', 'NTT Data']
    for name in companies:
      Company.objects.get_or_create(
        name=name, defaults={'creator_id': admin.id, 'modifier_id': admin.id}
      )

    locations = [
      'Lima, Perú',
      'Buenos Aires, Argentina',
      'Bogotá, Colombia',
    ]
    for name in locations:
      Location.objects.get_or_create(
        name=name, defaults={'creator_id': admin.id, 'modifier_id': admin.id}
      )

    technologies = ['Python', 'Django', 'React', 'TypeScript', 'PostgreSQL']
    for name in technologies:
      Technology.objects.get_or_create(
        name=name, defaults={'creator_id': admin.id, 'modifier_id': admin.id}
      )

    self.stdout.write(self.style.SUCCESS('Base de datos poblada con éxito'))
