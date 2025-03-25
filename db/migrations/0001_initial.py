# Generated by Django 5.0 on 2025-03-25 13:06

import datetime
import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='HackathonSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_team_size', models.PositiveIntegerField(default=4)),
                ('duration', models.DurationField(default=datetime.timedelta(seconds=10800))),
                ('has_started', models.BooleanField(default=False)),
                ('has_ended', models.BooleanField(default=False)),
                ('is_paused', models.BooleanField(default=False)),
                ('time_started', models.DateTimeField(blank=True, null=True)),
                ('time_ended', models.DateTimeField(blank=True, null=True)),
                ('time_paused', models.DateTimeField(blank=True, null=True)),
                ('time_spent_paused', models.DurationField(default=datetime.timedelta(0))),
                ('score_decrement_per_interval', models.IntegerField(default=10)),
                ('score_decrement_interval', models.DurationField(default=datetime.timedelta(seconds=600))),
                ('max_score', models.IntegerField(default=300)),
            ],
            options={
                'verbose_name_plural': 'Hackathon Settings',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('number', models.IntegerField(unique=True)),
                ('description', models.TextField()),
                ('difficulty', models.CharField(choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')], max_length=10)),
                ('samples', models.JSONField(blank=True, null=True)),
                ('tests', models.JSONField(blank=True, null=True)),
            ],
            options={
                'ordering': ['number'],
            },
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_admin', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='TeamProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=100)),
                ('score', models.IntegerField(default=0)),
                ('team_password', models.CharField(max_length=100)),
                ('participants_registered', models.PositiveSmallIntegerField(default=0)),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='team', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-score'],
            },
        ),
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('joined_at', models.DateTimeField(auto_now_add=True)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='db.teamprofile')),
            ],
            options={
                'ordering': ['-joined_at'],
            },
        ),
        migrations.CreateModel(
            name='SharedCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField()),
                ('time_shared', models.DateTimeField()),
                ('file_uuid', models.UUIDField(blank=True, default=uuid.uuid4, null=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shared_code', to='db.question')),
                ('team_member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shared_code', to='db.teammember')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shared_code', to='db.teamprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_code', models.TextField()),
                ('is_correct_answer', models.BooleanField(default=False)),
                ('score', models.IntegerField(default=0)),
                ('time_submitted', models.DateTimeField()),
                ('test_results', models.JSONField(blank=True, null=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='db.question')),
                ('team_member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='db.teammember')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='db.teamprofile')),
            ],
        ),
        migrations.AddIndex(
            model_name='teamprofile',
            index=models.Index(fields=['team_name'], name='db_teamprof_team_na_291c14_idx'),
        ),
        migrations.AddIndex(
            model_name='teamprofile',
            index=models.Index(fields=['team_password'], name='db_teamprof_team_pa_ce7f1d_idx'),
        ),
        migrations.AddIndex(
            model_name='teammember',
            index=models.Index(fields=['team'], name='db_teammemb_team_id_bbe8e2_idx'),
        ),
    ]
