# PROJECT_SPEC.md
# Cloud Kitchen Inventory Simulation — Project Specification

## Project Purpose

Build a Python-based simulation of a multi-brand cloud kitchen's inventory and order
management for a single operational day. The system processes customer orders, checks
recipe-linked inventory, deducts ingredients, tracks expiry risk, updates delivery status,
and generates a restock plan and business summary.

The purpose is to demonstrate AI-assisted coding practices: planning, incremental
implementation, validation, testing, debugging, and refactoring.

---

## Files

| File | Description |
|------|-------------|
| `seed_data.py` | All seed data tables (copied from `seed_data-1.py`) |
| `main.py` | Simulation logic — loading, processing, printing |
| `test_main.py` | Unit tests using Python `unittest` |
| `PROJECT_SPEC.md` | This file — external AI memory and project context |
| `AI_USAGE_LOG.md` | Log of AI prompts, responses, and decisions |

> Setup note: `seed_data-1.py` cannot be imported due to the hyphen in its name.
> Run `cp seed_data-1.py seed_data.py` before running any code.

---

## How to Run

```bash
# Run simulation
python3 main.py

# Run all tests
python3 -m unittest test_main -v

# Run a single test class
python3 -m unittest test_main.TestRestockRules -v

# Run a single test method
python3 -m unittest test_main.TestRestockRules.test_expiring_soon_sets_full_restock_quantity -v
```

---

## Data Structures (from seed_data.py)

### Recipes (5 records)
```
recipe_id | name              | ingredients: [{name, qty_grams}]
```
Items: Margherita Pizza, Chicken Burger, Caesar Salad, Pasta Alfredo, Chocolate Cake.
All ingredient quantities are per single serving (grams).

### Inventory (14 records)
```
ingredient | qty_grams | expiry_date (YYYY-MM-DD string)
```
All quantities stored in grams, including items like Bun.

### Orders (5 records)
```
order_id | brand | items: [{item, qty}]
```
Brands: Taco Bell (orders 1, 5), Subway (orders 2, 3, 4).
`item` must match `recipes.name` exactly (case-sensitive, no aliases).

### Restock (5 seed records — ignored at runtime)
```
item | qty_needed_grams | reason
```
The live restock table is cleared and rebuilt from final inventory after all orders
are processed. Seed values exist only for baseline loading tests.

### Status (5 seed records)
```
order_id | delivered (bool) | remark (string)
```
Updated in-place during `process_orders()`.

---

## Business Rules

| Rule | Value |
|------|-------|
| Recipe lookup | Exact name match — case-sensitive, no normalization |
| Fulfillment | All-or-nothing — full order rejected if any ingredient missing |
| Partial fulfillment | Not implemented in base version |
| Inventory deduction | Only on fully successful orders |
| Cumulative deduction | Yes — each order checks stock remaining after prior orders |
| Running low threshold | qty ≤ 1,000g |
| Out of stock | qty == 0 |
| Par level (restock target) | 10,000g |
| Expiry window | Within 5 days of simulation date |
| Restock rule priority | Expiry soon > Out of stock > Running low (elif chain, no overlap) |
| Simulation date | `date.today()` unless `reference_date` param is passed explicitly |

---

## Implementation Plan

### Part 1 — Data Connectivity
- **Task 3**: Load and print all 5 seed tables → `load_*()` and `print_*()` functions

### Part 2 — Application Flow
- **Task 4**: Recipe lookup and ingredient scaling → `find_recipe_by_name()`, `calculate_ingredient_requirements()`
- **Task 5**: Inventory availability check → `check_inventory_availability()`
- **Task 6**: Fulfillment and deduction → `deduct_inventory()`, `update_status_entry()`, `process_orders()`

### Part 3 — Logic Refinement
- **Task 7**: Cumulative inventory deduction → `deepcopy(inventory_data)` as `working_inventory` inside `process_orders()`; `apply_final_inventory_snapshot()` after all orders
- **Task 8**: Restock and expiry rules → `calculate_restock_needs()`, `refresh_restock_table()`

### Part 4 — Output and Quality
- **Task 9**: Business-friendly summary → `print_business_summary()` (TODO)
- **Task 10**: Refactoring review (TODO)
- **Task 11**: Written reflection (TODO)

---

## Testing Plan

| Test Class | What It Covers |
|------------|---------------|
| `TestLoadFunctions` | All 5 tables load, record counts correct, key field types valid |
| `TestOrderRecipeLookup` | Recipe match, missing recipe returns None, quantity scaling |
| `TestOrderFulfillment` | Delivered status, not-delivered status, inventory deduction, no deduction on failure |
| `TestCumulativeInventoryDeduction` | Combined deduction across orders, later order fails after prior depletes stock, final inventory values |
| `TestRestockRules` | Expiring soon, out of stock, running low, adequate stock not flagged |

All tests use explicit `reference_date=date(2026, 6, 3)` where date-sensitivity matters
to avoid time-dependent failures.

---

## Key Design Decisions

1. **Deepcopy for working inventory**: `process_orders()` uses `deepcopy(inventory_data)` as
   `working_inventory` so interim deductions during processing do not prematurely mutate
   the source table. The final table is updated once, after all orders complete.

2. **Restock rebuilt every run**: `refresh_restock_table()` clears and rebuilds `restock_data`
   from final inventory state. Seed restock values are intentionally discarded at runtime.

3. **Status entries created if missing**: `update_status_entry()` appends a new row if
   `order_id` is not found in `status_data`, supporting test-isolated scenarios with empty tables.

4. **Expiry rule priority via elif**: An ingredient can only receive one restock reason per run.
   Expiry-soon takes priority; if not triggered, out-of-stock is checked; if not that, running-low.

---

## Open Questions and Assumptions

- Expiry check uses `date.today()` when no `reference_date` is passed. The simulation date
  basis should be confirmed with the instructor.
- Recipe lookup is exact-match only. No case folding, whitespace trimming, or brand-specific
  variants are handled.
- An ingredient cannot currently be flagged for both expiry and stock reasons simultaneously
  (elif chain). Requirement 6 in `additional_instructions.txt` says to "preserve all relevant
  reasons" — this may need a future fix to use independent checks instead of elif.
- `Bun` and similar items are stored in grams even though they are typically counted in units.

---

## Completed Tasks

- [x] Task 3: Load and display all 5 seed tables
- [x] Task 4: Recipe lookup and ingredient scaling
- [x] Task 5: Inventory availability check
- [x] Task 6: Fulfillment logic and inventory deduction
- [x] Task 7: Cumulative inventory deduction
- [x] Task 8: Restock and expiry rules
- [ ] Task 9: Business-friendly summary output
- [ ] Task 10: Refactoring review
- [ ] Task 11: Written reflection
- [ ] Optional Enhancement (A / B / C / D — choose one)

---

## Current Task

**Task 9** — Implement `print_business_summary()` in `main.py`.

## Next Task

**Task 10** — Refactoring review: extract constants, eliminate duplication, improve clarity.
