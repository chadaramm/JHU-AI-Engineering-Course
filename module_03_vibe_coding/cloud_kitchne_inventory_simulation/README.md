# AI-Assisted Cloud Kitchen Inventory Simulation

A Python-based simulation of a multi-brand cloud kitchen's inventory and order management
for a single operational day. Built using AI-assisted coding practices as part of the JHU
AI Engineering Course — Module 03: Vibe Coding.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Project Setup](#project-setup)
3. [Step-by-Step Execution Guide](#step-by-step-execution-guide)
4. [Sample Output](#sample-output)
5. [Data Loading](#data-loading)
6. [Recipe Lookup](#recipe-lookup)
7. [Inventory Availability](#inventory-availability)
8. [Order Fulfillment](#order-fulfillment)
9. [Cumulative Processing](#cumulative-processing)
10. [Restock and Expiry Logic](#restock-and-expiry-logic)
11. [Business Summary](#business-summary)
12. [Optional Enhancement — Partial Fulfillment](#optional-enhancement--partial-fulfillment)
13. [Refactoring Notes](#refactoring-notes)
14. [Test Suite](#test-suite)
15. [AI Usage Summary](#ai-usage-summary)
16. [Reflection](#reflection)

---

## Quick Start

```bash
# 1. Clone the repo and navigate to the project folder
git clone <repo-url>
cd module_03_vibe_coding/cloud_kitchen

# 2. Create the importable seed data file
cp seed_data-1.py seed_data.py

# 3. Run the simulation
python3 main.py

# 4. Run all tests
python3 -m unittest test_main -v
```

No packages to install — uses Python standard library only.

---

## Project Setup

### Requirements

- Python 3.9 or later
- No third-party packages required

### File Structure

```
cloud_kitchen/
├── main.py              # Core simulation logic
├── seed_data.py         # Importable seed data (copied from seed_data-1.py)
├── seed_data-1.py       # Original provided seed file
├── test_main.py         # Unit tests — 31 tests across 5 test classes
├── PROJECT_SPEC.md      # Project specification and AI context anchor
├── AI_USAGE_LOG.md      # Log of all AI prompts, responses, and decisions
├── REFLECTION.md        # Written reflection on AI-assisted coding (Task 11)
└── README.md            # This file
```

### Important Note on `seed_data-1.py`

The seed file provided by the instructor is named `seed_data-1.py`. Python cannot import
a module whose name contains a hyphen. Before running the program or tests, copy it:

```bash
cp seed_data-1.py seed_data.py
```

Verify the import works:

```bash
python3 -c "from seed_data import recipes, inventory, orders, restock, status; print('OK')"
```

---

## Step-by-Step Execution Guide

### Step 1 — Set Up the Seed Data

```bash
cp seed_data-1.py seed_data.py
```

### Step 2 — Run the Full Simulation

```bash
python3 main.py
```

This runs the complete order fulfillment pipeline and prints:
- All recipes and their ingredient requirements
- All incoming orders
- Per-order processing detail (recipe lookup, ingredient demand, inventory check, result)
- Final inventory after all orders
- Restock recommendations
- Delivery status per order
- End-of-day business summary

### Step 3 — Run All Unit Tests

```bash
python3 -m unittest test_main -v
```

Expected output:

```
----------------------------------------------------------------------
Ran 31 tests in 0.002s

OK
```

### Step 4 — Run a Specific Test Class

```bash
# Data loading tests
python3 -m unittest test_main.TestLoadFunctions -v

# Recipe lookup tests
python3 -m unittest test_main.TestOrderRecipeLookup -v

# Fulfillment tests
python3 -m unittest test_main.TestOrderFulfillment -v

# Cumulative deduction tests
python3 -m unittest test_main.TestCumulativeInventoryDeduction -v

# Restock rule tests
python3 -m unittest test_main.TestRestockRules -v

# Business summary tests
python3 -m unittest test_main.TestBusinessSummary -v

# Partial fulfillment enhancement tests
python3 -m unittest test_main.TestPartialFulfillment -v
```

### Step 5 — Run a Single Test Method

```bash
python3 -m unittest test_main.TestRestockRules.test_expiring_soon_sets_full_restock_quantity -v
python3 -m unittest test_main.TestPartialFulfillment.test_one_item_unavailable_marks_order_partially_delivered -v
```

### Step 6 — Try the Partial Fulfillment Mode

To use the optional partial fulfillment logic from a Python shell:

```python
from copy import deepcopy
from main import load_recipes, load_inventory, load_orders, load_status
from main import process_orders_partial, print_business_summary

recipe_data  = load_recipes()
inventory_data = deepcopy(load_inventory())
order_data   = load_orders()
status_data  = deepcopy(load_status())
restock_data = []

processed = process_orders_partial(
    recipe_data, inventory_data, order_data, status_data, restock_data
)
print_business_summary(processed, inventory_data, restock_data)
```

---

## Sample Output

```
======================================================
   CLOUD KITCHEN — END OF DAY SUMMARY
======================================================

ORDERS PROCESSED:  5
  Delivered:       5
  Not Delivered:   0

FINAL INVENTORY
  Flour                     8850g   expires 2026-05-12
  Tomato Sauce              9700g   expires 2026-11-15
  Mozzarella Cheese         9550g   expires 2026-10-20
  Chicken Breast             800g   expires 2026-10-10
  Romaine Lettuce           9600g   expires 2026-05-12
  Caesar Dressing           9900g   expires 2026-10-15
  Croutons                  9940g   expires 2026-10-18
  Bun                       5400g   expires 2026-10-09
  Lettuce                   7700g   expires 2026-10-09
  Fettuccine Pasta          9800g   expires 2026-01-31
  Cream                     9900g   expires 2026-10-12
  Parmesan Cheese           9950g   expires 2026-10-15
  Chocolate                 9850g   expires 2026-01-15
  Sugar                     9900g   expires 2026-05-12

RESTOCK RECOMMENDATIONS
  Chicken Breast         order   9200g   (Running low on stock)

======================================================
```

---

## Data Loading

The simulation uses five core data structures imported from `seed_data.py`:

| Table | Records | Key Fields |
|-------|---------|------------|
| Recipes | 5 | `recipe_id`, `name`, `ingredients[{name, qty_grams}]` |
| Inventory | 14 | `ingredient`, `qty_grams`, `expiry_date` |
| Orders | 5 | `order_id`, `brand`, `items[{item, qty}]` |
| Restock | 5 (seed only) | `item`, `qty_needed_grams`, `reason` |
| Status | 5 | `order_id`, `delivered`, `remark` |

Five loader functions (`load_recipes()`, `load_inventory()`, `load_orders()`,
`load_restock()`, `load_status()`) import and return each table. Five corresponding
`print_*()` functions display them to the console.

All quantities are stored in grams. `main()` calls `deepcopy()` on mutable tables before
processing so the seed definitions stay unchanged across runs and tests.

**Verified by:** `TestLoadFunctions` — 6 tests covering successful import, record counts,
and key field types for all five tables.

---

## Recipe Lookup

`find_recipe_by_name(recipe_data, item_name)` searches the recipe table for an exact
case-sensitive name match against the ordered item name. Returns the matching recipe dict
or `None` if no recipe is found.

`calculate_ingredient_requirements(recipe, quantity)` multiplies each ingredient's
per-serving grams by the ordered quantity to produce total grams required.

**Example:** Margherita Pizza × 2 → Flour 600g, Tomato Sauce 200g, Mozzarella Cheese 300g.

Missing recipes are handled gracefully — the item is recorded with `recipe_found=False`
and the order is rejected without crashing.

**Verified by:** `TestOrderRecipeLookup` — 3 tests covering valid match, missing recipe,
and correct quantity scaling.

---

## Inventory Availability

`check_inventory_availability(inventory_data, requirements)` compares total ingredient
demand against available stock. Uses `_build_inventory_lookup()` to build a fast
name-keyed dict, then checks each required ingredient for presence and quantity.

Returns:
- `all_available` — `True` only if every required ingredient has enough stock
- `details` — per-ingredient breakdown of required vs available grams

`combine_requirements(requirement_groups)` merges demand across all items in the same
order before the check, so shared ingredients are evaluated against their combined total.

**Verified by:** `TestOrderFulfillment` — tests for sufficient stock, missing ingredient,
and correct deduction amounts.

---

## Order Fulfillment

`process_orders()` applies all-or-nothing fulfillment:

| Condition | Result | Stock Deducted? |
|-----------|--------|----------------|
| All ingredients available | **Delivered** | Yes |
| Any ingredient missing/insufficient | **Not Delivered** | No |
| Any item has no matching recipe | **Not Delivered** | No |

Failed orders always include a specific reason string naming the missing ingredients or
unmatched recipe items.

**Verified by:** `TestOrderFulfillment` — 3 tests for delivered status, not-delivered with
restock logging, and correct deduction with no unintended deduction on failure.

---

## Cumulative Processing

`process_orders()` deep-copies `inventory_data` into `working_inventory` at the start.
All checks and deductions run against this copy — not the original.

- Order 2 sees stock remaining after Order 1
- Order 3 sees stock remaining after Orders 1 and 2
- Competing orders: earlier order consumes first; later order gets what remains

After all orders complete, `apply_final_inventory_snapshot()` writes the final quantities
back to `inventory_data` in a single pass.

**Verified by:** `TestCumulativeInventoryDeduction` — 3 tests for combined deduction,
stock depletion failure, and final inventory values matching manual calculations.

---

## Restock and Expiry Logic

`calculate_restock_needs()` applies three rules in priority order after all orders are
processed:

| Priority | Condition | Label | Qty Needed |
|----------|-----------|-------|------------|
| 1 | Expiry within 5 days | `Expiring soon` | 10,000g |
| 2 | Stock == 0g | `Out of stock` | 10,000g |
| 3 | Stock ≤ 1,000g | `Running low on stock` | 10,000g − current qty |

Business rule constants are defined at the top of `main.py`:

```python
PAR_LEVEL_GRAMS         = 10_000
LOW_STOCK_THRESHOLD_GRAMS = 1_000
EXPIRY_WINDOW_DAYS      = 5
DATE_FORMAT             = "%Y-%m-%d"
```

The seed restock values are discarded at runtime — `refresh_restock_table()` rebuilds the
live restock table from final inventory after every run.

**Verified by:** `TestRestockRules` — 4 tests for expiring soon, out of stock, running
low, and adequate stock not flagged.

---

## Business Summary

`print_business_summary()` produces a human-readable end-of-day report with:

- Total orders processed, delivered, and not delivered
- Per-order failure reasons (when applicable)
- Final inventory table with quantities and expiry dates
- Restock recommendations with quantities and reasons

**Verified by:** `TestBusinessSummary` — 5 tests covering counts, failure reasons,
restock display, empty restock message, and full seed data end-to-end run.

---

## Optional Enhancement — Partial Fulfillment

`process_orders_partial()` evaluates each item in an order independently instead of
treating the order as all-or-nothing:

| Outcome | `fulfilled` | `partial` | Meaning |
|---------|------------|---------|---------|
| All items delivered | `True` | `False` | Fully delivered |
| Some items delivered | `True` | `True` | Partially delivered |
| No items delivered | `False` | `False` | Not delivered |

Stock is deducted immediately after each item passes its availability check, so later
items in the same order correctly see the reduced stock left by earlier items.

**Verified by:** `TestPartialFulfillment` — 6 tests covering full delivery, partial
delivery, full failure, selective deduction, missing recipe handling, and prevention of
double-spend within a single order when two items share one ingredient.

---

## Refactoring Notes

Two improvements were made after completing the core implementation (Task 10):

**1. Extracted `_build_inventory_lookup()` helper**

The dict comprehension `{item["ingredient"]: item for item in inventory_data}` appeared
identically in `check_inventory_availability()` and `deduct_inventory()`. Extracted into
a single private helper called by both.

**2. Replaced magic numbers with named constants**

| Before | After | Meaning |
|--------|-------|---------|
| `10000` | `PAR_LEVEL_GRAMS` | Target stock level after restock |
| `1000` | `LOW_STOCK_THRESHOLD_GRAMS` | Trigger for "running low" |
| `5` | `EXPIRY_WINDOW_DAYS` | Days ahead to flag expiring items |
| `"%Y-%m-%d"` | `DATE_FORMAT` | Seed data date string format |

All 25 existing tests passed without modification after refactoring.

---

## Test Suite

| Test Class | Tests | What It Covers |
|------------|-------|---------------|
| `TestLoadFunctions` | 6 | Import, record counts, field types for all 5 tables |
| `TestOrderRecipeLookup` | 3 | Recipe match, missing recipe, quantity scaling |
| `TestOrderFulfillment` | 3 | Delivered, not-delivered, inventory deduction |
| `TestCumulativeInventoryDeduction` | 3 | Sequential deduction, depletion failure, final values |
| `TestRestockRules` | 4 | Expiring soon, out of stock, running low, no flag |
| `TestBusinessSummary` | 5 | Counts, failure reasons, restock output, edge cases |
| `TestPartialFulfillment` | 6 | Per-item fulfillment, selective deduction, double-spend |
| **Total** | **31** | **All passing** |

---

## AI Usage Summary

AI was used as a coding assistant following an incremental workflow throughout the project.

**Prompt templates used:**
- **Template 1 — Planning:** Architecture before any code was written
- **Template 2 — Task Breakdown:** Order processing component broken into individual tasks
- **Template 3 — Implementation:** One task per prompt, "Do not implement any other tasks yet"
- **Template 4 — Debugging:** Used for the `datetime` vs `date` type crash in restock logic
- **Validation Hook:** Used after every implementation prompt to surface hidden assumptions

**Key bugs caught through review and testing:**

| Bug | Fix |
|-----|-----|
| `copy.copy()` shallow copy | Changed to `copy.deepcopy()` |
| `datetime.today()` type mismatch | Changed to `date.today()` |
| Per-item availability check | Changed to combined-total check |
| Restock appended inside loop | Changed to rebuild from final inventory |
| Simultaneous check-then-deduct in partial mode | Changed to immediate per-item deduction |

Full details of every AI interaction — prompts used, AI responses, and decisions made —
are documented in [`AI_USAGE_LOG.md`](./AI_USAGE_LOG.md).

---

## Reflection

See [`REFLECTION.md`](./REFLECTION.md) for the full written reflection (~570 words)
addressing:

1. How AI accelerated development
2. Where AI made mistakes or questionable assumptions
3. How testing helped evaluate AI-generated code
4. What was changed or rejected from AI suggestions
5. How `PROJECT_SPEC.md` helped maintain context across sessions
6. What would be done differently in a future AI-assisted project

---

## Course Information

**Course:** JHU AI Engineering Course  
**Module:** 03 — Vibe Coding  
**Assignment:** AI-Assisted Cloud Kitchen Inventory Simulation  
**Language:** Python 3.9+  
**Dependencies:** None (stdlib only)
