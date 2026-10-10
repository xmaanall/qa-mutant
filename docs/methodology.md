# Experimental Methodology

## Baseline

The original application must pass its full test suite before mutations are evaluated.

## Mutation run

Each mutation changes one targeted fragment of application logic. The same test suite is executed against the mutated copy.

- **Killed:** at least one test fails.
- **Survived:** all tests pass despite the mutation.
- **Invalid:** the mutation cannot be evaluated (reserved for future operators).

## Mutation score

`killed / (killed + survived) * 100`

## AI role

AI-assisted analysis is used to explain surviving mutations and propose targeted tests. Recommendations must be validated by execution and should not be treated as defects automatically.

## Stronger future experiment

For a rigorous evaluation, split mutants into a generation set and a hold-out set. Generate improvements using only the generation set, then evaluate whether the improved suite detects previously unseen mutations.
