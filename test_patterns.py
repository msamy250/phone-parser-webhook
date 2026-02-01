#!/usr/bin/env python3
"""Pattern-Based Detection Logic Test"""

def detect_country_from_local_number(phone_number_str):
    clean_number = ''.join(filter(str.isdigit, phone_number_str))
    length = len(clean_number)
    
    # EGYPT
    if length == 11 and clean_number.startswith(('010', '011', '012', '015')):
        return 'EG'
    
    # SAUDI ARABIA - must come before Egypt landline
    if length == 10 and clean_number.startswith('05'):
        return 'SA'
    
    # JORDAN - must come before Egypt landline
    if length == 10 and clean_number.startswith('07'):
        return 'JO'
    
    # PHILIPPINES - must come before Egypt landline
    if length == 12 and clean_number.startswith('63'):
        return None
    if length == 10 and clean_number.startswith('09'):
        return 'PH'
    
    # EGYPT landline (after checking 05, 07, 09)
    if 9 <= length <= 10 and clean_number.startswith('0'):
        if clean_number[1:2] in '234678':
            return 'EG'
    
    # UAE
    if length == 9 and clean_number.startswith(('50', '52', '54', '55', '56', '58')):
        return 'AE'
    
    # KUWAIT
    if length == 8 and clean_number[0] in ('5', '6', '9'):
        return 'KW'
    
    # BAHRAIN
    if length == 8 and clean_number.startswith('3'):
        return 'BH'
    
    # QATAR
    if length == 8 and clean_number[0] in ('3', '5', '6', '7'):
        if clean_number[0] in ('3', '7'):
            return 'QA'
        return 'KW'
    
    # TURKEY
    if length == 11 and clean_number.startswith('05'):
        return 'TR'
    
    # NEPAL
    if length == 13 and clean_number.startswith('977'):
        return None
    if length == 10 and clean_number.startswith(('984', '985', '986', '980', '981', '982')):
        return 'NP'
    
    # INDIA
    if length == 10 and clean_number[0] in ('6', '7', '8', '9'):
        return 'IN'
    
    # PAKISTAN
    if length == 10 and clean_number.startswith('3'):
        return 'PK'
    
    # UK
    if length == 11 and clean_number.startswith('0'):
        return 'GB'
    
    # US/CANADA
    if length == 10 and clean_number[0] in ('2', '3', '4', '5'):
        return 'US'
    
    return None

TEST_CASES = [
    ("01234567890", "EG", "Egypt mobile 012"),
    ("01012345678", "EG", "Egypt mobile 010"),
    ("0221234567", "EG", "Egypt landline Cairo"),
    ("505237982", "AE", "UAE mobile 50"),
    ("565900369", "AE", "UAE mobile 56"),
    ("0501234567", "SA", "Saudi mobile 050"),
    ("0551234567", "SA", "Saudi mobile 055"),
    ("51234567", "KW", "Kuwait mobile 5"),
    ("66123456", "KW", "Kuwait mobile 6"),
    ("33123456", "BH", "Bahrain mobile 33"),
    ("77123456", "QA", "Qatar mobile 77"),
    ("0791234567", "JO", "Jordan mobile 079"),
    ("05312345678", "TR", "Turkey mobile 0531"),
    ("9876543210", "IN", "India mobile 98"),
    ("8123456789", "IN", "India mobile 81"),
    ("7012345678", "IN", "India mobile 70"),
    ("6123456789", "IN", "India mobile 61"),
    ("3001234567", "PK", "Pakistan mobile 300"),
    ("0917123456", "PH", "Philippines mobile 0917"),
    ("9841234567", "NP", "Nepal mobile 984"),
    ("9851234567", "NP", "Nepal mobile 985"),
    ("07123456789", "GB", "UK mobile 071"),
    ("4155552671", "US", "US number 415"),
    ("2125551234", "US", "US number 212"),
]

print("=" * 90)
print("PHONE NUMBER DETECTION PATTERN TEST")
print("=" * 90)
print()

passed = 0
failed = 0
errors = []

for phone, expected, description in TEST_CASES:
    detected = detect_country_from_local_number(phone)
    clean = ''.join(filter(str.isdigit, phone))
    
    if detected == expected:
        status = "✅ PASS"
        passed += 1
    else:
        status = "❌ FAIL"
        failed += 1
        errors.append((phone, expected, detected, description))
    
    print(f"{status} | {phone:15} | Len: {len(clean):2} | Expected: {expected:3} | Got: {detected or 'None':3} | {description}")

print()
print("=" * 90)
print(f"RESULTS: {passed}/{len(TEST_CASES)} passed, {failed}/{len(TEST_CASES)} failed")
print("=" * 90)

if errors:
    print()
    print("FAILED TESTS:")
    print("-" * 90)
    for phone, expected, got, desc in errors:
        print(f"❌ {phone:15} | Expected: {expected:3} | Got: {got or 'None':3} | {desc}")

if failed == 0:
    print()
    print("🎉 ALL PATTERN TESTS PASSED!")
    print()
    print("✅ Detection logic is working correctly")
    print("✅ Ready to deploy!")
    print()
else:
    print()
    print(f"⚠️  {failed} test(s) failed")

print("=" * 90)
