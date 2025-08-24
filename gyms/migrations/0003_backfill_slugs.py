from django.db import migrations

def backfill_slugs(apps, schema_editor):
    from django.utils.text import slugify
    Franchise = apps.get_model('gyms', 'Franchise')
    Gym = apps.get_model('gyms', 'Gym')

    def unique_slug(model, base_text, pk=None):
        base = slugify(base_text) or "item"
        base = base[:130]  # deja espacio para sufijos
        slug = base
        i = 2
        exists = lambda s: model.objects.filter(slug=s).exclude(pk=pk).exists()
        while exists(slug):
            suf = f"-{i}"
            slug = (base[:140-len(suf)]) + suf
            i += 1
        return slug

    for obj in Franchise.objects.filter(slug__isnull=True):
        obj.slug = unique_slug(Franchise, obj.name, obj.pk)
        obj.save(update_fields=["slug"])

    for obj in Gym.objects.filter(slug__isnull=True):
        obj.slug = unique_slug(Gym, obj.name, obj.pk)
        obj.save(update_fields=["slug"])
        
class Migration(migrations.Migration):

    dependencies = [
        ('gyms', '0002_alter_franchise_options_alter_gym_options_and_more'),
    ]

    operations = [
        migrations.RunPython(backfill_slugs, migrations.RunPython.noop),
    ]

