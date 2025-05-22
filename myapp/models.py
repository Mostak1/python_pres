from django.db import models

class Business(models.Model):
    name = models.CharField(max_length=255)
    settings = models.JSONField(blank=True, null=True)  # If you store settings as JSON

    def __str__(self):
        return self.name

class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True)
    gender = models.CharField(max_length=10)
    contact = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Manufacturer(models.Model):
    manufacturer_name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, default='default-slug')
    generics_count = models.IntegerField(default=0)
    brand_names_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.manufacturer_name


class Generic(models.Model):
    generic_name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    monograph_link = models.URLField(blank=True, null=True)
    drug_class = models.CharField(max_length=255, blank=True, null=True)
    drug_class_id = models.IntegerField(blank=True, null=True)
    indication = models.CharField(max_length=255, blank=True, null=True)
    indication_id = models.IntegerField(blank=True, null=True)
    indication_description = models.TextField(blank=True, null=True)
    therapeutic_class_description = models.TextField(blank=True, null=True)
    pharmacology_description = models.TextField(blank=True, null=True)
    dosage_description = models.TextField(blank=True, null=True)
    administration_description = models.TextField(blank=True, null=True)
    interaction_description = models.TextField(blank=True, null=True)
    contraindications_description = models.TextField(blank=True, null=True)
    side_effects_description = models.TextField(blank=True, null=True)
    pregnancy_lactation_description = models.TextField(blank=True, null=True)
    precautions_description = models.TextField(blank=True, null=True)
    pediatric_usage_description = models.TextField(blank=True, null=True)
    overdose_effects_description = models.TextField(blank=True, null=True)
    duration_treatment_description = models.TextField(blank=True, null=True)
    reconstitution_description = models.TextField(blank=True, null=True)
    storage_conditions_description = models.TextField(blank=True, null=True)
    descriptions_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)  # Soft delete field

    def __str__(self):
        return self.generic_name

class Drug(models.Model):
    name = models.CharField(max_length=255)
    size = models.CharField(max_length=100, blank=True, null=True)
    business_id = models.IntegerField(blank=True, null=True)
    category_id = models.IntegerField(blank=True, null=True)
    sku = models.CharField(max_length=100, unique=True, blank=True, null=True)
    image = models.ImageField(upload_to='drugs/', blank=True, null=True)
    is_inactive = models.BooleanField(default=False)
    drug_type = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(unique=True)
    dosage_form_id = models.IntegerField(blank=True, null=True)
    generic = models.ForeignKey('Generic', on_delete=models.SET_NULL, blank=True, null=True)
    strength = models.CharField(max_length=100, blank=True, null=True)
    mfg_id = models.IntegerField(blank=True, null=True)
    package_container = models.CharField(max_length=100, blank=True, null=True)
    package_size = models.CharField(max_length=100, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)  # For soft deletion

    def __str__(self):
        return self.name


class Indication(models.Model):
    indication_name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    generics_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.indication_name

class DosageForm(models.Model):
    dosage_form_name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=50, blank=True, null=True)
    slug = models.SlugField(unique=True)
    brand_names_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.dosage_form_name
class DrugClass(models.Model):
    drug_class_name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    generics_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.drug_class_name
    
class DosageTime(models.Model):
    time = models.CharField(max_length=50)  # e.g., "Morning", "Evening"

    def __str__(self):
        return self.time


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.patient.name} - {self.date}"

class Prescription(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=50)  # e.g., "1 tablet"
    times = models.ManyToManyField(DosageTime)
    duration = models.CharField(max_length=50)  # e.g., "7 days"
    indication = models.ForeignKey(Indication, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.drug.name} for {self.appointment.patient.name}"
