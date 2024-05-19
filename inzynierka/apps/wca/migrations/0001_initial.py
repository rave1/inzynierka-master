# Generated by Django 5.0.6 on 2024-05-19 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArInternalMetadata',
            fields=[
                ('key', models.CharField(max_length=191, primary_key=True, serialize=False)),
                ('value', models.CharField(blank=True, max_length=191, null=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
            ],
            options={
                'db_table': 'ar_internal_metadata',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Championships',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('competition_id', models.CharField(max_length=191)),
                ('championship_type', models.CharField(max_length=191)),
            ],
            options={
                'db_table': 'championships',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Competitions',
            fields=[
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('cityname', models.CharField(db_column='cityName', max_length=50)),
                ('countryid', models.CharField(db_column='countryId', max_length=50)),
                ('information', models.TextField(blank=True, null=True)),
                ('year', models.PositiveSmallIntegerField()),
                ('month', models.PositiveSmallIntegerField()),
                ('day', models.PositiveSmallIntegerField()),
                ('endmonth', models.PositiveSmallIntegerField(db_column='endMonth')),
                ('endday', models.PositiveSmallIntegerField(db_column='endDay')),
                ('cancelled', models.IntegerField()),
                ('eventspecs', models.TextField(blank=True, db_column='eventSpecs', null=True)),
                ('wcadelegate', models.TextField(blank=True, db_column='wcaDelegate', null=True)),
                ('organiser', models.TextField(blank=True, null=True)),
                ('venue', models.CharField(max_length=240)),
                ('venueaddress', models.CharField(blank=True, db_column='venueAddress', max_length=120, null=True)),
                ('venuedetails', models.CharField(blank=True, db_column='venueDetails', max_length=120, null=True)),
                ('external_website', models.CharField(blank=True, max_length=200, null=True)),
                ('cellname', models.CharField(db_column='cellName', max_length=45)),
                ('latitude', models.IntegerField(blank=True, null=True)),
                ('longitude', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Competitions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Continents',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('recordname', models.CharField(db_column='recordName', max_length=3)),
                ('latitude', models.IntegerField()),
                ('longitude', models.IntegerField()),
                ('zoom', models.IntegerField()),
            ],
            options={
                'db_table': 'Continents',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Countries',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('continentid', models.CharField(db_column='continentId', max_length=50)),
                ('iso2', models.CharField(blank=True, max_length=2, null=True)),
            ],
            options={
                'db_table': 'Countries',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EligibleCountryIso2SForChampionship',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('championship_type', models.CharField(max_length=191)),
                ('eligible_country_iso2', models.CharField(max_length=191)),
            ],
            options={
                'db_table': 'eligible_country_iso2s_for_championship',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=54)),
                ('rank', models.IntegerField()),
                ('format', models.CharField(max_length=10)),
                ('cellname', models.CharField(db_column='cellName', max_length=45)),
            ],
            options={
                'db_table': 'Events',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Formats',
            fields=[
                ('id', models.CharField(max_length=1, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('sort_by', models.CharField(max_length=255)),
                ('sort_by_second', models.CharField(max_length=255)),
                ('expected_solve_count', models.IntegerField()),
                ('trim_fastest_n', models.IntegerField()),
                ('trim_slowest_n', models.IntegerField()),
            ],
            options={
                'db_table': 'Formats',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Persons',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('subid', models.IntegerField()),
                ('name', models.CharField(blank=True, max_length=80, null=True)),
                ('countryid', models.CharField(db_column='countryId', max_length=50)),
                ('gender', models.CharField(blank=True, max_length=1, null=True)),
            ],
            options={
                'db_table': 'Persons',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Ranksaverage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('personid', models.CharField(db_column='personId', max_length=10)),
                ('eventid', models.CharField(db_column='eventId', max_length=6)),
                ('best', models.IntegerField()),
                ('worldrank', models.IntegerField(db_column='worldRank')),
                ('continentrank', models.IntegerField(db_column='continentRank')),
                ('countryrank', models.IntegerField(db_column='countryRank')),
            ],
            options={
                'db_table': 'RanksAverage',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Rankssingle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('personid', models.CharField(db_column='personId', max_length=10)),
                ('eventid', models.CharField(db_column='eventId', max_length=6)),
                ('best', models.IntegerField()),
                ('worldrank', models.IntegerField(db_column='worldRank')),
                ('continentrank', models.IntegerField(db_column='continentRank')),
                ('countryrank', models.IntegerField(db_column='countryRank')),
            ],
            options={
                'db_table': 'RanksSingle',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('competitionid', models.CharField(db_column='competitionId', max_length=32)),
                ('eventid', models.CharField(db_column='eventId', max_length=6)),
                ('roundtypeid', models.CharField(db_column='roundTypeId', max_length=1)),
                ('pos', models.SmallIntegerField()),
                ('best', models.IntegerField()),
                ('average', models.IntegerField()),
                ('personname', models.CharField(blank=True, db_column='personName', max_length=80, null=True)),
                ('personid', models.CharField(db_column='personId', max_length=10)),
                ('personcountryid', models.CharField(blank=True, db_column='personCountryId', max_length=50, null=True)),
                ('formatid', models.CharField(db_column='formatId', max_length=1)),
                ('value1', models.IntegerField()),
                ('value2', models.IntegerField()),
                ('value3', models.IntegerField()),
                ('value4', models.IntegerField()),
                ('value5', models.IntegerField()),
                ('regionalsinglerecord', models.CharField(blank=True, db_column='regionalSingleRecord', max_length=3, null=True)),
                ('regionalaveragerecord', models.CharField(blank=True, db_column='regionalAverageRecord', max_length=3, null=True)),
            ],
            options={
                'db_table': 'Results',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Rounds',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sorry_message', models.CharField(db_collation='utf8_general_ci', max_length=172)),
            ],
            options={
                'db_table': 'Rounds',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Roundtypes',
            fields=[
                ('id', models.CharField(max_length=1, primary_key=True, serialize=False)),
                ('rank', models.IntegerField()),
                ('name', models.CharField(max_length=50)),
                ('cellname', models.CharField(db_column='cellName', max_length=45)),
                ('final', models.IntegerField()),
            ],
            options={
                'db_table': 'RoundTypes',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SchemaMigrations',
            fields=[
                ('version', models.CharField(max_length=191, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'schema_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Scrambles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scrambleid', models.PositiveIntegerField(db_column='scrambleId')),
                ('competitionid', models.CharField(db_column='competitionId', max_length=32)),
                ('eventid', models.CharField(db_column='eventId', max_length=6)),
                ('roundtypeid', models.CharField(db_column='roundTypeId', max_length=1)),
                ('groupid', models.CharField(db_column='groupId', max_length=3)),
                ('isextra', models.IntegerField(db_column='isExtra')),
                ('scramblenum', models.IntegerField(db_column='scrambleNum')),
                ('scramble', models.TextField()),
            ],
            options={
                'db_table': 'Scrambles',
                'managed': False,
            },
        ),
    ]