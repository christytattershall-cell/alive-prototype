import customtkinter as ctk
from pynput import keyboard
import json
import time
import threading
import hashlib 
import statistics
from pathlib import Path

# --- STRIPE COLOR PALETTE ---
STRIPE_BLUE = "#635bff"
STRIPE_SLATE = "#424770"
STRIPE_DARK = "#1a1f36"
STRIPE_LIGHT_BG = "#f6f9fc"
STRIPE_WHITE = "#ffffff"
STRIPE_BORDER = "#e6ebf1"

class AliveAgentApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Setup ---
        self.title("Alive Agent")
        self.geometry("480x620") 
        ctk.set_appearance_mode("light") # Stripe aesthetic is famously light
        self.configure(fg_color=STRIPE_LIGHT_BG)
        
        # --- Variables ---
        self.recording = False
        self.deltas = []
        self.last_time = None

        # --- HEADER SECTION ---
        self.header_frame = ctk.CTkFrame(self, fg_color=STRIPE_WHITE, corner_radius=0, height=80)
        self.header_frame.pack(fill="x", side="top")
        
        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="Alive", 
            font=("Segoe UI", 26, "bold"), 
            text_color=STRIPE_DARK
        )
        self.title_label.place(relx=0.08, rely=0.5, anchor="w")

        # --- STATUS INDICATOR ---
        self.status_pill = ctk.CTkFrame(self, fg_color=STRIPE_BORDER, corner_radius=20, height=30)
        self.status_pill.pack(pady=(30, 10))
        
        self.status_text = ctk.CTkLabel(
            self.status_pill, 
            text="● SYSTEM IDLE", 
            font=("Segoe UI", 12, "bold"), 
            text_color=STRIPE_SLATE
        )
        self.status_text.pack(padx=15)

        # --- MAIN ACTION AREA ---
        self.container = ctk.CTkFrame(self, fg_color=STRIPE_WHITE, corner_radius=12, border_color=STRIPE_BORDER, border_width=1)
        self.container.pack(pady=10, padx=30, fill="both", expand=True)

        self.btn_label = ctk.CTkLabel(self.container, text="Biometric Session", font=("Segoe UI", 14, "bold"), text_color=STRIPE_DARK)
        self.btn_label.pack(pady=(20, 10))

        self.toggle_button = ctk.CTkButton(
            self.container, 
            text="Start Recording", 
            fg_color=STRIPE_BLUE, 
            hover_color="#544dc0",
            font=("Segoe UI", 14, "bold"),
            height=45,
            width=200,
            corner_radius=8,
            command=self.toggle_recording
        )
        self.toggle_button.pack(pady=10)

        # --- CONTENT FINGERPRINTING SECTION ---
        self.text_label = ctk.CTkLabel(self.container, text="Document Content", font=("Segoe UI", 13, "bold"), text_color=STRIPE_SLATE)
        self.text_label.pack(pady=(20, 5))
        
        self.textbox = ctk.CTkTextbox(
            self.container, 
            width=360, 
            height=160, 
            fg_color="#fcfdff", 
            border_color=STRIPE_BORDER, 
            border_width=1,
            corner_radius=8,
            font=("Segoe UI", 13),
            text_color=STRIPE_DARK
        )
        self.textbox.pack(pady=10, padx=20)

        # --- FOOTER ---
        self.save_label = ctk.CTkLabel(self, text="Ready to secure your session.", font=("Segoe UI", 12), text_color="#a3acb9")
        self.save_label.pack(pady=20)

    # [Logic remains the same to preserve the "Unbreakable" functionality]
    def on_release(self, key):
        if not self.recording: return False 
        now = time.time()
        if self.last_time:
            delta = now - self.last_time
            if delta < 3.0: self.deltas.append(round(delta, 4))
        self.last_time = now

    def start_background_listener(self):
        with keyboard.Listener(on_release=self.on_release) as self.listener:
            self.listener.join()

    def toggle_recording(self):
        if not self.recording:
            self.recording = True
            self.deltas, self.last_time = [], None
            self.toggle_button.configure(text="Stop & Seal", fg_color="#e5424d", hover_color="#c03740")
            self.status_text.configure(text="● SESSION ACTIVE", text_color=STRIPE_BLUE)
            threading.Thread(target=self.start_background_listener, daemon=True).start()
        else:
            self.recording = False
            self.toggle_button.configure(text="Start Recording", fg_color=STRIPE_BLUE, hover_color="#544dc0")
            self.status_text.configure(text="● IDLE", text_color=STRIPE_SLATE)
            self.save_data()

    def save_data(self):
        raw_text = self.textbox.get("0.0", "end").strip()
        if len(self.deltas) > 10 and len(raw_text) > 0:
            ts = time.ctime() 
            combined = f"{raw_text}{ts}"
            content_hash = hashlib.sha256(combined.encode('utf-8')).hexdigest()
            variation = statistics.stdev(self.deltas)
            score = min(100, int(variation * 500))
            payload = {
                "id": f"{score}-H-{content_hash[:6]}-2025",
                "content_hash": content_hash,
                "jitter_data": self.deltas,
                "timestamp": ts,
                "score": score
            }
            download_path = Path.home() / "Downloads" / "rhythm.json"
            with open(download_path, "w") as f:
                json.dump(payload, f)
            self.save_label.configure(text=f"Session Sealed: {payload['id']}", text_color=STRIPE_BLUE)
        else:
            self.save_label.configure(text="Capture more data to seal.", text_color="#e5424d")

if __name__ == "__main__":
    app = AliveAgentApp()
    app.mainloop()