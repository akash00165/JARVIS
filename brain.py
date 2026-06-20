"""
J.A.R.V.I.S AI Brain
Handles communication with the Anthropic Claude API
(with optional LangSmith tracing)
"""

import datetime
import platform
import os


JARVIS_SYSTEM_PROMPT = """You are J.A.R.V.I.S (Just A Rather Very Intelligent System), a highly advanced AI assistant inspired by Tony Stark's AI from Iron Man. You are running as a desktop application on the user's computer with full system access.

Your personality:
- Highly intelligent, precise, and efficient
- Slightly formal with subtle dry British wit
- Address the user as "{username}"
- Occasionally reference your capabilities in technical terms
- Proactive — if you notice something, mention it

Your capabilities in this app:
- Open files and folders on the computer
- Launch applications
- Search the web
- Answer questions on any topic
- Help with coding, writing, analysis
- Execute system commands (when the user asks)
- Read directory listings and file contents

Current system info:
- OS: {os_info}
- Date/Time: {datetime}
- Home directory: {home_dir}

When the user asks you to open a file, app, or folder — respond with a special action tag at the END of your response:
[ACTION:open_file:/path/to/file]
[ACTION:open_url:https://example.com]
[ACTION:open_app:app_name]
[ACTION:run_command:command]
[ACTION:list_dir:/path]

Keep responses concise (2-5 sentences) unless detailed help is needed. Be the best assistant possible."""


class JarvisBrain:
    def __init__(self, api_key: str, username: str = "Sir", langsmith_api_key: str = None):
        self.api_key = api_key                  # Anthropic API key
        self.langsmith_api_key = langsmith_api_key  # Optional: enables LangSmith tracing
        self.username = username
        self.conversation_history = []  # list of {"role": "user"/"assistant", "content": "..."}
        self.client = None
        self._init_client()

    def _init_client(self):
        if not self.api_key:
            self.client = None
            return
        try:
            from anthropic import Anthropic
            client = Anthropic(api_key=self.api_key)

            # If a LangSmith key is set, wrap the client so every call/response
            # is automatically logged as a trace in LangSmith.
            if self.langsmith_api_key:
                os.environ["LANGSMITH_TRACING"] = "true"
                os.environ["LANGSMITH_API_KEY"] = self.langsmith_api_key
                from langsmith.wrappers import wrap_anthropic
                client = wrap_anthropic(client)

            self.client = client
        except ImportError:
            self.client = None

    def update_api_key(self, api_key: str):
        self.api_key = api_key
        self._init_client()

    def update_langsmith_key(self, langsmith_api_key: str):
        """Enable/refresh LangSmith tracing without touching the Anthropic key."""
        self.langsmith_api_key = langsmith_api_key
        self._init_client()

    def _build_system_prompt(self):
        return JARVIS_SYSTEM_PROMPT.format(
            username=self.username,
            os_info=f"{platform.system()} {platform.release()}",
            datetime=datetime.datetime.now().strftime("%A, %B %d, %Y at %I:%M %p"),
            home_dir=os.path.expanduser("~")
        )

    def chat(self, user_message: str, callback=None) -> str:
        """Send message to Claude and get response."""
        if not self.client:
            return (
                f"AI core not initialized, {self.username}. "
                "Please run: pip install anthropic  — then add your Anthropic API key in Settings."
            )

        # Anthropic takes the system prompt as a separate top-level param,
        # not as a message in the list.
        messages = list(self.conversation_history)
        messages.append({"role": "user", "content": user_message})

        try:
            full_response = ""
            with self.client.messages.stream(
                model="claude-sonnet-4-6",
                max_tokens=1024,
                temperature=0.7,
                system=self._build_system_prompt(),
                messages=messages,
            ) as stream:
                for text in stream.text_stream:
                    full_response += text
                    if callback:
                        callback(text)

            # Save to history
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": full_response})

            # Keep history from growing too large (last 20 messages)
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]

            return full_response

        except Exception as e:
            err_msg = str(e)
            if "authentication_error" in err_msg.lower() or "401" in err_msg:
                return f"Invalid API key, {self.username}. Please check your Anthropic API key in Settings."
            elif "rate_limit" in err_msg.lower() or "429" in err_msg:
                return f"Rate limit reached, {self.username}. Please wait a moment before trying again."
            elif "overloaded" in err_msg.lower() or "529" in err_msg:
                return f"The Claude API is overloaded at the moment, {self.username}. Please try again shortly."
            else:
                return f"I encountered an error, {self.username}: {err_msg}"

    def clear_history(self):
        self.conversation_history = []
        
brain = JarvisBrain(
    api_key="apikey_01Rj2N8SVvo6BePZj99NhmiT",
    username="Sir",
    langsmith_api_key="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",  # omit/None to skip tracing
)