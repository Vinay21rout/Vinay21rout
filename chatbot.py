import os
import json
import urllib.request
import subprocess

def main():
    # Fetch environment variables
    issue_title = os.environ.get("ISSUE_TITLE", "")
    issue_number = os.environ.get("ISSUE_NUMBER", "")
    sender = os.environ.get("ISSUE_SENDER", "guest")
    token = os.environ.get("GITHUB_TOKEN", "")
    repo = os.environ.get("GITHUB_REPOSITORY", "")

    if not token or not repo or not issue_number:
        print("Missing environment variables.")
        return

    # Extract user query
    original_query = issue_title
    if original_query.lower().startswith("chat:"):
        original_query = original_query[5:].strip()
    
    query = original_query.lower()

    # Rule-based response logic
    response = ""
    
    # 1. Greet/Hello
    if any(k in query for k in ["hello", "hi", "hey", "yo", "sup", "greet"]):
        response = (
            f"Hi @{sender}! 👋 I am Vinay's automated Profile Bot.\n\n"
            "I'm here to help you navigate his portfolio. You can ask me about:\n"
            "- **Projects** (e.g., *RecruiterIQ*, *DB-Agent*, *RAG Chatbot*, *PPE OpenCV*)\n"
            "- **Skills** (e.g., *CrewAI*, *Streamlit*, *AutoGluon*, *n8n*)\n"
            "- **Education** & **Internships**\n"
            "- **Contact info**\n\n"
            "What would you like to know?"
        )
    
    # 2. Projects
    elif any(k in query for k in ["project", "portfolio", "recruiteriq", "db-agent", "rag", "ppe", "object detection"]):
        response = (
            f"Hi @{sender}! Vinay has built several cool AI & automation projects:\n\n"
            "1. **RecruiterIQ**: An autonomous multi-agent recruitment pipeline built using **CrewAI**, LangChain, FastAPI, and Streamlit. It parses resumes, scores candidates, and automates email workflows.\n"
            "2. **DB-Agent**: A natural language interface to SQL databases built using **LangGraph** for multi-step query generation and schema validation.\n"
            "3. **RAG-Based AI Chatbot**: A document intelligence system utilizing **FAISS / ChromaDB** and LangSmith for tracing/evaluation.\n"
            "4. **PPE-Detection**: A Computer Vision pipeline using **OpenCV** to detect safety violation events (No Helmet/No Vest) with ~91% accuracy.\n\n"
            "Which one of these would you like to explore?"
        )
        
    # 3. Skills
    elif any(k in query for k in ["skill", "tech", "language", "crewai", "autogluon", "streamlit", "n8n", "tool", "stack"]):
        response = (
            f"Hi @{sender}! Here is a summary of Vinay's technical toolbox:\n\n"
            "- **GenAI & Agents**: LangChain, LangGraph, CrewAI, Prompt Engineering\n"
            "- **Workflow Automation**: n8n (multi-step loops, scheduled alerts)\n"
            "- **Machine Learning**: Fundamentals of Scikit-Learn and AutoGluon (AutoML)\n"
            "- **Computer Vision**: OpenCV (object tracking, image processing)\n"
            "- **Languages**: Python, SQL, C++\n"
            "- **Prototyping & Web**: Streamlit, MySQL, HTML/CSS\n\n"
            "He specializes in orchestrating AI agents and automated workflows."
        )

    # 4. Education
    elif any(k in query for k in ["education", "college", "university", "cgpa", "jindal", "study", "degree"]):
        response = (
            f"Hi @{sender}! Vinay is pursuing his **B.Tech in Computer Science and Engineering (AI/ML Specialization)** "
            "at **O.P. Jindal University**, Raigarh (2024–2028).\n\n"
            "He is currently entering his **3rd year** and maintains an impressive **CGPA of 9.1/10**!"
        )

    # 5. Experience / Internships
    elif any(k in query for k in ["experience", "intern", "flyrank", "inamigos", "work", "job"]):
        response = (
            f"Hi @{sender}! Here is Vinay's practical experience:\n\n"
            "- **Machine Learning Intern** at **Flyrank AI** (Ongoing) — working on machine learning pipelines and optimization.\n"
            "- **Web Development Intern** at **InAmigos Foundation** (May 2026 – June 2026) — built responsive layouts and web apps.\n"
            "- **Campus Ambassador** at IIT Delhi's Entrepreneurship Development Cell (EDC) (Dec 2025 – Jan 2026)."
        )

    # 6. Contact / Connect
    elif any(k in query for k in ["contact", "email", "linkedin", "reach", "gmail", "connect"]):
        response = (
            f"Hi @{sender}! You can connect with Vinay through the following channels:\n\n"
            "📧 **Email**: [vinayrout02@gmail.com](mailto:vinayrout02@gmail.com)\n"
            "🔗 **LinkedIn**: [linkedin.com/in/vinay-kumar-rout-4798372a9](https://linkedin.com/in/vinay-kumar-rout-4798372a9)\n"
            "🐙 **GitHub**: [github.com/Vinay21rout](https://github.com/Vinay21rout)"
        )

    # 7. CrewAI / Agents
    elif "crewai" in query:
        response = (
            f"Hi @{sender}! Vinay uses **CrewAI** to orchestrate multi-agent systems. In his **RecruiterIQ** project, "
            "he set up multiple agents (Resume Parser, Job Analyst, Candidate Scorer, and Email Generator) that work "
            "cooperatively to automate recruitment workflows."
        )

    # 8. AutoGluon / ML
    elif "autogluon" in query:
        response = (
            f"Hi @{sender}! Vinay uses **AutoGluon** for automated machine learning (AutoML). It allows him to quickly "
            "train, optimize, and ensemble models for tabular classification and regression datasets without manual "
            "tuning, speeding up his pipeline prototyping."
        )

    # 9. Streamlit
    elif "streamlit" in query:
        response = (
            f"Hi @{sender}! Vinay uses **Streamlit** to rapidly build clean, interactive web frontends for his AI applications. "
            "This enables non-technical users to interact with his LLM chatbots, SQL agents, and classification models."
        )

    # 10. Default fallback
    else:
        response = (
            f"Hi @{sender}! Thanks for reaching out.\n\n"
            "I'm a simple rule-based chatbot running on GitHub Actions. I didn't quite catch that question.\n\n"
            "Try asking me about:\n"
            "- **Projects** (e.g., *RecruiterIQ*, *DB-Agent*, *RAG Chatbot*, *PPE OpenCV*)\n"
            "- **Skills** (e.g., *CrewAI*, *Streamlit*, *AutoGluon*, *n8n*)\n"
            "- **Education & Internships**\n"
            "- **Contact info**"
        )

    print(f"Formulating response to issue #{issue_number}...")

    # Post a comment to the issue
    api_url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json"
    }
    
    req_body = json.dumps({"body": response}).encode("utf-8")
    req = urllib.request.Request(api_url, data=req_body, headers=headers, method="POST")
    try:
        urllib.request.urlopen(req)
        print("Successfully posted comment.")
    except Exception as e:
        print(f"Error posting comment: {e}")

    # Close the issue
    api_url_close = f"https://api.github.com/repos/{repo}/issues/{issue_number}"
    req_body_close = json.dumps({"state": "closed"}).encode("utf-8")
    req_close = urllib.request.Request(api_url_close, data=req_body_close, headers=headers, method="PATCH")
    try:
        urllib.request.urlopen(req_close)
        print("Successfully closed issue.")
    except Exception as e:
        print(f"Error closing issue: {e}")

    # Update README with latest interaction
    readme_path = "README.md"
    if os.path.exists(readme_path):
        try:
            with open(readme_path, "r", encoding="utf-8") as f:
                content = f.read()

            start_tag = "<!-- CHATBOT_LOG_START -->"
            end_tag = "<!-- CHATBOT_LOG_END -->"

            if start_tag in content and end_tag in content:
                start_idx = content.find(start_tag) + len(start_tag)
                end_idx = content.find(end_tag)

                new_log = f"\n🗣️ **Recent Query:** @{sender} asked: *\"{original_query}\"*<br>🤖 **Bot Reply:** *\"{response.splitlines()[0]}... [view full answer in issue #{issue_number}](https://github.com/{repo}/issues/{issue_number})\"*\n"
                updated_content = content[:start_idx] + new_log + content[end_idx:]

                with open(readme_path, "w", encoding="utf-8") as f:
                    f.write(updated_content)
                print("Updated README.md log.")

                # Commit changes back
                subprocess.run(["git", "config", "--global", "user.name", "github-actions[bot]"], check=True)
                subprocess.run(["git", "config", "--global", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"], check=True)
                subprocess.run(["git", "add", "README.md"], check=True)
                subprocess.run(["git", "commit", "-m", "chore: update chatbot conversation log [skip ci]"], check=True)
                subprocess.run(["git", "push"], check=True)
                print("Committed and pushed README.md update.")
            else:
                print("Chatbot tags not found in README.md.")
        except Exception as e:
            print(f"Error updating README.md: {e}")

if __name__ == "__main__":
    main()
