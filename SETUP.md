# Setting Up a New Project from gro_Grok_Template

This guide helps you start a new project using gro_Grok_template—a simple, no-API chat assistant framework.

## Prerequisites
- Python 3.11.11 (via Conda recommended)
- Git (optional for cloning)

## Steps
1. **Get the Template**
   - **Option 1: Local Copy**
     - Copy `F:\gro_Grok_Template` to a new folder (e.g., `F:\NewProject`).
   - **Option 2: Git Clone** (if on GitHub)
     - Run: `git clone https://github.com/<your-username>/gro_Grok_Template.git <new-project-name>`
     - Example: `git clone https://github.com/gritnz/gro_Grok_Template.git MyChatBot`
     - Then: `cd <new-project-name>`

2. **Set Up Conda Environment**
   - Create: `conda create -n <env-name> python=3.11.11`
     - Example: `conda create -n MyChatBotEnv python=3.11.11`
   - Activate: `conda activate <env-name>`
   - Verify: `python --version` (should show 3.11.11)

3. **Install Dependencies**
   - None yet—core runs on standard Python. Add optional tools later (e.g., NLTK, Sumy) via `pip install`.

4. **Run the Template**
   - Navigate: `cd <new-project-name>`
   - Start: `python src/gro_instructor.py`
   - Test: Type "Hello #e5"—expect "Hey there! How can I assist you today?"

5. **Customize**
   - Edit `state.json` for project-specific data.
   - Add new agents in `src/` (e.g., copy `gro_instructor.py` as a base).
   - Update `prompts.md` for new condense/expand prompts.

## Notes
- **Git**: Initialize with `git init` and commit: `git add . && git commit -m "New project start"`.
- **Backups**: Copy `data/` to `backups/` manually for now.