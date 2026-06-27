# JHU-AI-Engineering-Course

## Module 01: Introduction

This repository contains introductory example scripts for the JHU AI Engineering Course.

### Module folder
- `module_01_introduction`

### Scripts added
- `module_01_introduction/hello.py` — prints a welcome message from Murali Chadaram.
- `module_01_introduction/hello.js` — prints the same welcome message in JavaScript.

### Run the scripts

From the repository root:

```bash
python3 module_01_introduction/hello.py
node module_01_introduction/hello.js
```

---

## Module 02: Data Analytics

### Module folder
- `module_02_data_analysis`

### Assignment
- `module_02_data_analysis/assignment.md` — explores how data analytics and AI can maximize utilization of existing compute infrastructure, reducing the need for new data center builds while lowering costs and environmental impact.

---

## Module 03: Vibe Coding — AI-Assisted Cloud Kitchen Inventory Simulation

### Module folder
- `module_03_vibe_coding/cloud_kitchne_inventory_simulation`

### Assignment
A Python-based inventory and order management simulation for a multi-brand cloud kitchen, built using AI-assisted coding practices. The assignment demonstrates how to use AI as a coding assistant while maintaining critical review, testing, and documentation discipline.

### Files
| File | Description |
|------|-------------|
| `main.py` | Core simulation logic — order fulfillment, inventory deduction, restock rules, business summary |
| `seed_data.py` | Five seed tables: Recipes (5), Inventory (14), Orders (5), Restock, Status |
| `test_main.py` | 31 unit tests across 7 test classes — all passing |
| `PROJECT_SPEC.md` | Project specification and AI context anchor |
| `AI_USAGE_LOG.md` | Log of all AI prompts, responses, and decisions (Tasks 3–10) |
| `REFLECTION.md` | Written reflection on AI-assisted coding (Task 11, ~570 words) |
| `SUBMISSION_VALIDATION_REPORT.md` | Pre-submission checklist validation against all rubric items |

### Quick Start

```bash
cd module_03_vibe_coding/cloud_kitchne_inventory_simulation

# Create the importable seed data file (required — original filename has a hyphen)
cp seed_data-1.py seed_data.py

# Run the simulation
python3 main.py

# Run all tests
python3 -m unittest test_main -v
```

No packages to install — uses Python standard library only (`copy`, `datetime`, `io`, `sys`, `unittest`).

### Key Features Implemented
- **Cumulative inventory deduction** — each order depletes stock seen by later orders
- **All-or-nothing fulfillment** — failed orders record exact missing ingredients; no partial deduction
- **Restock and expiry rules** — flags out-of-stock, low-stock (≤1,000g), and expiring-soon (≤5 days) ingredients
- **Business summary** — human-readable end-of-day report for kitchen managers
- **Partial fulfillment (Optional Enhancement A)** — per-item independent fulfillment with immediate deduction to prevent double-spend

### Test Results
```
Ran 31 tests in 0.002s
OK
```

| Test Class | Tests | Coverage |
|------------|-------|----------|
| `TestLoadFunctions` | 6 | Import, record counts, field types |
| `TestOrderRecipeLookup` | 3 | Recipe match, missing recipe, quantity scaling |
| `TestOrderFulfillment` | 3 | Delivered, not-delivered, inventory deduction |
| `TestCumulativeInventoryDeduction` | 3 | Sequential deduction, depletion failure |
| `TestRestockRules` | 4 | Expiring soon, out of stock, running low |
| `TestBusinessSummary` | 5 | Counts, failure reasons, restock output |
| `TestPartialFulfillment` | 6 | Per-item fulfillment, double-spend prevention |


