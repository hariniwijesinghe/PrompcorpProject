import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def validate_australian_mobile_phone_number(phone_number):
    # Regular expression pattern for Australian mobile phone numbers
    # Format: National format starting with 04 and followed by 8 digits
    pattern = re.compile(r'^04\d{2}\s\d{3}\s\d{3}$')
    
    if not pattern.match(phone_number):
        raise ValidationError("Invalid Australian mobile phone number format. Must start with '04' and have 10 digits.")
    
    return phone_number
def validate_account_number(account_number):
    # Regular expression pattern for account numbers
    # Allowing 6 to 9 digits
    pattern = re.compile(r"^\d{6,9}$")
    
    if not pattern.match(account_number):
        raise ValidationError("Invalid account number format. Account number must be 6 to 9 digits long.")
    
    return account_number

def validate_bsb_number(bsb_number):
    # Regular expression pattern for BSB numbers
    # Format: 6 digits
    pattern = re.compile(r"^\d{6}$")
    
    if not pattern.match(bsb_number):
        raise ValidationError("Invalid BSB number format. BSB number must be 6 digits long.")
    
    return bsb_number
def validate_abn(abn):
    abn = abn.replace(' ', '')
    """
    Validate an Australian Business Number (ABN).
    ABN should be 11 digits long and pass the checksum validation.
    """
    if len(abn) != 11 or not abn.isdigit():
        raise ValidationError('ABN must be 11 digits long.')

    weights = [10, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    abn_as_digits = [int(digit) for digit in abn]

    # Adjust the first digit
    abn_as_digits[0] -= 1

    # Calculate the weighted sum
    weighted_sum = sum(weight * digit for weight, digit in zip(weights, abn_as_digits))

    # Validate the checksum
    if weighted_sum % 89 != 0:
        raise ValidationError('Invalid ABN number.')