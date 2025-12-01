from django.db import models

class School(models.Model):
    name = models.CharField(max_length=255, unique=True)
    short_name = models.CharField(max_length=100, blank=True, null=True, unique=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Classroom(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='classrooms')
    grade = models.PositiveIntegerField()
    section = models.CharField(max_length=20, blank=True)

    class Meta:
        unique_together = (('school', 'grade', 'section'),)
        ordering = ['school_id', 'grade', 'section']

    def __str__(self):
        sec = f"-{self.section}" if self.section else ""
        return f"{self.school.short_name or self.school.name} Grade {self.grade}{sec}"


class Teacher(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    classrooms = models.ManyToManyField(Classroom, related_name='teachers', blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Student(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    classroom = models.ForeignKey(Classroom, on_delete=models.PROTECT, related_name='students')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
