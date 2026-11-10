# API Testing with pytest and requests (`api-lab`)

This repository contains the automated integration test suite for the **QuickPizza** API (`https://quickpizza.grafana.com`), developed as part of **ITDS362 Software Quality Assurance and Testing**.

---

## 1. Setup and Installation

### Prerequisites
- Python 3.10 or newer (tested with Python 3.13)
- `curl` / `curl.exe`

### Virtual Environment Setup
1. Clone or open the repository folder:
   ```bash
   git clone <repository-url>
   cd api-lab
   ```

2. Create and activate a Python virtual environment:
   - **Windows PowerShell:**
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\activate
     ```
   - **macOS / Linux:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

---

## 2. Running Tests

### Run the full test suite
```bash
pytest -v
```

### Run and generate the HTML report
```bash
pytest -v --html=report.html --self-contained-html
```
Open `report.html` in your browser to inspect test results, execution durations, and defect traces.

---

## 3. Input Domain Model for `POST /api/ratings` (Step A1 & A2)

The operation `POST /api/ratings` accepts a JSON body with `pizza_id` and `stars`, alongside an `Authorization: token <token>` header.
The input domain is partitioned into four characteristics using **Base Choice Coverage**:

| Characteristic | Blocks | Values in the tests | Test covering the block |
| :--- | :--- | :--- | :--- |
| **C1 Value of stars** | 1 to 5 (base) | `3` | `test_base_choice_is_saved` |
| | below 1 | `0` | `test_stars_out_of_range[0]` |
| | above 5 | `6` | `test_stars_out_of_range[6]` |
| **C2 Type of stars** | whole number (base) | `3` | `test_base_choice_is_saved` |
| | decimal | `3.5` | `test_stars_decimal` |
| | text | `"3"` | `test_stars_text` |
| | missing | no field | `test_stars_missing` |
| **C3 Pizza** | exists (base) | a new pizza ID | `test_base_choice_is_saved` |
| | does not exist | `999999999` | `test_pizza_does_not_exist` |
| **C4 Token** | the user's own (base) | token from `auth` fixture | `test_base_choice_is_saved` |
| | none | no header | `test_token_missing` |
| | wrong length | `"token short"` | `test_token_wrong_length` |

### Coverage Calculation
- **Base Choice Coverage:**
  $$1 + (3 - 1) + (4 - 1) + (2 - 1) + (3 - 1) = 1 + 2 + 3 + 1 + 2 = 9\text{ tests}$$
- **All Combinations Coverage:**
  $$3 \times 4 \times 2 \times 3 = 72\text{ tests}$$

---

## 4. Repository Structure

```text
api-lab/
├── .gitignore               # Standard Python gitignore preventing .venv and caches from commit
├── README.md                # Installation, test execution guide, and Input Domain Model
├── RESULTS.md               # Recorded outputs, Defect Report, and Part B reflections
├── requirements.txt         # Required packages: pytest, requests, pytest-html
├── report.html              # Standalone HTML execution report (32 passed, 1 xfailed)
├── auth.txt                 # Public token header for curl testing
├── veg.json                 # Vegetarian request payload for curl testing
├── madeup.txt               # Arbitrary 16-character token header for security reflection
├── conftest.py              # Pytest fixtures: api, auth, pizza_id, rating, other_auth
├── test_names.py            # Step 0.6: GET /api/names test
├── test_tools.py            # Step 0.7: GET /api/tools test
├── test_pizza.py            # Step 0.8: POST /api/pizza tests (vegetarian and 401 refusal)
├── test_users.py            # Step 0.11: User session test
├── test_ratings.py          # Step 0.13 & 0.14: CRUD operations on /api/ratings
├── test_refused.py          # Step 0.15: Input validation refusal tests (duplicate, wrong pw, empty)
├── test_excluded_tools.py   # Step 0.16: Excluded tools and xfail bug hunt test
├── test_create_rating.py    # Step A1 & A2: Base choice coverage for ratings creation
├── test_update_rating.py    # Step A3: Boundary value analysis for rating updates
└── test_rating_owner.py     # Step A4: Access control and resource ownership tests
```
