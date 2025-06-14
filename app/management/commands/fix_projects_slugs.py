from django.core.management.base import BaseCommand
from info.models import Project

class Command(BaseCommand):
    help = 'Fix project slugs that are None or empty'

    def handle(self, *args, **kwargs):
        projects = Project.objects.filter(slug__isnull=True) | Project.objects.filter(slug='')
        for project in projects:
            old_slug = project.slug
            project.slug = None
            project.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Updated project "{project.title}": {old_slug} -> {project.slug}'
                )
            )
        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {projects.count()} projects')
        )
