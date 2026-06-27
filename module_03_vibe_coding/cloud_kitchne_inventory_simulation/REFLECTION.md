# Task 11 — Reflection on AI-Assisted Coding

## How did AI help you move faster?

The biggest time saver was the planning phase. When I asked AI to give me a high-level
plan before writing anything, it broke the problem into three clear layers: data loading,
order processing, and restock logic. That gave me a structure to follow rather than
figuring it out as I went.

On the code side, the repetitive parts went much faster. Writing five loader functions and
five print functions manually would have been tedious. I got all of them in one prompt and
spent my time reviewing rather than typing. The restock function was similar — I described
the three business rules in plain English and AI produced working Python with the date
parsing already handled.

## Where did AI make mistakes or questionable assumptions?

More often than I expected. The biggest issue was using `copy.copy()` instead of
`copy.deepcopy()` for the working inventory snapshot. A shallow copy of a list of dicts
still shares the inner dict objects, so deductions would have silently mutated the original
table mid-processing. I almost missed it because the code looked fine on the surface.

There was also a type mismatch where AI used `datetime.today()` instead of `date.today()`
in the restock function — subtracting a `datetime` from a parsed `date` throws a runtime
error. And when checking ingredient availability, AI checked each order item separately
instead of combining totals first, which could let an order pass incorrectly when two items
share one ingredient.

## How did testing help you evaluate AI-generated code?

Testing was what kept the project honest. Looking at code and thinking "that seems right"
is not the same as writing the expected value and making the program prove it.

The clearest example was the cumulative deduction test. I had to manually work out that
Flour should be at 9,450g after one Margherita Pizza and one Chocolate Cake. When I
asserted that and ran the test, it failed — the shallow copy was letting deductions show
up immediately in the source table. Without that specific number as an assertion, I would
never have caught the bug. Restock tests had the same effect: committing to exact values
forced me to verify the arithmetic rather than just read the logic and move on.

## What did you change or reject from AI suggestions?

I fixed the three bugs above. The more interesting rejections were design choices. AI
wanted to append missing items to the restock list inside the order processing loop, which
would have created duplicates and reflected in-progress state. I replaced it with a
function that rebuilds the restock table from final inventory after all orders complete.

For the partial fulfillment enhancement, AI suggested adding a `partial_fulfillment=False`
parameter to the existing `process_orders()` function. I said no — putting two behaviors
behind a flag makes both harder to test. A separate `process_orders_partial()` function is
cleaner and does not risk breaking tests that were already passing.

## How did PROJECT_SPEC.md help maintain context?

More than I expected. The spec forced me to write down decisions in plain language — things
like "recipe lookup uses exact case-sensitive matching" or "restock seed values are
discarded at runtime." Those feel obvious mid-session but are easy to forget later.

The payoff came when AI generated a case-insensitive recipe lookup in a follow-up prompt.
Because I had written the rule down, I caught the deviation immediately. I had also
documented that tests must always pass an explicit `reference_date`, which saved me from
a confusing intermittent test failure.

## What would you do differently next time?

Write the spec first. I started it partway through and had to backfill decisions already
made. If I had written it before the first prompt, every AI response would have had a fixed
standard to evaluate against from the start.

I would also test each function immediately after accepting it. Both the shallow copy bug
and the `datetime` error were caught because tests were written close in time to the code
that introduced them. Batching tests would have made those bugs much harder to trace.

And the simple one: verify your files can be imported before building on top of them. The
`seed_data-1.py` naming issue broke everything at the start and could have been caught with
one `python3 -c "import seed_data"` before writing any logic.
