# Python Error Debugging Assistant — QA Test Cases

## 1. Purpose
This document contains 10 test cases used to evaluate the Python Error Debugging Assistant.

The test cases cover common Python errors, logical bugs, ambiguous inputs, empty inputs, and off-topic queries.

## 2. Test Cases

### TC01 — IndexError
**Category:** Runtime Error

**Input Code:**
```python
numbers = [10, 20, 30]
print(numbers[5])
```

**Expected Result:**
- Identify IndexError.
- Explain that index 5 is outside the valid range.
- Suggest using a valid index or checking the list length.
- Provide corrected code.

### TC02 — NameError
**Category:** Runtime Error

**Input Code:**
```python
name = "Krushang"
print(nam)
```

**Expected Result:**
- Identify NameError.
- Explain that `nam` is undefined.
- Suggest using the variable `name`.
- Provide corrected code.

### TC03 — ZeroDivisionError
**Category:** Runtime Error

**Input Code:**
```python
a = 10
b = 0
result = a / b
print(result)
```

**Expected Result:**
- Identify ZeroDivisionError.
- Explain that division by zero is not allowed.
- Suggest checking the denominator before division.
- Provide corrected code.

### TC04 — TypeError
**Category:** Runtime Error

**Input Code:**
```python
age = 20
message = "Age: " + age
print(message)
```

**Expected Result:**
- Identify TypeError.
- Explain the string and integer type mismatch.
- Suggest using `str()` or an f-string.
- Provide corrected code.

### TC05 — KeyError
**Category:** Runtime Error

**Input Code:**
```python
student = {"name": "Rahul", "age": 20}
print(student["grade"])
```

**Expected Result:**
- Identify KeyError.
- Explain that the `grade` key is missing.
- Suggest adding the key or using `.get()`.
- Provide corrected code.

### TC06 — SyntaxError
**Category:** Syntax Error

**Input Code:**
```python
def greet(name)
    print("Hello", name)
```

**Expected Result:**
- Identify SyntaxError.
- Explain that a colon is missing after the function definition.
- Provide corrected code.

### TC07 — Multi-file Logical Bug
**Category:** Logical Error / Stretch Challenge

**main.py**
```python
from calculator import add

print(add(10, 20))
```

**calculator.py**
```python
def add(a, b):
    return a - b
```

**Expected Result:**
- Identify the logical error in the `add()` function.
- Explain that subtraction is used instead of addition.
- Suggest changing `a - b` to `a + b`.
- Provide a test such as `assert add(10, 20) == 30`.

### TC08 — Ambiguous Input
**Category:** Ambiguous / Incomplete Context

**Input Code:**
```python
def calculate_total(price, quantity):
    return price * quantity

total = calculate_total(price, quantity)
print(total)
```

**Traceback:**
```text
NameError: name 'price' is not defined
```

**Expected Result:**
- Identify the immediate NameError.
- Explain that `price` is undefined.
- Mention that `quantity` may also be undefined.
- Distinguish confirmed issues from assumptions.
- Ask for missing context if necessary.

### TC09 — Empty Input
**Category:** Edge Case

**Input:**
No code and no traceback provided.

**Expected Result:**
- Do not invent an error or diagnosis.
- Ask the user to provide Python code and/or traceback.
- Handle the empty input gracefully.

### TC10 — Off-topic Query
**Category:** Adversarial / Scope Handling

**Input:**
"Plan a 3-day trip to Goa."

**Expected Result:**
- Recognize that the request is unrelated to Python debugging.
- Politely redirect the user to provide Python code or an error traceback.
- Do not generate an unrelated travel itinerary.

## 3. Evaluation Method

Each test case is evaluated using:

- **PASS:** The application meets the expected behavior.
- **FAIL:** The application does not meet the expected behavior.
- **NOT RUN:** The test has not yet been executed.

## 4. Evaluation Metric

**QA Test Pass Rate (%)**

Formula:

Pass Rate = (Number of Passed Test Cases / Number of Executed Test Cases) × 100

The same 10 test cases should be used for both the first prompt version (V1) and final prompt version.

Actual results should be recorded after running the test cases on the application.
## 5. Test Results

The same 10 test cases are used to evaluate the first prompt version (V1) and the final prompt version.

| Test Case | V1 Result | Final Version Result |
|---|---|---|
| TC01 — IndexError | Pending | Pending |
| TC02 — NameError | Pending | Pending |
| TC03 — ZeroDivisionError | Pending | Pending |
| TC04 — TypeError | Pending | Pending |
| TC05 — KeyError | Pending | Pending |
| TC06 — SyntaxError | Pending | Pending |
| TC07 — Multi-file Logical Bug | Pending | Pending |
| TC08 — Ambiguous Input | Pending | Pending |
| TC09 — Empty Input | Pending | Pending |
| TC10 — Off-topic Query | Pending | Pending |
| **Total Passed** | **1/10** | Pending |
| **Total Failed** | **9/10** | Pending |
| **Pass Rate** | **10%** | Pending |

### Evaluation Labels
- **PASS:** Expected behavior is achieved.
- **FAIL:** Expected behavior is not achieved.
- **NOT RUN:** Test has not yet been executed.
