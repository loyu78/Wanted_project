# Generated by Django 3.0.6 on 2020-06-17 05:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'bookmarks',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'categories',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
            options={
                'db_table': 'cities',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('registration_number', models.IntegerField()),
                ('revenue', models.IntegerField()),
                ('description', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('contact_number', models.CharField(max_length=50)),
                ('website', models.TextField(blank=True)),
                ('keyword', models.CharField(max_length=300, null=True)),
                ('recommender', models.CharField(max_length=100, null=True)),
                ('image_url', models.URLField(max_length=2000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=0)),
            ],
            options={
                'db_table': 'companies',
            },
        ),
        migrations.CreateModel(
            name='Company_matchup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=0)),
            ],
            options={
                'db_table': 'companies_matchup',
            },
        ),
        migrations.CreateModel(
            name='Company_matchup_item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expiration', models.BooleanField(default=0)),
            ],
            options={
                'db_table': 'companies_matchup_items',
            },
        ),
        migrations.CreateModel(
            name='Company_tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'companies_tags',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('number', models.CharField(max_length=30, null=True)),
                ('currency', models.CharField(max_length=10, null=True)),
                ('english_currency', models.CharField(max_length=10)),
                ('exchange_rate', models.FloatField()),
                ('tenthousand_unit', models.CharField(max_length=10, null=True)),
            ],
            options={
                'db_table': 'countries',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'employees',
            },
        ),
        migrations.CreateModel(
            name='Expiration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'expirations',
            },
        ),
        migrations.CreateModel(
            name='Foundation_year',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'foundation_years',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.URLField(max_length=2000, null=True)),
            ],
            options={
                'db_table': 'images',
            },
        ),
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'industries',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'items',
            },
        ),
        migrations.CreateModel(
            name='Job_category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'job_categories',
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=0)),
            ],
            options={
                'db_table': 'like',
            },
        ),
        migrations.CreateModel(
            name='Matchup_item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('displayed_amount', models.IntegerField(default=0)),
                ('price_amount', models.IntegerField(default=0)),
                ('count', models.IntegerField(default=0)),
                ('days', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'matchup_items',
            },
        ),
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('period', models.IntegerField(default=0)),
                ('displayed_amount', models.IntegerField(default=0)),
                ('price_amount', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'networks',
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_level', models.IntegerField(default=0)),
                ('max_level', models.CharField(max_length=50)),
                ('entry', models.BooleanField(default=0)),
                ('mim_wage', models.IntegerField(default=0)),
                ('max_wage', models.IntegerField(default=0)),
                ('expiry_date', models.DateField(null=True)),
                ('always', models.BooleanField(default=0)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('responsibility', models.TextField()),
                ('qualification', models.TextField()),
                ('preferred', models.TextField(blank=True, null=True)),
                ('benefit', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('referrer', models.IntegerField()),
                ('volunteer', models.IntegerField()),
                ('total', models.IntegerField()),
            ],
            options={
                'db_table': 'positions',
            },
        ),
        migrations.CreateModel(
            name='Position_item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('image_url', models.URLField(max_length=2000, null=True)),
                ('title', models.CharField(max_length=50, null=True)),
                ('description', models.CharField(max_length=100, null=True)),
                ('click', models.IntegerField(default=0, null=True)),
                ('is_valid', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'positions_items',
            },
        ),
        migrations.CreateModel(
            name='Position_workplace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'positions_workplaces',
            },
        ),
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'proposals',
            },
        ),
        migrations.CreateModel(
            name='Reading',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read', models.BooleanField(default=0)),
            ],
            options={
                'db_table': 'readings',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'roles',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'tags',
            },
        ),
        migrations.CreateModel(
            name='Temp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tid', models.CharField(max_length=100, null=True)),
                ('user', models.IntegerField(null=True)),
            ],
            options={
                'db_table': 'temps',
            },
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
                ('image_url', models.URLField(max_length=2000)),
                ('inner_image_url', models.URLField(max_length=2000)),
                ('inner_description', models.TextField()),
            ],
            options={
                'db_table': 'themes',
            },
        ),
        migrations.CreateModel(
            name='Workplace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=1000)),
                ('lat', models.DecimalField(decimal_places=7, max_digits=10, null=True)),
                ('lng', models.DecimalField(decimal_places=7, max_digits=10, null=True)),
                ('represent', models.BooleanField(default=0)),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='company.City')),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='company', to='company.Company')),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='company.Country')),
            ],
            options={
                'db_table': 'workplaces',
            },
        ),
        migrations.CreateModel(
            name='Volunteers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('position', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='company.Position')),
            ],
            options={
                'db_table': 'volunteers',
            },
        ),
    ]
