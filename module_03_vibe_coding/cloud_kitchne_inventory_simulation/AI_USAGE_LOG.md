# AI_USAGE_LOG.md
# AI Usage Log — Cloud Kitchen Inventory Simulation

This file documents how AI was used during the development of this project.
Each entry records the task, the prompt given, a summary of the AI response,
and what was accepted, changed, or rejected.

---

## Task 3 — Load and Inspect Seed Data

**Goal:** Create `main.py` with functions to load and print all 5 seed tables.

**Prompt used (Template 1 — Planning):**
```
I want to build a Python cloud kitchen inventory simulation using seed_data.py.
Before writing any code, give me a high-level plan — what components do I need
and what should I build first?
```

**AI response summary:**
AI suggested building in three phases: (1) data connectivity layer with load/print
functions, (2) order processing pipeline, (3) restock and expiry logic. Recommended
starting with simple loaders before adding any business logic.

**Prompt used (Template 3 — Implementation):**
```
Implement Task 1: Create a baseline main.py file that imports all data from
seed_data.py. Write specific functions to load and print the contents of every
data table — including Recipes, Inventory, Orders, Restock, and Status — to the
console. Add comments explaining each function. Do not implement any other tasks yet.
```

**AI response summary:**
Generated `load_recipes()`, `load_inventory()`, `load_orders()`, `load_restock()`,
`load_status()` and corresponding `print_*()` functions. Each loader returned the
module-level list directly from `seed_data`.

**What I accepted:** All load and print functions.

**What I changed:**
- Added `deepcopy()` in `main()` before passing inventory and status to processing
  functions, to prevent seed data being mutated across runs.
- Added the Validation Hook prompt after code generation to surface assumptions.

**Issues found in AI output:**
- AI wrote `from seed_data import ...` but the provided file was named `seed_data-1.py`.
  Python cannot import a module with a hyphen in its name. Resolution: copy
  `seed_data-1.py` to `seed_data.py` before running.
- AI did not initially add inline assumption comments. Had to use the Validation Hook
  prompt separately to get those added.

**Validation Hook Prompt used:**
```
After generating the code, add inline comments that identify: (1) any assumptions
you made that I should verify, (2) any parts you are uncertain about, and (3) any
sections that are incomplete or require follow-up.
```

**Test generation prompt used:**
```
Write unit tests for the load functions using Python unittest. Cover: successful
import of all 5 tables, correct count of records in each table, and correct data
types for key fields (e.g. qty_grams is a number, expiry_date is a string).
```

**What I accepted from tests:** All generated test cases.
**What I changed in tests:** Verified expected record counts manually against seed data
(5 recipes, 14 inventory items, 5 orders, 5 restock, 5 status) before accepting.

---

## Task 4 — Recipe Lookup and Ingredient Scaling

**Goal:** Look up a recipe by item name and calculate total ingredient grams for a quantity.

**Prompt used (Template 2 — Task Breakdown):**
```
Here is component 'Order Processing' from our plan. Break it into individual
implementation tasks. Keep each task small enough to implement in a single prompt.
```

**AI response summary:**
AI broke it into: (1) recipe lookup by name, (2) ingredient quantity scaling,
(3) inventory check, (4) fulfillment decision, (5) inventory deduction. This matched
the planned task structure.

**Prompt used (Template 3 — Implementation):**
```
Implement Task 2: Update main.py to process orders from the Orders table. For each
order, the system should: 1. Look up the recipe for each item. 2. Calculate the total
grams of ingredients required. 3. Check the Inventory table to see if all required
ingredients are present in the necessary quantities. Add comments explaining each step.
Do not implement any other tasks yet.
```

**AI response summary:**
Generated `find_recipe_by_name()` using linear search with exact name match,
`calculate_ingredient_requirements()` multiplying per-serving grams by quantity,
and `check_inventory_availability()` building a lookup dict and comparing each
required ingredient against available stock.

**What I accepted:** All three functions.

**What I changed:**
- Confirmed that exact-match recipe lookup (no case folding) was intentional.
  Kept as-is since it matches the seed data exactly.
- Added `combine_requirements()` to merge ingredient demand across multiple items
  in the same order before the availability check, rather than checking per item.

**Issues found in AI output:**
- Initial version checked availability per order item separately, which could incorrectly
  pass an order if each item individually had enough but the combined total exceeded stock.
  Fixed by adding `combine_requirements()` and checking combined totals.

**Test generation prompt used:**
```
Write unit tests for the order-to-recipe lookup function using Python unittest.
Cover: a valid order item with a matching recipe, an order item with no matching recipe
(should handle gracefully), and correct calculation of total grams for an order with
quantity 2.
```

**What I accepted from tests:** All three test cases. Verified the quantity-2 doubling
manually (Margherita Pizza: Flour 300g × 2 = 600g, etc.).

---

## Task 5 — Inventory Availability Check

**Goal:** Check whether all required ingredients are available in sufficient quantity.

**Prompt used (Template 3 — Implementation):**
```
Implement Task 3: Add fulfillment logic. If all ingredients are available, mark the
order as 'Delivered' in the status table and deduct the used grams from the inventory.
If ingredients are missing, mark the order as 'Not Delivered,' record the reason, and
add the missing items to the Restock table. Add comments. Do not implement any other
tasks yet.
```

**AI response summary:**
Generated `deduct_inventory()`, `update_status_entry()`, and integrated them into an
order processing loop.

**What I accepted:** Core logic for status update and inventory deduction.

**What I changed:**
- Moved the processing loop into a standalone `process_orders()` function to keep
  `main()` clean and make the logic independently testable.
- Changed the restock addition to use `refresh_restock_table()` rather than appending
  directly inside the loop, so restock is rebuilt from final inventory instead of
  reflecting intermediate failures.

**Issues found in AI output:**
- AI initially deducted partial inventory for items whose recipes were found, even when
  other items in the same order had missing recipes. Added logic to reject the full
  order and skip deduction when any item lacks a recipe match.
- AI appended to `restock_data` inside the order loop, which could duplicate entries
  across orders. Replaced with a single rebuild after all orders are processed.

---

## Task 6 and Task 7 — Fulfillment + Cumulative Deduction

**Goal:** Ensure inventory deduction is cumulative across orders; update final inventory
only after all orders are processed.

**Prompt used (Template 3 — Implementation):**
```
Implement Task 4: Refine the inventory logic to be cumulative. Order 2 must check
availability against the quantity remaining after Order 1 was served. Update the final
inventory table only after all orders in the list have been processed to show the true
remaining stock. Add comments. Do not implement any other tasks yet.
```

**AI response summary:**
Suggested using a `deepcopy` of inventory as a working copy, deducting from it per
order, then applying the final state back to the original table at the end.

**What I accepted:** The deepcopy strategy and `apply_final_inventory_snapshot()` pattern.

**What I changed:** None significant. Confirmed that `deepcopy` (not a shallow copy or
reference) was used, which is critical for correctness.

**Issues found in AI output:**
- AI used `copy.copy()` (shallow) in the first draft. Corrected to `copy.deepcopy()`
  because `inventory_data` is a list of dicts — shallow copy would still share the inner
  dict objects, causing mutations to bleed through.

**Validation Hook Prompt used:**
```
After generating the code, add inline comments identifying: (1) whether a deep copy or
reference is used for the working inventory state, (2) what happens if two orders compete
for the same ingredient, and (3) any incomplete sections.
```

**Test generation prompt used:**
```
Write unit tests for cumulative deduction. Cover: two orders consuming the same ingredient
(verify combined deduction), an order that fails because a prior order consumed the
remaining stock, and final inventory state matching expected remaining quantities.
```

**What I accepted from tests:** All generated test cases after verifying the expected
flour quantity manually (10,000 − 300 − 250 = 9,450g for one pizza + one chocolate cake).

---

## Task 8 — Restock and Expiry Rules

**Goal:** Generate restock recommendations from final inventory using three priority rules.

**Prompt used (Template 3 — Implementation):**
```
Implement Task 5: Update the restock logic with these specific rules: 1. If an ingredient
is within 5 days of expiry (relative to today's date), mark it as 'Expiring soon' and set
the restock quantity to 10,000g. 2. If the final stock is 0, mark as 'Out of stock'
(10,000g needed). 3. If stock is ≤ 1,000g, mark as 'Running low on stock' and calculate
the needed amount to reach 10,000g. Add comments. Do not implement anything beyond this task.
```

**AI response summary:**
Generated `calculate_restock_needs()` with an if/elif/elif chain. Used `date.today()`
as the default reference date.

**What I accepted:** The rule structure and the `reference_date` parameter pattern.

**What I changed:**
- Added `reference_date=None` parameter and defaulted to `date.today()` only inside the
  function, so tests can always pass an explicit date and avoid time-sensitive failures.
- Wrapped expiry parsing in `datetime.strptime()` since seed data stores dates as strings.

**Issues found in AI output:**
- AI originally used `datetime.today()` instead of `date.today()`, which returned a
  `datetime` object that couldn't be directly subtracted from a `date` object parsed
  from the seed string. Fixed by using `date.today()` and `.date()` on the parsed value.
- The elif chain means an ingredient cannot be flagged for both expiry and low stock
  simultaneously. `additional_instructions.txt` Requirement 6 says to preserve all
  relevant reasons — this is a known open issue noted in PROJECT_SPEC.md.

**Validation Hook Prompt used:**
```
After generating the code, add inline comments identifying: (1) how today's date is
obtained — verify this is correct for the simulation, (2) whether an ingredient can be
flagged for both low stock and expiry simultaneously, and (3) any incomplete sections.
```

**Test generation prompt used:**
```
Write unit tests for the restock logic. Cover: an ingredient expiring within 5 days
(expect 'Expiring soon', 10,000g), an ingredient with 0 stock (expect 'Out of stock',
10,000g), an ingredient with 500g remaining (expect 'Running low', 9,500g needed), and
an ingredient with adequate stock and no expiry issue (expect not flagged).
```

**What I accepted from tests:** All four test cases.

---

## Duplication Check — After Tasks 3–8

**Refactoring Prompt used:**
```
Review the code in main.py for duplicated logic or functions — particularly any inventory
lookup, availability check, or restock flagging logic that appears more than once.
Suggest how to refactor it to eliminate duplication while keeping the behaviour identical.
Do not change any function signatures yet.
```

**AI response summary:**
Identified that inventory lookup (building a dict from the list) appeared in both
`check_inventory_availability()` and `deduct_inventory()`. Suggested extracting a shared
`_build_inventory_lookup()` helper. Also noted the `combine_requirements()` function was
only called from one place and could be inlined, but kept it separate for testability.

**What I accepted:** Noted the duplication; deferred refactoring to Task 10.
**What I rejected:** Inlining `combine_requirements()` — kept it separate for clarity.

---

## Task 9 — Business-Friendly Summary

**Goal:** Add a `print_business_summary()` function that outputs an end-of-day report
understandable to a non-technical kitchen manager.

**Prompt used (Template 3 — Implementation):**
```
Implement Task 9: Add a print_business_summary() function to main.py that takes
processed_orders, inventory_data, and restock_data as input and prints a clear,
human-readable summary. Include: total delivered vs not delivered, reasons for
non-delivery per order, final inventory levels, and restock recommendations with
reasons. Format the output so a non-technical kitchen manager can read it.
Do not modify any existing functions.
```

**AI response summary:**
Generated `print_business_summary()` with sections for order counts, unfulfilled order
reasons, final inventory snapshot, and restock recommendations. Used f-string column
alignment to make the inventory table readable. Added a "none" message when the restock
list is empty so the output is always complete.

**What I accepted:** Overall structure and column-aligned formatting for the inventory table.

**What I changed:**
- Added the separator line (`"=" * 54`) above and below the summary block to make it
  visually distinct from the detailed processing output printed above it.
- Changed the restock section to print "RESTOCK RECOMMENDATIONS: none" explicitly when
  the list is empty, so a manager reading the output can confirm the check ran.

**Issues found in AI output:**
- AI initially did not include unfulfilled order reasons in the summary section — it only
  printed counts. Added the "UNFULFILLED ORDERS" block to show order ID, brand, and
  specific reason per failed order so the manager knows what to act on.

**Test generation prompt used:**
```
Write unit tests for print_business_summary(). Cover: correct delivered and not-delivered
counts, unfulfilled orders listed with reasons, restock items shown with quantity and
reason, explicit "none" message when restock list is empty, and end-to-end run on full
seed data without error.
```

**What I accepted from tests:** All 5 generated test cases. Used `io.StringIO` and
`sys.stdout` redirection to capture printed output for assertion — confirmed this pattern
was correct before accepting it.

---

## Task 10 — Refactoring and Code Quality Review

**Goal:** Eliminate duplication, extract magic numbers as constants, and improve overall
code clarity.

**Prompt used (Refactoring):**
```
Review the code in main.py for duplicated logic or functions — particularly any inventory
lookup, availability check, or restock flagging logic that appears more than once. Also
identify any hard-coded values that should be named constants. Suggest refactoring
opportunities while keeping all function signatures and behaviour identical.
Do not change any function signatures yet.
```

**AI response summary:**
Identified two issues: (1) the inventory lookup dict-comprehension
`{item["ingredient"]: item for item in inventory_data}` appeared identically in both
`check_inventory_availability()` and `deduct_inventory()`; (2) the values `10000`, `1000`,
`5`, and `"%Y-%m-%d"` were scattered as magic numbers inside `calculate_restock_needs()`
with no explanation of their business meaning. AI suggested extracting a shared helper and
four module-level constants.

**Improvement 1 — Extracted `_build_inventory_lookup()` helper:**
The identical dict-comprehension was removed from both functions and replaced with a single
private helper. If the inventory schema key ever changes, there is now one place to fix.

**Improvement 2 — Replaced magic numbers with named constants:**
Four raw values were replaced with `PAR_LEVEL_GRAMS = 10_000`,
`LOW_STOCK_THRESHOLD_GRAMS = 1_000`, `EXPIRY_WINDOW_DAYS = 5`, and
`DATE_FORMAT = "%Y-%m-%d"` declared at the top of `main.py`. Changing a business rule
(e.g., raising the low-stock threshold) now requires editing one line instead of searching
the logic.

**What I accepted:** Both refactoring suggestions in full.

**What I rejected:** AI suggested inlining `combine_requirements()` since it is only called
from one place. Kept it as a separate function because it has its own clear responsibility
and is easier to test and read in isolation.

**What I changed:** Updated the module docstring from "Baseline entry point for loading and
printing cloud kitchen seed data" to accurately reflect the full scope of the file after
all tasks were implemented.

**Issues found:** None — all 25 existing tests passed without modification after the
refactoring, confirming the behaviour was preserved.

---

## Optional Enhancement A — Partial Fulfillment

**Enhancement chosen:** Option A — Partial Fulfillment

**Goal:** Modify order processing so that if only some items in an order can be fulfilled,
those items are delivered and marked separately rather than failing the entire order.

**Prompt used (Template 1 — Planning):**
```
I want to add partial fulfillment logic to the cloud kitchen simulation.
Before writing any code, give me a plan — what components need to change
and what should I build first?
```

**AI response summary:**
AI suggested modifying `process_orders()` in-place by adding a `partial_fulfillment=False`
parameter. Recommended evaluating each item independently, deducting immediately on success,
and introducing a "Partially Delivered" status when some items succeed and others fail.

**What I rejected:** Modifying `process_orders()` in-place. That function is covered by
existing tests and its all-or-nothing behaviour is correct for the base requirements. Adding
a boolean flag would make the function harder to follow and risk breaking passing tests.

**What I changed:** Implemented the enhancement as a standalone `process_orders_partial()`
function instead. This keeps the original behaviour fully intact, keeps the two modes
clearly separated, and allows each to be tested independently without conditional branching
inside a shared function.

**Prompt used (Template 3 — Implementation):**
```
Implement the partial fulfillment enhancement as a new standalone function
process_orders_partial() in main.py. For each order, evaluate each item independently.
Deliver and deduct stock for items that have sufficient ingredients. Skip items that do
not. Mark the order as 'Delivered' if all items fulfilled, 'Partially Delivered' if some
were fulfilled, and 'Not Delivered' if none were. Do not modify process_orders() or any
existing functions.
```

**AI response summary:**
Generated `process_orders_partial()` that loops per item, checks availability individually,
deducts immediately on success, and sets `fulfilled` and `partial` flags on the order
result. Reused `find_recipe_by_name()`, `calculate_ingredient_requirements()`,
`check_inventory_availability()`, `deduct_inventory()`, and `update_status_entry()` without
modification.

**What I accepted:** The overall structure and reuse of existing helper functions.

**What I changed:**
- AI's first draft checked all items then deducted all at once. Changed to deduct
  immediately after each item passes its availability check, so later items in the same
  order correctly see reduced stock left by earlier items rather than competing for the
  same grams simultaneously.
- Added the `partial` boolean field to the order result dict so tests and callers can
  distinguish "Partially Delivered" from "Delivered" without parsing the reason string.

**Issues found in AI output:**
- The simultaneous-check-then-deduct bug described above: two items sharing one ingredient
  could both pass the availability check before either deduction ran, effectively
  double-spending the same stock. Caught by the
  `test_per_item_deduction_prevents_double_spend_within_one_order` test.

**Test generation prompt used:**
```
Write unit tests for process_orders_partial(). Cover: all items available (fully
delivered), one item unavailable (partially delivered), no items available (not
delivered), stock deducted only for delivered items, missing recipe handled gracefully,
and two items sharing an ingredient deducting sequentially so the second sees reduced
stock.
```

**What I accepted from tests:** All 6 test cases. Verified the double-spend test manually
(400g Flour, Dish A uses 300g, Dish B needs 300g — only Dish A should succeed, leaving
100g) before accepting the assertion.
