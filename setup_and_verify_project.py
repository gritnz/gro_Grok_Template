import os
import subprocess
import shutil
import time
import sys

def run_command(command, cwd=None, shell=True, timeout=None, input_data=None):
    """Run a shell command and handle errors."""
    try:
        result = subprocess.run(
            command,
            shell=shell,
            cwd=cwd,
            text=True,
            capture_output=True,
            timeout=timeout,
            input=input_data
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        print(f"Command timed out after {timeout} seconds: {command}")
        return False, "", f"Command timed out after {timeout} seconds"
    except Exception as e:
        print(f"Error running command: {e}")
        return False, "", str(e)

def terminate_processes_using_dir(directory):
    """Terminate Python processes (except the current one) that might be locking files in the directory."""
    print(f"Checking for processes locking {directory}...")
    # Get the current process ID to avoid terminating this script
    current_pid = os.getpid()
    # Terminate all python.exe processes except the current one
    success, output, error = run_command(f"taskkill /IM python.exe /F /FI \"PID ne {current_pid}\"")
    if not success:
        print(f"Warning: Could not terminate Python processes: {error}")
        print("Proceeding with cleanup anyway...")
    time.sleep(1)  # Give the system a moment to release locks
    return True

def clean_directory(directory):
    """Delete a directory, handling file access issues."""
    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist, skipping cleanup.")
        return True
    print(f"Cleaning directory {directory}...")
    if not terminate_processes_using_dir(directory):
        print("Failed to terminate processes, proceeding with cleanup anyway...")
    try:
        shutil.rmtree(directory, ignore_errors=True)
        if os.path.exists(directory):
            print(f"Failed to delete {directory} using shutil.rmtree, trying rmdir...")
            success, _, _ = run_command(f"rmdir /S /Q {directory}")
            if not success:
                return False
        print(f"Successfully deleted {directory}.")
        return True
    except Exception as e:
        print(f"Failed to delete {directory}: {e}")
        return False

def git_operations(repo_dir):
    """Handle Git pull, merge, and push with conflict detection."""
    print(f"Performing Git operations in {repo_dir}...")
    os.chdir(repo_dir)

    # Check for uncommitted changes
    success, output, _ = run_command("git status --porcelain")
    if not success:
        return False
    if output.strip():
        print("Uncommitted changes detected, stashing them...")
        run_command("git stash")

    # Pull remote changes
    success, output, _ = run_command("git pull origin master")
    if not success:
        if "CONFLICT" in output:
            print("Merge conflict detected. Please resolve conflicts manually in VS Code:")
            print("1. Open the conflicting files in VS Code.")
            print("2. Resolve conflicts (look for <<<<<<<, =======, >>>>>>> markers).")
            print("3. Stage the resolved files: git add <file>")
            print("4. Complete the merge: git commit")
            return False
        print("Git pull failed, aborting.")
        return False

    # Push changes (if any)
    success, _, _ = run_command("git push origin master")
    if not success:
        print("Git push failed, please check the error and resolve manually.")
        return False
    return True

def setup_project(template_dir, project_dir, env_name):
    """Set up a new project from the template."""
    print(f"Setting up project in {project_dir}...")

    # Check if project_dir is already a cloned project
    is_cloned_project = os.path.exists(os.path.join(project_dir, "src", "gro_instructor.py")) and \
                        os.path.exists(os.path.join(project_dir, "template_data"))

    if not is_cloned_project:
        # Clone the repository
        print("Cloning repository...")
        clone_url = "https://github.com/gritnz/gro_Grok_Template.git"
        parent_dir = os.path.dirname(project_dir)
        project_name = os.path.basename(project_dir)
        if os.path.exists(project_dir):
            print(f"Directory {project_dir} already exists, cleaning it...")
            if not clean_directory(project_dir):
                return False
        success, _, _ = run_command(f"git clone {clone_url} {project_name}", cwd=parent_dir)
        if not success:
            return False

    # Ensure we're in the project directory
    os.chdir(project_dir)

    # Set up Conda environment
    print("Setting up Conda environment...")
    success, output, _ = run_command("conda env list")
    if env_name not in output:
        success, _, _ = run_command(f"conda create -n {env_name} python=3.11 -y")
        if not success:
            return False
    print(f"Conda environment '{env_name}' is ready. Ensure it's activated: conda activate {env_name}")

    # Initialize data
    print("Initializing data...")
    src_dir = os.path.join(project_dir, "template_data")
    dest_dir = os.path.join(project_dir, "data", "historical")
    if os.path.exists(dest_dir):
        print(f"Removing existing {dest_dir}...")
        if not clean_directory(dest_dir):
            return False
    os.makedirs(dest_dir, exist_ok=True)
    shutil.copytree(src_dir, dest_dir, dirs_exist_ok=True)
    print(f"Copied {src_dir} to {dest_dir}")

    # Copy the docs directory (including e3_summaries.md) from the template
    docs_src_dir = os.path.join(template_dir, "docs")
    docs_dest_dir = os.path.join(project_dir, "docs")
    if os.path.exists(docs_src_dir):
        if os.path.exists(docs_dest_dir):
            print(f"Removing existing {docs_dest_dir}...")
            if not clean_directory(docs_dest_dir):
                return False
        os.makedirs(docs_dest_dir, exist_ok=True)
        shutil.copytree(docs_src_dir, docs_dest_dir, dirs_exist_ok=True)
        print(f"Copied {docs_src_dir} to {docs_dest_dir}")

    # Initialize history_log.jsonl and state.json if they don't exist
    history_log = os.path.join(dest_dir, "history_log.jsonl")
    state_file = os.path.join(dest_dir, "state.json")
    if not os.path.exists(history_log):
        with open(history_log, "w") as f:
            pass  # Create empty file
        print(f"Created {history_log}")
    if not os.path.exists(state_file):
        with open(state_file, "w") as f:
            f.write("{}")  # Create empty JSON
        print(f"Created {state_file}")

    # Test gro_instructor.py with input and timeout
    print("Testing gro_instructor.py...")
    success, output, error = run_command(
        "python src/gro_instructor.py",
        shell=True,
        timeout=10,  # 10-second timeout
        input_data="Hello #e5\n"  # Provide the expected input
    )
    print(f"Output: {output}")
    print(f"Error: {error}")
    if "User interaction: I’ll respond directly to your query." not in output:
        print("gro_instructor.py did not respond as expected. Check the script and data setup.")
        return False
    if not success:
        print("gro_instructor.py exited with an error, but produced the expected output, so proceeding.")

    print(f"Setup complete! Project ready at {project_dir}")
    return True

def main():
    template_dir = r"F:\gro_Grok_Template"
    project_dir = r"F:\TestProject"
    env_name = "TestEnv"

    # Step 1: Clean up nested directories
    nested_dir = os.path.join(project_dir, "TestProject")
    if not clean_directory(nested_dir):
        print("Failed to clean nested directory. Aborting.")
        sys.exit(1)

    # Step 2: Perform Git operations in the template repository
    if not git_operations(template_dir):
        print("Git operations failed. Resolve any issues and rerun the script.")
        sys.exit(1)

    # Step 3: Set up the project
    if not setup_project(template_dir, project_dir, env_name):
        print("Project setup failed. Check the errors above and resolve them.")
        sys.exit(1)

    print("All steps completed successfully!")

if __name__ == "__main__":
    main()