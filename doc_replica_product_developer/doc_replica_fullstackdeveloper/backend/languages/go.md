# Go Backend Engineering

Go (Golang) is a statically typed, compiled programming language designed at Google. It features a fast compiler, built-in garbage collection, structural typing, and first-class concurrency support using goroutines.

## Installation & Downloads

To install Go (Golang) on your machine:
1. Navigate to the [Official Go Downloads Page](https://go.dev/dl/).
2. Download the packaged installer corresponding to your Operating System (e.g. `.msi` for Windows, `.pkg` for macOS, or `.tar.gz` archive for Linux).
3. Run the installer and proceed with the prompts.
4. Verify the Go bin directory (usually `C:\Program Files\Go\bin` or `/usr/local/go/bin`) is in your system `PATH`.
5. Verify the installation by running:
   ```bash
   go version
   ```

### Official Download Portal
![Go Downloads Page](../../../assets/go_download.png)

---

## 1. Go Concurrency Model: Communicating Sequential Processes (CSP)

Go avoids shared memory synchronization (locks/mutexes) by utilizing channels to pass data between goroutines.

```mermaid
graph LR
    subgraph Go Runtime Scheduler
        G1[Goroutine A] -->|Send Data| Chan[Go Channel]
        Chan -->|Receive Data| G2[Goroutine B]
    end
    Scheduler[OS Thread Pool] <-->|M:N Scheduler| GoRuntime[Go Runtime Engine]
```

### Core Architecture:
* **Compiled to Native Code**: Go compiles directly to a single, statically linked machine binary containing no virtual machines or heavy external dependency runtimes.
* **Goroutines**: Lightweight execution threads managed by the Go runtime rather than the OS. Goroutines start with a small stack size (approx. 2KB) and scale dynamically, allowing backends to spawn millions of concurrent routines.
* **Channels**: Typed conduits through which goroutines synchronize execution and share data.

---

## 2. Pointers & Structs

Go is not a traditional object-oriented language; it uses structs to model data and interfaces to model behaviors.

### Code Demonstration: Structs, Pointers, and Methods
```go
package main

import (
	"errors"
	"fmt"
)

// Item defines a generic framework database resource structure
type Item struct {
	ID          int
	Name        string
	Description string
}

// ModifyDescription modifies the item struct using a pointer receiver
func (item *Item) ModifyDescription(newDesc string) {
	// Pointers allow directly mutating the underlying struct memory instead of copying it
	item.Description = newDesc
}

func main() {
	// Create struct instance
	myResource := Item{ID: 1, Name: "Asset A", Description: "Raw data"}

	// Invoke method using pointer reference
	myResource.ModifyDescription("Cleaned analytical record")

	fmt.Printf("Resource: %s (Desc: %s)\n", myResource.Name, myResource.Description)
}
```

---

## 3. Concurrency in Action: Goroutines & Channels

```go
package main

import (
	"fmt"
	"time"
)

// Worker function executing simulated asynchronous API work
func fetchDatabaseRecord(id int, dataChannel chan<- string) {
	time.Sleep(100 * time.Millisecond) // Simulate network delay
	dataChannel <- fmt.Sprintf("Fetched database row content for ID %d", id)
}

func main() {
	// Create buffered channel to receive string outputs
	dataChannel := make(chan string, 3)

	// Spawn 3 concurrent workers using the "go" keyword
	for i := 1; i <= 3; i++ {
		go fetchDatabaseRecord(i, dataChannel)
	}

	// Read outputs from the channel as they arrive
	for i := 1; i <= 3; i++ {
		record := <-dataChannel
		fmt.Println("Receiver Queue:", record)
	}
}
```

---

## 4. Key Go Frameworks & Tools
* **Gin / Fiber**: High-performance HTTP routers for API routing.
* **Go Modules**: Dependency management configured in `go.mod`.
* **Gofmt**: In-built code formatter to enforce a single code style.
