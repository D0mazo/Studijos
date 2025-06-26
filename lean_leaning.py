```python
import json
import os
from datetime import datetime

# File to store user progress
PROGRESS_FILE = "lean_progress.json"

def load_progress():
    """Load user progress from a JSON file."""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    return {"completed_sections": [], "quiz_scores": {}, "last_accessed": None}

def save_progress(progress):
    """Save user progress to a JSON file."""
    progress["last_accessed"] = datetime.now().isoformat()
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=4)

def display_welcome(progress):
    """Display welcome message and user progress."""
    print("\n=== Welcome to the Lean Expert Program ===")
    print("This program will guide you to become a Lean Methodology expert.")
    print("You'll learn Lean principles, tools, case studies, and apply concepts through exercises.\n")
    
    if progress["last_accessed"]:
        print(f"Last accessed: {progress['last_accessed']}")
    if progress["completed_sections"]:
        print(f"Completed sections: {', '.join(progress['completed_sections'])}")
    if progress["quiz_scores"]:
        print("Quiz scores:")
        for section, score in progress["quiz_scores"].items():
            print(f"  {section}: {score['score']}/{score['total']} ({score['percentage']}%)")
    print("\n")

def section_intro_to_lean():
    """Teach the introduction to Lean Methodology."""
    print("=== Section 1: Introduction to Lean Methodology ===")
    print("Lean Methodology originated from Toyota's production system in the 1950s.")
    print("It focuses on delivering maximum customer value while minimizing waste.")
    print("Key concepts:")
    print("- **Value**: What the customer is willing to pay for.")
    print("- **Waste**: Anything that doesn't add value (e.g., overproduction, defects).")
    print("- **Continuous Improvement (Kaizen)**: Small, incremental changes to improve processes.")
    print("\nExample: Toyota reduced inventory waste by implementing Just-In-Time production.")
    input("Press Enter to continue...")

def section_lean_principles():
    """Teach the five core Lean principles."""
    print("=== Section 2: The Five Lean Principles ===")
    principles = [
        ("Identify Value", "Determine what the customer values in your product/service."),
        ("Map the Value Stream", "Analyze all steps in the process to identify waste."),
        ("Create Flow", "Ensure smooth, uninterrupted flow of value-creating steps."),
        ("Establish Pull", "Produce only what is needed, when needed, based on customer demand."),
        ("Seek Perfection", "Continuously improve processes to eliminate waste and maximize value.")
    ]
    for principle, description in principles:
        print(f"- **{principle}**: {description}")
    print("\nCase Study: A coffee shop mapped its order process, found delays in restocking, and implemented a pull system to restock only when needed.")
    input("Press Enter to continue...")

def section_lean_tools():
    """Teach key Lean tools and techniques."""
    print("=== Section 3: Lean Tools and Techniques ===")
    tools = [
        ("Value Stream Mapping (VSM)", "Visualize the entire process to identify waste and optimize flow."),
        ("5S System", "Sort, Set in order, Shine, Standardize, Sustain - for workplace organization."),
        ("Kanban", "Visual system to manage work and ensure pull-based production."),
        ("Poka-Yoke", "Mistake-proofing to prevent errors (e.g., color-coded parts)."),
        ("Kaizen Events", "Focused, short-term projects to improve specific processes.")
    ]
    for tool, description in tools:
        print(f"- **{tool}**: {description}")
    print("\nExercise: Imagine you're managing a bakery. How would you use Kanban to manage inventory?")
    answer = input("Enter your response: ").strip()
    print("Feedback: A good Kanban approach might involve a board with columns like 'To Do', 'In Progress', and 'Done' to track inventory tasks.")
    input("Press Enter to continue...")

def section_case_studies():
    """Present real-world Lean case studies."""
    print("=== Section 4: Lean Case Studies ===")
    print("1. **Toyota**: Used Just-In-Time to reduce inventory costs by 50%.")
    print("2. **Nike**: Applied Lean to streamline supply chain, reducing lead time by 20%.")
    print("3. **Hospital**: Implemented 5S to organize surgical tools, reducing setup time by 30%.")
    print("\nExercise: Pick one case study and suggest another Lean tool that could enhance it.")
    answer = input("Enter your response: ").strip()
    print("Feedback: For example, in the hospital case, VSM could map patient flow to further reduce wait times.")
    input("Press Enter to continue...")

def section_advanced_lean():
    """Teach advanced Lean concepts."""
    print("=== Section 5: Advanced Lean Concepts ===")
    print("- **Hoshin Kanri**: Strategic planning to align goals with Lean initiatives.")
    print("- **Jidoka (Autonomation)**: Automation with a human touch to stop processes when defects are detected.")
    print("- **Lean Six Sigma**: Combines Lean with Six Sigma for process improvement and quality control.")
    print("\nExample: A manufacturer used Jidoka to stop a production line when a defective part was detected, saving $10,000 in rework costs.")
    input("Press Enter to continue...")

def comprehensive_quiz(progress):
    """Administer a comprehensive quiz on Lean Methodology."""
    print("=== Comprehensive Lean Methodology Quiz ===")
    questions = [
        {
            "question": "What is the primary goal of Lean Methodology?",
            "options": [
                "A. Maximize production speed",
                "B. Deliver maximum customer value with minimal waste",
                "C. Increase employee workload",
                "D. Focus only on cost reduction"
            ],
            "correct": "B",
            "section": "Introduction"
        },
        {
            "question": "Which Lean principle involves producing only what is needed?",
            "options": [
                "A. Identify Value",
                "B. Create Flow",
                "C. Establish Pull",
                "D. Seek Perfection"
            ],
            "correct": "C",
            "section": "Principles"
        },
        {
            "question": "What does the 5S System focus on?",
            "options": [
                "A. Financial planning",
                "B. Workplace organization",
                "C. Marketing strategies",
                "D. Customer surveys"
            ],
            "correct": "B",
            "section": "Tools"
        },
        {
            "question": "In a Lean case study, how did a hospital benefit from 5S?",
            "options": [
                "A. Increased inventory",
                "B. Reduced setup time",
                "C. Higher defect rates",
                "D. Longer patient wait times"
            ],
            "correct": "B",
            "section": "Case Studies"
        },
        {
            "question": "What is Jidoka in Lean Methodology?",
            "options": [
                "A. A strategic planning tool",
                "B. Automation with human intervention for quality control",
                "C. A customer feedback system",
                "D. A waste identification method"
            ],
            "correct": "B",
            "section": "Advanced"
        }
    ]
    
    score = 0
    total = len(questions)
    
    for i, q in enumerate(questions, 1):
        print(f"\nQuestion {i}: {q['question']}")
        for option in q["options"]:
            print(option)
        answer = input("Enter your answer (A, B, C, or D): ").strip().upper()
        
        if answer == q["correct"]:
            print("Correct!")
            score += 1
        else:
            print(f"Wrong! The correct answer was {q['correct']}.")
    
    percentage = (score / total) * 100
    print(f"\nQuiz completed! Your score: {score}/{total} ({percentage:.1f}%)")
    if percentage >= 80:
        print("Excellent! You're well on your way to becoming a Lean expert.")
    elif percentage >= 50:
        print("Good effort! Review the sections to improve your score.")
    else:
        print("You may need to revisit the material. Keep studying!")
    
    # Update progress with quiz results
    progress["quiz_scores"]["Comprehensive Quiz"] = {
        "score": score,
        "total": total,
        "percentage": percentage
    }
    save_progress(progress)

def main():
    progress = load_progress()
    sections = [
        ("Introduction to Lean Methodology", section_intro_to_lean),
        ("The Five Lean Principles", section_lean_principles),
        ("Lean Tools and Techniques", section_lean_tools),
        ("Lean Case Studies", section_case_studies),
        ("Advanced Lean Concepts", section_advanced_lean)
    ]
    
    while True:
        display_welcome(progress)
        print("Available Sections:")
        for i, (title, _) in enumerate(sections, 1):
            status = "✔" if title in progress["completed_sections"] else " "
            print(f"{i}. {title} [{status}]")
        print(f"{len(sections) + 1}. Take Comprehensive Quiz")
        print(f"{len(sections) + 2}. Exit")
        
        choice = input("\nSelect an option (1-{}): ".format(len(sections) + 2)).strip()
        
        try:
            choice = int(choice)
            if 1 <= choice <= len(sections):
                sections[choice - 1][1]()
                if sections[choice - 1][0] not in progress["completed_sections"]:
                    progress["completed_sections"].append(sections[choice - 1][0])
                    save_progress(progress)
            elif choice == len(sections) + 1:
                comprehensive_quiz(progress)
            elif choice == len(sections) + 2:
                print("Thank you for using the Lean Expert Program! Goodbye.")
                save_progress(progress)
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

if __name__ == "__main__":
    main()
```