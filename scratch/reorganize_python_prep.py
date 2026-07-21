import re
import json

python_md_path = r"doc_replica_product_developer/doc_replica_fullstackdeveloper/backend/languages/python.md"

# Import details and generation from the previous script
from enrich_python_20_quizzes import TOPICS, TOPIC_DETAILS, generate_20_quizzes, generate_100_interview_questions

def format_question(idx, q_data):
    q_text = q_data["question"]
    ans_idx = q_data["answerIndex"]
    correct_ans = q_data["options"][ans_idx]
    explanation = q_data["explanation"]
    
    # Strip prefixes if any to keep clean
    correct_ans = re.sub(r'^(Option [A-D]:\s*|Correct Answer:\s*|Answer:\s*)', '', correct_ans, flags=re.IGNORECASE)
    
    return (
        f"### Question {idx}: {q_text}\n"
        f"**Answer:** {correct_ans}\n\n"
        f"**Explanation:** {explanation}\n"
    )

def run_reorganization():
    output_lines = []
    output_lines.append("# Python Backend Engineering & AI Agent Interview Preparation\n")
    output_lines.append("Welcome to the comprehensive Python Backend Engineering and AI Agent interview preparation guide. This document is structured in a professional, clean Q&A format to systematically test and reinforce core competencies.\n\n")

    # 1. Generate sections for all 26 topics
    for topic in TOPICS:
        output_lines.append(f"# {topic}\n")
        
        quizzes = generate_20_quizzes(topic)
        
        # Split into 10 Medium and 10 Advanced
        medium_quizzes = quizzes[:10]
        advanced_quizzes = quizzes[10:]
        
        # Medium Questions Section
        output_lines.append("## Medium Interview Questions\n")
        for i, q in enumerate(medium_quizzes, 1):
            output_lines.append(format_question(i, q))
            output_lines.append("") # Spacing
            
        output_lines.append("---\n")
        
        # Advanced Questions Section
        output_lines.append("## Advanced Interview Questions\n")
        for i, q in enumerate(advanced_quizzes, 1):
            output_lines.append(format_question(i, q))
            output_lines.append("") # Spacing
            
        output_lines.append("\n") # Section spacing

    # 2. General Backend & Agent Core Interview Questions Section (the 100 questions)
    output_lines.append("# General Backend & Agent Core Interview Questions\n")
    
    final_questions = generate_100_interview_questions()
    # Split into 50 Medium and 50 Advanced
    medium_final = final_questions[:50]
    advanced_final = final_questions[50:]
    
    output_lines.append("## Medium Interview Questions\n")
    for i, (q, a) in enumerate(medium_final, 1):
        output_lines.append(f"### Question {i}: {q}\n")
        output_lines.append(f"**Answer:** {a}\n")
        output_lines.append("")
        
    output_lines.append("---\n")
    
    output_lines.append("## Advanced Interview Questions\n")
    for i, (q, a) in enumerate(advanced_final, 1):
        output_lines.append(f"### Question {i}: {q}\n")
        output_lines.append(f"**Answer:** {a}\n")
        output_lines.append("")
        
    output_lines.append("\n")

    # 3. Append Cheat Sheet
    output_lines.append("## Cheat Sheet\n")
    output_lines.append("| Syntax | Pattern | Description |\n")
    output_lines.append("|---|---|---|\n")
    output_lines.append("| `async def` | Async execution | Defines non-blocking coroutines |\n")
    output_lines.append("| `await` | Event yield | Pauses coroutine execution until result resolves |\n")
    output_lines.append("| `@tool` | Tool binder | Auto-generates schemas for LLMs |\n")
    output_lines.append("| `logging.info` | Structured Logging | Logs structured objects to tracers |\n")

    # Join and write out
    final_md = "\n".join(output_lines)
    with open(python_md_path, "w", encoding="utf-8") as f:
        f.write(final_md)
        
    print("python.md successfully reorganized into interview-preparation format!")

if __name__ == "__main__":
    run_reorganization()
