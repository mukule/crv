from import_export import resources, fields
from .models import Resume

class ResumeResource(resources.ModelResource):
    username = fields.Field(attribute='user__username')
    academic_level = fields.Field(attribute='academic_level__level')

    class Meta:
        model = Resume
        fields = ('username', 'academic_level',)
