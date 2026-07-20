import os
import re
import json

base_dir = r"c:\Users\nishu\workspace\wscs_bedrock\doc_replica_product_developer"

# High-precision Quiz database (12 quizzes per category across 13 tech domains = 156 quizzes)
CATEGORIES = {
    "python": [
        {
            "question": "Which of the following statements about Python's dynamic typing is correct?",
            "options": [
                "Variables are bound to a specific data type at compilation.",
                "Variable names are references to objects, and types are resolved at runtime.",
                "A variable cannot change its type once initialized.",
                "Dynamic typing requires explicit casting before variable reassignment."
            ],
            "answerIndex": 1,
            "explanation": "In Python, variables are names that reference objects. The type is associated with the object itself, not the variable name, allowing dynamic reassignment at runtime."
        },
        {
            "question": "What is the primary difference between a list and a tuple in Python?",
            "options": [
                "Lists are immutable, while tuples are mutable.",
                "Lists use parenthesis, while tuples use square brackets.",
                "Lists are mutable, while tuples are immutable.",
                "Tuples support more built-in methods than lists."
            ],
            "answerIndex": 2,
            "explanation": "Lists are mutable and can be modified after creation. Tuples are immutable, making them hashable and useful as dictionary keys."
        },
        {
            "question": "Which list comprehension correctly filters even numbers from a list `nums`?",
            "options": [
                "[x if x % 2 == 0 for x in nums]",
                "[x for x in nums if x % 2 == 0]",
                "[x for x in nums while x % 2 == 0]",
                "[x filter x % 2 == 0 for x in nums]"
            ],
            "answerIndex": 1,
            "explanation": "The standard list comprehension syntax with an 'if' filter places the condition at the end: `[expression for item in iterable if condition]`."
        },
        {
            "question": "What does the `yield` keyword accomplish in a Python function?",
            "options": [
                "It terminates the function and returns a list.",
                "It pauses execution, returns a value, and saves state to create a generator.",
                "It forces the compiler to run the function in a background thread.",
                "It raises an exception to halt execution."
            ],
            "answerIndex": 1,
            "explanation": "`yield` turns a standard function into a generator. It yields values lazily one at a time, pausing execution state between calls to save memory."
        },
        {
            "question": "How is a Python decorator structurally implemented?",
            "options": [
                "As a class that inherits from a thread handler.",
                "As a function that takes another function as an argument and returns a wrapped replacement function.",
                "As a built-in compiler macro written in C.",
                "As a system-level process interrupt."
            ],
            "answerIndex": 1,
            "explanation": "Decorators are higher-order functions that accept a function as an argument, define an inner wrapper function to add behavior, and return that wrapper."
        },
        {
            "question": "What is the main benefit of using a context manager (`with` statement) in Python?",
            "options": [
                "It improves computation speed by running code in parallel.",
                "It guarantees proper cleanup and release of resources (e.g. closing files) even if errors occur.",
                "It automatically converts code into machine language.",
                "It registers the block within global shared variables."
            ],
            "answerIndex": 1,
            "explanation": "Context managers implement the `__enter__` and `__exit__` methods to guarantee resource cleanup, preventing memory leaks and locked files."
        },
        {
            "question": "What is the Global Interpreter Lock (GIL) in CPython?",
            "options": [
                "A compiler feature that prevents variable reassignment.",
                "A mutex that protects access to Python objects, preventing multiple native threads from executing Python bytecodes at once.",
                "A database locking mechanism for handling concurrent transactions.",
                "A sandbox security feature that restricts file system access."
            ],
            "answerIndex": 1,
            "explanation": "The GIL is a mechanism in CPython (the standard Python interpreter) that ensures only one thread executes Python bytecode at any given time, limiting CPU-bound multithreading."
        },
        {
            "question": "In Python function signatures, what are `*args` and `**kwargs` used for?",
            "options": [
                "To enforce strict type checking for variables.",
                "To accept an arbitrary number of positional arguments (as a tuple) and keyword arguments (as a dict) respectively.",
                "To declare global variables within local scope.",
                "To compile functions into C-compatible interfaces."
            ],
            "answerIndex": 1,
            "explanation": "`*args` collects extra positional arguments into a tuple, while `**kwargs` collects extra keyword arguments into a dictionary."
        },
        {
            "question": "What is a requirement for an object to be used as a key in a Python dictionary?",
            "options": [
                "It must be a mutable sequence.",
                "It must be hashable, meaning its hash value never changes during its lifetime and it can be compared to other objects.",
                "It must inherit from the DictKey class.",
                "It must be a numeric type."
            ],
            "answerIndex": 1,
            "explanation": "Dictionary keys must be hashable. Immutable types like strings, numbers, and tuples are hashable by default, whereas mutable objects like lists and dicts are not."
        },
        {
            "question": "Which of the following describes a Python lambda function?",
            "options": [
                "A function that runs recursively by default.",
                "An anonymous, single-expression function defined using the `lambda` keyword.",
                "A background process that manages memory allocation.",
                "A decorator class for logging execution times."
            ],
            "answerIndex": 1,
            "explanation": "Lambdas are anonymous, inline functions containing a single expression whose result is returned directly: `lambda arguments: expression`."
        },
        {
            "question": "What is the difference between the `is` operator and the `==` operator in Python?",
            "options": [
                "`is` compares values, while `==` compares data types.",
                "`is` checks identity (same memory address), while `==` checks equality (same value).",
                "`is` is used for strings, while `==` is used for numbers.",
                "There is no difference; they are completely interchangeable."
            ],
            "answerIndex": 1,
            "explanation": "`is` checks if two variables point to the exact same object in memory, while `==` compares the underlying values of the objects."
        },
        {
            "question": "How does `asyncio` achieve concurrency in Python?",
            "options": [
                "By starting new OS processes in parallel.",
                "Using cooperative multitasking on a single thread managed by an Event Loop.",
                "By compiling the code to multithreaded native binaries.",
                "Through hardware interrupts on multi-core processors."
            ],
            "answerIndex": 1,
            "explanation": "`asyncio` uses cooperative multitasking via coroutines and an Event Loop, allowing a single thread to context-switch when waiting for I/O operations."
        }
    ],
    "java": [
        {
            "question": "How does Java achieve platform independence?",
            "options": [
                "By compiling code directly to raw hardware machine instructions.",
                "By compiling source code to bytecode, which is then executed by the Java Virtual Machine (JVM).",
                "By dynamically translating Java into Javascript at runtime.",
                "By executing code directly from raw `.java` text files."
            ],
            "answerIndex": 1,
            "explanation": "Java code is compiled into platform-neutral bytecode (`.class` files), which the JVM translates into machine instructions for the host platform."
        },
        {
            "question": "In the JVM memory model, where are objects allocated and where are local variables stored?",
            "options": [
                "Objects on the Stack, local variables on the Heap.",
                "Objects and local variables are both stored on the Stack.",
                "Objects on the Heap, local variables on the Stack.",
                "Objects and local variables are both stored on the Heap."
            ],
            "answerIndex": 2,
            "explanation": "The Heap memory area is used for dynamic allocation of objects, while the Stack contains method frames storing local variables and reference pointers."
        },
        {
            "question": "What is the primary role of the Java Garbage Collector (GC)?",
            "options": [
                "To optimize SQL queries in databases.",
                "To automatically reclaim memory by deleting objects that are no longer reachable in the application code.",
                "To compile Java files into JAR archives.",
                "To monitor system file permissions."
            ],
            "answerIndex": 1,
            "explanation": "The JVM Garbage Collector manages memory by automatically tracking object reachability and freeing up Heap space occupied by unreachable objects."
        },
        {
            "question": "Which access modifier in Java restricts visibility strictly to the declaring class itself?",
            "options": ["public", "protected", "private", "default (no modifier)"],
            "answerIndex": 2,
            "explanation": "The `private` access modifier limits access exclusively to fields, methods, or constructors within the class where they are declared."
        },
        {
            "question": "What is a major difference between an interface and an abstract class in Java?",
            "options": [
                "Interfaces can hold instance fields, abstract classes cannot.",
                "A class can implement multiple interfaces, but can extend only one abstract class.",
                "Interfaces must contain method bodies, abstract classes cannot.",
                "Abstract classes cannot declare constructors."
            ],
            "answerIndex": 1,
            "explanation": "Java supports single class inheritance (only one abstract class can be extended) but multiple interface implementation."
        },
        {
            "question": "What does the `@RestController` annotation do in a Spring Boot application?",
            "options": [
                "It registers the class as a database access repository.",
                "It combines `@Controller` and `@ResponseBody`, serializing return values (like objects) directly into HTTP responses (typically JSON).",
                "It launches a background compilation process.",
                "It maps a class to a container load balancer."
            ],
            "answerIndex": 1,
            "explanation": "`@RestController` simplifies REST API creation. It tells Spring Boot that handlers return serialized data objects rather than routing to HTML templates."
        },
        {
            "question": "In Spring Boot, how does the `@Autowired` annotation facilitate dependency injection?",
            "options": [
                "It automatically compiles dependencies on startup.",
                "It allows the Spring context to automatically resolve and inject matching bean dependencies into fields, constructors, or setters.",
                "It downloads external dependencies from Maven Central.",
                "It starts a new server thread for bean instances."
            ],
            "answerIndex": 1,
            "explanation": "`@Autowired` directs Spring Boot's dependency injection container to automatically wire matching bean components into the decorated construct."
        },
        {
            "question": "What is the key difference between Checked and Unchecked exceptions in Java?",
            "options": [
                "Checked exceptions occur at runtime, unchecked exceptions occur at compile time.",
                "Checked exceptions must be declared in throws or caught; unchecked exceptions (RuntimeException) do not require compile-time handling.",
                "Unchecked exceptions can never be caught in code.",
                "Checked exceptions consume more CPU cycles to process."
            ],
            "answerIndex": 1,
            "explanation": "Checked exceptions are verified at compile time. Unchecked exceptions extend `RuntimeException` and represent programming bugs (like NullPointerException) that are resolved at runtime."
        },
        {
            "question": "How does a Java `HashMap` resolve collision when two keys have the same hash code?",
            "options": [
                "It overwrites the old key-value pair immediately.",
                "It throws a RuntimeException.",
                "It stores colliding nodes in a linked list (or red-black tree) associated with that hash bucket.",
                "It resizes the map dynamically to double its size."
            ],
            "answerIndex": 2,
            "explanation": "HashMap uses chaining. Colliding entries are placed in a linked list at the bucket index. If the bucket exceeds a threshold (8), Java 8+ converts it to a red-black tree."
        },
        {
            "question": "What are the states that a Java Thread can enter during its lifecycle?",
            "options": [
                "Active, Inactive, Completed.",
                "NEW, RUNNABLE, BLOCKED, WAITING, TIMED_WAITING, TERMINATED.",
                "Starting, Working, Finished.",
                "Local, Global, Shared."
            ],
            "answerIndex": 1,
            "explanation": "Java threads follow a strict state diagram represented by the `Thread.State` enum: NEW, RUNNABLE, BLOCKED, WAITING, TIMED_WAITING, and TERMINATED."
        },
        {
            "question": "What is the difference between method overloading and method overriding in Java?",
            "options": [
                "Overloading is done in subclassing, overriding is done within the same class.",
                "Overloading is determined at compile-time (same method name, different signatures), overriding at runtime (replaces parent method in subclass).",
                "Overloading changes return type only, overriding changes parameters.",
                "There is no difference; they are synonymous."
            ],
            "answerIndex": 1,
            "explanation": "Method overloading is compile-time polymorphism (same name, different arguments). Method overriding is run-time polymorphism (subclass overrides parent method with identical signature)."
        },
        {
            "question": "What does the `synchronized` keyword enforce in Java?",
            "options": [
                "It forces compilation to run synchronously.",
                "It ensures that only one thread can execute a block or method on a locked object at any given time, preventing race conditions.",
                "It automatically runs code in parallel across all CPU cores.",
                "It updates local fields directly to database records."
            ],
            "answerIndex": 1,
            "explanation": "`synchronized` utilizes monitor locks (intrinsic locks) on objects, ensuring mutually exclusive thread access to critical sections of multi-threaded code."
        }
    ],
    "go": [
        {
            "question": "What makes Go's goroutines much lighter than standard operating system threads?",
            "options": [
                "Goroutines do not consume any RAM.",
                "Goroutines run inside the browser environment.",
                "Goroutines start with a very small stack (about 2KB) that grows and shrinks dynamically, and are multiplexed onto OS threads.",
                "Goroutines run only when the system is idle."
            ],
            "answerIndex": 2,
            "explanation": "Unlike OS threads which have large, fixed-size stacks (typically 1MB-2MB), goroutines start with 2KB stacks managed dynamically by the Go runtime scheduler."
        },
        {
            "question": "How do goroutines communicate and synchronize data in Go?",
            "options": [
                "Through global variables protected by thread locks.",
                "By using Channels to pass data and signal execution state.",
                "Using native operating system thread interrupts.",
                "Through shared database connections."
            ],
            "answerIndex": 1,
            "explanation": "Go uses channels as concurrency primitives to allow goroutines to pass typed data and safely synchronize without manual lock primitives."
        },
        {
            "question": "What is the purpose of a pointer receiver (*StructName) in a Go method definition?",
            "options": [
                "It automatically compiles the method as a static C binary.",
                "It allows the method to mutate the receiver's fields directly and avoids copying the struct's data on invocation.",
                "It renders the struct read-only.",
                "It registers the method with a garbage collection worker."
            ],
            "answerIndex": 1,
            "explanation": "A pointer receiver passes the memory address of the struct instance, enabling direct field modification and optimizing performance by avoiding struct copying."
        },
        {
            "question": "What is the difference between an array and a slice in Go?",
            "options": [
                "Arrays are dynamically sized, while slices have a fixed length.",
                "Arrays have a fixed size defined at compilation, while slices are dynamic windows pointing to an underlying array.",
                "Arrays are always passed by reference, while slices are passed by value.",
                "There is no difference; they are synonyms."
            ],
            "answerIndex": 1,
            "explanation": "Go arrays have a fixed size that is part of their type. Slices are flexible, dynamic wrappers containing a pointer to an underlying array, a length, and a capacity."
        },
        {
            "question": "What is Go's standard approach for handling errors?",
            "options": [
                "Using try-catch blocks to capture runtime exceptions.",
                "Returning an error interface as the last return value from functions, which the caller must check explicitly.",
                "Throwing fatal panics that terminate the program immediately.",
                "Writing errors automatically to a system syslog file."
            ],
            "answerIndex": 1,
            "explanation": "Go does not have standard try/catch blocks. Instead, functions return multiple values, including an error value, which callers inspect using `if err != nil`."
        },
        {
            "question": "How does a class or struct implement an interface in Go?",
            "options": [
                "By using the `implements` keyword in the declaration.",
                "Implicitly, by defining all methods declared in the interface (no explicit declaration needed).",
                "By inheriting from an interface helper base class.",
                "By wrapping the struct inside a package interface container."
            ],
            "answerIndex": 1,
            "explanation": "Go interfaces are implemented implicitly. A struct implements an interface simply by defining methods with matching signatures, enabling clean decoupling."
        },
        {
            "question": "Which scheduling model does Go's runtime scheduler use to multiplex goroutines onto OS threads?",
            "options": [
                "The M:N scheduler model (M goroutines onto N OS threads).",
                "A round-robin scheduling algorithm directly managed by the CPU.",
                "A single-threaded loop similar to Javascript.",
                "A multi-process fork scheduling model."
            ],
            "answerIndex": 0,
            "explanation": "The Go scheduler uses an M:N model (represented by G for goroutines, M for machine threads, and P for logical processors) to run millions of goroutines on a small pool of CPU threads."
        },
        {
            "question": "When does a Go `defer` statement execute its associated function call?",
            "options": [
                "Immediately when the defer line is parsed.",
                "In a separate background thread.",
                "When the surrounding function finishes and returns.",
                "Only if the program panics."
            ],
            "answerIndex": 2,
            "explanation": "A `defer` statement pushes a function call onto a stack. The deferred calls are executed in Last-In-First-Out (LIFO) order right before the surrounding function returns."
        },
        {
            "question": "How are struct fields mapped to JSON properties during marshaling in Go?",
            "options": [
                "By naming fields exactly the same as the JSON keys (case-insensitive).",
                "Using struct tags defined after field declarations, e.g. `json:\"fieldName\"`.",
                "By registering the struct inside an XML schema registry.",
                "Go automatically maps fields dynamically using reflection (no custom tags)."
            ],
            "answerIndex": 1,
            "explanation": "Go uses struct tags containing metadata (e.g. `json:\"id\"`) which the `encoding/json` package parses via reflection to serialize/deserialize fields."
        },
        {
            "question": "How is package-level visibility (public/private) determined in Go?",
            "options": [
                "By using the public or private keyword before declarations.",
                "Through directory path names.",
                "By capitalization: identifiers starting with an uppercase letter are public (exported), others are private.",
                "By declaring them in an external `package.json` configurations file."
            ],
            "answerIndex": 2,
            "explanation": "Go relies on capitalization for visibility. An identifier starting with an uppercase letter is exported (public) and visible outside its package; lowercase is unexported."
        },
        {
            "question": "What is cap(slice) in Go?",
            "options": [
                "The number of elements currently stored in the slice.",
                "The maximum length a slice can grow to before raising an exception.",
                "The capacity: the number of elements in the underlying array, starting from the first element of the slice.",
                "The memory size of the slice in bytes."
            ],
            "answerIndex": 2,
            "explanation": "The capacity of a slice represents the size of the underlying array allocation from the start of the slice. It is accessed via `cap(s)`, while `len(s)` returns the current item count."
        },
        {
            "question": "What is the purpose of the `select` statement in Go?",
            "options": [
                "To choose database rows from a table.",
                "To block execution until one of multiple channel operations (sends or receives) is ready to run.",
                "To implement standard switch cases for string values.",
                "To pick variables from system arrays."
            ],
            "answerIndex": 1,
            "explanation": "The `select` statement lets a goroutine wait on multiple channel communication operations. It blocks until one of its cases is ready to execute, then runs that case."
        }
    ],
    "javascript_node": [
        {
            "question": "How does Node.js handle asynchronous operations if JavaScript is single-threaded?",
            "options": [
                "By spawning a new CPU thread for each async callback.",
                "Using an Event Loop to offload non-blocking I/O tasks to the OS kernel or a thread pool, processing results sequentially when the call stack is empty.",
                "By compiling JavaScript code to a multithreaded native application.",
                "Through cooperative process-forking on multi-core servers."
            ],
            "answerIndex": 1,
            "explanation": "Node.js uses a single-threaded Event Loop that delegates asynchronous tasks (such as network or file operations) to system APIs or libuv's thread pool, processing callbacks sequentially."
        },
        {
            "question": "What are the states of a JavaScript Promise?",
            "options": [
                "Started, Running, Stopped.",
                "pending, fulfilled, rejected.",
                "Active, Resolved, Terminated.",
                "Waiting, Done, Failed."
            ],
            "answerIndex": 1,
            "explanation": "A Promise is always in one of three mutually exclusive states: pending (initial state), fulfilled (operation completed successfully), or rejected (operation failed)."
        },
        {
            "question": "How does `async/await` relate to JavaScript Promises?",
            "options": [
                "It compiles Javascript to native asynchronous C code.",
                "It is syntactic sugar built on top of Promises, making asynchronous code write and read like synchronous code.",
                "It deletes Promises entirely from runtime memory.",
                "It forces callbacks to run in parallel threads."
            ],
            "answerIndex": 1,
            "explanation": "`async` functions automatically return a Promise. The `await` keyword pauses execution of the async function until the awaited Promise resolves, making async code highly readable."
        },
        {
            "question": "What parameters do Express.js middleware functions receive in their execution signature?",
            "options": [
                "Only the request object (`req`).",
                "The Request (`req`), Response (`res`), and a call-forwarding function (`next`).",
                "The database client and router instances.",
                "System process and port information."
            ],
            "answerIndex": 1,
            "explanation": "Express middleware signature accepts `(req, res, next)`. This gives it access to request data, response handling, and control routing to subsequent handlers via `next()`."
        },
        {
            "question": "What is a closure in JavaScript?",
            "options": [
                "A function that automatically closes database connections.",
                "The combination of a function bundled together with references to its surrounding state (the lexical environment).",
                "A compile-time block syntax warning.",
                "An object that cannot hold properties."
            ],
            "answerIndex": 1,
            "explanation": "A closure allows an inner function to access variables from its outer (enclosing) scope even after the outer function has finished executing."
        },
        {
            "question": "What is the difference between CommonJS and ES Modules (ESM) in Node.js?",
            "options": [
                "CommonJS uses `require()` and `module.exports`, while ES Modules use `import` and `export` statements.",
                "CommonJS is asynchronous, while ESM is synchronous.",
                "CommonJS runs only in the browser, while ESM runs only in Node.js.",
                "There is no difference in syntax."
            ],
            "answerIndex": 0,
            "explanation": "CommonJS is Node's historical module system using `require`/`module.exports`. ESM is the ES6 standard using `import`/`export`, which supports static analysis and tree shaking."
        },
        {
            "question": "Which C++ library does Node.js rely on to manage its thread pool and asynchronous event processing?",
            "options": ["V8", "libuv", "Webpack", "Boost"],
            "answerIndex": 1,
            "explanation": "Node.js uses the libuv library to handle the event loop, thread pool workers, file system notifications, and asynchronous networking events."
        },
        {
            "question": "How does prototypical inheritance work in JavaScript?",
            "options": [
                "Objects copy all properties from a class blueprint on instantiation.",
                "Objects inherit properties and methods directly from other objects via a prototype chain link.",
                "Inheritance is resolved strictly at compile time.",
                "JavaScript does not support inheritance."
            ],
            "answerIndex": 1,
            "explanation": "Every JS object has a link to a prototype object. When a property or method is requested, JS searches the object first, then traverses up the prototype chain until found or null is reached."
        },
        {
            "question": "What is the scoping difference between `var`, `let`, and `const`?",
            "options": [
                "`var` is block-scoped, while `let` and `const` are function-scoped.",
                "`var` is function-scoped (or global), while `let` and `const` are block-scoped.",
                "`const` is globally scoped, while `let` is locally scoped.",
                "All three share identical scoping rules."
            ],
            "answerIndex": 1,
            "explanation": "`var` is scoped to its declaring function. `let` and `const` are block-scoped (scoped to the nearest `{}` block). Additionally, `const` cannot be reassigned."
        },
        {
            "question": "Which array method returns a single accumulated value by running a callback on each element?",
            "options": ["map", "filter", "reduce", "forEach"],
            "answerIndex": 2,
            "explanation": "The `reduce` method executes a reducer function on each array element, accumulating the results into a single value (e.g. summing numbers)."
        },
        {
            "question": "What is the difference between `==` and `===` operators in JavaScript?",
            "options": [
                "`==` is strict equality, while `===` performs type coercion.",
                "`==` performs type coercion before comparison, while `===` compares both value and type strictly.",
                "They behave identically.",
                "`==` is used for objects, `===` is used for primitive types."
            ],
            "answerIndex": 1,
            "explanation": "The loose equality operator (`==`) converts operands to a common type (coercion) before comparing. The strict equality operator (`===`) compares value and type without conversion."
        },
        {
            "question": "What is the purpose of Node's `EventEmitter` class?",
            "options": [
                "To manage browser mouse click events.",
                "To implement the observer pattern, allowing objects to emit named events that trigger registered listener callbacks.",
                "To execute database transactions.",
                "To create child server processes."
            ],
            "answerIndex": 1,
            "explanation": "The `EventEmitter` class in Node's `events` module enables event-driven programming, facilitating asynchronous communication between different components of an app."
        }
    ],
    "databases_sql": [
        {
            "question": "When must the `HAVING` clause be used in SQL instead of the `WHERE` clause?",
            "options": [
                "When filtering records containing string patterns.",
                "When filtering groups of query results based on aggregate functions (e.g. SUM, AVG).",
                "When sorting results in descending order.",
                "When performing SQL join operations."
            ],
            "answerIndex": 1,
            "explanation": "The `WHERE` clause filters individual rows before grouping. The `HAVING` clause filters grouped results after aggregation has been applied."
        },
        {
            "question": "Which type of SQL Join returns all rows from the left table, and matching rows from the right table, filling with NULL if no match is found?",
            "options": ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL OUTER JOIN"],
            "answerIndex": 1,
            "explanation": "A `LEFT JOIN` (or LEFT OUTER JOIN) returns all records from the left table and any corresponding matching records from the right table."
        },
        {
            "question": "How does a B-Tree index speed up database SELECT queries, and what is its overhead?",
            "options": [
                "It compresses table files to half size, slowing down writes.",
                "It provides logarithmic time search (O(log N)) for matching rows, but adds write overhead to update the index on INSERT, UPDATE, and DELETE operations.",
                "It turns relational tables into NoSQL collections.",
                "It runs queries in parallel on the GPU."
            ],
            "answerIndex": 1,
            "explanation": "B-Tree indexes speed up lookups by organizing data in a balanced search tree. However, every modification to indexed columns requires updating the tree structure, adding write overhead."
        },
        {
            "question": "What does the ACID acronym stand for in database transaction management?",
            "options": [
                "Aggregation, Consolidation, Indexing, Distribution.",
                "Atomicity, Consistency, Isolation, Durability.",
                "Availability, Concurrency, Isolation, Deletion.",
                "Access, Control, Integrity, Definition."
            ],
            "answerIndex": 1,
            "explanation": "ACID properties (Atomicity, Consistency, Isolation, Durability) ensure database transactions are processed reliably, maintaining data integrity."
        },
        {
            "question": "Which ANSI SQL transaction isolation level prevents dirty reads and non-repeatable reads, but can allow phantom reads?",
            "options": ["Read Uncommitted", "Read Committed", "Repeatable Read", "Serializable"],
            "answerIndex": 2,
            "explanation": "Repeatable Read prevents dirty reads and non-repeatable reads by holding locks on read rows, but does not lock index ranges, potentially allowing phantom rows to be inserted."
        },
        {
            "question": "What is the primary goal of Third Normal Form (3NF) in database design?",
            "options": [
                "To optimize search queries using caching.",
                "To eliminate transitive dependencies, ensuring all non-key columns depend only on the primary key, thereby reducing data redundancy.",
                "To split tables into document-based JSON rows.",
                "To enforce foreign key constraints across different databases."
            ],
            "answerIndex": 1,
            "explanation": "A database is in 3NF if it is in 2NF and has no transitive functional dependencies, meaning every non-prime attribute depends directly on the primary key."
        },
        {
            "question": "What is a key difference between a Primary Key and a Unique constraint?",
            "options": [
                "A table can have multiple Primary Keys, but only one Unique constraint.",
                "Primary Keys can contain NULL values, Unique constraints cannot.",
                "A table can have only one Primary Key, but multiple Unique constraints, and Unique constraints can allow NULL values.",
                "They are identical and have no functional differences."
            ],
            "answerIndex": 2,
            "explanation": "A table is limited to one primary key, which uniquely identifies rows and forbids NULL values. Unique constraints allow duplicate prevention across other columns, allowing NULLs."
        },
        {
            "question": "What does a Foreign Key constraint enforce in a relational schema?",
            "options": [
                "It encrypts columns to secure foreign user access.",
                "Referential integrity, guaranteeing that values in a column match existing values in the primary key of a referenced parent table.",
                "It automatically synchronizes tables with external APIs.",
                "It indexes columns for faster search."
            ],
            "answerIndex": 1,
            "explanation": "Foreign keys maintain referential integrity, preventing invalid data entries in child tables by ensuring they point to a valid parent record."
        },
        {
            "question": "Which SQL aggregate function computes the rank of rows within query partitions without skipping rank numbers?",
            "options": ["RANK()", "DENSE_RANK()", "ROW_NUMBER()", "PERCENT_RANK()"],
            "answerIndex": 1,
            "explanation": "Unlike `RANK()`, which leaves gaps when ties occur (e.g. 1, 2, 2, 4), `DENSE_RANK()` assigns consecutive integers without gaps (e.g. 1, 2, 2, 3)."
        },
        {
            "question": "What is the difference between a View and a Materialized View?",
            "options": [
                "Views are stored on disk, Materialized Views exist only in memory.",
                "A View is a virtual table that executes its query dynamically, while a Materialized View precomputes and stores its result query data on disk.",
                "Materialized Views are used only in NoSQL databases.",
                "There is no difference; they are identical."
            ],
            "answerIndex": 1,
            "explanation": "Views run their queries on-demand, consuming computation resources each time. Materialized views cache query results physically on disk and must be refreshed when base data changes."
        },
        {
            "question": "Why are Columnar databases preferred over Row-oriented databases for OLAP (Analytical) workloads?",
            "options": [
                "They run transactions faster.",
                "They allow reading only the specific columns needed for aggregations, drastically reducing disk I/O and improving compression rates.",
                "They use JSON format internally.",
                "They require less memory to load."
            ],
            "answerIndex": 1,
            "explanation": "Row-oriented databases are optimized for OLTP (reading whole rows). Columnar databases group column values together, enabling high compression and fast aggregation over specific fields."
        },
        {
            "question": "What is a Common Table Expression (CTE) in SQL?",
            "options": [
                "A permanent database table used for caching.",
                "A temporary named result set defined within the scope of a single SELECT, INSERT, UPDATE, or DELETE query using the `WITH` keyword.",
                "A table index optimization strategy.",
                "A database schema validation rule."
            ],
            "answerIndex": 1,
            "explanation": "CTEs are defined using the `WITH` keyword. They act as temporary queries that exist during the execution of a main statement, improving query readability and enabling recursion."
        }
    ],
    "nosql_caching": [
        {
            "question": "What is the primary characteristic of key-value stores like Redis?",
            "options": [
                "They store data in relational schemas with strict tables.",
                "They store records in-memory, mapping keys to values for sub-millisecond retrieval speeds.",
                "They compile code snippets to native binaries.",
                "They require GraphQL to access properties."
            ],
            "answerIndex": 1,
            "explanation": "Redis stores key-value pairs in memory, which allows it to act as an extremely fast cache, session store, or queue."
        },
        {
            "question": "How are records represented and structured in a document database like MongoDB?",
            "options": [
                "As rows in contiguous tables.",
                "As JSON-like documents (internally serialized as BSON) with dynamic schemas.",
                "As nodes and edge relationships.",
                "As key-value byte strings only."
            ],
            "answerIndex": 1,
            "explanation": "MongoDB is a document-oriented database. It stores records as BSON (Binary JSON) documents, letting applications persist nested object structures directly."
        },
        {
            "question": "According to the CAP Theorem, which two properties must a distributed database choose between in the event of a Network Partition (P)?",
            "options": [
                "Security vs Performance.",
                "Consistency (C) vs Availability (A).",
                "Scalability vs Relational Integrity.",
                "Replication vs Indexing."
            ],
            "answerIndex": 1,
            "explanation": "The CAP theorem states that a distributed system cannot simultaneously guarantee Consistency, Availability, and Partition Tolerance. Under network partitions, it must trade consistency for availability, or vice versa."
        },
        {
            "question": "Which cache eviction policy removes the least recently accessed items first when memory limit is reached?",
            "options": ["LFU (Least Frequently Used)", "LRU (Least Recently Used)", "FIFO (First In First Out)", "TTL (Time To Live)"],
            "answerIndex": 1,
            "explanation": "Least Recently Used (LRU) evicts the key that has not been accessed for the longest duration, optimizing cache retention for temporal locality."
        },
        {
            "question": "Why is denormalization commonly practiced in NoSQL database design?",
            "options": [
                "To enforce strict SQL constraints.",
                "To optimize read performance by storing related data together, avoiding expensive runtime join operations across tables.",
                "To decrease disk space consumption.",
                "To make databases ACID-compliant."
            ],
            "answerIndex": 1,
            "explanation": "NoSQL databases generally lack relational join features. Denormalization repeats data in single documents to allow fast, single-query reads."
        },
        {
            "question": "What are the two primary persistence options provided by Redis to survive restarts?",
            "options": [
                "SQL replication and JSON dumps.",
                "RDB (snapshotting at intervals) and AOF (logging write commands to an append-only file).",
                "Direct memory allocation and swap files.",
                "B-Tree index logging and caching."
            ],
            "answerIndex": 1,
            "explanation": "Redis provides durability through RDB snapshots (point-in-time state dumps) and AOF logs (recording every write transaction as it happens)."
        },
        {
            "question": "What is the role of MongoDB replica sets?",
            "options": [
                "To split collections into separate shard keys.",
                "To provide high availability and automatic failover by replicating data across primary and secondary nodes.",
                "To speed up local memory reads by caching records.",
                "To compile database functions."
            ],
            "answerIndex": 1,
            "explanation": "Replica sets consist of a primary node (handling writes) and secondary nodes replicating data. If primary fails, secondary nodes hold an election to promote a new primary."
        },
        {
            "question": "How does Consistent Hashing benefit distributed caching clusters?",
            "options": [
                "It encrypts hash values for data security.",
                "It minimizes the reshuffling of cached keys when cache nodes are added or removed from the cluster.",
                "It compiles string keys to integer keys.",
                "It distributes data evenly to one single primary node."
            ],
            "answerIndex": 1,
            "explanation": "Consistent hashing maps cache nodes and keys to a logical ring. Adding or removing a node only impacts a fraction of keys (K/N), preventing massive cache misses."
        },
        {
            "question": "What is the difference between Cache Avalanche and Cache Breakdown?",
            "options": [
                "Avalanche is caused by database server crashes; Breakdown is client side.",
                "Cache Avalanche occurs when many keys expire simultaneously, flooding the database; Cache Breakdown is when a single popular hot key expires, causing concurrent DB queries.",
                "They are identical terms.",
                "Breakdown is caused by network timeouts."
            ],
            "answerIndex": 1,
            "explanation": "Avalanche happens when massive key expirations send concurrent spikes to databases. Breakdown (or cache stampede) is target-focused: a single hot key expires, causing concurrent database reads."
        },
        {
            "question": "What defines the data model of a Graph Database (like Neo4j)?",
            "options": [
                "Key-value string blobs.",
                "Nodes (entities), Edges (relationships), and Properties (key-value attributes on nodes/edges).",
                "Tabular records organized in rows.",
                "JSON documents stored inside buckets."
            ],
            "answerIndex": 1,
            "explanation": "Graph databases use the Property Graph model. Entities are represented as nodes, and their connections as edges, allowing fast traversal of complex relations."
        },
        {
            "question": "Which NoSQL wide-column database uses keyspaces and column families to scale horizontally across multi-master nodes?",
            "options": ["MongoDB", "Redis", "Apache Cassandra", "SQLite"],
            "answerIndex": 2,
            "explanation": "Cassandra is a distributed wide-column store designed for high-availability write workloads, utilizing partitioning keys and ring topologies."
        },
        {
            "question": "What is the difference between Write-through and Write-back caching strategies?",
            "options": [
                "Write-through is slower because it writes to cache and database synchronously; Write-back writes to cache and updates the database asynchronously.",
                "Write-through is for NoSQL; Write-back is for SQL databases.",
                "Write-back deletes keys automatically.",
                "Write-through bypasses the cache entirely."
            ],
            "answerIndex": 0,
            "explanation": "Write-through updates both cache and DB immediately, avoiding stale data but adding write latency. Write-back updates cache and returns, queueing DB updates for background processing."
        }
    ],
    "docker_devops": [
        {
            "question": "What is the primary difference between a Docker Image and a Docker Container?",
            "options": [
                "Images are running instances of containers.",
                "An image is an immutable, read-only template; a container is a runnable, isolated instance created from that image.",
                "Images are used in production; containers in development.",
                "There is no functional difference."
            ],
            "answerIndex": 1,
            "explanation": "An image represents the application and its dependencies. A container is a runtime instantiation of that blueprint containing an isolated file system and execution space."
        },
        {
            "question": "In a Dockerfile, what is the difference between `RUN` and `CMD` instructions?",
            "options": [
                "`RUN` executes commands during image build time; `CMD` specifies default commands to run when the container starts.",
                "`RUN` runs only in background; `CMD` runs in foreground.",
                "`RUN` starts the container; `CMD` compiles dependencies.",
                "They are completely interchangeable."
            ],
            "answerIndex": 0,
            "explanation": "`RUN` commands execute on top of intermediate layers to build the image. `CMD` provides the runtime entry point commands when executing `docker run`."
        },
        {
            "question": "What are Docker Volumes used for?",
            "options": [
                "To control container CPU priority.",
                "To persist data generated and used by Docker containers, bypassing the container's writable storage layer.",
                "To increase network communication speeds.",
                "To compress Docker image size."
            ],
            "answerIndex": 1,
            "explanation": "Containers are ephemeral; their data is deleted on termination. Docker Volumes mount directory maps from the host system to maintain persistent state."
        },
        {
            "question": "What does Docker Compose allow developers to do?",
            "options": [
                "Compile Go code into Python applications.",
                "Define, manage, and run multi-container applications using a single YAML configuration file.",
                "Deploy containers directly to AWS lambda functions.",
                "Monitor container CPU usage dynamically."
            ],
            "answerIndex": 1,
            "explanation": "Docker Compose automates orchestration. Running `docker compose up` uses a `docker-compose.yml` config file to build, link, and run networks of service containers."
        },
        {
            "question": "What is the difference between the `EXPOSE` instruction and publishing a port (`-p`) in Docker?",
            "options": [
                "`EXPOSE` maps ports to the host; `-p` is documentation.",
                "`EXPOSE` is documentation indicating intended ports; `-p` actually binds and forwards host ports to the container.",
                "`EXPOSE` works only for database containers.",
                "They behave identically."
            ],
            "answerIndex": 1,
            "explanation": "`EXPOSE` serves as documentation showing which ports are used by the app. The runtime flag `-p hostPort:containerPort` is required to open traffic mapping to the host."
        },
        {
            "question": "How does Docker leverage layer caching during image builds?",
            "options": [
                "It caches database queries.",
                "It skips rebuilding image layers if the Dockerfile instruction and referenced files have not changed since the last build.",
                "It stores container outputs in memory.",
                "It compiles Javascript modules on the fly."
            ],
            "answerIndex": 1,
            "explanation": "Docker processes Dockerfile lines sequentially. If a layer's instruction and its context files match a cached layer, Docker reuses that layer, saving build time."
        },
        {
            "question": "Which Docker network driver connects containers directly to the host's networking stack, bypassing virtualization?",
            "options": ["bridge", "host", "overlay", "none"],
            "answerIndex": 1,
            "explanation": "The `host` network driver runs the container's processes directly in the host's network namespaces, matching host port mappings directly."
        },
        {
            "question": "What is a primary benefit of using Multi-stage builds in Dockerfiles?",
            "options": [
                "It lets containers run on different operating systems.",
                "It reduces the final image size by copying only compiler outputs (artifacts) to a minimal runtime base image, excluding compiler dependencies.",
                "It speeds up database migration runs.",
                "It spawns multiple containers at once."
            ],
            "answerIndex": 1,
            "explanation": "Multi-stage builds use multiple `FROM` clauses. Heavy tools and source files are used in build stages, and only finished binaries are copied into final light containers."
        },
        {
            "question": "What is a Docker Registry used for?",
            "options": [
                "To register domain names for containers.",
                "To store, distribute, and manage Docker Images (e.g. Docker Hub, Amazon ECR).",
                "To track database schemas.",
                "To balance network requests."
            ],
            "answerIndex": 1,
            "explanation": "A registry is a repository service. Developers push built images to registries so they can be pulled and run on staging or production servers."
        },
        {
            "question": "In Kubernetes, what is a Pod?",
            "options": [
                "A physical server cabinet.",
                "The smallest deployable unit representing a single instance of a running process, wrapping one or more tightly coupled containers.",
                "A database storage volume.",
                "A network load balancer."
            ],
            "answerIndex": 1,
            "explanation": "Pods share network namespaces, IP addresses, and storage volumes. Containers inside a Pod collaborate closely, acting as a single logical host."
        },
        {
            "question": "What is the difference between Continuous Integration (CI) and Continuous Deployment (CD)?",
            "options": [
                "CI manages databases; CD manages servers.",
                "CI automates building and testing code on repository commits; CD automates releasing and deploying passing code to production environment.",
                "CI is done by developers; CD by system admins.",
                "They are synonyms."
            ],
            "answerIndex": 1,
            "explanation": "CI focuses on code validation and integration (PR testing). CD automates the downstream release pipeline to deploy verified builds directly to environment servers."
        },
        {
            "question": "What is the core principle of Infrastructure as Code (IaC)?",
            "options": [
                "Writing server code using Javascript.",
                "Managing and provisioning infrastructure resources (servers, databases, networks) using machine-readable definition files rather than manual UI configs.",
                "Compiling Dockerfiles to native code.",
                "Running automated unit tests."
            ],
            "answerIndex": 1,
            "explanation": "IaC (e.g. Terraform, CloudFormation) defines infrastructure in config code, allowing infrastructure setup to be version-controlled, reviewed, and reproduced easily."
        }
    ],
    "pandas_numpy": [
        {
            "question": "What does Vectorization mean in NumPy?",
            "options": [
                "Converting arrays into lists of coordinates.",
                "Executing operations on entire arrays at once using compiled C code, avoiding slow Python loops.",
                "Running operations in parallel threads using the GIL.",
                "Creating multi-dimensional graphs."
            ],
            "answerIndex": 1,
            "explanation": "Vectorization delegates array computations to compiled, highly optimized C libraries underneath, which execute operations across block memory without Python loop overhead."
        },
        {
            "question": "How does NumPy's Broadcasting mechanism work?",
            "options": [
                "It streams array contents over network sockets.",
                "It allows arithmetic operations on arrays of different shapes by conceptually expanding the smaller array to match the shape of the larger array.",
                "It flattens arrays into a single dimension.",
                "It allocates memory across different clusters."
            ],
            "answerIndex": 1,
            "explanation": "Broadcasting applies element-wise operations on arrays of different shapes by replicating dimensions of size 1, matching array shapes under strict compatibility rules."
        },
        {
            "question": "What is a Pandas DataFrame?",
            "options": [
                "A 1-dimensional array of numbers.",
                "A 2-dimensional, size-mutable, tabular data structure with labeled axes (rows and columns).",
                "A binary tree database structure.",
                "A layout engine for plotting images."
            ],
            "answerIndex": 1,
            "explanation": "A Pandas DataFrame represents tabular data, mapping columns of potentially different data types to rows, similar to a spreadsheet or SQL table."
        },
        {
            "question": "What is the primary difference between Pandas Series and a 1D NumPy array?",
            "options": [
                "Series can only store float values.",
                "Series contains an associated index (labels) for accessing data, while NumPy arrays use zero-based integer index offsets only.",
                "NumPy arrays are mutable, Series are not.",
                "Series cannot be sliced."
            ],
            "answerIndex": 1,
            "explanation": "Pandas Series is a labeled 1D array. It maintains an index array mapping label keys to data elements, allowing database-like joins and alignment."
        },
        {
            "question": "What describes the Split-Apply-Combine pattern in Pandas GroupBy operations?",
            "options": [
                "Splitting code files, applying formatting, and combining to a single file.",
                "Splitting data into groups based on keys, applying a function (e.g. aggregation, transform), and combining results into a new DataFrame.",
                "Sorting rows by index, filtering nulls, and saving.",
                "Converting DataFrames into NumPy arrays."
            ],
            "answerIndex": 1,
            "explanation": "`groupby()` splits data based on criteria, applies functions (like `sum()` or `mean()`) independently to groups, and combines outcomes back to a summary structure."
        },
        {
            "question": "How does Pandas handle missing values in a DataFrame?",
            "options": [
                "It throws a NullPointerException immediately.",
                "Using Sentinel values (NaN/None), which can be managed using functions like `dropna()` (filtering nulls) or `fillna()` (imputing values).",
                "By writing a zero value automatically.",
                "By converting columns to string types."
            ],
            "answerIndex": 1,
            "explanation": "Pandas labels missing values as NaN (Not a Number) or None. Methods like `dropna()` prune rows/columns containing NaNs, and `fillna()` replaces them with defaults."
        },
        {
            "question": "What is the difference between `.loc` and `.iloc` indexers in Pandas?",
            "options": [
                "There is no difference.",
                "`.loc` indexes data using labels/names; `.iloc` indexes data using integer positions (0-indexed offsets).",
                "`.loc` is for rows, `.iloc` is for columns.",
                "`.loc` is faster than `.iloc`."
            ],
            "answerIndex": 1,
            "explanation": "`.loc` is label-based (e.g. `df.loc['row_label', 'col_label']`). `.iloc` is integer-position based (e.g. `df.iloc[0, 1]`), mirroring standard Python list slicing."
        },
        {
            "question": "In NumPy, what is the role of the `reshape()` method?",
            "options": [
                "It deletes array dimensions.",
                "It returns a new view of the array with a modified shape (dimensions) without changing the underlying data values.",
                "It resizes array memory allocation.",
                "It normalizes element values between 0 and 1."
            ],
            "answerIndex": 1,
            "explanation": "`reshape()` allows altering the shape of an array (e.g. turning 1D array of 6 elements into a 2D array of 2x3) as long as total element count remains identical."
        },
        {
            "question": "What is the difference between merging (`pd.merge`) and joining (`df.join`) in Pandas?",
            "options": [
                "Merging is for SQL databases; joining is for Excel files.",
                "Merging matches columns on shared keys; joining combines DataFrames based on their row indexes by default.",
                "They perform opposite operations.",
                "Merging is done in memory; joining writes to disk."
            ],
            "answerIndex": 1,
            "explanation": "`pd.merge()` is a database-style join matching on arbitrary column keys. `df.join()` is a convenience method that aligns data columns based on row index coordinates."
        },
        {
            "question": "Why are operations on NumPy arrays faster than running standard Python loops over lists?",
            "options": [
                "NumPy bypasses system memory.",
                "NumPy arrays store elements of homogeneous types in contiguous memory blocks, enabling hardware-level vector processing (SIMD).",
                "Python lists are compiled to slower database rows.",
                "NumPy uses parallel background processes."
            ],
            "answerIndex": 1,
            "explanation": "Python lists are arrays of pointers to scattered objects. NumPy arrays store uniform raw data bytes contiguously in memory, allowing CPUs to fetch data efficiently and execute vectorized math instructions."
        },
        {
            "question": "In Pandas DataFrame operations, what does `axis=0` and `axis=1` signify?",
            "options": [
                "`axis=0` refers to columns; `axis=1` refers to rows.",
                "`axis=0` refers to rows (downwards calculation); `axis=1` refers to columns (sideways calculation).",
                "They are scaling parameters.",
                "They represent the dimensions of plot figures."
            ],
            "answerIndex": 1,
            "explanation": "Operations (like `mean()` or `drop()`) along `axis=0` run vertically down row indices. Operations along `axis=1` run horizontally across column fields."
        },
        {
            "question": "What is the cap on dimensions for a NumPy ndarray?",
            "options": [
                "Maximum 2 dimensions (tables).",
                "Maximum 3 dimensions (tensors).",
                "Practically arbitrary; ndarrays support N-dimensional arrays.",
                "It is limited by CPU core count."
            ],
            "answerIndex": 2,
            "explanation": "NumPy arrays are N-dimensional. An ndarray can represent 1D vectors, 2D matrices, 3D color images, or any higher-dimensional tensors."
        }
    ],
    "ml_dl_fundamentals": [
        {
            "question": "What is the difference between Supervised and Unsupervised Learning?",
            "options": [
                "Supervised learning requires human monitoring during model training.",
                "Supervised learning trains models on labeled input-output pairs; Unsupervised learning finds patterns within unlabeled data.",
                "Supervised learning runs only on local machines.",
                "Unsupervised learning uses no algorithms."
            ],
            "answerIndex": 1,
            "explanation": "Supervised learning maps inputs to target labels (e.g. regression/classification). Unsupervised learning clusters or processes input data without ground-truth labels."
        },
        {
            "question": "What occurs when a machine learning model suffers from Overfitting?",
            "options": [
                "The model runs too slowly on GPUs.",
                "The model performs well on training data but fails to generalize to unseen test data.",
                "The model gets deleted from disk memory.",
                "The model underperforms on both training and test data."
            ],
            "answerIndex": 1,
            "explanation": "Overfitting happens when a model learns noise and specifics of training data instead of general patterns. Regularization, dropout, or early stopping are used to mitigate this."
        },
        {
            "question": "How are parameter weight gradients calculated in neural networks?",
            "options": [
                "By guessing random weight changes.",
                "Using Backpropagation, which applies the calculus Chain Rule to compute loss gradients with respect to weights from output layer backward to input.",
                "By compiling code to native binaries.",
                "Through file system metadata scanning."
            ],
            "answerIndex": 1,
            "explanation": "Backpropagation computes loss gradients. The error is propagated backward through network layers using the chain rule, allowing optimizers (like SGD) to update model weights."
        },
        {
            "question": "Why are non-linear Activation Functions (like ReLU, Tanh) necessary in hidden layers?",
            "options": [
                "To speed up matrix multiplication.",
                "To enable the network to learn complex, non-linear relationships in data; without them, the network acts as a single linear combination.",
                "To keep values strictly positive.",
                "To prevent files from being corrupted."
            ],
            "answerIndex": 1,
            "explanation": "A network of linear layers mathematically collapses into a single linear function. Non-linear activations introduce non-linearity, allowing deep networks to approximate arbitrary functions."
        },
        {
            "question": "Which loss function is commonly used for multiclass classification tasks?",
            "options": ["Mean Squared Error (MSE)", "Binary Cross-Entropy", "Categorical Cross-Entropy", "Huber Loss"],
            "answerIndex": 2,
            "explanation": "Categorical Cross-Entropy compares the model's predicted probability distribution (via Softmax) against the ground-truth one-hot encoded labels, penalizing incorrect predictions."
        },
        {
            "question": "What role does the Learning Rate play in gradient descent updates?",
            "options": [
                "It adjusts the speed of model file writing.",
                "It scales step size: the fraction of gradient value subtracted from weights to minimize loss.",
                "It dictates GPU memory allocations.",
                "It counts total epochs of training."
            ],
            "answerIndex": 1,
            "explanation": "Learning rate is a hyperparameter. A rate too high causes optimization to diverge; a rate too low makes training extremely slow."
        },
        {
            "question": "What is the Bias-Variance Tradeoff?",
            "options": [
                "Trading calculation speed for precision.",
                "The balance between errors from simple assumptions (high bias, underfitting) and errors from high sensitivity to training noise (high variance, overfitting).",
                "The tradeoff between CPU and GPU RAM.",
                "The difference between SQL and NoSQL databases."
            ],
            "answerIndex": 1,
            "explanation": "Minimizing bias increases variance, and vice versa. An optimal model minimizes total error by balancing both terms to generalize well."
        },
        {
            "question": "Why is it critical to split dataset into training, validation, and test sets?",
            "options": [
                "To speed up file reading.",
                "Training updates weights; Validation tunes hyperparameters; Test evaluates final generalization performance on completely unseen data.",
                "To format data into JSON columns.",
                "It is only done to prevent memory leaks."
            ],
            "answerIndex": 1,
            "explanation": "This separation prevents data leakage. Validation guides selection of best epochs/models, and the test set acts as an unbiased final check."
        },
        {
            "question": "In binary classification, what does Precision represent?",
            "options": [
                "The total fraction of correct predictions.",
                "The ratio of True Positives to all predicted positives (True Positives + False Positives).",
                "The model compilation speed.",
                "The ratio of True Positives to all actual positives (True Positives + False Negatives)."
            ],
            "answerIndex": 1,
            "explanation": "Precision answers: 'Out of all items predicted as positive, how many were actually positive?' (True Positives / (True Positives + False Positives))."
        },
        {
            "question": "What does the Softmax function output?",
            "options": [
                "A binary 0 or 1 value.",
                "A probability distribution: normalizes output values into range [0, 1] that sum to 1.",
                "An array of integer index values.",
                "A matrix of weight gradients."
            ],
            "answerIndex": 1,
            "explanation": "Softmax is applied to logits in final classification layers. It exponentiates and divides inputs by their sum, mapping them to probabilities."
        },
        {
            "question": "What is the purpose of Dropout in training deep neural networks?",
            "options": [
                "To drop invalid database rows.",
                "A regularization technique that randomly ignores (sets to zero) a fraction of neurons during training to prevent co-adaptation and overfitting.",
                "To close inactive server threads.",
                "To reset learning rates."
            ],
            "answerIndex": 1,
            "explanation": "By turning off random neurons during forward passes, the network cannot rely on specific node paths, forcing it to learn redundant, robust features."
        },
        {
            "question": "Why is Feature Scaling (Normalization/Standardization) important before model training?",
            "options": [
                "To save disk storage space.",
                "It ensures features share comparable value ranges, preventing variables with large scales from dominating gradients and accelerating optimization convergence.",
                "To convert numbers to strings.",
                "To index columns."
            ],
            "answerIndex": 1,
            "explanation": "Gradient descent updates weights proportionally to input features. Scaling coordinates numeric variables, yielding smoother loss landscapes and faster optimization."
        }
    ],
    "llms_genai": [
        {
            "question": "What does Retrieval-Augmented Generation (RAG) accomplish in LLM deployment?",
            "options": [
                "It fine-tunes model weights on private PDFs.",
                "It queries external databases for relevant context based on user prompt, injecting that context into the prompt to provide accurate, up-to-date answers.",
                "It translates English prompts to SQL queries automatically.",
                "It speeds up token processing rates."
            ],
            "answerIndex": 1,
            "explanation": "RAG bridges foundation models with external search. It fetches domain documents semantically and feeds them as prompt context, reducing hallucinations."
        },
        {
            "question": "What is the difference between Fine-tuning and Prompt Engineering?",
            "options": [
                "Fine-tuning alters the model's static weight parameters; Prompt Engineering designs context prompts to guide pre-trained models without modifying weights.",
                "Fine-tuning is done in Javascript; Prompt Engineering in Python.",
                "Prompt Engineering is done only by compilers.",
                "There is no difference."
            ],
            "answerIndex": 0,
            "explanation": "Fine-tuning updates weights via gradient descent on specific datasets. Prompt engineering adjusts the query layout to leverage the model's in-context learning."
        },
        {
            "question": "How are text prompts processed by LLM architectures?",
            "options": [
                "As whole paragraphs in memory.",
                "Text is split into sub-word units called tokens, which are mapped to numerical IDs using a vocabulary tokenizer.",
                "By compiling words to native C strings.",
                "By index lookup in SQL databases."
            ],
            "answerIndex": 1,
            "explanation": "Models read sequences of tokens. Tokenization algorithms (like Byte Pair Encoding) break strings down into sub-word tokens representing common character sets."
        },
        {
            "question": "What is a text embedding?",
            "options": [
                "A compressed zip file of text documentation.",
                "A dense, high-dimensional vector representation of text that captures semantic meaning, enabling mathematical similarity comparison.",
                "A database primary key value.",
                "An HTML container tag."
            ],
            "answerIndex": 1,
            "explanation": "Embeddings map words or sentences into a continuous vector space where semantically similar items reside close to each other (e.g. calculated via Cosine Similarity)."
        },
        {
            "question": "What database type is optimized to index and query vector embeddings for semantic search?",
            "options": ["Relational Database (SQL)", "Vector Database (e.g. Pinecone, Milvus, Chroma)", "Graph Database", "Key-Value Store"],
            "answerIndex": 1,
            "explanation": "Vector databases specialize in storing embeddings and executing fast nearest-neighbor queries (like KNN or ANN search algorithms) over high-dimensional vector spaces."
        },
        {
            "question": "Which core mechanism in Transformer architectures calculates the relevance of tokens relative to each other in a sequence?",
            "options": ["Backpropagation", "Self-Attention", "Activation gating", "Vector indexing"],
            "answerIndex": 1,
            "explanation": "Self-attention computes dynamic weight vectors for each token based on query, key, and value matrices, letting tokens capture contextual relationships across sequences."
        },
        {
            "question": "What is an LLM 'hallucination'?",
            "options": [
                "A crash in the GPU server.",
                "When a model generates factually incorrect, nonsensical, or ungrounded statements with high statistical confidence.",
                "A syntax error in model compilation.",
                "A network timeout in API requests."
            ],
            "answerIndex": 1,
            "explanation": "Hallucinations occur because models predict the most statistically probable next token based on training data, without actual validation of factual truth."
        },
        {
            "question": "What is the role of a System Prompt in LLM systems?",
            "options": [
                "To control operating system threads.",
                "To define the overall persona, constraints, instructions, and behavior limits of the model prior to processing user queries.",
                "To index documentation documents.",
                "To handle database exceptions."
            ],
            "answerIndex": 1,
            "explanation": "System prompts establish the runtime frame. They tell the model how to act (e.g., 'You are a helpful assistant', 'Only output JSON') and set formatting guidelines."
        },
        {
            "question": "How does the Temperature setting affect LLM responses?",
            "options": [
                "It adjusts the GPU server cooling system.",
                "It controls randomness: low temperature yields deterministic responses; high temperature introduces variety and creativity by flattening probability logits.",
                "It alters context token limits.",
                "It tracks execution time."
            ],
            "answerIndex": 1,
            "explanation": "Temperature scales logit values before Softmax. Values near 0 produce greedy sampling (same output). Values near 1.0 introduce randomness."
        },
        {
            "question": "What is the Context Window of an LLM?",
            "options": [
                "The UI window displaying chats.",
                "The maximum sequence length (in tokens) the model can process in a single forward pass, covering both prompt input and generated output.",
                "The total training dataset file size.",
                "The API request time limit."
            ],
            "answerIndex": 1,
            "explanation": "The context window limits total token capacity (e.g. 8k, 32k, or 1M tokens). Exceeding it requires truncating history or using retrieval."
        },
        {
            "question": "What defines Few-shot prompting?",
            "options": [
                "Training models on few GPUs.",
                "Providing a few complete examples of inputs and desired outputs directly inside the prompt to demonstrate task format before query.",
                "Fine-tuning models on a tiny dataset.",
                "Running inference multiple times."
            ],
            "answerIndex": 1,
            "explanation": "Few-shot prompting leverages the in-context learning of LLMs. Showing examples of matching transformations guides the model to reproduce the target format."
        },
        {
            "question": "What is the objective of Chunking in a RAG ingestion pipeline?",
            "options": [
                "To delete empty lines in source documents.",
                "To split large documents into smaller, semantically coherent segments before vector indexing, ensuring focused embedding calculations and context injections.",
                "To convert markdown into HTML tables.",
                "To encrypt data fields."
            ],
            "answerIndex": 1,
            "explanation": "Chunking aligns document scale. Injecting a whole book exceeds context windows; chunking splits it into focused parts (e.g., 500-token segments) for exact retrieval."
        }
    ],
    "data_engineering": [
        {
            "question": "What are the two core phases of a MapReduce job?",
            "options": [
                "Read and Write phases.",
                "Map (transforming input records) and Reduce (aggregating key-value pairs after shuffling).",
                "Compile and Execute phases.",
                "Load and Partition phases."
            ],
            "answerIndex": 1,
            "explanation": "MapReduce divides work. The Map step processes input lines to produce intermediate key-value sets. The Reduce step summarizes those values per key."
        },
        {
            "question": "Why is Apache Spark faster than legacy Hadoop MapReduce for iterative algorithms?",
            "options": [
                "It runs queries in the web browser.",
                "It performs processing in-memory (RAM) and caches intermediate states, avoiding MapReduce's frequent disk reads and writes.",
                "It uses NoSQL databases internally.",
                "It bypasses network communication entirely."
            ],
            "answerIndex": 1,
            "explanation": "Hadoop writes intermediate step outputs to HDFS disk. Spark keeps data in memory as Resilient Distributed Datasets (RDDs) and updates lazily, boosting speed."
        },
        {
            "question": "What does a Resilient Distributed Dataset (RDD) represent in Spark?",
            "options": [
                "A SQL table stored on a single host.",
                "A read-only, partitioned collection of records that can be operated on in parallel across a cluster with automatic lineage-based fault tolerance.",
                "A backup directory of CSV files.",
                "An index structure for fast search."
            ],
            "answerIndex": 1,
            "explanation": "RDDs are Spark's core abstraction. Distributed across worker nodes, RDDs track transformation history (lineage), allowing partitions to be rebuilt if nodes fail."
        },
        {
            "question": "How are messages distributed within an Apache Kafka Topic?",
            "options": [
                "All messages are written to one single log file.",
                "Topics are split into Partitions distributed across brokers; messages are appended sequentially to partitions using keys for routing.",
                "Messages are stored in MongoDB collections.",
                "Messages are deleted automatically on read."
            ],
            "answerIndex": 1,
            "explanation": "Partitions enable Kafka to scale. A partition is an ordered append-only commit log. Distributing partitions across cluster brokers supports high write and read scaling."
        },
        {
            "question": "What does a Kafka Consumer Group enable?",
            "options": [
                "Running multiple database queries concurrently.",
                "Coordinated parallel reading of topic partitions, where each partition is assigned to exactly one consumer member in the group.",
                "Creating backup copies of Kafka topics.",
                "Compiling stream processing binaries."
            ],
            "answerIndex": 1,
            "explanation": "Consumer groups partition message reading. By coordinating partition assignments, Kafka scales processing: adding group members divides the read workload."
        },
        {
            "question": "What is a Directed Acyclic Graph (DAG) in data workflow orchestration (e.g. Apache Airflow)?",
            "options": [
                "A database schema layout diagram.",
                "A collection of all tasks to run, organized in a way that reflects their relationships and execution dependencies without loop cycles.",
                "A network path routing table.",
                "A type of column-oriented index."
            ],
            "answerIndex": 1,
            "explanation": "Airflow uses DAGs to define workflows. Tasks are represented as nodes. Directed edges define dependencies. The acyclic rule prevents circular dependency loops."
        },
        {
            "question": "How does dbt (data build tool) differ from traditional ETL tools?",
            "options": [
                "It focuses strictly on the 'T' (Transformation) phase in ELT pipelines, compiling SQL models and running them inside the target data warehouse.",
                "It handles data extraction from APIs.",
                "It stores data in-memory on local server nodes.",
                "It compiles SQL into Go binaries."
            ],
            "answerIndex": 0,
            "explanation": "dbt doesn't move data. It acts after data is loaded (ELT), letting analysts write SQL models that dbt compiles and executes as tables/views inside warehouses."
        },
        {
            "question": "What is Schema Evolution in data storage frameworks (like Parquet or Delta Lake)?",
            "options": [
                "Updating database driver software automatically.",
                "The ability to modify database schema definitions (e.g. adding columns) over time without rewriting historical data files.",
                "Deleting old database files when schemas change.",
                "Automatically compiling queries to match new versions."
            ],
            "answerIndex": 1,
            "explanation": "Schema evolution allows column additions or type changes. Query engines read historical data with back-compatibility, avoiding expensive dataset rewrites."
        },
        {
            "question": "What is the difference between Partitioning and Bucketing in large-scale table optimization?",
            "options": [
                "Partitioning is for databases; Bucketing is for cache.",
                "Partitioning divides tables into directories based on column values (e.g. date); Bucketing splits data into fixed files using a hash function on a key.",
                "They are synonyms.",
                "Bucketing encrypts column fields."
            ],
            "answerIndex": 1,
            "explanation": "Partitioning creates folder hierarchies (e.g. `year=2026/month=07`). Bucketing (Clustering) hashes a key column to divide data into equal files within partition paths, optimizing joins."
        },
        {
            "question": "What does Lazy Evaluation mean in Apache Spark execution?",
            "options": [
                "The cluster waits for system idle time before executing jobs.",
                "Spark delays execution of transformations until an Action (e.g. `count()`, `collect()`) is called, enabling optimization of the entire execution plan.",
                "Spark runs computations slowly to save energy.",
                "Queries are executed only on subset samples."
            ],
            "answerIndex": 1,
            "explanation": "Transformations (like `filter()`, `select()`) only build a logical execution plan (DAG). When an action requests output, Spark optimizes and compiles the DAG for execution."
        },
        {
            "question": "What is Change Data Capture (CDC) in data pipelines?",
            "options": [
                "A system for version-controlling SQL files.",
                "A design pattern that identifies and tracks changes (inserts, updates, deletes) in a source database, streaming those events to target systems in real-time.",
                "A data quality validation framework.",
                "A database snapshotting utility."
            ],
            "answerIndex": 1,
            "explanation": "CDC monitors database transaction logs. Whenever modifications occur, events are streamed (e.g. via Debezium and Kafka) to update analytical warehouses immediately."
        },
        {
            "question": "What is the primary difference between Lambda and Kappa data pipeline architectures?",
            "options": [
                "Lambda uses Python; Kappa uses Go.",
                "Lambda processes data through batch and speed layers in parallel; Kappa processes all data using a single stream processing engine, treating batch as historical stream.",
                "Kappa uses SQL databases; Lambda uses NoSQL databases.",
                "Lambda is serverless; Kappa runs on VMs."
            ],
            "answerIndex": 1,
            "explanation": "Lambda balances batch stability and stream latency by using duplicate code paths. Kappa simplifies this by processing all data through a single stream pipeline (e.g., Flink) with raw logs."
        }
    ],
    "cloud_system_design": [
        {
            "question": "What is a key protocol difference between REST and gRPC APIs?",
            "options": [
                "REST uses TCP; gRPC uses UDP.",
                "REST relies on HTTP/1.1 and exchanges JSON/XML text; gRPC uses HTTP/2 and serializes binary data via Protocol Buffers.",
                "REST is stateful; gRPC is stateless.",
                "REST is faster for server-to-server streaming."
            ],
            "answerIndex": 1,
            "explanation": "gRPC leverages HTTP/2 features (like multiplexing, header compression, bidirectional streaming) and binary protobuf encoding to offer high-efficiency server communication."
        },
        {
            "question": "What is the core idea of a Microservices architecture?",
            "options": [
                "Compiling all code into a single massive server executable.",
                "Decomposing an application into a collection of small, loosely coupled, independently deployable services organized around business capabilities.",
                "Running all code on a single developer machine.",
                "Writing applications using tiny javascript packages."
            ],
            "answerIndex": 1,
            "explanation": "Microservices isolate database and code scope. Each service manages its own stack and data, communicating via APIs (REST, gRPC, or messaging), enhancing scale."
        },
        {
            "question": "What is AWS EC2?",
            "options": [
                "A serverless database service.",
                "A web service providing secure, resizable compute capacity in the cloud (Virtual Machines).",
                "An object storage bucket container.",
                "An API routing gateway."
            ],
            "answerIndex": 1,
            "explanation": "Elastic Compute Cloud (EC2) provides virtual machine instances where developers configure operating systems, middleware, and applications manually."
        },
        {
            "question": "What defines AWS Lambda compute execution?",
            "options": [
                "A physical server cabinet allocated to a tenant.",
                "Serverless, event-driven compute service that runs application code automatically in response to triggers, scaling container resources dynamically.",
                "A virtual machine running 24/7.",
                "A managed Redis caching node."
            ],
            "answerIndex": 1,
            "explanation": "Lambda is serverless. Users upload code and set trigger events. Lambda instantiates containers to execute the code, scaling to zero when requests finish, charging by run duration."
        },
        {
            "question": "What is Amazon S3?",
            "options": [
                "A relational database service.",
                "An object storage service offering industry-leading scalability, data availability, security, and performance for files.",
                "A serverless message broker.",
                "An AWS networking load balancer."
            ],
            "answerIndex": 1,
            "explanation": "Simple Storage Service (S3) stores flat files (images, backups, datasets) as key-value objects in buckets, providing high durability and scalability."
        },
        {
            "question": "What is the primary role of a Load Balancer in system design?",
            "options": [
                "To compress database tables.",
                "To distribute incoming network traffic across a group of backend servers to prevent overload and ensure high availability.",
                "To encrypt API request bodies.",
                "To coordinate server database backups."
            ],
            "answerIndex": 1,
            "explanation": "Load Balancers (like Nginx, AWS ALB) sit between clients and servers. They monitor server health and forward requests, optimizing response speeds and uptime."
        },
        {
            "question": "What is an API Gateway used for in microservice architectures?",
            "options": [
                "To store document collections.",
                "As a single entry point that routes requests, handles authentication, collects metrics, and applies rate limiting for all downstream microservices.",
                "To compile code files.",
                "To back up server instances."
            ],
            "answerIndex": 1,
            "explanation": "API Gateways centralize cross-cutting concerns. They shield internal service locations from clients, applying access checks, load routing, and SSL termination."
        },
        {
            "question": "What is the role of Service Discovery in microservices?",
            "options": [
                "To scan code directories for new files.",
                "A mechanism (like Consul, Eureka) that allows service instances to dynamically register their IP addresses and ports so other services can find them.",
                "To find new AWS accounts.",
                "To parse SQL query paths."
            ],
            "answerIndex": 1,
            "explanation": "Microservice instances scale dynamically, changing host IPs. Service Discovery acts as a registry where instances advertise addresses, allowing load routing."
        },
        {
            "question": "What is a major trade-off of Microservices over Monolith architectures?",
            "options": [
                "Microservices are always slower.",
                "Microservices introduce operational complexity (deployment, monitoring, networking, distributed transactions) that monolithic apps avoid.",
                "Monoliths require more servers to run in development.",
                "Microservices cannot access database tables."
            ],
            "answerIndex": 1,
            "explanation": "Monoliths are simple to build and test. Microservices offer decoupling and scalable team organization but add distributed system overhead (network latency, consistency)."
        },
        {
            "question": "What is the difference between Vertical Scaling and Horizontal Scaling?",
            "options": [
                "Vertical scaling is for SQL; Horizontal is for NoSQL.",
                "Vertical scaling adds more resources (CPU, RAM) to a single server; Horizontal scaling adds more server nodes to the resource pool.",
                "Vertical scaling requires compiling binaries; Horizontal scaling does not.",
                "They are synonyms."
            ],
            "answerIndex": 1,
            "explanation": "Vertical scaling (scaling up) hits hardware limits. Horizontal scaling (scaling out) adds nodes to handle traffic, matching distributed design requirements."
        },
        {
            "question": "What is a Message Broker (e.g. RabbitMQ, AWS SQS) used for?",
            "options": [
                "To direct API traffic to target IP endpoints.",
                "To enable asynchronous, decoupled communication between services by queuing messages until receiver services consume them.",
                "To compile code blocks.",
                "To run relational queries."
            ],
            "answerIndex": 1,
            "explanation": "Message brokers enable asynchronous architectures. A service publishes a message and resumes execution; receiver services process tasks asynchronously, reducing system coupling."
        },
        {
            "question": "What is an Event-driven architecture?",
            "options": [
                "An architecture running on specific user interface events (clicks).",
                "A system design pattern where services react to state changes (events) produced and consumed asynchronously via event logs or message channels.",
                "An architecture running only at specified clock times.",
                "A database schema design technique."
            ],
            "answerIndex": 1,
            "explanation": "In event-driven architectures, services communicate by publishing event streams (e.g., 'OrderCreated'). Downstream microservices subscribe and react, decoupling operations."
        }
    ],
    "software_engineering_general": [
        {
            "question": "What is the difference between Git Merge and Git Rebase?",
            "options": [
                "Merge deletes commits; Rebase copies them.",
                "Merge creates a new commit combining branch histories; Rebase moves or applies branch commits on top of another base commit, creating a linear history.",
                "Merge is done locally; Rebase is done on remote servers.",
                "They perform identical operations."
            ],
            "answerIndex": 1,
            "explanation": "`git merge` preserves historical branch structures by adding a merge commit. `git rebase` rewrites history by applying commits sequentially, resulting in a cleaner git log."
        },
        {
            "question": "What is the difference between Unit testing and Integration testing?",
            "options": [
                "Unit tests are run by QA; Integration tests by developers.",
                "Unit tests verify individual components/functions in isolation (using mocks); Integration tests verify interactions between combined modules or systems.",
                "Unit tests require a database; Integration tests do not.",
                "They focus on identical scopes."
            ],
            "answerIndex": 1,
            "explanation": "Unit testing isolated modules ensures base logic works. Integration testing checks how modules collaborate, validating database setups, API calls, and components."
        },
        {
            "question": "Which phase of the Software Development Life Cycle (SDLC) defines user requirements and system specifications?",
            "options": ["Implementation", "Requirement Analysis & Planning", "Testing", "Deployment"],
            "answerIndex": 1,
            "explanation": "Requirement analysis gathers project scopes, user stories, and specs, laying out the foundation before design and coding phases begin."
        },
        {
            "question": "What does the DRY principle stand for in clean coding?",
            "options": [
                "Do Repeat Yourself.",
                "Don't Repeat Yourself (reducing repetition of software patterns through abstraction).",
                "Design Reliable Yields.",
                "Document Runtime Yields."
            ],
            "answerIndex": 1,
            "explanation": "DRY aims to avoid duplicate logic. If code repeats, extracting it to reusable functions or classes reduces bugs when modifying that logic later."
        },
        {
            "question": "Which design principles are represented by the SOLID acronym?",
            "options": [
                "Static, Oriented, Logical, Integrated, Dynamic.",
                "Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion.",
                "Secure, Optimized, Linear, Indexed, Distributed.",
                "Speed, Organization, Leverage, Integration, Delivery."
            ],
            "answerIndex": 1,
            "explanation": "SOLID principles are guidelines for object-oriented design that improve software maintainability, understandability, and scalability."
        },
        {
            "question": "What does Code Refactoring mean?",
            "options": [
                "Rewriting code in a different programming language.",
                "Restructuring existing code to improve internal design and readability without changing its external behavior.",
                "Adding new features to an application.",
                "Compiling source code files."
            ],
            "answerIndex": 1,
            "explanation": "Refactoring improves code health (reducing complexity, cleaning code smells, renaming fields) while ensuring functional regression tests continue to pass."
        },
        {
            "question": "Which of the following describes Git commit message best practices?",
            "options": [
                "Write generic messages like 'fix' or 'update'.",
                "Write a short imperative summary (e.g. 'Fix pointer check') followed by detailed explanations of what changed and why.",
                "Commit messages should contain raw code diffs.",
                "Commit messages are ignored by version control."
            ],
            "answerIndex": 1,
            "explanation": "Clear, structured commit messages help team members trace code history, automate changelogs, and simplify revert operations."
        },
        {
            "question": "What is Continuous Integration (CI)?",
            "options": [
                "Deploying servers dynamically in the cloud.",
                "The practice of merging developer code branches into a shared mainline frequently, automatically running builds and test suites on each commit.",
                "Writing documentation in parallel with coding.",
                "Fusing database tables into single collections."
            ],
            "answerIndex": 1,
            "explanation": "CI checks code regressions automatically. Early detection of merge conflicts and failing tests speeds up release cycles and secures code quality."
        },
        {
            "question": "Why are Code Reviews valuable in team development workflows?",
            "options": [
                "They compile code faster.",
                "They help maintain code standards, share domain knowledge across the team, and catch bugs before code merges to the main branch.",
                "They allocate server resources.",
                "They automate deployment pipelines."
            ],
            "answerIndex": 1,
            "explanation": "Peer review verifies design approaches, improves code readability, and educates team members, acting as a collaborative quality gate."
        },
        {
            "question": "What is Technical Debt?",
            "options": [
                "Financial cost of server hosting.",
                "The implied cost of additional refactoring work caused by choosing an easy, fast solution now instead of a better long-term design.",
                "Fines paid for software license violations.",
                "The storage capacity of code repositories."
            ],
            "answerIndex": 1,
            "explanation": "Technical debt is a metaphor. Speeding features out by skipping tests or structure is like taking a loan: it must be paid back with refactoring interest later."
        },
        {
            "question": "What is the structure of Semantic Versioning (SemVer)?",
            "options": [
                "Year.Month.Day.",
                "MAJOR.MINOR.PATCH (e.g. 2.1.4), where MAJOR increment represents breaking changes, MINOR new features, and PATCH bug fixes.",
                "A random string identifier.",
                "Version numbers incremented sequentially (Version 1, Version 2)."
            ],
            "answerIndex": 1,
            "explanation": "SemVer structures dependencies. Consumers understand if updating a package is safe (PATCH/MINOR) or requires adjusting code (MAJOR breaking update)."
        },
        {
            "question": "What is the primary purpose of Regression Testing?",
            "options": [
                "To test math algorithms.",
                "To ensure that new code changes or bug fixes have not introduced unexpected bugs or broken existing functionality in the application.",
                "To stress-test server load capacity.",
                "To format database indexing."
            ],
            "answerIndex": 1,
            "explanation": "Regression tests run existing test suites against new commits, validating that established behaviors remain correct after modifications."
        }
    ]
}

# Mapping of keywords to categories
KEYWORDS_MAPPING = {
    # Go
    "goroutine": "go",
    "channel": "go",
    "select {": "go",
    "defer ": "go",
    "struct": "go",
    # Python
    "def ": "python",
    "import os": "python",
    "list comprehension": "python",
    "decorator": "python",
    "generator": "python",
    # Java
    "public class": "java",
    "system.out": "java",
    "jvm": "java",
    "springboot": "java",
    "spring_boot": "java",
    # JS/Node
    "const fs =": "javascript_node",
    "require(": "javascript_node",
    "async ": "javascript_node",
    "await ": "javascript_node",
    "express": "javascript_node",
    "middleware": "javascript_node",
    # Relational Database
    "select *": "databases_sql",
    "having ": "databases_sql",
    "inner join": "databases_sql",
    "where ": "databases_sql",
    "index": "databases_sql",
    # NoSQL/Cache
    "redis": "nosql_caching",
    "mongodb": "nosql_caching",
    "cache": "nosql_caching",
    "bson": "nosql_caching",
    # DevOps/Docker
    "docker": "docker_devops",
    "dockerfile": "docker_devops",
    "docker-compose": "docker_devops",
    "container": "docker_devops",
    # Data Science
    "pandas": "pandas_numpy",
    "numpy": "pandas_numpy",
    "dataframe": "pandas_numpy",
    "ndarray": "pandas_numpy",
    # Data Engineering
    "spark": "data_engineering",
    "kafka": "data_engineering",
    "airflow": "data_engineering",
    "dbt": "data_engineering",
    "mapreduce": "data_engineering",
    # ML/DL
    "neural network": "ml_dl_fundamentals",
    "backpropagation": "ml_dl_fundamentals",
    "activation function": "ml_dl_fundamentals",
    "loss function": "ml_dl_fundamentals",
    "pytorch": "ml_dl_fundamentals",
    "tensorflow": "ml_dl_fundamentals",
    # LLM/GenAI
    "rag": "llms_genai",
    "llm": "llms_genai",
    "transformer": "llms_genai",
    "embedding": "llms_genai",
    "prompt": "llms_genai",
    # Cloud/System Design
    "grpc": "cloud_system_design",
    "rest api": "cloud_system_design",
    "aws": "cloud_system_design",
    "lambda": "cloud_system_design",
    "s3": "cloud_system_design",
    "microservice": "cloud_system_design",
}

def get_quizzes_for_file(filepath, content):
    rel_path = os.path.relpath(filepath, base_dir).lower()
    lower_content = content.lower()
    
    # Initialize scores for all categories
    scores = {cat: 0 for cat in CATEGORIES.keys()}
    
    # Path-based scoring (highest priority)
    if "python" in rel_path:
        scores["python"] += 100
    if "java" in rel_path or "springboot" in rel_path or "spring_boot" in rel_path:
        scores["java"] += 100
    if "go.md" in rel_path or "languages/go" in rel_path:
        scores["go"] += 100
    if "nodejs" in rel_path or "express" in rel_path:
        scores["javascript_node"] += 100
    if any(db in rel_path for db in ["mysql", "postgresql", "sqlite", "oracle", "sql"]):
        scores["databases_sql"] += 100
    if any(db in rel_path for db in ["mongodb", "redis", "cassandra", "couchbase", "nosql", "caching"]):
        scores["nosql_caching"] += 100
    if "docker" in rel_path or "devops" in rel_path or "kubernetes" in rel_path:
        scores["docker_devops"] += 100
    if "pandas" in rel_path:
        scores["pandas_numpy"] += 80
    if "numpy" in rel_path:
        scores["pandas_numpy"] += 80
    if "ai_ml" in rel_path or "ai-ml" in rel_path:
        scores["ml_dl_fundamentals"] += 50
        if "llm" in rel_path or "genai" in rel_path or "transformer" in rel_path:
            scores["llms_genai"] += 100
        if "pytorch" in rel_path or "tensorflow" in rel_path:
            scores["ml_dl_fundamentals"] += 80
    if "dataengineer" in rel_path:
        scores["data_engineering"] += 50
        if "spark" in rel_path or "hadoop" in rel_path:
            scores["data_engineering"] += 80
        if "kafka" in rel_path or "streaming" in rel_path:
            scores["data_engineering"] += 80
        if "airflow" in rel_path or "orchestration" in rel_path:
            scores["data_engineering"] += 80
    if "cloud" in rel_path:
        scores["cloud_system_design"] += 100
    if "architecture" in rel_path or "system_design" in rel_path or "design" in rel_path:
        scores["cloud_system_design"] += 80
    if "interview" in rel_path or "career" in rel_path:
        scores["software_engineering_general"] += 50

    # Content-based scoring
    for keyword, cat in KEYWORDS_MAPPING.items():
        if keyword in lower_content:
            scores[cat] += lower_content.count(keyword)

    # Sort categories by score
    sorted_cats = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    best_cat, best_score = sorted_cats[0]
    
    # If no topic has enough score, fallback to general software engineering
    if best_score < 1:
        best_cat = "software_engineering_general"
        
    selected_quizzes = list(CATEGORIES[best_cat])
    
    # Safeguard size (ensure exactly 12 quizzes)
    if len(selected_quizzes) < 12:
        fill_count = 12 - len(selected_quizzes)
        fallback_quizzes = [q for q in CATEGORIES["software_engineering_general"] if q not in selected_quizzes]
        selected_quizzes.extend(fallback_quizzes[:fill_count])
        
    return selected_quizzes[:12]

def process_file(filepath):
    filename = os.path.basename(filepath)
    # Skip python.md and java.md as they are already customized premium docs
    if filename.lower() in ("python.md", "java.md"):
        return False
        
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # --- STEP A: REVERT PREVIOUS INJECTIONS ---
    # Revert Progress Trackers
    content = re.sub(r'<ProgressTracker\s+currentSection=\{\d+\}\s+totalSections=\{\d+\}\s*/>\s*\n*', '', content)
    content = re.sub(r'<ProgressTracker\s+currentSection=\d+\s+totalSections=\d+\s*/>\s*\n*', '', content)

    # Revert Quiz Blocks (reverts any single or multiple Quiz structures globally)
    content = re.sub(r'<Quiz\s+.*?\n/>\s*\n*', '', content, flags=re.DOTALL)
    content = re.sub(r'\n*---\s*\n*### Knowledge Verification Check\s*\n*', '', content)

    # Revert Tabs blocks back to the inner code block
    tabs_pattern = re.compile(
        r'<Tabs>\s*<Tab label="Syntax & Example">\s*\n*(```(python|java|javascript|js|go)\n.*?\n```)\s*\n*</Tab>\s*<Tab label="Interactive Playground">.*?</Tabs>',
        re.DOTALL
    )
    content = re.sub(tabs_pattern, r'\1', content)

    # --- STEP B: APPLY NEW ENRICHMENT ---
    # 1. Parse headings to inject progress trackers
    headings = re.findall(r'^(##\s+.*)$', content, re.MULTILINE)
    total_sections = len(headings)
    
    if total_sections > 0:
        section_idx = 1
        def replace_heading(match):
            nonlocal section_idx
            heading_text = match.group(1)
            tracker = f"<ProgressTracker currentSection={section_idx} totalSections={total_sections} />\n\n"
            section_idx += 1
            return f"{tracker}{heading_text}"
        content = re.sub(r'^(##\s+.*)$', replace_heading, content, flags=re.MULTILINE)
    else:
        content = "<ProgressTracker currentSection={1} totalSections={1} />\n\n" + content

    # 2. Convert code blocks to tabs + playground
    code_block_pattern = re.compile(r'```(python|java|javascript|js|go)\n(.*?)\n```', re.DOTALL)
    
    def replace_code_block(match):
        lang = match.group(1)
        code = match.group(2)
        
        # Skip small snippets
        if len(code.strip().split('\n')) <= 1:
            return match.group(0)
            
        escaped_code = json.dumps(code)[1:-1]
        
        tabs_wrapper = f"""<Tabs>
  <Tab label="Syntax & Example">

```{lang}
{code}
```

  </Tab>
  <Tab label="Interactive Playground">
    <InteractiveExample 
      language="{lang}"
      initialCode="{escaped_code}" 
      instruction="Execute and edit this {lang.upper()} example."
    />
  </Tab>
</Tabs>"""
        return tabs_wrapper

    content = re.sub(code_block_pattern, replace_code_block, content)

    # 3. Generate 12 high-precision quizzes and append them
    quizzes = get_quizzes_for_file(filepath, content)
    
    quiz_components_str = ""
    for quiz_data in quizzes:
        options_str = json.dumps(quiz_data["options"])
        escaped_question = json.dumps(quiz_data["question"])[1:-1]
        escaped_explanation = json.dumps(quiz_data["explanation"])[1:-1]
        quiz_components_str += f"""
<Quiz 
  question="{escaped_question}" 
  options={options_str} 
  answerIndex={quiz_data['answerIndex']} 
  explanation="{escaped_explanation}" 
/>
"""

    quiz_section = f"""

---

### Knowledge Verification Check
{quiz_components_str}"""
    content += quiz_section

    # 4. Save file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
        
    return True

# Walk and modify
updated_count = 0
for root, dirs, files in os.walk(base_dir):
    if "assets" in root or "node_modules" in root:
        continue
    for file in files:
        if file.endswith(".md"):
            filepath = os.path.join(root, file)
            try:
                if process_file(filepath):
                    updated_count += 1
            except Exception as e:
                print(f"Error processing {file}: {str(e)}")

print(f"Successfully re-enriched {updated_count} files with 12 sequential quizzes.")
