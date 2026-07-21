# 06_Chapter_project_setup

## 1. Introduction
Standardizing local development configurations requires isolated virtual environments and locked dependency packages.

> **Analogy:** Think of a sterile surgical room. Only approved, sterilized tools (packages) are brought in, following an inventory manifest (uv.lock) to prevent external contamination.

---

## 2. Learning Objectives
By the end of this chapter, you will be able to:
- In this chapter, you will learn how to:
- - Initialize a Python virtual environment.
- - Synchronize project packages using the `uv` toolchain.
- - Manage dependencies using lockfiles.
- - Validate your active package versions.

---

## 3. Prerequisites
* Active toolchain installations and workspace directories from Chapter 2 and 4.

---

## 4. Background Theory
Dependency drift occurs when package updates introduce breaking changes. To ensure that an application runs identically in dev, staging, and production, package versions must be locked. Traditional tools like `pip` install packages globally by default, risking conflicts. Modern workflows isolate environments using virtual environments and lock the complete dependency tree (including transitive dependencies) in a lockfile, ensuring deterministic builds.

---

## 5. Core Concepts
**📦 Technical Term: Package Manager**

* **Simple Explanation:** A tool that automates installing, updating, and removing software packages.
* **Why it exists:** Simplifies dependency resolution and version management.
* **Where is it used:** The `uv` or `pip` command-line tools.

**📦 Technical Term: Virtual Environment**

* **Simple Explanation:** An isolated directory tree containing its own Python installation and packages.
* **Why it exists:** Prevents library version conflicts between projects.
* **Where is it used:** The local `.venv/` folder.

**📦 Technical Term: Lockfile**

* **Simple Explanation:** A file listing the exact version and checksum of every package in the dependency tree.
* **Why it exists:** Guarantees identical builds across all environments.
* **Where is it used:** The `uv.lock` file.

---

## 6. Internal Mechanics
1. Developer runs `uv venv` to scaffold an isolated environment.
2. Running `uv sync` reads the dependencies listed in `pyproject.toml`.
3. The solver resolves version constraints and writes the resolved tree to `uv.lock`.
4. Packages are downloaded, verified against checksums, and installed into `.venv/lib/site-packages`.

---

## 7. Architecture Overview
The following architectural details outline the components and relationship schemas active in this module:

```mermaid
graph TD
    Project[Project Workspace] -->|uv venv| Venv[.venv Folder]
    Venv -->|uv sync| Packages[Installed Packages]
    Packages -->|Locks Versions| D[uv.lock File]
```

---

## 8. Installation & Setup
Initialize the virtual environment and synchronize dependencies using `uv`:
```bash
uv venv
```
Activate the environment:
- **Windows (PowerShell):**
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  source .venv/bin/activate
  ```
Synchronize packages:
```bash
uv sync
```

---

## 9. Configuration
Dependencies are declared in the `pyproject.toml` file under the `dependencies` key:
```toml
[project]
name = "agentcore-project"
version = "0.1.0"
dependencies = [
    "boto3>=1.34.0",
    "bedrock-agent-core>=1.0.0"
]
```

---

## 10. Hands-on Examples
### Simple Example
```python
# Verify virtual environment status using python sys parameters
import sys

def check_venv():
    # sys.prefix changes when inside a virtual environment
    is_venv = sys.prefix != sys.base_prefix
    print("Is virtual environment active?", is_venv)
    print("Active Python executable path:", sys.executable)

if __name__ == "__main__":
    check_venv()
```

### Intermediate Example
```python
# Script to check if all dependencies in pyproject.toml are installed in venv
import pkg_resources
import tomllib

def check_packages():
    try:
        with open("pyproject.toml", "rb") as f:
            config = tomllib.load(f)
        deps = config.get("project", {}).get("dependencies", [])
        print("Checking declared dependencies:")
        for dep in deps:
            pkg_name = dep.split(">=")[0].split("==")[0].strip()
            try:
                dist = pkg_resources.get_distribution(pkg_name)
                print(f"- [OK] {pkg_name} is installed: {dist.version}")
            except pkg_resources.DistributionNotFound:
                print(f"- [FAIL] {pkg_name} is missing!")
    except FileNotFoundError:
        print("pyproject.toml not found in current folder.")

if __name__ == "__main__":
    check_packages()
```

### Advanced Example
```python
# Complete automated setup audit and sync verification script
import subprocess
import sys
import os

def audit_environment():
    if not os.path.exists(".venv"):
        print("Virtual environment '.venv' is missing. Creating...")
        subprocess.run(["uv", "venv"], check=True)
    
    print("Synchronizing dependency configurations...")
    res = subprocess.run(["uv", "sync"], capture_output=True, text=True)
    if res.returncode == 0:
        print("[SUCCESS] Dependencies synchronized successfully!")
        # List installed packages
        res_list = subprocess.run(["uv", "pip", "list"], capture_output=True, text=True)
        print(res_list.stdout)
    else:
        print("[FAIL] Dependency sync failed:")
        print(res.stderr)
        sys.exit(1)

if __name__ == "__main__":
    audit_environment()
```

---

## 11. Code Walkthrough
Let's perform a line-by-line code walk of the core logic implementation:

```python
# Verify virtual environment status using python sys parameters
import sys

def check_venv():
    # sys.prefix changes when inside a virtual environment
    is_venv = sys.prefix != sys.base_prefix
    print("Is virtual environment active?", is_venv)
    print("Active Python executable path:", sys.executable)

if __name__ == "__main__":
    check_venv()
```

* **`import` statements:** Load libraries and core modules required by the package.
* **Initialization:** Instantiates execution frameworks and logs operational events.
* **Handler logic:** Executes input validations and triggers core business routines.

---

## 12. Production Best Practices
* Always exclude the `.venv/` directory from version control by adding it to `.gitignore`.
* Always commit `uv.lock` to ensure all developers use identical package versions.
* Use `uv sync --frozen` in CI/CD pipelines to prevent updating dependencies during builds.

---

## 13. Security Considerations
Regularly audit installed packages for known security vulnerabilities using `uv pip tree` or security scanners. Keep dependencies updated to apply patches for security advisories.

---

## 14. Performance Optimization
Leverage `uv`'s global package caching. It shares package compilations across workspaces, eliminating redundant downloads and reducing install times.

---

## 15. Cost Optimization
Package sync operations are performed locally and do not consume cloud resources or incur AWS charges.

---

## 16. Common Mistakes
* Committing the `.venv` folder to Git, bloating the repository size.
* Installing packages globally using administrative permissions instead of isolating them in a local virtual environment.

---

## 17. Troubleshooting
Below is the diagnostic reference table for identifying and resolving issues:

| Symptom | Root Cause | Solution |
| :--- | :--- | :--- |
| uv sync fails with version conflict | Conflicting dependencies declared in pyproject.toml. | Audit declared version constraints and update pyproject.toml to resolve conflicts. |
| Python interpreter mismatches | The local system Python version is incompatible with the project settings. | Configure uv to build using a specific Python version: 'uv venv --python 3.11'. |

---

## 18. Interview Questions
### Q: Why is pyproject.toml preferred over setup.py in modern Python?
* **Answer:** It standardizes configuration by replacing execution scripts (`setup.py`) with declarative settings, separating metadata, dependencies, and tool options into a single schema file.

### Q: What is the difference between requirements.txt and a lockfile?
* **Answer:** `requirements.txt` typically lists top-level packages with loose version bounds. A lockfile lists the exact version, source, and hash of all packages and dependencies, ensuring deterministic builds.

### Q: How does uv achieve faster performance compared to standard pip?
* **Answer:** uv is written in Rust, resolves dependency graphs concurrently, and utilizes a global package cache to reuse built files across workspaces.

---

## 19. Real-World Use Cases
Establishing clean workspaces for new Python projects to manage dependencies.

---

## 20. Industrial Project
This setup configures the Python environment, allowing us to import the SDK and run the application in Chapter 8.

---

## 21. Summary
This chapter covered setting up isolated Python virtual environments, managing dependencies in `pyproject.toml`, and using `uv` to synchronize packages.

---

## 22. Key Takeaways
* Virtual environments prevent package conflicts.
* Lockfiles ensure reproducible builds across environments.
* The `uv` toolchain accelerates package management tasks.

---

## 23. Practice Exercises
* Beginner: Delete the `.venv` folder and run `uv sync` to restore the environment.
* Intermediate: Add the `requests` library to `pyproject.toml` and synchronize packages to verify lockfile updates.

---

## 24. Further Reading
* [uv Package Manager Documentation](https://docs.astral.sh/uv/)
* [PEP 518 - Specifying Build Requirements](https://peps.python.org/pep-0518/)
