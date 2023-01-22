from django.db import models
import datetime

    
gender_choice = (
    ('m', 'Male'),
    ('f', 'Female'),
)

rank_choice = (
    ('sub', 'Sub-inspector'),
    ('ins', 'Inspector'),
)

class State(models.Model):
    Country = models.CharField(max_length=20, default='India')
    Name = models.CharField(max_length=20, default='')

    class Meta:
        db_table = 'State'

    def __str__(self):
        return self.Name

class City(models.Model):
    State = models.ForeignKey(State, on_delete=models.CASCADE)
    Name = models.CharField(max_length=20)

    class Meta:
        db_table = 'City'

    def __str__(self):
        return self.Name

# multiple user roles
class Role(models.Model):
    Role = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'Role'

    def __str__(self):
        return self.Role

class Master(models.Model):
    Role = models.ForeignKey(Role, on_delete=models.CASCADE)
    Email = models.EmailField(max_length=50, unique=True)
    Password = models.CharField(max_length=50)
    IsActive = models.BooleanField(default=False)
    DateCreated = models.DateTimeField(auto_now_add=True)
    DateUpdated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Master'
    
    def __str__(self):
        return self.Email

# department table
class Department(models.Model):
    Master = models.ForeignKey(Master,on_delete=models.CASCADE)
    State = models.ForeignKey(State, on_delete=models.CASCADE, blank=True)
    DeptID = models.CharField(max_length=20, default='') # random_num/
    Image = models.FileField(upload_to="image/departments/profile_pic", default="avtar.jpg")
    DeptName = models.CharField(max_length=50, default='')
    Mobile = models.CharField(max_length=10, default='')
    HeadOfficeAddress = models.CharField(max_length=100, default='')
    About = models.CharField(max_length=500, default='')

    class Meta:
        db_table = 'Department'

    def __str__(self):
        return self.State.Name

# police official tables
class PolicePerson(models.Model):
    Master = models.ForeignKey(Master,on_delete=models.CASCADE)
    PoID = models.CharField(max_length=20, default='') # Dept_code/random_num/
    Department = models.ForeignKey(Department,on_delete=models.CASCADE)
    Image = models.FileField(upload_to="image/department/police_person/", default="avtar.jpg")
    FullName = models.CharField(max_length=50, default='')
    Mobile = models.CharField(max_length=10, default='')
    Gender = models.CharField(max_length=50, choices=gender_choice)

    class Meta:
        db_table = 'PolicePerson'

    def __str__(self):
        return self.FullName

class Station(models.Model):
    StID = models.CharField(max_length=20, default='') # city_code/random_num/
    Department = models.ForeignKey(Department,on_delete=models.CASCADE)
    StationName = models.CharField(max_length=50)
    Email = models.EmailField(max_length=50, unique=True)
    Mobile = models.CharField(max_length=10, default='')
    Address = models.TextField(max_length=50, default='')
    City = models.ForeignKey(City, on_delete=models.CASCADE)
    Pincode = models.CharField(max_length=6, default='')

    class Meta:
        db_table = 'Station'

    def __str__(self):
        return self.StationName

class Inspector(models.Model):
    PolicePerson = models.ForeignKey(PolicePerson, on_delete=models.CASCADE)
    Station = models.ForeignKey(Station, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Inspector'

    def __str__(self):
        return self.PolicePerson.FullName

class Chowki(models.Model):
    ChID = models.CharField(max_length=20, default='')
    Station = models.ForeignKey(Station, on_delete=models.CASCADE)
    Mobile = models.CharField(max_length=10, default='')
    ChowkiName = models.CharField(max_length=50)
    Address = models.TextField(max_length=50, default='')

    class Meta:
        db_table = 'Chowki'

    def __str__(self):
        return self.ChowkiName

class SubInspector(models.Model):
    PolicePerson = models.ForeignKey(PolicePerson, on_delete=models.CASCADE)
    Chowki = models.ForeignKey(Chowki, on_delete=models.CASCADE)

    class Meta:
        db_table = 'SubInspector'

    def __str__(self):
        return self.PolicePerson.FullName

# citizen tables
class Citizen(models.Model):
    UID = models.CharField(max_length=20)
    Master = models.ForeignKey(Master,on_delete=models.CASCADE)
    Image = models.FileField(upload_to="image/users/profile_pic/", default="avtar.jpg")
    FullName = models.CharField(max_length=50, default='')
    Mobile = models.CharField(max_length=10, default='')
    Gender = models.CharField(max_length=50, choices=gender_choice)
    Address = models.TextField(max_length=50, default='')
    Country = models.CharField(max_length=20, default='India')
    State = models.CharField(max_length=20, default='')
    City = models.CharField(max_length=20, default='')
    Pincode = models.CharField(max_length=6, default='')

    class Meta:
        db_table = 'Citizen'

    def __str__(self):
        return self.Master.Email

class CrimeList(models.Model):
    Crime = models.CharField(max_length=50)
    Type = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'CrimeList'

    def __str__(self):
        return self.Crime

class SuspectList(models.Model):
    # prime suspect details
    Citizen = models.ForeignKey(Citizen, on_delete=models.CASCADE)
    Image = models.FileField(upload_to="image/users/suspects/", default="avtar.jpg")
    SuspectName = models.CharField(max_length=50)
    SuspectMobile = models.CharField(max_length=10, null=True) # if victim know them
    Gender = models.CharField(max_length=50, choices=gender_choice)
    SuspectAddress = models.TextField(max_length=200)

    class Meta:
        db_table = 'SuspectList'

    def __str__(self):
        return self.SuspectName

class Complaint(models.Model):
    ComplaintID = models.CharField(max_length=12)
    DateCreated = models.DateTimeField(auto_now_add=True)
    DateOfCrime = models.DateField(default=datetime.datetime.now())
    Description = models.TextField(max_length=500)

    class Meta:
        db_table = 'Complaint'

