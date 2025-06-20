# Generated by Django 5.1.7 on 2025-03-30 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_update_province_no_1_to_koshi'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='google_maps_link',
            field=models.URLField(blank=True, help_text='Direct link to this location on Google Maps', null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='district',
            field=models.CharField(choices=[('Achham', 'Achham'), ('Arghakhanchi', 'Arghakhanchi'), ('Baglung', 'Baglung'), ('Baitadi', 'Baitadi'), ('Bajhang', 'Bajhang'), ('Bajura', 'Bajura'), ('Banke', 'Banke'), ('Bara', 'Bara'), ('Bardiya', 'Bardiya'), ('Bhaktapur', 'Bhaktapur'), ('Bhojpur', 'Bhojpur'), ('Chitwan', 'Chitwan'), ('Dadeldhura', 'Dadeldhura'), ('Dailekh', 'Dailekh'), ('Dang', 'Dang'), ('Darchula', 'Darchula'), ('Dhading', 'Dhading'), ('Dhankuta', 'Dhankuta'), ('Dhanusha', 'Dhanusha'), ('Dolakha', 'Dolakha'), ('Dolpa', 'Dolpa'), ('Doti', 'Doti'), ('Gorkha', 'Gorkha'), ('Gulmi', 'Gulmi'), ('Humla', 'Humla'), ('Ilam', 'Ilam'), ('Jajarkot', 'Jajarkot'), ('Jhapa', 'Jhapa'), ('Jumla', 'Jumla'), ('Kailali', 'Kailali'), ('Kalikot', 'Kalikot'), ('Kanchanpur', 'Kanchanpur'), ('Kapilvastu', 'Kapilvastu'), ('Kaski', 'Kaski'), ('Kathmandu', 'Kathmandu'), ('Kavrepalanchok', 'Kavrepalanchok'), ('Khotang', 'Khotang'), ('Lalitpur', 'Lalitpur'), ('Lamjung', 'Lamjung'), ('Mahottari', 'Mahottari'), ('Makwanpur', 'Makwanpur'), ('Manang', 'Manang'), ('Morang', 'Morang'), ('Mugu', 'Mugu'), ('Mustang', 'Mustang'), ('Myagdi', 'Myagdi'), ('Nawalparasi East', 'Nawalparasi East'), ('Nawalparasi West', 'Nawalparasi West'), ('Nuwakot', 'Nuwakot'), ('Okhaldhunga', 'Okhaldhunga'), ('Palpa', 'Palpa'), ('Panchthar', 'Panchthar'), ('Parbat', 'Parbat'), ('Parsa', 'Parsa'), ('Pyuthan', 'Pyuthan'), ('Ramechhap', 'Ramechhap'), ('Rasuwa', 'Rasuwa'), ('Rautahat', 'Rautahat'), ('Rolpa', 'Rolpa'), ('Rukum East', 'Rukum East'), ('Rukum West', 'Rukum West'), ('Rupandehi', 'Rupandehi'), ('Salyan', 'Salyan'), ('Sankhuwasabha', 'Sankhuwasabha'), ('Saptari', 'Saptari'), ('Sarlahi', 'Sarlahi'), ('Sindhuli', 'Sindhuli'), ('Sindhupalchok', 'Sindhupalchok'), ('Siraha', 'Siraha'), ('Solukhumbu', 'Solukhumbu'), ('Sunsari', 'Sunsari'), ('Surkhet', 'Surkhet'), ('Syangja', 'Syangja'), ('Tanahun', 'Tanahun'), ('Taplejung', 'Taplejung'), ('Terhathum', 'Terhathum'), ('Udayapur', 'Udayapur')], max_length=50),
        ),
        migrations.AlterField(
            model_name='school',
            name='province',
            field=models.CharField(choices=[('Koshi Pradesh', 'Koshi Pradesh'), ('Madhesh Pradesh', 'Madhesh Pradesh'), ('Bagmati Pradesh', 'Bagmati Pradesh'), ('Gandaki Pradesh', 'Gandaki Pradesh'), ('Lumbini Pradesh', 'Lumbini Pradesh'), ('Karnali Pradesh', 'Karnali Pradesh'), ('Sudurpashchim Pradesh', 'Sudurpashchim Pradesh')], max_length=50),
        ),
    ]
