# F:\gro_Grok_Template\setup_and_verify_project.py
import os
import shutil
import subprocess
import sys

def setup_project(project_dir):
    """Set up the project directory by copying necessary files from the template."""
    if not os.path.exists(project_dir):
        os.makedirs(project_dir)

    template_dir = os.path.dirname(os.path.abspath(__file__))
    for dir_name in ["src", "template_data", "docs"]:  # Added "docs"
        src_dir = os.path.join(template_dir, dir_name)
        dst_dir = os.path.join(project_dir, dir_name)
        if os.path.exists(src_dir):
            shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True)
        else:
            print(f"Warning: {src_dir} does not exist in template.")

def verify_project(project_dir):
    """Verify the project setup by running gro_instructor.py and checking its response."""
    process = subprocess.run(
        ["python", "src/gro_instructor.py"],
        cwd=project_dir,
        input="#e1\n",
        text=True,
        capture_output=True,
        timeout=10
    )
    expected_response = "Debug info: Low relevance, focusing on setup or minor issues."
    if expected_response not in process.stdout:
        print(f"Verification failed: Expected '{expected_response}' in output, got: {process.stdout}")
        return False
    print("Verification passed: gro_instructor.py responded as expected.")
    return True

def terminate_processes():
    """Terminate any lingering Python processes (excluding the current one)."""
    subprocess.run(
        f"taskkill /F /IM python.exe /T /FI \"PID ne {os.getpid()}\"",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

def main():
    if len(sys.argv) != 2:
        print("Usage: python setup_and_verify_project.py <project_dir>")
        sys.exit(1)

    project_dir = sys.argv[1]
    print(f"Setting up project in {project_dir}...")
    setup_project(project_dir)

    print("Verifying project setup...")
    if not verify_project(project_dir):
        print("Project verification failed.")
        sys.exit(1)

    print("Cleaning up processes...")
    terminate_processes()

    print("Project setup and verification completed successfully!")

if __name__ == "__main__":
    main()