from django.db import models
from django.contrib.auth.models import User

# Province Choices
PROVINCE_CHOICES = [
    ('Province No. 1', 'Province No. 1'),
    ('Madhesh Pradesh', 'Madhesh Pradesh'),
    ('Bagmati Pradesh', 'Bagmati Pradesh'),
    ('Gandaki Pradesh', 'Gandaki Pradesh'),
    ('Lumbini Pradesh', 'Lumbini Pradesh'),
    ('Karnali Pradesh', 'Karnali Pradesh'),
    ('Sudurpashchim Pradesh', 'Sudurpashchim Pradesh'),
]

# District Choices (Partial Example, Add All)
DISTRICT_CHOICES = [
    # Province No. 1
    ('Bhojpur', 'Bhojpur'),
    ('Dhankuta', 'Dhankuta'),
    ('Ilam', 'Ilam'),
    ('Jhapa', 'Jhapa'),
    ('Khotang', 'Khotang'),
    ('Morang', 'Morang'),
    ('Okhaldhunga', 'Okhaldhunga'),
    ('Panchthar', 'Panchthar'),
    ('Sankhuwasabha', 'Sankhuwasabha'),
    ('Solukhumbu', 'Solukhumbu'),
    ('Sunsari', 'Sunsari'),
    ('Taplejung', 'Taplejung'),
    ('Terhathum', 'Terhathum'),
    ('Udayapur', 'Udayapur'),
    
    # Madhesh Pradesh
    ('Bara', 'Bara'),
    ('Dhanusha', 'Dhanusha'),
    ('Mahottari', 'Mahottari'),
    ('Parsa', 'Parsa'),
    ('Rautahat', 'Rautahat'),
    ('Saptari', 'Saptari'),
    ('Sarlahi', 'Sarlahi'),
    ('Siraha', 'Siraha'),
    
    # Bagmati Pradesh
    ('Bhaktapur', 'Bhaktapur'),
    ('Chitwan', 'Chitwan'),
    ('Dhading', 'Dhading'),
    ('Dolakha', 'Dolakha'),
    ('Kathmandu', 'Kathmandu'),
    ('Kavrepalanchok', 'Kavrepalanchok'),
    ('Lalitpur', 'Lalitpur'),
    ('Makwanpur', 'Makwanpur'),
    ('Nuwakot', 'Nuwakot'),
    ('Ramechhap', 'Ramechhap'),
    ('Rasuwa', 'Rasuwa'),
    ('Sindhuli', 'Sindhuli'),
    ('Sindhupalchok', 'Sindhupalchok'),
    
    # Gandaki Pradesh
    ('Baglung', 'Baglung'),
    ('Gorkha', 'Gorkha'),
    ('Kaski', 'Kaski'),
    ('Lamjung', 'Lamjung'),
    ('Manang', 'Manang'),
    ('Mustang', 'Mustang'),
    ('Myagdi', 'Myagdi'),
    ('Nawalparasi East', 'Nawalparasi East'),
    ('Parbat', 'Parbat'),
    ('Syangja', 'Syangja'),
    ('Tanahun', 'Tanahun'),
    
    # Lumbini Pradesh
    ('Arghakhanchi', 'Arghakhanchi'),
    ('Banke', 'Banke'),
    ('Bardiya', 'Bardiya'),
    ('Dang', 'Dang'),
    ('Gulmi', 'Gulmi'),
    ('Kapilvastu', 'Kapilvastu'),
    ('Nawalparasi West', 'Nawalparasi West'),
    ('Palpa', 'Palpa'),
    ('Pyuthan', 'Pyuthan'),
    ('Rolpa', 'Rolpa'),
    ('Rupandehi', 'Rupandehi'),
    ('Rukum East', 'Rukum East'),
    
    # Karnali Pradesh
    ('Dailekh', 'Dailekh'),
    ('Dolpa', 'Dolpa'),
    ('Humla', 'Humla'),
    ('Jajarkot', 'Jajarkot'),
    ('Jumla', 'Jumla'),
    ('Kalikot', 'Kalikot'),
    ('Mugu', 'Mugu'),
    ('Rukum West', 'Rukum West'),
    ('Salyan', 'Salyan'),
    ('Surkhet', 'Surkhet'),
    
    # Sudurpashchim Pradesh
    ('Achham', 'Achham'),
    ('Baitadi', 'Baitadi'),
    ('Bajhang', 'Bajhang'),
    ('Bajura', 'Bajura'),
    ('Dadeldhura', 'Dadeldhura'),
    ('Darchula', 'Darchula'),
    ('Doti', 'Doti'),
    ('Kailali', 'Kailali'),
    ('Kanchanpur', 'Kanchanpur')
]

# Municipality Type Choices
MUNICIPALITY_TYPE_CHOICES = [
    ('Metropolitan City', 'Metropolitan City'),
    ('Sub-Metropolitan City', 'Sub-Metropolitan City'),
    ('Municipality', 'Municipality'),
    ('Rural Municipality', 'Rural Municipality'),
]

# School Type Choices
SCHOOL_TYPE_CHOICES = [
    ('Public', 'Public'),
    ('Community', 'Community'),
    ('Private', 'Private'),
    ('Other', 'Other'),
]

class School(models.Model):
    """Stores public and community school details."""
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField()
    
    # Location Data
    province = models.CharField(max_length=50, choices=PROVINCE_CHOICES)
    district = models.CharField(max_length=50, choices=DISTRICT_CHOICES)
    municipality_type = models.CharField(max_length=50, choices=MUNICIPALITY_TYPE_CHOICES)
    
    # Coordinates for Map
    latitude = models.DecimalField(max_digits=17, decimal_places=15)
    longitude = models.DecimalField(max_digits=17, decimal_places=15)

    # Contact & Other Details
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    
    # School Type
    school_type = models.CharField(max_length=50, choices=SCHOOL_TYPE_CHOICES)
    
    # Additional Information
    established_year = models.PositiveIntegerField(blank=True, null=True)
    principal_name = models.CharField(max_length=255, blank=True, null=True)
    facilities = models.ManyToManyField('Facility', blank=True)

    # Metadata
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Facility(models.Model):
    """Stores available facilities in schools."""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
