# Module 18 - CI/CD Integration

## Learning Objectives
* Build and push images using GitHub Actions pipelines, manage registry logins, cache builds, and tag releases.

## Prerequisites
* **Prerequisites**: Module 17

---

## Detailed Explanation
### Container CI/CD Pipeline
In modern DevOps pipelines, every code commit automatically triggers a runner to test the code, build the Docker image, and push it to a registry.

### Example GitHub Actions Workflow (`.github/workflows/docker-publish.yml`)
```yaml
name: Build and Push Docker Image

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v3

      - name: Set up QEMU (for multi-platform support)
        uses: docker/setup-qemu-action@v2

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Log in to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Build and Push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: |
            myusername/myapp:latest
            myusername/myapp:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### Optimization: Remote Cache Storage
By configuring `cache-from` and `cache-to` with Actions Cache (`gha`), subsequent build runners will pull intermediate layers from the GitHub cache, reducing build times from minutes to seconds.

---

## Hands-on Exercise
### Hands-on Exercise: Configure GitHub Secrets
Create a public repository, save dummy login credentials in GitHub Actions Secrets, and draft a test workflow file.

## Assignment
Write a pipeline configuration file for GitLab CI or Bitbucket Pipelines that executes `docker build`.

---

## Quiz

### Q1: What action logs in to Docker registries in GitHub Actions?
- docker/login-action
- docker/log-in
- actions/login
- auth/docker

*Answer*: **docker/login-action**

### Q2: Why should you tag images with the commit SHA in CI?
- To ensure unique, traceable tags for deployments
- To speed up compilation
- To encrypt the image
- To bypass registries

*Answer*: **To ensure unique, traceable tags for deployments**

---

## Interview Preparation

### Q: How can you speed up Docker builds inside cloud CI/CD runners?
*Answer*: By using remote caching features (e.g. BuildKit's gha cache or registry caching), multi-stage builds, and choosing slim baseline images.

---

## Common Mistakes & Troubleshooting
* **Common Mistakes**: Exposing Docker Hub passwords directly in pipeline YAML files instead of using Repository Secrets.
* **Troubleshooting**: If logins fail inside your pipelines, verify secret token expiration limits on Docker Hub.

## Best Practices & Tips
* Always configure build pipelines to tag images with semantic versions or commit SHAs instead of just 'latest'.

---

## Summary & Cheat Sheet
| GitHub Action | Purpose |
|---|---|
| `docker/setup-buildx-action` | Enable BuildKit builders |
| `docker/login-action` | Login to Docker Hub/ECR/GHCR |
| `docker/build-push-action` | Compile and upload image |

---

## References & Further Reading
* Docker GitHub Actions (docs.docker.com/build/ci/github-actions/).
