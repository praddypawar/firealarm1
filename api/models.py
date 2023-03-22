from django.db import models
from utils.models.base_fire import Base_fire,StatusBase
from datetime import datetime
import os

# Create your models here.
class admins(Base_fire,StatusBase):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    region= models.CharField(max_length=100)
    password = models.CharField(max_length=255)

    class Meta:
        ordering = ['-id']
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

# {
#     "first_name":"kadir",
#     "last_name":"bhai",
#     "email":"ashaelesservice@gmail.com",
#     "password":"75487548",
#     "region":"as"
# }
def set_cover_pic(instance, filename):
    print("--------",filename)
    ext = filename.split('.')[-1]
    # filename = "%s.%s" % (str(int(datetime.timestamp(datetime.now()))) + '_'+ instance.name, ext)
    filename = f"profile-pic-{instance.id or 'o'}-{int(datetime.timestamp(datetime.now()))}.{ext}"  # It's work only on PUT
    # print('---profile-pic-filename---', filename)
    return os.path.join('media/webs/client/cover-pic/', filename)


class client(Base_fire,StatusBase):
    cover_pic = models.ImageField(upload_to=set_cover_pic)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)


    class Meta:
        ordering = ['-id']
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'


# {
#     "first_name":"pradip",
#     "last_name":"pawar",
#     "email":"pradip@gmail.com",
#     "password":"123",
#     "address":"dindoli",
#     "phone":"2332345490",
# }

class devices(Base_fire,StatusBase):
    status_choice = (
        ("on","on"),
        ("off","off"),
    )
    admin_id = models.ForeignKey(admins,on_delete=models.DO_NOTHING)
    name= models.CharField(max_length=255)
    device_id = models.CharField(max_length=255)
    device_status=models.CharField(default="off",choices=status_choice,max_length=100)

    class Meta:
        ordering = ['-id']
    
    def __str__(self):
        return f'{self.admin_id}-{self.device_id}'


class sharedevices(Base_fire,StatusBase):
    status_choice = (
        ("true","True"),
        ("false","False"),
    )
    client_id = models.ForeignKey(client,on_delete=models.DO_NOTHING)
    device_pk = models.ForeignKey(devices,on_delete=models.DO_NOTHING)
    from_date = models.DateField()
    to_date = models.DateField()
    sharedevices_status=models.CharField(default="true",choices=status_choice,max_length=100)


# {
#     "client_id":1,
#     "device_pk":1,
#     "from_date":"2022-04-29",
#     "to_date":"2022-04-29",
# }


