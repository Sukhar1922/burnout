from django.db import migrations

def fill_tables(apps, schema_editor):
    sql_files = ['Everyweek_task_fill_delta.sql']
    conn = schema_editor.connection
    with conn.cursor() as cursor:
        for file in sql_files:
            with open(f'api/SQL/{file}', encoding='utf-8') as f:
                content = f.read().strip()
                cursor.execute(content)

class Migration(migrations.Migration):

    atomic = False

    dependencies = [
        ('api', '0011_options_notification_day_options_notification_week'),
    ]

    operations = [
        migrations.RunPython(fill_tables),
    ]