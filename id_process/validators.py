import re
from datetime import datetime
from typing import Dict, Any, Tuple

class NationalIDValidator:
    
    GOVERNORATE_CODES = {
        '01': 'Cairo', '02': 'Alexandria', '03': 'Port Said', '04': 'Suez',
        '11': 'Damietta', '12': 'Dakahlia', '13': 'Sharqia', '14': 'Kalyubia',
        '15': 'Kafr El Sheikh', '16': 'Gharbia', '17': 'Menoufia', '18': 'Beheira',
        '19': 'Ismailia', '21': 'Giza', '22': 'Beni Suef', '23': 'Fayyum',
        '24': 'Minya', '25': 'Assiut', '26': 'Sohag', '27': 'Qena',
        '28': 'Aswan', '29': 'Luxor', '31': 'Red Sea', '32': 'New Valley',
        '33': 'Matrouh', '34': 'North Sinai', '35': 'South Sinai', '88': 'Foreign'
    }
    
    @staticmethod
    def validate(national_id: str) -> Tuple[bool, Dict[str, Any]]:
        result = {
            'is_valid': False,
            'errors': [],
            'extracted_data': {}
        }
        
        if not national_id or not isinstance(national_id, str):
            result['errors'].append('National ID must be a non-empty string')
            return False, result
            
        
        if len(national_id) != 14:
            result['errors'].append('National ID must be exactly 14 digits')
            return False, result
            
        if not national_id.isdigit():
            result['errors'].append('National ID must contain only digits')
            return False, result
        
        try:
            birth_year_code = national_id[0:1]  
            birth_year_digits = national_id[1:3]
            birth_month = national_id[3:5]
            birth_day = national_id[5:7]
            governorate_code = national_id[7:9]
            sequential = national_id[9:12]
            gender_digit = national_id[13:14]
            
            birth_year = NationalIDValidator._extract_birth_year(birth_year_code, birth_year_digits)
            if not birth_year:
                result['errors'].append('Invalid birth year encoding')
                return False, result
            
            if not (1 <= int(birth_month) <= 12):
                result['errors'].append('Invalid birth month')
                return False, result
                
            if not (1 <= int(birth_day) <= 31):
                result['errors'].append('Invalid birth day')
                return False, result
            
            if governorate_code not in NationalIDValidator.GOVERNORATE_CODES:
                result['errors'].append('Invalid governorate code')
                return False, result
            
            try:
                birth_date = datetime(birth_year, int(birth_month), int(birth_day))
            except ValueError:
                result['errors'].append('Invalid birth date')
                return False, result
            
            if birth_date > datetime.now():
                result['errors'].append('Birth date cannot be in the future')
                return False, result
            
            gender = 'Male' if int(gender_digit) % 2 == 1 else 'Female'
            age = datetime.now().year - birth_year
            
            result.update({
                'is_valid': True,
                'errors': [],
                'extracted_data': {
                    'national_id': national_id,
                    'birth_date': birth_date.strftime('%Y-%m-%d'),
                    'birth_year': birth_year,
                    'birth_month': int(birth_month),
                    'birth_day': int(birth_day),
                    'age': age,
                    'gender': gender,
                    'governorate_code': governorate_code,
                    'governorate_name': NationalIDValidator.GOVERNORATE_CODES[governorate_code],
                    'sequential_number': sequential,
                }
            })
            
            return True, result
            
        except (ValueError, IndexError) as e:
            result['errors'].append(f'Error in National ID structure: {str(e)}')
            return False, result
    
    @staticmethod
    def _extract_birth_year(century_code: str, year_digits: str) -> int:
        """Extract full birth year from century code and year digits"""
        try:
            century_digit = int(century_code)
            year = int(year_digits)
            
            if century_digit == 2:
                return 1900 + year
            elif century_digit == 3:
                return 2000 + year
            else:
                return None
        except ValueError:
            return None
  