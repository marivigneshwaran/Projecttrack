from django.db import models
from django.contrib.auth.models import User 

class Role(models.Model):
    # Renamed from 'Roles' to 'Role' (Django convention uses singular names)
    role_name = models.CharField("Role Name", max_length=50)

    def __str__(self):
        return self.role_name

# class UserMaster(models.Model):
#     # Renamed to camel case 'UserMaster' for standard Python class naming
#     name = models.CharField("Name", max_length=50)
#     email = models.EmailField("Email", max_length=100, unique=True)
#     # Corrected ForeignKey naming and added on_delete logic
#     role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name='users')
#     password = models.CharField("Password", max_length=128) # Increased for hashed passwords
#     designation = models.CharField("Designation", max_length=100, blank=True, null=True)
#     department = models.CharField("Department", max_length=50, blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name

class UserMaster(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True)
    password = models.CharField(max_length=255) # Stored locally as profile reference
    designation = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        # 1. Check if an authenticating User account already exists for this email
        # We use email as a clean, unique Username string for the login page
        if not User.objects.filter(username=self.email).exists():
            # 2. Create an authenticating system account behind the scenes
            user = User.objects.create_user(
                username=self.email, # Use email or a slugified version of their name
                email=self.email,
                password=self.password # This automatically hashes the password securely!
            )
            # 3. Give them access to log into this administration panel
            user.is_staff = True
            user.is_superuser = True # Give full dashboard management rights
            user.save()
            
        # Run standard model saving for your custom UserMaster table row
        super(UserMaster, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class UserSkill(models.Model):
    user = models.ForeignKey(UserMaster, on_delete=models.CASCADE, related_name='skills')
    skill_name = models.CharField("Skill Name", max_length=100)

    def __str__(self):
        # FIXED: Must return a string, not the user object itself
        return f"{self.user.name} - {self.skill_name}"

class UserMedia(models.Model):
    user = models.ForeignKey(UserMaster, on_delete=models.CASCADE, related_name='media')
    system_path = models.CharField("System Path", max_length=255, blank=True)
    file_name = models.FileField("Files", upload_to='user_files/', blank=True, null=True)

    def __str__(self):
        return f"Media for {self.user.name}"