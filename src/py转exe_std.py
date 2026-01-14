import os
import sys
import json
import shutil
import subprocess
import threading
import re
import time
import importlib.util
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

# =================================================================
# 1. 国际化与配置 (I18N & Config)
# =================================================================
TL = {
    "title": ["Python 分发大师 (Standard) v10.2 Master Build", "Python Distribution Master (Standard) v10.2"],
    "header": ["📦 Python 分发大师 [标准版]", "📦 Python Distribution [Standard]"],
    "theme": ["🌓 主题", "🌓 Theme"],
    "cleanup": ["🧹 清理", "🧹 Cleanup"],
    "select": ["📁 选择脚本", "📁 Select Script"],
    "settings": [" 基础设置 ", " Basic Settings "],
    "engine": ["编译引擎:", "Build Engine:"],
    "arch": ["多架构兼容 (X64/ARM64)", "Multi-Arch (X64/ARM64)"],
    "start": ["🚀 开始转换 (不含加密项)", "🚀 Start Conversion (No Encryption)"],
    "clean_log": ["🧹 [系统维护] 正在清理构建缓存...", "🧹 [System] Cleaning build cache..."],
    "clean_done": ["✓ 清理完成，处理了 {} 个项目。", "✓ Cleanup done, processed {} items."],
    "import_done": ["已导入 {} 个文件。", "Imported {} files."],
    "processing": ["\n➤ 正在处理: {}", "\n➤ Processing: {}"],
    "success": ["✓ {} 成功！", "✓ {} Success!"],
    "failed": ["✗ {} 失败。", "✗ {} Failed."],
    "error": ["出错: {}", "Error: {}"],
    "dep_err": ["未检测到 {} 模块。\n请在终端运行: pip install {}", "{} module not found.\nPlease run: pip install {}"],
    "finished": ["所有任务已处理完毕。", "All tasks completed."]
}

class ConfigManager:
    def __init__(self):
        self.config_path = Path("config_std.json")
        self.defaults = {
            "engine": "pyinstaller",
            "theme": "light",
            "multi_arch": False,
            "version": "1.0.2.0",
            "github_user": "Developer"
        }
        self.current = self.load()

    def load(self):
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return {**self.defaults, **json.load(f)}
            except: pass
        return self.defaults

    def save(self):
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.current, f, indent=4, ensure_ascii=False)
        except Exception as e: print(f"Save Error: {e}")

# =================================================================
# 2. 标准分发引擎 (Standard Engine)
# =================================================================
class StandardEngine:
    def __init__(self, logger, ui):
        self.log = logger
        self.ui = ui

    def perform_cleanup(self):
        self.log(TL["clean_log"][self.ui.li])
        targets = ["build", "__pycache__"]
        count = 0
        for t in targets:
            if Path(t).exists():
                shutil.rmtree(t, ignore_errors=True)
                count += 1
        self.log(TL["clean_done"][self.ui.li].format(count))

    def check_dependency(self, engine):
        # 针对 PyInstaller 的特殊大小写处理
        target = "PyInstaller" if engine.lower() == "pyinstaller" else engine
        
        # 方法 1: 使用 importlib 探测
        if importlib.util.find_spec(target):
            return True
            
        # 方法 2: 使用 subprocess 探测 (备用)
        try:
            subprocess.run([sys.executable, "-m", target, "--version"], 
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            return True
        except:
            return False

# =================================================================
# 3. 标准版 UI (Standard Suite UI)
# =================================================================
class StandardUI:
    def __init__(self, root):
        self.root = root
        self.ui = self
        self.config = ConfigManager()
        self.engine = StandardEngine(self.write_log, self)
        self.files = []
        
        self.themes = {
            "light": {"bg": "#ffffff", "fg": "#333333", "accent": "#0078d4"},
            "dark": {"bg": "#202020", "fg": "#e0e0e0", "accent": "#00a2ed"}
        }
        
        self.setup_ui()
        self.apply_theme()

    def setup_ui(self):
        # 0: CN, 1: EN (Auto-detect logic could go here)
        self.li = 0 if "zh" in (os.environ.get("LANG", "") or "zh").lower() else 1
        
        self.root.title(TL["title"][self.li])
        self.root.geometry("900x700")
        
        header = ttk.Frame(self.root)
        header.pack(fill=tk.X, padx=30, pady=20)
        ttk.Label(header, text=TL["header"][self.li], font=("微软雅黑", 16, "bold")).pack(side=tk.LEFT)
        ttk.Button(header, text=TL["theme"][self.li], command=self.toggle_theme).pack(side=tk.RIGHT, padx=5)
        ttk.Button(header, text=TL["cleanup"][self.li], command=self.engine.perform_cleanup).pack(side=tk.RIGHT, padx=5)
        ttk.Button(header, text=TL["select"][self.li], command=self.import_files).pack(side=tk.RIGHT, padx=5)

        # Settings
        f_set = ttk.LabelFrame(self.root, text=TL["settings"][self.li], padding=15)
        f_set.pack(fill=tk.X, padx=30, pady=5)
        
        ttk.Label(f_set, text=TL["engine"][self.li]).pack(side=tk.LEFT)
        self.eng_var = tk.StringVar(value=self.config.current["engine"])
        ttk.Combobox(f_set, textvariable=self.eng_var, values=["pyinstaller", "nuitka"]).pack(side=tk.LEFT, padx=10)
        
        self.arch_var = tk.BooleanVar(value=self.config.current["multi_arch"])
        ttk.Checkbutton(f_set, text=TL["arch"][self.li], variable=self.arch_var).pack(side=tk.LEFT, padx=20)

        # Log
        self.log_win = scrolledtext.ScrolledText(self.root, height=15, font=("Consolas", 10))
        self.log_win.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        # Action
        self.btn_go = ttk.Button(self.root, text=TL["start"][self.li], command=self.run_process)
        self.btn_go.pack(pady=20)

    def apply_theme(self):
        t = self.themes[self.config.current["theme"]]
        self.root.configure(bg=t["bg"])
        self.log_win.configure(bg=t["bg"], fg=t["fg"])

    def toggle_theme(self):
        self.config.current["theme"] = "dark" if self.config.current["theme"] == "light" else "light"
        self.config.save()
        self.apply_theme()

    def write_log(self, text):
        self.log_win.insert(tk.END, f"{text}\n")
        self.log_win.see(tk.END)
        self.root.update_idletasks()

    def import_files(self):
        fs = filedialog.askopenfilenames(filetypes=[("Python Files", "*.py")])
        if fs: self.files = [Path(f) for f in fs]; self.write_log(TL["import_done"][self.li].format(len(self.files)))

    def run_process(self):
        if not self.files: return messagebox.showwarning("提示", "请选择脚本。")
        engine = self.eng_var.get()
        if not self.engine.check_dependency(engine):
            return messagebox.showerror("Error", TL["dep_err"][self.li].format(engine, engine))
        
        self.btn_go.config(state=tk.DISABLED)
        threading.Thread(target=self.work, daemon=True).start()

    def work(self):
        self.config.current.update({"engine": self.eng_var.get(), "multi_arch": self.arch_var.get()})
        self.config.save()
        
        for py_path in self.files:
            try:
                self.write_log(TL["processing"][self.li].format(py_path.name))
                if self.eng_var.get() == "nuitka":
                    cmd = [sys.executable, "-m", "nuitka", "--standalone", "--onefile", "--remove-output", str(py_path)]
                else:
                    cmd = [sys.executable, "-m", "PyInstaller", "--clean", "-F", "-w", str(py_path)]
                
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='ignore')
                while True:
                    line = p.stdout.readline()
                    if not line and p.poll() is not None: break
                    if line: self.write_log(f"  {line.strip()}")
                
                if p.returncode == 0: self.write_log(TL["success"][self.li].format(py_path.name))
                else: self.write_log(TL["failed"][self.li].format(py_path.name))
            except Exception as e: self.write_log(TL["error"][self.li].format(e))
        
        self.root.after(0, lambda: self.btn_go.config(state=tk.NORMAL))
        self.root.after(0, lambda: messagebox.showinfo("Done", TL["finished"][self.li]))

if __name__ == "__main__":
    root = tk.Tk()
    StandardUI(root)
    root.mainloop()
