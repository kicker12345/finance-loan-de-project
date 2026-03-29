import pytest
import re

# ============================================================
# TEST 1: emp_length cleaning (Notebook 2)
# Remove non-digits from emp_length
# ============================================================

def clean_emp_length(value):
    if value is None:
        return None
    return re.sub(r'\D', '', value)

def test_emp_length_cleaning():
    assert clean_emp_length("9 years") == "9"
    assert clean_emp_length("< 1 year") == "1"
    assert clean_emp_length("10+ years") == "10"
    assert clean_emp_length(None) is None
    print("✅ TEST 1 PASSED: emp_length cleaning works correctly")


# ============================================================
# TEST 2: address_state cleaning (Notebook 2)
# Replace states longer than 2 chars with 'NA'
# ============================================================

def clean_address_state(value):
    if value is None:
        return "NA"
    return "NA" if len(value) > 2 else value

def test_address_state_cleaning():
    assert clean_address_state("CA") == "CA"
    assert clean_address_state("New York") == "NA"
    assert clean_address_state("TX") == "TX"
    assert clean_address_state("Florida") == "NA"
    assert clean_address_state(None) == "NA"
    print("✅ TEST 2 PASSED: address_state cleaning works correctly")


# ============================================================
# TEST 3: loan_purpose standardization (Notebook 3)
# Keep valid purposes, replace others with 'other'
# ============================================================

VALID_LOAN_PURPOSES = [
    "debt_consolidation", "credit_card", "home_improvement",
    "other", "major_purchase", "medical", "small_business",
    "car", "vacation", "moving", "house", "wedding",
    "renewable_energy", "educational"
]

def clean_loan_purpose(value):
    if value in VALID_LOAN_PURPOSES:
        return value
    return "other"

def test_loan_purpose_cleaning():
    assert clean_loan_purpose("debt_consolidation") == "debt_consolidation"
    assert clean_loan_purpose("vacation") == "vacation"
    assert clean_loan_purpose("unknown_purpose") == "other"
    assert clean_loan_purpose("xyz") == "other"
    assert clean_loan_purpose(None) == "other"
    print("✅ TEST 3 PASSED: loan_purpose cleaning works correctly")


# ============================================================
# TEST 4: null annual_income removal (Notebook 2)
# ============================================================

def filter_null_income(records):
    return [r for r in records if r["annual_income"] is not None]

def test_null_annual_income_removal():
    records = [
        {"member_id": 1, "annual_income": 50000.0},
        {"member_id": 2, "annual_income": None},
        {"member_id": 3, "annual_income": 75000.0},
        {"member_id": 4, "annual_income": None}
    ]
    filtered = filter_null_income(records)
    assert len(filtered) == 2
    assert all(r["annual_income"] is not None for r in filtered)
    print("✅ TEST 4 PASSED: Null annual_income rows removed correctly")


# ============================================================
# TEST 5: emp_length null replacement with average (Notebook 2)
# ============================================================

def replace_null_emp_length(values, avg):
    return [avg if v is None else v for v in values]

def test_emp_length_null_replacement():
    values = [5, 3, None, 8, None, 6]
    avg = 6
    result = replace_null_emp_length(values, avg)
    assert None not in result
    assert result[2] == 6
    assert result[4] == 6
    print("✅ TEST 5 PASSED: emp_length null replacement works correctly")


# ============================================================
# TEST 6: loan_term conversion months to years (Notebook 3)
# ============================================================

def convert_loan_term_to_years(term_str):
    if term_str is None:
        return None
    digits = re.sub(r'\D', '', term_str)
    return int(digits) // 12

def test_loan_term_conversion():
    assert convert_loan_term_to_years("36 months") == 3
    assert convert_loan_term_to_years("60 months") == 5
    assert convert_loan_term_to_years(None) is None
    print("✅ TEST 6 PASSED: loan_term months to years conversion works correctly")


# ============================================================
# TEST 7: zero payment fix (Notebook 4)
# If total_payment = 0 but principal != 0, fix it
# ============================================================

def fix_total_payment(principal, interest, late_fee, total_payment):
    if principal != 0.0 and total_payment == 0.0:
        return principal + interest + late_fee
    return total_payment

def test_zero_payment_fix():
    # Case 1: payment is 0 but principal exists → fix it
    assert fix_total_payment(1000.0, 50.0, 10.0, 0.0) == 1060.0
    # Case 2: payment is already correct → keep it
    assert fix_total_payment(1000.0, 50.0, 10.0, 1060.0) == 1060.0
    # Case 3: both are 0 → keep 0
    assert fix_total_payment(0.0, 0.0, 0.0, 0.0) == 0.0
    print("✅ TEST 7 PASSED: Zero payment fix works correctly")


# ============================================================
# TEST 8: loan score calculation (Notebook 9)
# ============================================================

def calculate_loan_score(last_payment_pts, total_payment_pts,
                          delinq_pts, pub_rec_pts,
                          pub_bankruptcies_pts, enq_pts,
                          loan_status_pts, home_pts,
                          credit_limit_pts, grade_pts):
    payment_history = (last_payment_pts + total_payment_pts) * 0.25
    defaulters_history = (delinq_pts + pub_rec_pts + pub_bankruptcies_pts + enq_pts) * 0.45
    financial_health = (loan_status_pts + home_pts + credit_limit_pts + grade_pts) * 0.30
    return payment_history + defaulters_history + financial_health

def test_loan_score_calculation():
    score = calculate_loan_score(
        last_payment_pts=800, total_payment_pts=650,
        delinq_pts=800, pub_rec_pts=800,
        pub_bankruptcies_pts=800, enq_pts=800,
        loan_status_pts=800, home_pts=800,
        credit_limit_pts=800, grade_pts=2500
    )
    assert score > 0
    assert score == (800 + 650) * 0.25 + (800 + 800 + 800 + 800) * 0.45 + (800 + 800 + 800 + 2500) * 0.30
    print("✅ TEST 8 PASSED: Loan score calculation works correctly")


# ============================================================
# TEST 9: loan final grade assignment (Notebook 9)
# ============================================================

def get_loan_grade(score):
    if score > 2500:
        return "A"
    elif score > 1500:
        return "B"
    elif score > 1000:
        return "C"
    elif score > 500:
        return "D"
    elif score > 0:
        return "E"
    else:
        return "F"

def test_loan_grade_assignment():
    assert get_loan_grade(3000) == "A"
    assert get_loan_grade(2000) == "B"
    assert get_loan_grade(1200) == "C"
    assert get_loan_grade(750)  == "D"
    assert get_loan_grade(300)  == "E"
    assert get_loan_grade(0)    == "F"
    assert get_loan_grade(-100) == "F"
    print("✅ TEST 9 PASSED: Loan grade assignment works correctly")