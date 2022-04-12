from django.db import models
from accounts import models as accounts_models

# Create your models here.


class Service(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.IntegerField()

    def __str__(self):
        return self.name


class Appointment(models.Model):
    # PENDING = "pending"
    # CANCELED = "canceled"
    # COMPLETED = "completed"
    # STATUS_CHOICES = [
    #     (PENDING, "Pending"),
    #     (CANCELED, "Canceled"),
    #     (COMPLETED, "Completed"),
    # ]
    doctor = models.ForeignKey(
        accounts_models.CustomUser, on_delete=models.CASCADE, related_name='doctor')
    patient = models.ForeignKey(
        accounts_models.CustomUser, on_delete=models.CASCADE, related_name='patient')
    date = models.DateField()
    services = models.ManyToManyField(
        Service, related_name='appointment_services', default=None)
    time = models.IntegerField()

    def __str__(self):
        return self.doctor.last_name + ' ' + self.patient.last_name

    def get_services(self):
        return ", ".join([service.name for service in self.services.all()])


class Bill(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE,related_name='bill')

    def __str__(self):
        return self.appointment.doctor.last_name + ' ' + self.appointment.patient.last_name

    def get_services(self):
        print("-----------------")
        for item in self.appointment.services.all():
            print(item.price)
        print("-----------------")
        return ", ".join([service.name + ":" + str(service.price) for service in self.appointment.services.all()])

    def get_services_objects(self):
        print("-----------------")
        for item in self.appointment.services.all():
            print({"name": item.name, "price": item.price})
        print("-----------------")
        return ([{"name": service.name, "price": service.price}for service in self.appointment.services.all()])


class DoctorInfo(models.Model):

    PENDING = "pending"

# list of doctors
    ALLERGISTS = "allergists"
    DIABETOLOGIST = "diabetologist"
    DERMATOLOGIST = "dermatologist"
    CARDIOLOGIST = "cardiologist"
    UROLOGIST = "urologist"
    DENTIST = "dentist"
    GENERALIST = "generalist"
    PSYCHIATRIST = "psychiatrist"
    RADIOLOGIST = "radiologist"

    SPECIALITY_CHOICES = [
        (ALLERGISTS, "Allergists"),
        (DIABETOLOGIST, "Diabetologist"),
        (DERMATOLOGIST, "Dermatologist"),
        (CARDIOLOGIST, "Cardiologist"),
        (UROLOGIST, "Urologist"),
        (DENTIST, "Dentist"),
        (GENERALIST, "Generalist"),
        (PSYCHIATRIST, "Psychiatrist"),
        (RADIOLOGIST, "Radiologist"),
    ]

    doctor = models.OneToOneField(
        accounts_models.CustomUser, on_delete=models.CASCADE)
    speciality = models.CharField(
        max_length=40, choices=SPECIALITY_CHOICES, default=GENERALIST)
    description = models.TextField()
    services = models.ManyToManyField(
        Service, related_name='doctor_services', default=None)

    def __str__(self):
        return self.speciality

    def get_services(self):
        return ", ".join([service.name for service in self.services.all()])

    def get_services_array(self):
        return [{"id": service.id, "name": service.name, "price": service.price} for service in self.services.all()]
