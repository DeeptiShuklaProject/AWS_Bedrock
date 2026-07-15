

# Implement code before or after Lambda function snapshots
<a name="snapstart-runtime-hooks"></a>

You can use runtime hooks to implement code before Lambda creates a snapshot or after Lambda resumes a function from a snapshot. Runtime hooks are useful for a variety of purposes, such as:
+ **Cleanup and initialization:** Before a snapshot is created, you can use a runtime hook to perform cleanup or resource release operations. After a snapshot is restored, you can use a runtime hook to re-initialize any resources or state that were not captured in the snapshot.
+ **Dynamic configuration:** You can use runtime hooks to dynamically update configuration or other metadata before a snapshot is created or after it is restored. This can be useful if your function needs to adapt to changes in the runtime environment.
+ **External integrations:** You can use runtime hooks to integrate with external services or systems, such as sending notifications or updating external state, as part of the checkpointing and restoration process.
+ **Performance tuning:** You can use runtime hooks to fine-tune your function's startup sequence, such as by preloading dependencies. For more information, see [Performance tuning](snapstart-best-practices.md#snapstart-tuning).

The following pages explain how to implement runtime hooks for your preferred runtime.

**Topics**
+ [Java](snapstart-runtime-hooks-java.md)
+ [Python](snapstart-runtime-hooks-python.md)
+ [.NET](snapstart-runtime-hooks-dotnet.md)