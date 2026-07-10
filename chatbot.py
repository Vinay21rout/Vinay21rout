import os
import json
import urllib.request
import subprocess

def fetch_recent_activity(token):
    url = "https://api.github.com/users/Vinay21rout/events/public"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept": "application/vnd.github.v3+json"
        }
    )
    if token:
        req.add_header("Authorization", f"token {token}")
        
    try:
        with urllib.request.urlopen(req) as r:
            events = json.loads(r.read().decode())
    except Exception as e:
        print(f"Error fetching public events: {e}")
        return ""

    activities = []
    seen_events = set()
    
    for event in events:
        if len(activities) >= 5:
            break
            
        event_type = event.get("type", "")
        repo_name = event.get("repo", {}).get("name", "")
        
        display_repo = repo_name
        if display_repo.startswith("Vinay21rout/"):
            display_repo = display_repo[12:]
            
        payload = event.get("payload", {})
        
        if event_type == "PushEvent":
            commits = payload.get("commits", [])
            if commits:
                commit_msg = commits[0].get("message", "").split("\n")[0]
                key = f"push-{display_repo}-{commit_msg}"
                if key not in seen_events:
                    activities.append(f"📝 Pushed to `{display_repo}`: *\"{commit_msg}\"*")
                    seen_events.add(key)
        elif event_type == "PullRequestEvent":
            action = payload.get("action", "")
            pr = payload.get("pull_request", {})
            pr_title = pr.get("title", "")
            pr_url = pr.get("html_url", "")
            key = f"pr-{pr.get('id', '')}"
            if key not in seen_events:
                activities.append(f"🔀 {action.capitalize()} PR [#{pr.get('number', '')}]({pr_url}) in `{display_repo}`: *\"{pr_title}\"*")
                seen_events.add(key)
        elif event_type == "IssuesEvent":
            action = payload.get("action", "")
            issue = payload.get("issue", {})
            issue_title = issue.get("title", "")
            issue_url = issue.get("html_url", "")
            key = f"issue-{issue.get('id', '')}"
            if key not in seen_events:
                activities.append(f"🐞 {action.capitalize()} Issue [#{issue.get('number', '')}]({issue_url}) in `{display_repo}`: *\"{issue_title}\"*")
                seen_events.add(key)
        elif event_type == "CreateEvent":
            ref_type = payload.get("ref_type", "")
            ref = payload.get("ref", "")
            if ref_type == "repository":
                activities.append(f"🆕 Created repository `{display_repo}`")
            elif ref_type == "branch":
                activities.append(f"🌿 Created branch `{ref}` in `{display_repo}`")
                
    if not activities:
        return "- No recent public activity recorded."
        
    return "\n".join(f"- {act}" for act in activities)

def main():
    # Fetch environment variables
    event_name = os.environ.get("EVENT_NAME", "issues")
    issue_title = os.environ.get("ISSUE_TITLE", "")
    issue_number = os.environ.get("ISSUE_NUMBER", "")
    sender = os.environ.get("ISSUE_SENDER", "guest")
    token = os.environ.get("GITHUB_TOKEN", "")
    repo = os.environ.get("GITHUB_REPOSITORY", "")

    is_issue_trigger = (event_name == "issues" and issue_title.lower().startswith("chat:"))

    # Handle Chatbot Logic if triggered by an issue
    if is_issue_trigger:
        if not token or not repo or not issue_number:
            print("Missing issue environment variables.")
            return

        # Extract user query
        original_query = issue_title
        if original_query.lower().startswith("chat:"):
            original_query = original_query[5:].strip()
        
        query = original_query.lower()

        # Rule-based response logic
        response = ""
        
        if any(k in query for k in ["hello", "hi", "hey", "yo", "sup", "greet"]):
            response = (
                f"Hi @{sender}! 👋 I am Vinay's automated Profile Bot.\n\n"
                "I'm here to help you navigate his portfolio. You can ask me about:\n"
                "- **Projects** (e.g., *RecruiterIQ*, *DB-Agent*, *PPE*, *highway-vehicle-detection*)\n"
                "- **Skills** (e.g., *CrewAI*, *Streamlit*, *AutoGluon*, *n8n*)\n"
                "- **Education** & **Internships**\n"
                "- **Contact info**\n\n"
                "What would you like to know?"
            )
        elif any(k in query for k in ["project", "portfolio", "recruiteriq", "db-agent", "rag", "ppe", "object detection", "mcp", "speed", "vehicle", "annonymizer", "color"]):
            response = (
                f"Hi @{sender}! Vinay has structured his repositories into three main categories:\n\n"
                "🤖 **Agentic & GenAI Architectures**:\n"
                "- **RecruiterIQ**: Autonomous recruitment pipeline using CrewAI, LangChain, and Streamlit.\n"
                "- **DB-Agent**: Natural language to SQL parser built using LangGraph workflows.\n"
                "- **EDA_intelligence_Agent**: Conversational agent for loading and analyzing datasets.\n"
                "- **Chatbot_with_mcp**: Chatbot implementing Model Context Protocol (MCP).\n\n"
                "👁️ **Computer Vision & Image Tracking**:\n"
                "- **PPE-Detection-System**: Safety violation detection (No Helmet/No Vest) with ~91% accuracy.\n"
                "- **highway-vehicle-detection-polynomial**: Speed tracking and polynomial ROI mapping in OpenCV.\n"
                "- **face-annonymizer**: Real-time privacy blurring of camera streams.\n\n"
                "🗂️ **RAG & System Automation**:\n"
                "- **RAG-Based-Chatbot** / **RAG-with-LangGraph**: Dense document Q&A pipelines using FAISS/ChromaDB.\n"
                "- **N8N-Automation**: Self-hosted n8n workflows for automated scraping and alerts.\n\n"
                "Which area or project would you like to discuss?"
            )
        elif any(k in query for k in ["skill", "tech", "language", "crewai", "autogluon", "streamlit", "n8n", "tool", "stack"]):
            response = (
                f"Hi @{sender}! Here is Vinay's verified technical skillset directly from his resume:\n\n"
                "- **GenAI & Agentic AI**: LangChain, LangGraph, RAG, Prompt Engineering, LangSmith, LLM API Integration, CrewAI\n"
                "- **Machine Learning**: Fundamentals of Scikit-Learn and AutoGluon (AutoML) including Regression, Classification, Clustering, Feature Engineering, and Model Evaluation\n"
                "- **Computer Vision**: OpenCV (object tracking, real-time ROI annotation, image processing)\n"
                "- **Vector Databases**: FAISS, ChromaDB\n"
                "- **Workflow Automation**: n8n\n"
                "- **Languages**: Python, SQL\n"
                "- **Databases & Tools**: MySQL, Firebase, NumPy, Pandas, Matplotlib, Streamlit, Git, GitHub, Jupyter Notebook, Google Colab, VS Code, HTML, CSS"
            )
        elif any(k in query for k in ["education", "college", "university", "cgpa", "jindal", "study", "degree"]):
            response = (
                f"Hi @{sender}! Vinay is pursuing his **B.Tech in Computer Science and Engineering (AI/ML Specialization)** "
                "at **O.P. Jindal University**, Raigarh (2024–2028).\n\n"
                "He is currently entering his **3rd year** and maintains an impressive **CGPA of 9.1/10**!"
            )
        elif any(k in query for k in ["experience", "intern", "flyrank", "inamigos", "work", "job"]):
            response = (
                f"Hi @{sender}! Here is Vinay's practical experience:\n\n"
                "- **Machine Learning Intern** at **Flyrank AI** (Ongoing) — working on machine learning pipelines and optimization.\n"
                "- **Web Development Intern** at **InAmigos Foundation** (May 2026 – June 2026) — built responsive layouts and web apps.\n"
                "- **Campus Ambassador** at IIT Delhi's Entrepreneurship Development Cell (EDC) (Dec 2025 – Jan 2026)."
            )
        elif any(k in query for k in ["contact", "email", "linkedin", "reach", "gmail", "connect"]):
            response = (
                f"Hi @{sender}! You can connect with Vinay through the following channels:\n\n"
                "📧 **Email**: [vinayrout02@gmail.com](mailto:vinayrout02@gmail.com)\n"
                "🔗 **LinkedIn**: [linkedin.com/in/vinay-kumar-rout-4798372a9](https://linkedin.com/in/vinay-kumar-rout-4798372a9)\n"
                "🐙 **GitHub**: [github.com/Vinay21rout](https://github.com/Vinay21rout)"
            )
        elif "crewai" in query:
            response = (
                f"Hi @{sender}! Vinay uses **CrewAI** to orchestrate multi-agent systems. In his **RecruiterIQ** project, "
                "he set up multiple agents (Resume Parser, Job Analyst, Candidate Scorer, and Email Generator) that work "
                "cooperatively to automate recruitment workflows."
            )
        elif "autogluon" in query:
            response = (
                f"Hi @{sender}! Vinay uses **AutoGluon** for automated machine learning (AutoML). It allows him to quickly "
                "train, optimize, and ensemble models for tabular classification and regression datasets without manual "
                "tuning, speeding up his pipeline prototyping."
            )
        elif "streamlit" in query:
            response = (
                f"Hi @{sender}! Vinay uses **Streamlit** to rapidly build clean, interactive web frontends for his AI applications. "
                "This enables non-technical users to interact with his LLM chatbots, SQL agents, and classification models."
            )
        else:
            response = (
                f"Hi @{sender}! Thanks for reaching out.\n\n"
                "I'm a simple rule-based chatbot running on GitHub Actions. I didn't quite catch that question.\n\n"
                "Try asking me about:\n"
                "- **Projects** (e.g., *RecruiterIQ*, *DB-Agent*, *PPE*, *highway-vehicle-detection*)\n"
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

        # Manage rolling chat history in JSON
        history_file = "chat_history.json"
        history = []
        if os.path.exists(history_file):
            try:
                with open(history_file, "r", encoding="utf-8") as f:
                    history = json.load(f)
            except Exception as e:
                print(f"Error reading history file: {e}")
                history = []

        history.append({
            "sender": sender,
            "query": original_query,
            "answer": response,
            "issue_number": int(issue_number)
        })
        history = history[-3:]

        try:
            with open(history_file, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
            print("Updated chat_history.json ledger.")
        except Exception as e:
            print(f"Error writing history file: {e}")

    # Generate HTML representation of rolling chats (regardless of trigger)
    history_file = "chat_history.json"
    history = []
    if os.path.exists(history_file):
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                history = json.load(f)
        except Exception as e:
            print(f"Error reading history file for html generation: {e}")

    if history:
        html_lines = ['<table width="100%" cellpadding="8" cellspacing="0" border="0">']
        for chat in history:
            user_name = chat["sender"]
            q = chat["query"]
            ans = chat["answer"].replace("\n", "<br>").replace("  ", "&nbsp;&nbsp;")
            num = chat["issue_number"]
            
            html_lines.append('  <tr>')
            html_lines.append('    <td align="left" bgcolor="#161b22" style="border-bottom: 1px solid #21262d;">')
            html_lines.append(f'      👤 <b>@{user_name}</b>: <i>"{q}"</i>')
            html_lines.append('    </td>')
            html_lines.append('  </tr>')
            html_lines.append('  <tr>')
            html_lines.append(f'    <td align="left" bgcolor="#0d1117" style="border-bottom: 1px solid #21262d; padding-left: 20px;">')
            html_lines.append(f'      🤖 <b>Profile Bot</b>:<br>')
            html_lines.append(f'      {ans}')
            html_lines.append(f'      <br><br>')
            html_lines.append(f'      <sub><a href="https://github.com/{repo}/issues/{num}">View thread #{num}</a></sub>')
            html_lines.append('    </td>')
            html_lines.append('  </tr>')
        html_lines.append('</table>')
        html_content = "\n".join(html_lines)
    else:
        # Default placeholder HTML if history is empty
        html_content = (
            '<table width="100%" cellpadding="8" cellspacing="0" border="0">\n'
            '  <tr>\n'
            '    <td align="left" bgcolor="#161b22" style="border-bottom: 1px solid #21262d;">\n'
            '      👤 <b>@Guest</b>: <i>"Hello bot!"</i>\n'
            '    </td>\n'
            '  </tr>\n'
            '  <tr>\n'
            '    <td align="left" bgcolor="#0d1117" style="border-bottom: 1px solid #21262d; padding-left: 20px;">\n'
            '      🤖 <b>Profile Bot</b>:<br>\n'
            '      Hi! I\'m Vinay\'s Profile Bot. Click any of the quick queries above to ask me questions about his projects, skills, experience, or education.\n'
            '    </td>\n'
            '  </tr>\n'
            '</table>'
        )

    # Fetch recent public events
    recent_activity = fetch_recent_activity(token)

    # Update README.md
    readme_path = "README.md"
    if os.path.exists(readme_path):
        try:
            with open(readme_path, "r", encoding="utf-8") as f:
                content = f.read()

            # 1. Update Chatbot Log
            start_tag = "<!-- CHATBOT_LOG_START -->"
            end_tag = "<!-- CHATBOT_LOG_END -->"
            if start_tag in content and end_tag in content:
                start_idx = content.find(start_tag) + len(start_tag)
                end_idx = content.find(end_tag)
                content = content[:start_idx] + "\n" + html_content + "\n" + content[end_idx:]

            # 2. Update Activity Log
            act_start = "<!-- ACTIVITY_LOG_START -->"
            act_end = "<!-- ACTIVITY_LOG_END -->"
            if act_start in content and act_end in content:
                start_idx = content.find(act_start) + len(act_start)
                end_idx = content.find(act_end)
                content = content[:start_idx] + "\n" + recent_activity + "\n" + content[end_idx:]

            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(content)
            print("Successfully updated README.md.")

            # Commit and push back to repository
            subprocess.run(["git", "config", "--global", "user.name", "github-actions[bot]"], check=True)
            subprocess.run(["git", "config", "--global", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"], check=True)
            subprocess.run(["git", "add", "README.md"], check=True)
            if os.path.exists(history_file):
                subprocess.run(["git", "add", "chat_history.json"], check=True)
            
            # Check if there are changes before committing
            status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
            if status.stdout.strip():
                subprocess.run(["git", "commit", "-m", "chore: update chatbot & activity logs [skip ci]"], check=True)
                subprocess.run(["git", "push"], check=True)
                print("Committed and pushed updates.")
            else:
                print("No changes to commit.")
        except Exception as e:
            print(f"Error modifying files/pushing to Git: {e}")

if __name__ == "__main__":
    main()
