# Skill: YouTube Course YAML Generator

This document (Skill File) defines the workflow and instructions for an AI assistant to automatically generate a structured YAML configuration file (like `uday.yaml`) from a single YouTube playlist or video URL.

---

## 📋 Input Parameters

To trigger the YAML generation, provide:
* **Playlist_URL:** The URL of the YouTube playlist or video.
* **Target_File_Name:** The destination YAML file path (e.g., `uday.yaml`).

---

## ⚙️ Execution Pipeline

### Step 1: Video Metadata Extraction
* Fetch the playlist webpage or call public oEmbed/metadata APIs to retrieve:
  - Total number of videos/tracks in the playlist.
  - The title and video ID for each index.
  - The custom index order of the videos.

### Step 2: Tech Stack Auto-Detection
* Analyze each video title and description for keywords representing programming languages, frameworks, or cloud services.
* Map keywords to standardized tags:
  - "React", "Angular", "Vue" -> `React` (or respective framework)
  - "Node", "Express", "npm" -> `NodeJS`
  - "TypeScript", "ts" -> `TypeScript`
  - "Python", "pip", "boto3" -> `Python`
  - "CodePipeline", "CodeBuild", "Elastic Beanstalk", "S3", "EC2" -> `AWS` (with specific services)
  - "Docker", "Dockerfile", "container" -> `Docker`
  - "Terraform", "IaC" -> `Terraform`

### Step 3: YAML Output Assembly
* Compile the collected metadata into a single YAML configuration file with the following schema:

```yaml
Tech_Stack:
  - NodeJS
  - React
  - TypeScript
  - AWS (Elastic Beanstalk)
  - CI/CD (buildspec.yml, appspec.yml)
Destination_Directory: "aws_codepipeline"
Playlist_URL: "https://www.youtube.com/playlist?list=PLYaGyqgf-ksFRh-qXcjUTtqcVFv2hjHbW"
Videos:
  - Episode_01:
      Title: "AWS CodePipeline tutorial | Build a CI/CD Pipeline on AWS"
      URL: "https://www.youtube.com/watch?v=NwzJCSPSPZs&list=PLYaGyqgf-ksFRh-qXcjUTtqcVFv2hjHbW&index=1"
      Tech: "NodeJS, AWS CodePipeline, Elastic Beanstalk"
  - Episode_02:
      ...
```

---

## 💡 Usage Example

### Command:
"Generate the YAML configuration file for the playlist: `https://www.youtube.com/playlist?list=PLYaGyqgf-ksFRh-qXcjUTtqcVFv2hjHbW`"

### Action:
1. Extract all video titles and URLs.
2. Determine `Tech_Stack` from titles.
3. Write the compiled YAML configuration to the root of the workspace.
