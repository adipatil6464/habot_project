from rest_framework import serializers
from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Name cannot be empty.")
        return value

    def validate_email(self, value):
        if self.instance:
            if Employee.objects.filter(email=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("An employee with this email already exists.")
        else:
            if Employee.objects.filter(email=value).exists():
                raise serializers.ValidationError("An employee with this email already exists.")
        return value
