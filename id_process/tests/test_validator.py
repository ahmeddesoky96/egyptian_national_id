import unittest
from id_process.validators import NationalIDValidator
from django.test import TestCase

class TestNationalIDValidator(TestCase):
    
    def test_valid_ids(self):
        valid_ids = [
            '29001011234567',  
        ]
        
        for national_id in valid_ids:
            with self.subTest(national_id=national_id):
                is_valid, result = NationalIDValidator.validate(national_id)
                self.assertTrue(is_valid, f"ID {national_id} should be valid")
                self.assertIn('extracted_data', result)
                self.assertIn('birth_year', result['extracted_data'])
    
    def test_invalid_length(self):
        invalid_ids = ['123', '12345678901234567890']
        
        for national_id in invalid_ids:
            with self.subTest(national_id=national_id):
                is_valid, result = NationalIDValidator.validate(national_id)
                self.assertFalse(is_valid)
                self.assertIn('National ID must be exactly 14 digits', result['errors'])
    
    def test_non_numeric(self):
        is_valid, result = NationalIDValidator.validate('29001a11234567')
        self.assertFalse(is_valid)
        self.assertIn('National ID must contain only digits', result['errors'])
    
    def test_invalid_month(self):
        is_valid, result = NationalIDValidator.validate('29013011234567')  
        self.assertFalse(is_valid)
        self.assertIn('Invalid birth month', result['errors'])
    
    def test_invalid_day(self):
        is_valid, result = NationalIDValidator.validate('29001321234567')  
        self.assertFalse(is_valid)
        self.assertIn('Invalid birth day', result['errors'])

if __name__ == '__main__':
    unittest.main()
