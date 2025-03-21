import pytest
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '../src/data_masker/data_masker'))
from function import mask_email, mask_phone, mask_credit_card, mask_ssn, main

# Email tests
def test_mask_email_medium():
    assert mask_email('john.doe@example.com', 'medium') == 'j******@e******.com'

def test_mask_email_high():
    assert mask_email('john.doe@example.com', 'high') == '********@*******.com'

def test_mask_email_low():
    assert mask_email('john.doe@example.com', 'low') == 'j******e@example.com'

def test_mask_email_edge_cases():
    assert mask_email('', 'medium') == ''
    assert mask_email(None, 'medium') == None
    assert mask_email('no-at-sign', 'medium') == 'no-at-sign'

# Phone tests
def test_mask_phone_medium():
    assert mask_phone('123-456-7890', 'medium') == 'XXX-XXX-7890'

def test_mask_phone_high():
    assert mask_phone('123-456-7890', 'high') == 'XXX-XXX-XX90'

def test_mask_phone_low():
    assert mask_phone('123-456-7890', 'low') == 'XXX-456-7890'

def test_mask_phone_edge_cases():
    assert mask_phone('', 'medium') == ''
    assert mask_phone(None, 'medium') == None
    assert mask_phone('1234567890', 'medium') == 'XXXXXX7890'  # No formatting

# Credit card tests
def test_mask_credit_card_medium():
    assert mask_credit_card('4111-1111-1111-1111', 'medium') == '4XXX-XXXX-XXXX-1111'

def test_mask_credit_card_high():
    assert mask_credit_card('4111-1111-1111-1111', 'high') == 'XXXX-XXXX-XXXX-1111'

def test_mask_credit_card_low():
    assert mask_credit_card('4111-1111-1111-1111', 'low') == '4111-XXXX-XXXX-1111'

def test_mask_credit_card_edge_cases():
    assert mask_credit_card('', 'medium') == ''
    assert mask_credit_card(None, 'medium') == None
    assert mask_credit_card('4111111111111111', 'medium') == '4XXXXXXXXXXX1111'  # No formatting

# SSN tests
def test_mask_ssn_medium():
    assert mask_ssn('123-45-6789', 'medium') == 'XXX-XX-6789'

def test_mask_ssn_high():
    assert mask_ssn('123-45-6789', 'high') == 'XXX-XX-XXXX'

def test_mask_ssn_low():
    assert mask_ssn('123-45-6789', 'low') == 'XXX-XX-6789'

def test_mask_ssn_edge_cases():
    assert mask_ssn('', 'medium') == ''
    assert mask_ssn(None, 'medium') == None
    assert mask_ssn('123456789', 'medium') == 'XXXXX6789'  # No formatting

# Main function tests
def test_main_default():
    assert main('john.doe@example.com') == mask_email('john.doe@example.com', 'medium')

def test_main_phone():
    assert main('123-456-7890', 'phone') == mask_phone('123-456-7890', 'medium')

def test_main_credit_card():
    assert main('4111-1111-1111-1111', 'credit_card') == mask_credit_card('4111-1111-1111-1111', 'medium')

def test_main_ssn():
    assert main('123-45-6789', 'ssn') == mask_ssn('123-45-6789', 'medium')

def test_main_level_override():
    assert main('john.doe@example.com', 'email', 'high') == mask_email('john.doe@example.com', 'high')

def test_main_unknown_type():
    assert main('some value', 'unknown_type') == 'some value'
