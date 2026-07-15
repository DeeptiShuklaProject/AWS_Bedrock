# Episode 5 Summary: Input Variables and Schema Validation

Using input variables allows your configurations to be reusable and customizable across environments.

## Best Practices
- **Type Constraints:** Always specify `type = string`, `type = list`, or `type = map` to avoid runtime parsing issues.
- **Validations:** Add `validation` rules to restrict input values at the plan phase, avoiding failed deployments halfway through.
