from django.db import models
from django.contrib.auth.models import User

# Province Choices
PROVINCE_CHOICES = [
    ('Koshi Pradesh', 'Koshi Pradesh'),
    ('Madhesh Pradesh', 'Madhesh Pradesh'),
    ('Bagmati Pradesh', 'Bagmati Pradesh'),
    ('Gandaki Pradesh', 'Gandaki Pradesh'),
    ('Lumbini Pradesh', 'Lumbini Pradesh'),
    ('Karnali Pradesh', 'Karnali Pradesh'),
    ('Sudurpashchim Pradesh', 'Sudurpashchim Pradesh'),
]

# District Choices (Partial Example, Add All)
# District Choices in alphabetical order
DISTRICT_CHOICES = [
    ('Achham', 'Achham'),
    ('Arghakhanchi', 'Arghakhanchi'),
    ('Baglung', 'Baglung'),
    ('Baitadi', 'Baitadi'),
    ('Bajhang', 'Bajhang'),
    ('Bajura', 'Bajura'),
    ('Banke', 'Banke'),
    ('Bara', 'Bara'),
    ('Bardiya', 'Bardiya'),
    ('Bhaktapur', 'Bhaktapur'),
    ('Bhojpur', 'Bhojpur'),
    ('Chitwan', 'Chitwan'),
    ('Dadeldhura', 'Dadeldhura'),
    ('Dailekh', 'Dailekh'),
    ('Dang', 'Dang'),
    ('Darchula', 'Darchula'),
    ('Dhading', 'Dhading'),
    ('Dhankuta', 'Dhankuta'),
    ('Dhanusha', 'Dhanusha'),
    ('Dolakha', 'Dolakha'),
    ('Dolpa', 'Dolpa'),
    ('Doti', 'Doti'),
    ('Gorkha', 'Gorkha'),
    ('Gulmi', 'Gulmi'),
    ('Humla', 'Humla'),
    ('Ilam', 'Ilam'),
    ('Jajarkot', 'Jajarkot'),
    ('Jhapa', 'Jhapa'),
    ('Jumla', 'Jumla'),
    ('Kailali', 'Kailali'),
    ('Kalikot', 'Kalikot'),
    ('Kanchanpur', 'Kanchanpur'),
    ('Kapilvastu', 'Kapilvastu'),
    ('Kaski', 'Kaski'),
    ('Kathmandu', 'Kathmandu'),
    ('Kavrepalanchok', 'Kavrepalanchok'),
    ('Khotang', 'Khotang'),
    ('Lalitpur', 'Lalitpur'),
    ('Lamjung', 'Lamjung'),
    ('Mahottari', 'Mahottari'),
    ('Makwanpur', 'Makwanpur'),
    ('Manang', 'Manang'),
    ('Morang', 'Morang'),
    ('Mugu', 'Mugu'),
    ('Mustang', 'Mustang'),
    ('Myagdi', 'Myagdi'),
    ('Nawalparasi East', 'Nawalparasi East'),
    ('Nawalparasi West', 'Nawalparasi West'),
    ('Nuwakot', 'Nuwakot'),
    ('Okhaldhunga', 'Okhaldhunga'),
    ('Palpa', 'Palpa'),
    ('Panchthar', 'Panchthar'),
    ('Parbat', 'Parbat'),
    ('Parsa', 'Parsa'),
    ('Pyuthan', 'Pyuthan'),
    ('Ramechhap', 'Ramechhap'),
    ('Rasuwa', 'Rasuwa'),
    ('Rautahat', 'Rautahat'),
    ('Rolpa', 'Rolpa'),
    ('Rukum East', 'Rukum East'),
    ('Rukum West', 'Rukum West'),
    ('Rupandehi', 'Rupandehi'),
    ('Salyan', 'Salyan'),
    ('Sankhuwasabha', 'Sankhuwasabha'),
    ('Saptari', 'Saptari'),
    ('Sarlahi', 'Sarlahi'),
    ('Sindhuli', 'Sindhuli'),
    ('Sindhupalchok', 'Sindhupalchok'),
    ('Siraha', 'Siraha'),
    ('Solukhumbu', 'Solukhumbu'),
    ('Sunsari', 'Sunsari'),
    ('Surkhet', 'Surkhet'),
    ('Syangja', 'Syangja'),
    ('Tanahun', 'Tanahun'),
    ('Taplejung', 'Taplejung'),
    ('Terhathum', 'Terhathum'),
    ('Udayapur', 'Udayapur'),
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
