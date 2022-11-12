from django.core.exceptions import ValidationError

def validate_cnic(value):
    value=str(value)
    if len(value) ==13  or len(value)==15:
        return int(value)
    else:
        raise ValidationError("Invalid cnic")

def validate_money(value):
    value=str(value)
    if len(value)<7:
        return int(value)
    else:
        raise ValidationError("Enter correct amount")

def validate_phone(value):
    value=str(value)
    if len(value)==10:
        return int(value)
    else:
        raise ValidationError("Enter correct phone number")


def validate_date(value):
    value = str(value)
    if len(value) <= 2:
        return int(value)
    else:
        raise ValidationError("Enter correct date")

def validate_year(value):
    value = str(value)
    if len(value) == 4:
        return int(value)
    else:
        raise ValidationError("Enter correct year")
