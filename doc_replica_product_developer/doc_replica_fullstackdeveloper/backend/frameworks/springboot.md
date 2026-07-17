# Spring Boot Framework (Java)

Spring Boot is an opinionated framework built on top of the Spring framework, providing auto-configuration and embedded servlet containers to streamline Java enterprise backend development.

---

## 1. Dependency Injection & IoC Container

The **Inversion of Control (IoC)** container manages the instantiation, lifecycle, and configuration of Java classes (registered as Spring Beans).

```mermaid
graph TD
    IoC[Spring IoC Container] -->|Instantiates & Injects| Controller[@RestController]
    IoC -->|Instantiates & Injects| Service[@Service Component]
    IoC -->|Instantiates & Injects| Repo[@Repository Interface]
```

---

## 2. Code Demonstration: Spring REST API

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

---

## 3. Core Characteristics
* **Auto-Configuration**: Dynamically configures components based on classpath dependencies (e.g., automatically configuring a DataSource if PostgreSQL driver is present).
* **Spring Boot Starters**: Simplified dependency descriptors to quickly bootstrap specific features (e.g., `spring-boot-starter-web`).
* **JPA/Hibernate ORM**: Provides data persistence layers using Java Persistence API specifications.

---

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

