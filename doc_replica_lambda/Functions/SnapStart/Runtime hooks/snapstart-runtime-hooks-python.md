

# Lambda SnapStart runtime hooks for Python
<a name="snapstart-runtime-hooks-python"></a>

You can use runtime hooks to implement code before Lambda creates a snapshot or after Lambda resumes a function from a snapshot. Python runtime hooks are available as part of the open-source [Snapshot Restore for Python library](https://pypi.org/project/snapshot-restore-py/), which is included in Python managed runtimes. This library provides two decorators that you can use to define your runtime hooks:
+ `@register_before_snapshot`: For functions you want to run before Lambda creates a snapshot.
+ `@register_after_restore`: For functions you want to run when Lambda resumes a function from a snapshot.

Alternatively, you can use the following methods to register callables for runtime hooks:
+ `register_before_snapshot(func, *args, **kwargs)`
+ `register_after_restore(func, *args, **kwargs)`

## Runtime hook registration and execution
<a name="runtime-hooks-registration-python"></a>

The order that Lambda executes your runtime hooks is determined by the order of registration:
+ Before snapshot: Executed in the reverse order of registration
+ After snapshot: Executed in the order of registration

The order of runtime hook registration depends on how you define the hooks. When using decorators (`@register_before_snapshot` and `@register_after_restore`), the registration order follows the order of import, definition, or execution in your code. If you need more control over the registration order, use the `register_before_snapshot()` and `register_after_restore()` methods instead of decorators.

Make sure that all registered hooks are properly imported and included in your function's code. If you register runtime hooks in a separate file or module, you must ensure that the module is imported, either directly or as part of a larger package, in your function's handler file. If the file or module is not imported in the function handler, Lambda ignores the runtime hooks.

**Note**  
When Lambda creates a snapshot, your initialization code can run for up to 15 minutes. The time limit is 130 seconds or the [configured function timeout](configuration-timeout.md) (maximum 900 seconds), whichever is higher. Your `@register_before_snapshot` runtime hooks count towards the initialization code time limit. When Lambda restores a snapshot, the runtime must load and `@register_after_restore` runtime hooks must complete within the timeout limit (10 seconds). Otherwise, you'll get a SnapStartTimeoutException.

## Example
<a name="runtime-hooks-python-code-sample"></a>

The following example handler shows how to run code before checkpointing (`@register_before_snapshot`) and after restoring (`@register_after_restore`).

```
from snapshot_restore_py import register_before_snapshot, register_after_restore

def lambda_handler(event, context):
    # Handler code

@register_before_snapshot
def before_checkpoint():
    # Logic to be executed before taking snapshots

@register_after_restore
def after_restore():
    # Logic to be executed after restore
```

For more examples, see [Snapshot Restore for Python](https://github.com/aws/snapshot-restore-py/tree/main/examples) in the AWS GitHub repository.