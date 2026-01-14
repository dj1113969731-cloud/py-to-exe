import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import subprocess
from pathlib import Path

# =================================================================
# Python Distribution Suite - Master Launcher v10.2
# =================================================================

class MasterLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Distribution Suite v10.2 Master Build")
        self.root.geometry("600x450")
        self.root.resizable(False, False)
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.setup_ui()

    def setup_ui(self):
        # Background / Accent colors
        bg_color = "#f0f2f5"
        accent_blue = "#0078d4"
        accent_gold = "#d4af37"
        
        self.root.configure(bg=bg_color)
        
        # Header
        header = tk.Frame(self.root, bg=accent_blue, height=100)
        header.pack(fill=tk.X)
        
        tk.Label(header, text="PYTHON DISTRIBUTION SUITE / Python 分发大师", 
                 font=("Segoe UI", 18, "bold"), fg="white", bg=accent_blue).pack(pady=(20, 0))
        tk.Label(header, text="v10.2 Master Build / 10.2 大师版", 
                 font=("Segoe UI", 10), fg="white", bg=accent_blue).pack()

        # Body
        body = tk.Frame(self.root, bg=bg_color)
        body.pack(fill=tk.BOTH, expand=True, padx=50, pady=30)

        tk.Label(body, text="请选择您要启动的版本 / Select Edition:", 
                 font=("微软雅黑", 12), bg=bg_color, fg="#333").pack(pady=(0, 20))

        # Standard Button
        btn_std = tk.Button(body, text="📦 标准版 (Standard Edition)\n精简核心 | 无加密 | 快速分发\nCore Logic | No Encryption | Fast Distribution", 
                          font=("微软雅黑", 10), bg="white", fg="#333", relief="flat",
                          command=self.launch_std, cursor="hand2")
        btn_std.pack(fill=tk.X, pady=10, ipady=5)
        btn_std.bind("<Enter>", lambda e: btn_std.configure(bg="#e1e4e8"))
        btn_std.bind("<Leave>", lambda e: btn_std.configure(bg="white"))

        # Pro Button
        btn_pro = tk.Button(body, text="🛡️ 专业版 (Professional Edition)\n完全特性 | 内存保护 | CVE 审计\nFull Features | Memory Guard | CVE Audit", 
                          font=("微软雅黑", 10), bg=accent_gold, fg="black", relief="flat",
                          command=self.launch_pro, cursor="hand2")
        btn_pro.pack(fill=tk.X, pady=10, ipady=5)
        btn_pro.bind("<Enter>", lambda e: btn_pro.configure(bg="#c5a02c"))
        btn_pro.bind("<Leave>", lambda e: btn_pro.configure(bg=accent_gold))

        # Footer
        footer = tk.Frame(self.root, bg=bg_color)
        footer.pack(fill=tk.X, side=tk.BOTTOM, pady=10)
        tk.Label(footer, text="Powered by Antigravity AI Engine", 
                 font=("Segoe UI", 8, "italic"), bg=bg_color, fg="#888").pack()

    def launch_std(self):
        self._run_script("src/py转exe_std.py")

    def launch_pro(self):
        self._run_script("src/py转exe_pro.py")

    def _run_script(self, rel_path):
        script_path = Path(__file__).parent / rel_path
        if not script_path.exists():
            # Try current directory if we are in src already (though main.py is in src root)
            script_path = Path(__file__).parent / rel_path.replace("src/", "")
            
        if script_path.exists():
            self.root.destroy()
            subprocess.Popen([sys.executable, str(script_path)])
        else:
            messagebox.showerror("Error", f"无法找到组件: {script_path}\nComponent not found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MasterLauncher(root)
    root.mainloop()