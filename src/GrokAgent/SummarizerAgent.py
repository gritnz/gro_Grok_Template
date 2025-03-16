import os
import json
import yaml
from datetime import datetime

class SummarizerAgent:
    def __init__(self):
        with open("F:/gro_Grok_Template/config/dev_config.yaml", "r") as f:
            self.config = yaml.safe_load(f)
        self.state_file = "F:/gro_Grok_Template/data/historical/state.json"
        self.sync_file = "F:/gro_Grok_Template/data/sync.json"
        self.max_size_mb = self.config["data"]["max_size_mb"]

    def summarize_and_prune(self):
        if not os.path.exists(self.state_file):
            state = {"history": []}
        else:
            try:
                with open(self.state_file, "r") as f:
                    state = json.load(f)
            except (json.JSONDecodeError, ValueError):
                state = {"history": []}

        # Debug: Print state before processing
        print("State before update:", json.dumps(state))

        # Ensure history exists
        if "history" not in state or not isinstance(state["history"], list):
            state["history"] = []

        # Get latest input
        latest_input = state.get("input", "")
        print("Latest input from state:", latest_input)

        # Add to history if new and non-empty
        if latest_input and (not state["history"] or state["history"][-1]["input"] != latest_input):
            state["history"].append({
                "input": latest_input,
                "timestamp": datetime.now().isoformat()
            })

        # Keep last 5
        state["history"] = state["history"][-5:]

        # Update summary
        summary = {
            "latest_input": latest_input,
            "timestamp": datetime.now().isoformat(),
            "progress": state.get("progress", "Started")
        }
        state.update(summary)

        # Prune if over size
        while os.path.exists(self.state_file) and os.path.getsize(self.state_file) > self.max_size_mb * 1024 * 1024:
            state["history"] = state["history"][-1:]
            break

        # Save state
        with open(self.state_file, "w") as f:
            json.dump(state, f)

        # Save sync
        with open(self.sync_file, "w") as f:
            json.dump(summary, f)

if __name__ == "__main__":
    summarizer = SummarizerAgent()
    summarizer.summarize_and_prune()
    print("Summarized and synced")