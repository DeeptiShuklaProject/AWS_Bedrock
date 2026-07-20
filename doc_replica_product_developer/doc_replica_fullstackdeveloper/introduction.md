# Full Stack Developer Guide

Welcome to the Full Stack Developer guide. This document serves as a comprehensive reference for designing, building, and maintaining modern web applications from frontend to backend.

---

<ProgressTracker currentSection=1 totalSections=3 />

## 1. Core Architecture Pattern

Modern full-stack web applications leverage a decoupled client-server architecture to ensure high performance, scalability, and clean separation of concerns.

```mermaid
graph TD
    A[Client Browser] <-->|HTTPS / WebSockets| B[API Gateway / Reverse Proxy]
    B <-->|REST / GraphQL| C["Application Server (Node.js/FastAPI)"]
    C <-->|SQL/NoSQL| D[(Database System)]
    C <-->|Cache| E[(Redis Cache)]
```

### Frontend vs Backend Architecture

| Tier | Primary Technologies | Core Responsibilities | Key Performance Metrics |
| :--- | :--- | :--- | :--- |
| **Frontend** | React, Next.js, HTML5, CSS3, JavaScript/TypeScript | User interface, State management, Routing, Client-side validation | LCP, FID, CLS, Page Load Time |
| **Backend** | Node.js, Express, FastAPI, Python, Go | Business logic, Data authorization, Database queries, APIs | Latency, Throughput, Error Rate |
| **Data** | PostgreSQL, MongoDB, Redis | Persistent storage, Caching, Relational integrity | Query time, Connection Pool health |

---

<ProgressTracker currentSection=2 totalSections=3 />

## 2. Frontend Development

A great frontend must be responsive, performant, and offer rich aesthetics.

### Key Concepts:
1. **Component-Driven Design**: Build UI components using Atomic Design principles.
2. **State Management**: Use React Context, Redux Toolkit, or Zustand to manage global client state.
3. **Optimized Rendering**: Leverage Server-Side Rendering (SSR), Static Site Generation (SSG), and Incremental Static Regeneration (ISR) via frameworks like Next.js.
4. **Premium Styling**: Use vanilla CSS or modern CSS-in-JS solutions with CSS Variables for theme consistency.

<Tabs>
  <Tab label="Syntax & Example">

```javascript
// Example React Component with Clean State Handling
import React, { useState, useEffect } from 'react';

export const UserProfile = ({ userId }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;
    const fetchUser = async () => {
      try {
        const res = await fetch(`/api/users/${userId}`);
        const data = await res.json();
        if (active) setUser(data);
      } catch (err) {
        console.error(err);
      } finally {
        if (active) setLoading(false);
      }
    };
    fetchUser();
    return () => { active = false; };
  }, [userId]);

  if (loading) return <div className="spinner">Loading Profile...</div>;
  if (!user) return <div>User not found.</div>;

  return (
    <div className="profile-card">
      <img src={user.avatarUrl} alt={user.name} />
      <h3>{user.name}</h3>
      <p>{user.email}</p>
    </div>
  );
};
```

  </Tab>
  <Tab label="Interactive Playground">
    <InteractiveExample 
      language="javascript"
      initialCode="// Example React Component with Clean State Handling\nimport React, { useState, useEffect } from 'react';\n\nexport const UserProfile = ({ userId }) => {\n  const [user, setUser] = useState(null);\n  const [loading, setLoading] = useState(true);\n\n  useEffect(() => {\n    let active = true;\n    const fetchUser = async () => {\n      try {\n        const res = await fetch(`/api/users/${userId}`);\n        const data = await res.json();\n        if (active) setUser(data);\n      } catch (err) {\n        console.error(err);\n      } finally {\n        if (active) setLoading(false);\n      }\n    };\n    fetchUser();\n    return () => { active = false; };\n  }, [userId]);\n\n  if (loading) return <div className=\"spinner\">Loading Profile...</div>;\n  if (!user) return <div>User not found.</div>;\n\n  return (\n    <div className=\"profile-card\">\n      <img src={user.avatarUrl} alt={user.name} />\n      <h3>{user.name}</h3>\n      <p>{user.email}</p>\n    </div>\n  );\n};" 
      instruction="Execute and edit this JAVASCRIPT example."
    />
  </Tab>
</Tabs>

---

<ProgressTracker currentSection=3 totalSections=3 />

## 3. Backend & API Engineering

A robust backend exposes structured, secure APIs and executes efficient business logic.

### API Best Practices:
* **RESTful Standards**: Use proper HTTP verbs (`GET`, `POST`, `PUT`, `DELETE`) and status codes (`200 OK`, `201 Created`, `400 Bad Request`, `401 Unauthorized`, `500 Server Error`).
* **Security & Authentication**: Secure API endpoints with JWT, OAuth2, and CORS configurations.
* **Input Validation**: Validate payload schemas strictly at the API boundaries (e.g., using Pydantic or Joi).
* **Database Optimization**: Optimize queries using indexing, pagination, and query logging.

---

### Knowledge Verification Check

<Quiz 
  question="How does Node.js handle asynchronous operations if JavaScript is single-threaded?" 
  options=["By spawning a new CPU thread for each async callback.", "Using an Event Loop to offload non-blocking I/O tasks to the OS kernel or a thread pool, processing results sequentially when the call stack is empty.", "By compiling JavaScript code to a multithreaded native application.", "Through cooperative process-forking on multi-core servers."] 
  answerIndex=1 
  explanation="Node.js uses a single-threaded Event Loop that delegates asynchronous tasks (such as network or file operations) to system APIs or libuv's thread pool, processing callbacks sequentially." 
/>

<Quiz 
  question="What are the states of a JavaScript Promise?" 
  options=["Started, Running, Stopped.", "pending, fulfilled, rejected.", "Active, Resolved, Terminated.", "Waiting, Done, Failed."] 
  answerIndex=1 
  explanation="A Promise is always in one of three mutually exclusive states: pending (initial state), fulfilled (operation completed successfully), or rejected (operation failed)." 
/>

<Quiz 
  question="How does `async/await` relate to JavaScript Promises?" 
  options=["It compiles Javascript to native asynchronous C code.", "It is syntactic sugar built on top of Promises, making asynchronous code write and read like synchronous code.", "It deletes Promises entirely from runtime memory.", "It forces callbacks to run in parallel threads."] 
  answerIndex=1 
  explanation="`async` functions automatically return a Promise. The `await` keyword pauses execution of the async function until the awaited Promise resolves, making async code highly readable." 
/>

<Quiz 
  question="What parameters do Express.js middleware functions receive in their execution signature?" 
  options=["Only the request object (`req`).", "The Request (`req`), Response (`res`), and a call-forwarding function (`next`).", "The database client and router instances.", "System process and port information."] 
  answerIndex=1 
  explanation="Express middleware signature accepts `(req, res, next)`. This gives it access to request data, response handling, and control routing to subsequent handlers via `next()`." 
/>

<Quiz 
  question="What is a closure in JavaScript?" 
  options=["A function that automatically closes database connections.", "The combination of a function bundled together with references to its surrounding state (the lexical environment).", "A compile-time block syntax warning.", "An object that cannot hold properties."] 
  answerIndex=1 
  explanation="A closure allows an inner function to access variables from its outer (enclosing) scope even after the outer function has finished executing." 
/>

<Quiz 
  question="What is the difference between CommonJS and ES Modules (ESM) in Node.js?" 
  options=["CommonJS uses `require()` and `module.exports`, while ES Modules use `import` and `export` statements.", "CommonJS is asynchronous, while ESM is synchronous.", "CommonJS runs only in the browser, while ESM runs only in Node.js.", "There is no difference in syntax."] 
  answerIndex=0 
  explanation="CommonJS is Node's historical module system using `require`/`module.exports`. ESM is the ES6 standard using `import`/`export`, which supports static analysis and tree shaking." 
/>

<Quiz 
  question="Which C++ library does Node.js rely on to manage its thread pool and asynchronous event processing?" 
  options=["V8", "libuv", "Webpack", "Boost"] 
  answerIndex=1 
  explanation="Node.js uses the libuv library to handle the event loop, thread pool workers, file system notifications, and asynchronous networking events." 
/>

<Quiz 
  question="How does prototypical inheritance work in JavaScript?" 
  options=["Objects copy all properties from a class blueprint on instantiation.", "Objects inherit properties and methods directly from other objects via a prototype chain link.", "Inheritance is resolved strictly at compile time.", "JavaScript does not support inheritance."] 
  answerIndex=1 
  explanation="Every JS object has a link to a prototype object. When a property or method is requested, JS searches the object first, then traverses up the prototype chain until found or null is reached." 
/>

<Quiz 
  question="What is the scoping difference between `var`, `let`, and `const`?" 
  options=["`var` is block-scoped, while `let` and `const` are function-scoped.", "`var` is function-scoped (or global), while `let` and `const` are block-scoped.", "`const` is globally scoped, while `let` is locally scoped.", "All three share identical scoping rules."] 
  answerIndex=1 
  explanation="`var` is scoped to its declaring function. `let` and `const` are block-scoped (scoped to the nearest `{}` block). Additionally, `const` cannot be reassigned." 
/>

<Quiz 
  question="Which array method returns a single accumulated value by running a callback on each element?" 
  options=["map", "filter", "reduce", "forEach"] 
  answerIndex=2 
  explanation="The `reduce` method executes a reducer function on each array element, accumulating the results into a single value (e.g. summing numbers)." 
/>

<Quiz 
  question="What is the difference between `==` and `===` operators in JavaScript?" 
  options=["`==` is strict equality, while `===` performs type coercion.", "`==` performs type coercion before comparison, while `===` compares both value and type strictly.", "They behave identically.", "`==` is used for objects, `===` is used for primitive types."] 
  answerIndex=1 
  explanation="The loose equality operator (`==`) converts operands to a common type (coercion) before comparing. The strict equality operator (`===`) compares value and type without conversion." 
/>

<Quiz 
  question="What is the purpose of Node's `EventEmitter` class?" 
  options=["To manage browser mouse click events.", "To implement the observer pattern, allowing objects to emit named events that trigger registered listener callbacks.", "To execute database transactions.", "To create child server processes."] 
  answerIndex=1 
  explanation="The `EventEmitter` class in Node's `events` module enables event-driven programming, facilitating asynchronous communication between different components of an app." 
/>
