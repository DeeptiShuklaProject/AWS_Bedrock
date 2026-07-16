# 06_Chapter_project_setup

## 🎯 Learning Objectives
In this chapter, you will learn how to:
- Initialize a Python virtual environment.
- Synchronize project packages using the `uv` toolchain.
- Manage dependencies using lockfiles.
- Validate your active package versions.

### Importance of This Chapter
Using a package manager like `uv` ensures that dependency versions are resolved consistently, reducing the risk of package mismatches across local and cloud environments.

---

## 📦 Technical Terms Explained

> **📦 Technical Term Explained**
>
> **Term:** Package Manager
>
> **Simple Explanation:** A package manager is a tool that automates the process of installing, upgrading, configuring, and removing software packages or libraries for a programming language.
>
> **Why do we need it?** It handles downloading external dependencies and resolving version requirements.
>
> **Where is it used?** In your terminal to install libraries (e.g. `pip install` or `uv sync`).

---

> **📦 Technical Term Explained**
>
> **Term:** Lockfile
>
> **Simple Explanation:** A lockfile is a generated file that records the exact version of every package and sub-dependency installed in a project.
>
> **Why do we need it?** It ensures that every developer and deployment environment uses the exact same package versions, preventing "works on my machine" bugs.
>
> **Where is it used?** Automatically read and updated by package managers (e.g. `uv.lock` or `package-lock.json`).

---

## 🛠️ Step-by-Step Installation and Sync

Follow these steps to configure your environment.

### Step 1: Create a Virtual Environment
1. Open your terminal at the project root directory.
2. Execute the environment creation command:
   ```bash
   uv venv
   ```
- **Why this is required:** Isolates project-specific packages from other Python projects.
- **Expected Output:**
  ```text
  Using Python 3.11.5 interpreter at: C:\Users\...\python.exe
  Creating virtual environment at: .venv
  Activate with: .venv\Scripts\activate
  ```

---

### Step 2: Activate the Virtual Environment
1. To active the environment for your terminal session:
   - **Windows (PowerShell):**
     ```powershell
     .venv\Scripts\activate.ps1
     ```
   - **macOS / Linux:**
     ```bash
     source .venv/bin/activate
     ```

---

### Step 3: Synchronize Dependencies
1. To install the dependencies defined in your project settings:
   ```bash
   uv sync
   ```
- **Why this is required:** Downloads and compiles the exact dependency package versions required by the application.
- **Expected Output:**
  ```text
  Resolved 48 packages in 452ms
  Installed 48 packages in 1.2s
   + boto3 v1.34.40
   + strands-agents v0.1.2
   + bedrock-agent-core-starter-toolkit v0.1.0
  ```

---

## 📝 Practical Exercise
Initialize a new virtual environment using `uv venv`, activate it, and run `uv pip list` to check the installed packages.

---

## 🔄 Chapter Recap
- We set up our virtual environment using `uv`.
- We synchronized dependencies, locking package versions in `uv.lock`.
- We are ready to inspect our environment and configure properties in the configuration files.
