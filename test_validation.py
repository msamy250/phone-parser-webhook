#!/usr/bin/env python3
"""
Test validation - ensure success=false when fields are empty
"""

print("=" * 90)
print("VALIDATION TEST - Testing Empty Field Detection")
print("=" * 90)
print()

# Test cases that should fail (invalid/unsupported numbers)
INVALID_TEST_CASES = [
    ("123", "Too short"),
    ("abc123def", "Contains letters"),
    ("00000000", "All zeros"),
    ("111", "Invalid format"),
]

print("These test cases should be tested with the actual API:")
print()

for phone, description in INVALID_TEST_CASES:
    print(f"📝 Test: {phone:15} - {description}")
    print(f"   curl -X POST http://localhost:8000/parse-phone \\")
    print(f"     -H 'Content-Type: application/json' \\")
    print(f"     -d '{{\"phone_number\": \"{phone}\"}}'")
    print()

print("=" * 90)
print("EXPECTED BEHAVIOR:")
print("=" * 90)
print()
print("✅ Valid numbers → success: true, all fields populated")
print("❌ Invalid numbers → success: false, error message shown")
print()
print("Valid number example:")
print('  {"success": true, "data": {"local_number": "...", "country_code": "...", "country_name": "...", "country_reference": "..."}}')
print()
print("Invalid number example:")
print('  {"success": false, "error": "Unable to parse phone number completely", "data": {...}}')
print()
print("=" * 90)
