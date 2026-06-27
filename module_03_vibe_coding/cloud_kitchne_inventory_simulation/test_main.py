"""Unit tests for the baseline seed-data loading functions."""

from copy import deepcopy
from datetime import date
import unittest

import io
import sys

from main import (
    calculate_ingredient_requirements,
    calculate_restock_needs,
    find_recipe_by_name,
    load_inventory,
    load_orders,
    load_recipes,
    load_restock,
    load_status,
    print_business_summary,
    process_orders,
    process_orders_partial,
)


class TestLoadFunctions(unittest.TestCase):
    """Verify the Task 1 data-loading helpers return the expected seed tables."""

    def test_loads_all_five_tables_successfully(self):
        """Each load function should return a non-empty list from seed_data."""
        # Assumption to verify: Task 1 considers a successful import equivalent to
        # each loader returning the seeded module-level list without raising errors.
        self.assertIsInstance(load_recipes(), list)
        self.assertIsInstance(load_inventory(), list)
        self.assertIsInstance(load_orders(), list)
        self.assertIsInstance(load_restock(), list)
        self.assertIsInstance(load_status(), list)

        self.assertGreater(len(load_recipes()), 0)
        self.assertGreater(len(load_inventory()), 0)
        self.assertGreater(len(load_orders()), 0)
        self.assertGreater(len(load_restock()), 0)
        self.assertGreater(len(load_status()), 0)

    def test_record_counts_match_seed_data(self):
        """Each load function should return the expected number of seed records."""
        self.assertEqual(len(load_recipes()), 5)
        self.assertEqual(len(load_inventory()), 14)
        self.assertEqual(len(load_orders()), 5)
        self.assertEqual(len(load_restock()), 5)
        self.assertEqual(len(load_status()), 5)

    def test_recipe_key_field_types(self):
        """Recipe records should expose the expected identifier and ingredient types."""
        recipe = load_recipes()[0]
        ingredient = recipe["ingredients"][0]

        self.assertIsInstance(recipe["recipe_id"], int)
        self.assertIsInstance(recipe["name"], str)
        self.assertIsInstance(recipe["ingredients"], list)
        self.assertIsInstance(ingredient["name"], str)
        self.assertIsInstance(ingredient["qty_grams"], (int, float))

    def test_inventory_key_field_types(self):
        """Inventory records should provide valid quantity and expiry field types."""
        item = load_inventory()[0]

        self.assertIsInstance(item["ingredient"], str)
        self.assertIsInstance(item["qty_grams"], (int, float))
        self.assertIsInstance(item["expiry_date"], str)

    def test_order_key_field_types(self):
        """Order records should expose valid identifiers, brands, and quantities."""
        order = load_orders()[0]
        item = order["items"][0]

        self.assertIsInstance(order["order_id"], int)
        self.assertIsInstance(order["brand"], str)
        self.assertIsInstance(order["items"], list)
        self.assertIsInstance(item["item"], str)
        self.assertIsInstance(item["qty"], int)

    def test_restock_key_field_types(self):
        """Restock records should provide an item name, numeric quantity, and reason."""
        item = load_restock()[0]

        self.assertIsInstance(item["item"], str)
        self.assertIsInstance(item["qty_needed_grams"], (int, float))
        self.assertIsInstance(item["reason"], str)

    def test_status_key_field_types(self):
        """Status records should provide order linkage and delivery state types."""
        item = load_status()[0]

        self.assertIsInstance(item["order_id"], int)
        self.assertIsInstance(item["delivered"], bool)
        self.assertIsInstance(item["remark"], str)
        # Incomplete / follow-up: if the project later formalizes a status enum or
        # richer state machine, these tests should be expanded beyond simple types.


class TestOrderRecipeLookup(unittest.TestCase):
    """Verify order items can be matched to recipes and scaled correctly."""

    def test_find_recipe_by_name_returns_matching_recipe(self):
        """A valid order item should return its matching recipe record."""
        recipe = find_recipe_by_name(load_recipes(), "Chicken Burger")

        self.assertIsNotNone(recipe)
        self.assertEqual(recipe["recipe_id"], 2)
        self.assertEqual(recipe["name"], "Chicken Burger")

    def test_find_recipe_by_name_handles_missing_recipe_gracefully(self):
        """A missing order item should return None instead of raising an error."""
        recipe = find_recipe_by_name(load_recipes(), "Paneer Wrap")

        self.assertIsNone(recipe)

    def test_calculate_ingredient_requirements_scales_for_quantity_two(self):
        """Ingredient requirements should double when the order quantity is two."""
        recipe = find_recipe_by_name(load_recipes(), "Margherita Pizza")
        requirements = calculate_ingredient_requirements(recipe, 2)

        expected_requirements = [
            {"name": "Flour", "required_qty_grams": 600},
            {"name": "Tomato Sauce", "required_qty_grams": 200},
            {"name": "Mozzarella Cheese", "required_qty_grams": 300},
        ]

        self.assertEqual(requirements, expected_requirements)


class TestOrderFulfillment(unittest.TestCase):
    """Verify fulfillment updates status, restock, and inventory correctly."""

    def test_process_orders_marks_delivered_when_ingredients_are_available(self):
        """An order with sufficient stock should be marked as delivered."""
        recipe_data = deepcopy(load_recipes())
        inventory_data = deepcopy(load_inventory())
        status_data = deepcopy(load_status())
        restock_data = deepcopy(load_restock())
        order_data = [
            {
                "order_id": 101,
                "brand": "Test Kitchen",
                "items": [{"item": "Chicken Burger", "qty": 1}],
            }
        ]

        processed_orders = process_orders(
            recipe_data, inventory_data, order_data, status_data, restock_data
        )

        self.assertTrue(processed_orders[0]["fulfilled"])
        self.assertEqual(processed_orders[0]["reason"], "Delivered")
        self.assertEqual(status_data[-1]["order_id"], 101)
        self.assertTrue(status_data[-1]["delivered"])
        self.assertEqual(status_data[-1]["remark"], "Delivered")

    def test_process_orders_marks_not_delivered_and_adds_missing_item_to_restock(self):
        """An order with a missing ingredient should fail and log the shortage."""
        recipe_data = [
            {
                "recipe_id": 1,
                "name": "Test Wrap",
                "ingredients": [
                    {"name": "Chicken Breast", "qty_grams": 200},
                    {"name": "Bun", "qty_grams": 100},
                ],
            }
        ]
        inventory_data = [
            {"ingredient": "Chicken Breast", "qty_grams": 500, "expiry_date": "2026-12-31"},
            {"ingredient": "Bun", "qty_grams": 0, "expiry_date": "2026-12-31"},
        ]
        order_data = [
            {"order_id": 202, "brand": "Test Kitchen", "items": [{"item": "Test Wrap", "qty": 1}]}
        ]
        status_data = []
        restock_data = []

        processed_orders = process_orders(
            recipe_data,
            inventory_data,
            order_data,
            status_data,
            restock_data,
            reference_date=date(2026, 6, 3),
        )

        self.assertFalse(processed_orders[0]["fulfilled"])
        self.assertIn("Missing or insufficient ingredients: Bun", processed_orders[0]["reason"])
        self.assertEqual(status_data[0]["order_id"], 202)
        self.assertFalse(status_data[0]["delivered"])
        self.assertIn("Bun", status_data[0]["remark"])
        bun_restock = next(item for item in restock_data if item["item"] == "Bun")
        self.assertEqual(bun_restock["qty_needed_grams"], 10000)
        self.assertEqual(bun_restock["reason"], "Out of stock")

    def test_process_orders_deducts_inventory_after_successful_delivery(self):
        """A delivered order should reduce inventory by the required grams."""
        recipe_data = deepcopy(load_recipes())
        inventory_data = deepcopy(load_inventory())
        status_data = []
        restock_data = []
        order_data = [
            {
                "order_id": 303,
                "brand": "Test Kitchen",
                "items": [{"item": "Margherita Pizza", "qty": 2}],
            }
        ]

        original_flour_qty = next(
            item["qty_grams"] for item in inventory_data if item["ingredient"] == "Flour"
        )
        original_sauce_qty = next(
            item["qty_grams"] for item in inventory_data if item["ingredient"] == "Tomato Sauce"
        )
        original_cheese_qty = next(
            item["qty_grams"] for item in inventory_data if item["ingredient"] == "Mozzarella Cheese"
        )

        process_orders(recipe_data, inventory_data, order_data, status_data, restock_data)

        updated_flour_qty = next(
            item["qty_grams"] for item in inventory_data if item["ingredient"] == "Flour"
        )
        updated_sauce_qty = next(
            item["qty_grams"] for item in inventory_data if item["ingredient"] == "Tomato Sauce"
        )
        updated_cheese_qty = next(
            item["qty_grams"] for item in inventory_data if item["ingredient"] == "Mozzarella Cheese"
        )

        self.assertEqual(updated_flour_qty, original_flour_qty - 600)
        self.assertEqual(updated_sauce_qty, original_sauce_qty - 200)
        self.assertEqual(updated_cheese_qty, original_cheese_qty - 300)


class TestCumulativeInventoryDeduction(unittest.TestCase):
    """Verify inventory is consumed cumulatively across sequential orders."""

    def test_two_orders_consuming_same_ingredient_use_combined_deduction(self):
        """Two delivered orders should deduct the combined shared ingredient total."""
        recipe_data = deepcopy(load_recipes())
        inventory_data = deepcopy(load_inventory())
        status_data = []
        restock_data = []
        order_data = [
            {"order_id": 401, "brand": "Test Kitchen", "items": [{"item": "Margherita Pizza", "qty": 1}]},
            {"order_id": 402, "brand": "Test Kitchen", "items": [{"item": "Chocolate Cake", "qty": 1}]},
        ]

        original_flour_qty = next(
            item["qty_grams"] for item in inventory_data if item["ingredient"] == "Flour"
        )

        processed_orders = process_orders(
            recipe_data, inventory_data, order_data, status_data, restock_data
        )

        updated_flour_qty = next(
            item["qty_grams"] for item in inventory_data if item["ingredient"] == "Flour"
        )

        self.assertTrue(processed_orders[0]["fulfilled"])
        self.assertTrue(processed_orders[1]["fulfilled"])
        self.assertEqual(updated_flour_qty, original_flour_qty - 550)

    def test_later_order_fails_after_prior_order_consumes_remaining_stock(self):
        """A later order should fail if an earlier order uses the remaining shared stock."""
        recipe_data = [
            {
                "recipe_id": 1,
                "name": "First Dish",
                "ingredients": [{"name": "Cheese", "qty_grams": 600}],
            },
            {
                "recipe_id": 2,
                "name": "Second Dish",
                "ingredients": [{"name": "Cheese", "qty_grams": 500}],
            },
        ]
        inventory_data = [
            {"ingredient": "Cheese", "qty_grams": 1000, "expiry_date": "2026-12-31"}
        ]
        order_data = [
            {"order_id": 501, "brand": "Test Kitchen", "items": [{"item": "First Dish", "qty": 1}]},
            {"order_id": 502, "brand": "Test Kitchen", "items": [{"item": "Second Dish", "qty": 1}]},
        ]
        status_data = []
        restock_data = []

        processed_orders = process_orders(
            recipe_data,
            inventory_data,
            order_data,
            status_data,
            restock_data,
            reference_date=date(2026, 6, 3),
        )

        self.assertTrue(processed_orders[0]["fulfilled"])
        self.assertFalse(processed_orders[1]["fulfilled"])
        self.assertIn("Cheese", processed_orders[1]["reason"])
        self.assertEqual(status_data[1]["order_id"], 502)
        self.assertFalse(status_data[1]["delivered"])
        self.assertEqual(restock_data[0]["item"], "Cheese")
        self.assertEqual(restock_data[0]["qty_needed_grams"], 9600)
        self.assertEqual(restock_data[0]["reason"], "Running low on stock")

    def test_final_inventory_matches_expected_remaining_quantities(self):
        """Final inventory should reflect all successful cumulative deductions."""
        recipe_data = deepcopy(load_recipes())
        inventory_data = deepcopy(load_inventory())
        status_data = []
        restock_data = []
        order_data = [
            {"order_id": 601, "brand": "Test Kitchen", "items": [{"item": "Margherita Pizza", "qty": 2}]},
            {"order_id": 602, "brand": "Test Kitchen", "items": [{"item": "Chocolate Cake", "qty": 1}]},
        ]

        process_orders(recipe_data, inventory_data, order_data, status_data, restock_data)

        flour_qty = next(item["qty_grams"] for item in inventory_data if item["ingredient"] == "Flour")
        sauce_qty = next(
            item["qty_grams"] for item in inventory_data if item["ingredient"] == "Tomato Sauce"
        )
        cheese_qty = next(
            item["qty_grams"] for item in inventory_data if item["ingredient"] == "Mozzarella Cheese"
        )
        chocolate_qty = next(
            item["qty_grams"] for item in inventory_data if item["ingredient"] == "Chocolate"
        )
        sugar_qty = next(item["qty_grams"] for item in inventory_data if item["ingredient"] == "Sugar")

        self.assertEqual(flour_qty, 9150)
        self.assertEqual(sauce_qty, 9800)
        self.assertEqual(cheese_qty, 9700)
        self.assertEqual(chocolate_qty, 9850)
        self.assertEqual(sugar_qty, 9900)


class TestRestockRules(unittest.TestCase):
    """Verify the Task 5 rule-based restock calculations."""

    def test_expiring_soon_sets_full_restock_quantity(self):
        """Ingredients expiring within 5 days should be marked as expiring soon."""
        inventory_data = [
            {"ingredient": "Cream", "qty_grams": 7000, "expiry_date": "2026-06-06"}
        ]

        restock_data = calculate_restock_needs(inventory_data, reference_date=date(2026, 6, 3))

        self.assertEqual(
            restock_data,
            [{"item": "Cream", "qty_needed_grams": 10000, "reason": "Expiring soon"}],
        )

    def test_out_of_stock_sets_full_restock_quantity(self):
        """Zero final stock should be marked as out of stock with 10,000 grams needed."""
        inventory_data = [
            {"ingredient": "Bun", "qty_grams": 0, "expiry_date": "2026-12-31"}
        ]

        restock_data = calculate_restock_needs(inventory_data, reference_date=date(2026, 6, 3))

        self.assertEqual(
            restock_data,
            [{"item": "Bun", "qty_needed_grams": 10000, "reason": "Out of stock"}],
        )

    def test_running_low_calculates_amount_needed_to_reach_ten_thousand(self):
        """Low stock should request only the amount needed to reach 10,000 grams."""
        inventory_data = [
            {"ingredient": "Chicken Breast", "qty_grams": 500, "expiry_date": "2026-12-31"}
        ]

        restock_data = calculate_restock_needs(inventory_data, reference_date=date(2026, 6, 3))

        self.assertEqual(
            restock_data,
            [
                {
                    "item": "Chicken Breast",
                    "qty_needed_grams": 9500,
                    "reason": "Running low on stock",
                }
            ],
        )

    def test_adequate_stock_without_expiry_issue_is_not_flagged(self):
        """Adequate stock with no near-expiry condition should not appear in restock."""
        inventory_data = [
            {"ingredient": "Tomato Sauce", "qty_grams": 7000, "expiry_date": "2026-12-31"}
        ]

        restock_data = calculate_restock_needs(inventory_data, reference_date=date(2026, 6, 3))

        self.assertEqual(restock_data, [])


class TestBusinessSummary(unittest.TestCase):
    """Verify the end-of-day business summary output."""

    def _run_summary(self, processed_orders, inventory_data, restock_data):
        """Capture stdout from print_business_summary and return it as a string."""
        captured = io.StringIO()
        sys.stdout = captured
        try:
            print_business_summary(processed_orders, inventory_data, restock_data)
        finally:
            sys.stdout = sys.__stdout__
        return captured.getvalue()

    def test_summary_shows_correct_delivered_and_not_delivered_counts(self):
        """Summary should reflect the actual number of delivered and failed orders."""
        processed_orders = [
            {"order_id": 1, "brand": "A", "fulfilled": True, "reason": "Delivered"},
            {"order_id": 2, "brand": "B", "fulfilled": False, "reason": "Missing: Bun"},
            {"order_id": 3, "brand": "A", "fulfilled": True, "reason": "Delivered"},
        ]
        inventory_data = [
            {"ingredient": "Flour", "qty_grams": 9400, "expiry_date": "2026-12-31"}
        ]
        restock_data = []

        output = self._run_summary(processed_orders, inventory_data, restock_data)

        self.assertIn("Delivered:       2", output)
        self.assertIn("Not Delivered:   1", output)

    def test_summary_lists_unfulfilled_orders_with_reasons(self):
        """Summary should include the order ID, brand, and reason for each failed order."""
        processed_orders = [
            {"order_id": 7, "brand": "Subway", "fulfilled": False,
             "reason": "Missing or insufficient ingredients: Chicken Breast"},
        ]
        inventory_data = [
            {"ingredient": "Chicken Breast", "qty_grams": 0, "expiry_date": "2026-12-31"}
        ]
        restock_data = [
            {"item": "Chicken Breast", "qty_needed_grams": 10000, "reason": "Out of stock"}
        ]

        output = self._run_summary(processed_orders, inventory_data, restock_data)

        self.assertIn("Order #7", output)
        self.assertIn("Subway", output)
        self.assertIn("Chicken Breast", output)

    def test_summary_shows_restock_recommendations(self):
        """Summary should list each restock item with quantity and reason."""
        processed_orders = [
            {"order_id": 1, "brand": "A", "fulfilled": True, "reason": "Delivered"}
        ]
        inventory_data = [
            {"ingredient": "Bun", "qty_grams": 0, "expiry_date": "2026-12-31"}
        ]
        restock_data = [
            {"item": "Bun", "qty_needed_grams": 10000, "reason": "Out of stock"}
        ]

        output = self._run_summary(processed_orders, inventory_data, restock_data)

        self.assertIn("Bun", output)
        self.assertIn("10000", output)
        self.assertIn("Out of stock", output)

    def test_summary_shows_none_message_when_no_restock_needed(self):
        """Summary should clearly state no restock is needed when restock list is empty."""
        processed_orders = [
            {"order_id": 1, "brand": "A", "fulfilled": True, "reason": "Delivered"}
        ]
        inventory_data = [
            {"ingredient": "Flour", "qty_grams": 9000, "expiry_date": "2026-12-31"}
        ]
        restock_data = []

        output = self._run_summary(processed_orders, inventory_data, restock_data)

        self.assertIn("none", output)

    def test_summary_runs_on_full_seed_data_without_error(self):
        """Summary should run end-to-end on real seed data without raising an exception."""
        recipe_data = load_recipes()
        inventory_data = deepcopy(load_inventory())
        order_data = load_orders()
        restock_data = []
        status_data = deepcopy(load_status())

        processed_orders = process_orders(
            recipe_data, inventory_data, order_data, status_data, restock_data
        )

        try:
            captured = io.StringIO()
            sys.stdout = captured
            print_business_summary(processed_orders, inventory_data, restock_data)
        finally:
            sys.stdout = sys.__stdout__

        output = captured.getvalue()
        self.assertIn("CLOUD KITCHEN", output)
        self.assertIn("ORDERS PROCESSED", output)
        self.assertIn("FINAL INVENTORY", output)
        self.assertIn("RESTOCK RECOMMENDATIONS", output)


class TestPartialFulfillment(unittest.TestCase):
    """Verify Option A: per-item partial fulfillment logic."""

    # Shared recipe and inventory fixtures used across multiple tests.
    RECIPES = [
        {
            "recipe_id": 1,
            "name": "Dish A",
            "ingredients": [{"name": "Tomato", "qty_grams": 200}],
        },
        {
            "recipe_id": 2,
            "name": "Dish B",
            "ingredients": [{"name": "Cheese", "qty_grams": 300}],
        },
    ]

    def _make_inventory(self, tomato=500, cheese=500):
        return [
            {"ingredient": "Tomato", "qty_grams": tomato, "expiry_date": "2026-12-31"},
            {"ingredient": "Cheese", "qty_grams": cheese, "expiry_date": "2026-12-31"},
        ]

    def test_all_items_available_marks_order_fully_delivered(self):
        """An order whose every item has sufficient stock should be fully delivered."""
        order_data = [
            {"order_id": 1, "brand": "X", "items": [
                {"item": "Dish A", "qty": 1},
                {"item": "Dish B", "qty": 1},
            ]}
        ]
        inventory_data = self._make_inventory(tomato=500, cheese=500)
        result = process_orders_partial(
            self.RECIPES, inventory_data, order_data, [], [],
            reference_date=date(2026, 6, 3),
        )

        self.assertTrue(result[0]["fulfilled"])
        self.assertFalse(result[0]["partial"])
        self.assertEqual(result[0]["reason"], "Delivered")

    def test_one_item_unavailable_marks_order_partially_delivered(self):
        """If one item lacks stock and another is available, the order is partial."""
        order_data = [
            {"order_id": 2, "brand": "X", "items": [
                {"item": "Dish A", "qty": 1},   # Tomato available
                {"item": "Dish B", "qty": 1},   # Cheese out of stock
            ]}
        ]
        inventory_data = self._make_inventory(tomato=500, cheese=0)
        result = process_orders_partial(
            self.RECIPES, inventory_data, order_data, [], [],
            reference_date=date(2026, 6, 3),
        )

        self.assertTrue(result[0]["fulfilled"])
        self.assertTrue(result[0]["partial"])
        self.assertIn("Partially delivered", result[0]["reason"])
        self.assertIn("Dish B", result[0]["reason"])

    def test_no_items_available_marks_order_not_delivered(self):
        """An order with no deliverable items should be marked as not delivered."""
        order_data = [
            {"order_id": 3, "brand": "X", "items": [
                {"item": "Dish A", "qty": 1},
                {"item": "Dish B", "qty": 1},
            ]}
        ]
        inventory_data = self._make_inventory(tomato=0, cheese=0)
        result = process_orders_partial(
            self.RECIPES, inventory_data, order_data, [], [],
            reference_date=date(2026, 6, 3),
        )

        self.assertFalse(result[0]["fulfilled"])
        self.assertFalse(result[0]["partial"])
        self.assertIn("Not delivered", result[0]["reason"])

    def test_delivered_items_deducted_failed_items_not_deducted(self):
        """Stock is deducted for delivered items only; failed items leave stock unchanged."""
        order_data = [
            {"order_id": 4, "brand": "X", "items": [
                {"item": "Dish A", "qty": 1},   # Tomato: should be deducted
                {"item": "Dish B", "qty": 1},   # Cheese: out of stock, no deduction
            ]}
        ]
        inventory_data = self._make_inventory(tomato=500, cheese=0)
        process_orders_partial(
            self.RECIPES, inventory_data, order_data, [], [],
            reference_date=date(2026, 6, 3),
        )

        tomato_qty = next(
            i["qty_grams"] for i in inventory_data if i["ingredient"] == "Tomato"
        )
        cheese_qty = next(
            i["qty_grams"] for i in inventory_data if i["ingredient"] == "Cheese"
        )
        self.assertEqual(tomato_qty, 300)   # 500 - 200 = 300
        self.assertEqual(cheese_qty, 0)     # unchanged

    def test_missing_recipe_item_treated_as_failed_without_crashing(self):
        """An item with no recipe should be recorded as failed; other items still process."""
        order_data = [
            {"order_id": 5, "brand": "X", "items": [
                {"item": "Dish A", "qty": 1},        # valid
                {"item": "Unknown Dish", "qty": 1},  # no recipe
            ]}
        ]
        inventory_data = self._make_inventory(tomato=500, cheese=500)
        result = process_orders_partial(
            self.RECIPES, inventory_data, order_data, [], [],
            reference_date=date(2026, 6, 3),
        )

        self.assertTrue(result[0]["partial"])
        item_results = {i["item"]: i for i in result[0]["items"]}
        self.assertTrue(item_results["Dish A"]["delivered"])
        self.assertFalse(item_results["Unknown Dish"]["delivered"])
        self.assertFalse(item_results["Unknown Dish"]["recipe_found"])

    def test_per_item_deduction_prevents_double_spend_within_one_order(self):
        """Two items sharing an ingredient both deduct from the same pool in sequence."""
        recipes = [
            {"recipe_id": 1, "name": "Dish A", "ingredients": [{"name": "Flour", "qty_grams": 300}]},
            {"recipe_id": 2, "name": "Dish B", "ingredients": [{"name": "Flour", "qty_grams": 300}]},
        ]
        inventory_data = [
            {"ingredient": "Flour", "qty_grams": 400, "expiry_date": "2026-12-31"}
        ]
        order_data = [
            {"order_id": 6, "brand": "X", "items": [
                {"item": "Dish A", "qty": 1},  # uses 300g — leaves 100g
                {"item": "Dish B", "qty": 1},  # needs 300g — only 100g left, should fail
            ]}
        ]
        result = process_orders_partial(
            recipes, inventory_data, order_data, [], [],
            reference_date=date(2026, 6, 3),
        )

        self.assertTrue(result[0]["partial"])
        item_results = {i["item"]: i for i in result[0]["items"]}
        self.assertTrue(item_results["Dish A"]["delivered"])
        self.assertFalse(item_results["Dish B"]["delivered"])
        flour_qty = next(i["qty_grams"] for i in inventory_data if i["ingredient"] == "Flour")
        self.assertEqual(flour_qty, 100)   # only Dish A's 300g was deducted


if __name__ == "__main__":
    unittest.main()
