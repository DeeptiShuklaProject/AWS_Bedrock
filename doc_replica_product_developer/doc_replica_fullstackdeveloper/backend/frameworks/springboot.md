# Spring Boot Framework (Java)

Spring Boot is an opinionated framework built on top of the Spring framework, providing auto-configuration and embedded servlet containers to streamline Java enterprise backend development.

---

<ProgressTracker currentSection=1 totalSections=4 />

## 1. Dependency Injection & IoC Container

The **Inversion of Control (IoC)** container manages the instantiation, lifecycle, and configuration of Java classes (registered as Spring Beans).

```mermaid
graph TD
    IoC[Spring IoC Container] -->|Instantiates & Injects| Controller[@RestController]
    IoC -->|Instantiates & Injects| Service[@Service Component]
    IoC -->|Instantiates & Injects| Repo[@Repository Interface]
```

---

<ProgressTracker currentSection=2 totalSections=4 />

## 2. Code Demonstration: Spring REST API

<Tabs>
  <Tab label="Syntax & Example">

```java
package com.example.demo;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.*;

import jakarta.persistence.*;
import java.util.List;

// 1. Entity Definition
@Entity
@Table(name = "items")
class Item {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String name;

    // Getters and Setters
    public Long getId() { return id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
}

// 2. Data JPA Repository Layer
@Repository
interface ItemRepository extends JpaRepository<Item, Long> {}

// 3. Controller Layer
@RestController
@RequestMapping("/api/items")
class ItemController {

    @Autowired
    private ItemRepository itemRepository;

    @GetMapping
    public List<Item> getAllItems() {
        return itemRepository.findAll();
    }

    @PostMapping
    public Item createItem(@RequestBody Item item) {
        return itemRepository.save(item);
    }
}
```

  </Tab>
  <Tab label="Interactive Playground">
    <InteractiveExample 
      language="java"
      initialCode="package com.example.demo;\n\nimport org.springframework.beans.factory.annotation.Autowired;\nimport org.springframework.data.jpa.repository.JpaRepository;\nimport org.springframework.stereotype.Repository;\nimport org.springframework.stereotype.Service;\nimport org.springframework.web.bind.annotation.*;\n\nimport jakarta.persistence.*;\nimport java.util.List;\n\n// 1. Entity Definition\n@Entity\n@Table(name = \"items\")\nclass Item {\n    @Id\n    @GeneratedValue(strategy = GenerationType.IDENTITY)\n    private Long id;\n    private String name;\n\n    // Getters and Setters\n    public Long getId() { return id; }\n    public String getName() { return name; }\n    public void setName(String name) { this.name = name; }\n}\n\n// 2. Data JPA Repository Layer\n@Repository\ninterface ItemRepository extends JpaRepository<Item, Long> {}\n\n// 3. Controller Layer\n@RestController\n@RequestMapping(\"/api/items\")\nclass ItemController {\n\n    @Autowired\n    private ItemRepository itemRepository;\n\n    @GetMapping\n    public List<Item> getAllItems() {\n        return itemRepository.findAll();\n    }\n\n    @PostMapping\n    public Item createItem(@RequestBody Item item) {\n        return itemRepository.save(item);\n    }\n}" 
      instruction="Execute and edit this JAVA example."
    />
  </Tab>
</Tabs>

---

<ProgressTracker currentSection=3 totalSections=4 />

## 3. Core Characteristics
* **Auto-Configuration**: Dynamically configures components based on classpath dependencies (e.g., automatically configuring a DataSource if PostgreSQL driver is present).
* **Spring Boot Starters**: Simplified dependency descriptors to quickly bootstrap specific features (e.g., `spring-boot-starter-web`).
* **JPA/Hibernate ORM**: Provides data persistence layers using Java Persistence API specifications.

---

<ProgressTracker currentSection=4 totalSections=4 />

## 4. Project Creation & Execution Commands

### Scaffolding a New Project
```bash
# Bootstrap a new project using Spring Initializr CLI
curl https://start.spring.io/starter.zip -d dependencies=web,data-jpa -d javaVersion=21 -o myapp.zip
unzip myapp.zip -d myapp
cd myapp
```

### Building & Running the Application
```bash
# Build and run the project using Maven Wrapper (automatically installs dependencies)
./mvnw spring-boot:run

# For Gradle projects:
./gradlew bootRun
```

### Packaging for Production
```bash
# Package the application into a runnable fat JAR file
./mvnw clean package

# Run the packaged production JAR
java -jar target/demo-0.0.1-SNAPSHOT.jar
```

---

### Knowledge Verification Check

<Quiz 
  question="How does Java achieve platform independence?" 
  options=["By compiling code directly to raw hardware machine instructions.", "By compiling source code to bytecode, which is then executed by the Java Virtual Machine (JVM).", "By dynamically translating Java into Javascript at runtime.", "By executing code directly from raw `.java` text files."] 
  answerIndex=1 
  explanation="Java code is compiled into platform-neutral bytecode (`.class` files), which the JVM translates into machine instructions for the host platform." 
/>

<Quiz 
  question="In the JVM memory model, where are objects allocated and where are local variables stored?" 
  options=["Objects on the Stack, local variables on the Heap.", "Objects and local variables are both stored on the Stack.", "Objects on the Heap, local variables on the Stack.", "Objects and local variables are both stored on the Heap."] 
  answerIndex=2 
  explanation="The Heap memory area is used for dynamic allocation of objects, while the Stack contains method frames storing local variables and reference pointers." 
/>

<Quiz 
  question="What is the primary role of the Java Garbage Collector (GC)?" 
  options=["To optimize SQL queries in databases.", "To automatically reclaim memory by deleting objects that are no longer reachable in the application code.", "To compile Java files into JAR archives.", "To monitor system file permissions."] 
  answerIndex=1 
  explanation="The JVM Garbage Collector manages memory by automatically tracking object reachability and freeing up Heap space occupied by unreachable objects." 
/>

<Quiz 
  question="Which access modifier in Java restricts visibility strictly to the declaring class itself?" 
  options=["public", "protected", "private", "default (no modifier)"] 
  answerIndex=2 
  explanation="The `private` access modifier limits access exclusively to fields, methods, or constructors within the class where they are declared." 
/>

<Quiz 
  question="What is a major difference between an interface and an abstract class in Java?" 
  options=["Interfaces can hold instance fields, abstract classes cannot.", "A class can implement multiple interfaces, but can extend only one abstract class.", "Interfaces must contain method bodies, abstract classes cannot.", "Abstract classes cannot declare constructors."] 
  answerIndex=1 
  explanation="Java supports single class inheritance (only one abstract class can be extended) but multiple interface implementation." 
/>

<Quiz 
  question="What does the `@RestController` annotation do in a Spring Boot application?" 
  options=["It registers the class as a database access repository.", "It combines `@Controller` and `@ResponseBody`, serializing return values (like objects) directly into HTTP responses (typically JSON).", "It launches a background compilation process.", "It maps a class to a container load balancer."] 
  answerIndex=1 
  explanation="`@RestController` simplifies REST API creation. It tells Spring Boot that handlers return serialized data objects rather than routing to HTML templates." 
/>

<Quiz 
  question="In Spring Boot, how does the `@Autowired` annotation facilitate dependency injection?" 
  options=["It automatically compiles dependencies on startup.", "It allows the Spring context to automatically resolve and inject matching bean dependencies into fields, constructors, or setters.", "It downloads external dependencies from Maven Central.", "It starts a new server thread for bean instances."] 
  answerIndex=1 
  explanation="`@Autowired` directs Spring Boot's dependency injection container to automatically wire matching bean components into the decorated construct." 
/>

<Quiz 
  question="What is the key difference between Checked and Unchecked exceptions in Java?" 
  options=["Checked exceptions occur at runtime, unchecked exceptions occur at compile time.", "Checked exceptions must be declared in throws or caught; unchecked exceptions (RuntimeException) do not require compile-time handling.", "Unchecked exceptions can never be caught in code.", "Checked exceptions consume more CPU cycles to process."] 
  answerIndex=1 
  explanation="Checked exceptions are verified at compile time. Unchecked exceptions extend `RuntimeException` and represent programming bugs (like NullPointerException) that are resolved at runtime." 
/>

<Quiz 
  question="How does a Java `HashMap` resolve collision when two keys have the same hash code?" 
  options=["It overwrites the old key-value pair immediately.", "It throws a RuntimeException.", "It stores colliding nodes in a linked list (or red-black tree) associated with that hash bucket.", "It resizes the map dynamically to double its size."] 
  answerIndex=2 
  explanation="HashMap uses chaining. Colliding entries are placed in a linked list at the bucket index. If the bucket exceeds a threshold (8), Java 8+ converts it to a red-black tree." 
/>

<Quiz 
  question="What are the states that a Java Thread can enter during its lifecycle?" 
  options=["Active, Inactive, Completed.", "NEW, RUNNABLE, BLOCKED, WAITING, TIMED_WAITING, TERMINATED.", "Starting, Working, Finished.", "Local, Global, Shared."] 
  answerIndex=1 
  explanation="Java threads follow a strict state diagram represented by the `Thread.State` enum: NEW, RUNNABLE, BLOCKED, WAITING, TIMED_WAITING, and TERMINATED." 
/>

<Quiz 
  question="What is the difference between method overloading and method overriding in Java?" 
  options=["Overloading is done in subclassing, overriding is done within the same class.", "Overloading is determined at compile-time (same method name, different signatures), overriding at runtime (replaces parent method in subclass).", "Overloading changes return type only, overriding changes parameters.", "There is no difference; they are synonymous."] 
  answerIndex=1 
  explanation="Method overloading is compile-time polymorphism (same name, different arguments). Method overriding is run-time polymorphism (subclass overrides parent method with identical signature)." 
/>

<Quiz 
  question="What does the `synchronized` keyword enforce in Java?" 
  options=["It forces compilation to run synchronously.", "It ensures that only one thread can execute a block or method on a locked object at any given time, preventing race conditions.", "It automatically runs code in parallel across all CPU cores.", "It updates local fields directly to database records."] 
  answerIndex=1 
  explanation="`synchronized` utilizes monitor locks (intrinsic locks) on objects, ensuring mutually exclusive thread access to critical sections of multi-threaded code." 
/>
