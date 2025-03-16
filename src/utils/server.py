import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from src.GrokAgent.GrokAgent import GrokAgent
from src.GrokAgent.SummarizerAgent import SummarizerAgent

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        with open("F:/gro_Grok_Template/data/sync.json", "r") as f:
            self.wfile.write(f.read().encode())

    def do_POST(self):
        print("Received POST request")
        try:
            length = int(self.headers["Content-Length"])
            print(f"Content length: {length}")
            data = json.loads(self.rfile.read(length).decode())
            print(f"Data received: {data}")
            agent = GrokAgent()
            print("Agent initialized")
            agent.scrape_data(data)
            print("Data scraped")
            state_file = "F:/gro_Grok_Template/data/historical/state.json"
            if os.path.exists(state_file):
                with open(state_file, "r") as f:
                    state = json.load(f)
            else:
                state = {"history": []}
            state["input"] = data.get("input", "")
            with open(state_file, "w") as f:
                json.dump(state, f)
            print(f"Forced input: {state['input']}")
            summarizer = SummarizerAgent()
            summarizer.summarize_and_prune()
            print("Data summarized and pruned")
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "saved"}).encode())
            print("Response sent")
        except Exception as e:
            print(f"Error in POST: {str(e)}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
print("Server running at localhost:8000")
httpd.serve_forever()