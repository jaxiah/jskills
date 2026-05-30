#!/usr/bin/env python3
import sys
import subprocess
import re
from pathlib import Path

try:
    from textual.app import App, ComposeResult
    from textual.widgets import Header, Footer, Input, RichLog
    from rich.markdown import Markdown
    from rich.panel import Panel
    from rich.text import Text
except ImportError:
    print("Error: The 'textual' and 'rich' libraries are required for the TUI.")
    print("Please run: pip install textual rich")
    sys.exit(1)

MESSAGE_RE = re.compile(r"^(\d+)-([a-z0-9_-]+)\.md$")

class RoundtableApp(App):
    TITLE = "Roundtable Control Room"
    CSS = """
    Input {
        dock: bottom;
        margin: 1 1;
    }
    RichLog {
        height: 1fr;
        margin: 1 1;
        border: solid #30333b;
        background: #17181c;
    }
    """

    def __init__(self):
        super().__init__()
        self.root_dir = Path(".").resolve()
        self.messages_dir = self.root_dir / ".roundtable" / "messages"
        self.seen_files = set()

    def compose(self) -> ComposeResult:
        yield Header()
        # wrap=True allows text to wrap, markup=True allows rich tags
        yield RichLog(id="chat_log", wrap=True, markup=True)
        yield Input(
            placeholder="HumanSay> (Type message and press Enter, use @name: to address)", 
            id="chat_input"
        )
        yield Footer()

    async def on_mount(self) -> None:
        self.messages_dir.mkdir(parents=True, exist_ok=True)
        self.chat_log = self.query_one("#chat_log", RichLog)
        
        # 欢迎信息
        self.chat_log.write(Panel("[bold cyan]Welcome to the Roundtable TUI[/]\nType your messages below. The log will automatically scroll.", border_style="cyan"))
        
        # 启动定时器，每 0.5 秒检查一次新文件。第一次检查会自动加载所有历史。
        self.set_interval(0.5, self.check_new_messages)
        self.query_one("#chat_input").focus()

    def check_new_messages(self) -> None:
        if not self.messages_dir.exists():
            return
        
        # 获取并排序所有匹配的消息文件
        files = sorted([p for p in self.messages_dir.iterdir() if MESSAGE_RE.match(p.name)])
        
        for path in files:
            if path.name not in self.seen_files:
                self.render_message(path)
                self.seen_files.add(path.name)

    def render_message(self, path: Path) -> None:
        try:
            content = path.read_text(encoding="utf-8")
            parts = content.split("---", 2)
            body = parts[-1].strip() if len(parts) >= 3 else content.strip()
            
            match = MESSAGE_RE.match(path.name)
            num = match.group(1) if match else "??"
            speaker = match.group(2) if match else "unknown"

            # 颜色分配
            colors = {
                "human": "cyan", 
                "codex": "green", 
                "gemini": "magenta", 
                "claude": "orange3"
            }
            color = colors.get(speaker, "yellow")
            
            header = Text(f"#{num} {speaker.upper()}", style=f"bold {color}")
            panel = Panel(Markdown(body), title=header, title_align="left", border_style=color)
            
            self.chat_log.write(panel)
        except Exception as e:
            self.chat_log.write(f"[red]Error reading message {path.name}: {e}[/red]")

    async def on_input_submitted(self, message: Input.Submitted) -> None:
        msg = message.value.strip()
        if not msg:
            return
        
        # 清空输入框
        input_widget = self.query_one("#chat_input", Input)
        input_widget.value = ""
        
        say_script = Path(__file__).parent / "humansay.py"
        cmd = [sys.executable, str(say_script), "--root", str(self.root_dir)]
        
        if msg.startswith("@") and ":" in msg:
            parts = msg.split(":", 1)
            target = parts[0][1:].strip()
            content = parts[1].strip()
            cmd.extend(["--at", target, content])
        else:
            cmd.append(msg)
            
        try:
            # 后台运行 humansay.py，不阻塞 UI
            subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            self.chat_log.write(f"[red]Failed to send message: {e}[/red]")

if __name__ == "__main__":
    app = RoundtableApp()
    app.run()
