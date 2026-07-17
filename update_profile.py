import os
import json
import urllib.request
import subprocess
from datetime import datetime, timedelta, timezone

def fetch_data(url, token):
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
            return json.loads(r.read().decode())
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def fetch_recent_activity(token):
    events = fetch_data("https://api.github.com/users/Vinay21rout/events/public", token)
    if not events:
        return "- No recent public activity recorded."

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

def fetch_latest_repos(token):
    # Fetch repos sorted by updated time
    repos = fetch_data("https://api.github.com/users/Vinay21rout/repos?per_page=15&sort=updated", token)
    if not repos:
        return "- No recent repository activity found."
        
    lines = []
    count = 0
    for r in repos:
        if count >= 5:
            break
        if r.get("fork", False):
            continue
            
        name = r.get("name")
        html_url = r.get("html_url")
        desc = r.get("description") or "Building intelligent systems."
        stars = r.get("stargazers_count", 0)
        lang = r.get("language") or "Python"
        
        lines.append(f"- 📁 **[{name}]({html_url})** - `{lang}` | ★ `{stars}` stars<br>_{desc}_")
        count += 1
        
    if not lines:
        return "- No recent repository activity found."
    return "\n".join(lines)

def fetch_profile_stats(token):
    # Fetch profile details
    profile = fetch_data("https://api.github.com/users/Vinay21rout", token)
    # Fetch repositories list
    repos = fetch_data("https://api.github.com/users/Vinay21rout/repos?per_page=100", token)
    
    if not profile or not repos:
        return {}
        
    followers = profile.get("followers", 0)
    public_repos = profile.get("public_repos", 0)
    
    stars = sum(r.get("stargazers_count", 0) for r in repos if not r.get("fork", False))
    forks = sum(r.get("forks_count", 0) for r in repos if not r.get("fork", False))
    
    lang_count = {}
    for r in repos:
        if not r.get("fork", False):
            lang = r.get("language")
            if lang:
                lang_count[lang] = lang_count.get(lang, 0) + 1
                
    sorted_langs = sorted(lang_count.items(), key=lambda x: x[1], reverse=True)
    primary_langs = ", ".join(lang for lang, count in sorted_langs[:5])
    
    return {
        "public_repos": public_repos,
        "stars": stars,
        "forks": forks,
        "followers": followers,
        "primary_langs": primary_langs
    }

def get_last_updated():
    # Convert UTC to IST (UTC + 5:30)
    utc_now = datetime.now(timezone.utc)
    ist_offset = timedelta(hours=5, minutes=30)
    ist_now = utc_now + ist_offset
    return f"🕒 *Last synced on: {ist_now.strftime('%A, %b %d, %Y at %I:%M %p')} (IST)*"

def main():
    token = os.environ.get("GITHUB_TOKEN", "")
    
    # 1. Fetch recent activity
    print("Fetching recent public activity events...")
    recent_activity = fetch_recent_activity(token)
    
    # 2. Fetch latest repos
    print("Fetching latest active repositories...")
    latest_repos = fetch_latest_repos(token)
    
    # 3. Fetch stats
    print("Fetching profile statistics...")
    stats_data = fetch_profile_stats(token)
    
    # 4. Get last updated timestamp
    last_updated = get_last_updated()
    
    # 5. Update README.md
    readme_path = "README.md"
    if os.path.exists(readme_path):
        try:
            with open(readme_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Update stats block if stats_data is valid
            if stats_data:
                # Update individual stats placeholders in dashboard
                stats_lines = [
                    f"- **Public Repositories**: {stats_data['public_repos']}",
                    f"- **Total Stars Received**: {stats_data['stars']}",
                    f"- **Forks Created (Own Repos)**: {stats_data['forks']}",
                    f"- **Followers**: {stats_data['followers']}",
                    f"- **Primary Languages**: {stats_data['primary_langs']}"
                ]
                profile_stats_text = "\n".join(stats_lines)
                
                stats_start = "<!-- STATS_LOG_START -->"
                stats_end = "<!-- STATS_LOG_END -->"
                if stats_start in content and stats_end in content:
                    start_idx = content.find(stats_start) + len(stats_start)
                    end_idx = content.find(stats_end)
                    content = content[:start_idx] + "\n" + profile_stats_text + "\n" + content[end_idx:]

                # Update live dashboard values if present as comments
                def update_placeholder(text, start_tag, end_tag, new_val):
                    if start_tag in text and end_tag in text:
                        s_idx = text.find(start_tag) + len(start_tag)
                        e_idx = text.find(end_tag)
                        return text[:s_idx] + str(new_val) + text[e_idx:]
                    return text
                
                content = update_placeholder(content, "<!-- DYNAMIC_REPOS_VAL -->", "<!-- DYNAMIC_REPOS_VAL_END -->", stats_data["public_repos"])
                content = update_placeholder(content, "<!-- DYNAMIC_STARS_VAL -->", "<!-- DYNAMIC_STARS_VAL_END -->", stats_data["stars"])
                content = update_placeholder(content, "<!-- DYNAMIC_FOLLOWERS_VAL -->", "<!-- DYNAMIC_FOLLOWERS_VAL_END -->", stats_data["followers"])

            # Update activity block
            act_start = "<!-- ACTIVITY_LOG_START -->"
            act_end = "<!-- ACTIVITY_LOG_END -->"
            if act_start in content and act_end in content:
                start_idx = content.find(act_start) + len(act_start)
                end_idx = content.find(act_end)
                content = content[:start_idx] + "\n" + recent_activity + "\n" + content[end_idx:]

            # Update latest repos block
            repos_start = "<!-- LATEST_REPOS_START -->"
            repos_end = "<!-- LATEST_REPOS_END -->"
            if repos_start in content and repos_end in content:
                start_idx = content.find(repos_start) + len(repos_start)
                end_idx = content.find(repos_end)
                content = content[:start_idx] + "\n" + latest_repos + "\n" + content[end_idx:]

            # Update last updated block
            lu_start = "<!-- LAST_UPDATED_START -->"
            lu_end = "<!-- LAST_UPDATED_END -->"
            if lu_start in content and lu_end in content:
                start_idx = content.find(lu_start) + len(lu_start)
                end_idx = content.find(lu_end)
                content = content[:start_idx] + "\n" + last_updated + "\n" + content[end_idx:]

            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(content)
            print("Successfully updated README.md.")

            # Commit and push changes back (if inside GitHub Actions)
            if os.environ.get("GITHUB_ACTIONS") == "true":
                subprocess.run(["git", "config", "--global", "user.name", "github-actions[bot]"], check=True)
                subprocess.run(["git", "config", "--global", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"], check=True)
                subprocess.run(["git", "add", "README.md"], check=True)
                
                # Check if there are changes before committing
                status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
                if status.stdout.strip():
                    subprocess.run(["git", "commit", "-m", "chore: sync GitHub metrics and activity [skip ci]"], check=True)
                    subprocess.run(["git", "push"], check=True)
                    print("Committed and pushed updates.")
                else:
                    print("No changes to commit.")
            else:
                print("Running locally. Skipping Git commit/push.")
        except Exception as e:
            print(f"Error modifying files/pushing to Git: {e}")

if __name__ == "__main__":
    main()
