from  import_export import resources
from accounts.models import User

class  UserResource(resources.ModelResource):
    class Meta:
        model=User
        import_id_fields = ('registration_number',)
        exclude = ('id', 'date_joned',)
        skip_unchanged = True
        fields=[
           'registration_number','email','first_name','last_name','is_student','national_ID','dob','phone','course_assigned','department','gender','intake'
           ,'password','class_assigned','student_term','next_of_kin_phone', 'next_of_kin'
        ]




    