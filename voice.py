"""
J.A.R.V.I.S Voice Engine
Handles wake word detection, speech recognition, and text-to-speech
"""

import threading
import queue
import time


class VoiceEngine:
    def __init__(self, wake_word="jarvis", on_command=None, on_wake=None, on_listening=None):
        self.wake_word = wake_word.lower()
        self.on_command = on_command    # callback(text)
        self.on_wake = on_wake          # callback()
        self.on_listening = on_listening  # callback(bool)

        self.is_running = False
        self.is_listening = False
        self.tts_engine = None
        self.recognizer = None
        self.microphone = None

        self._available = False
        self._init_engines()

    def _init_engines(self):
        """Initialize speech engines."""
        try:
            import speech_recognition as sr
            self.recognizer = sr.Recognizer()
            self.recognizer.energy_threshold = 3000
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 0.8
            self.microphone = sr.Microphone()
            self._available = True
        except ImportError:
            self._available = False
            return

        try:
            import pyttsx3
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 150)
            self.tts_engine.setProperty('volume', 0.9)
            # Try to set a nice voice
            voices = self.tts_engine.getProperty('voices')
            for voice in voices:
                if 'english' in voice.name.lower() and ('uk' in voice.id.lower() or 'british' in voice.name.lower()):
                    self.tts_engine.setProperty('voice', voice.id)
                    break
        except:
            self.tts_engine = None

    @property
    def available(self):
        return self._available

    def speak(self, text: str, blocking: bool = False):
        """Convert text to speech."""
        # Strip markdown
        import re
        clean = re.sub(r'[*_`#\[\]]', '', text)
        clean = re.sub(r'\[ACTION:\w+:.+?\]', '', clean).strip()
        # Limit length for speech
        if len(clean) > 400:
            clean = clean[:397] + "..."

        if self.tts_engine:
            def _speak():
                try:
                    self.tts_engine.say(clean)
                    self.tts_engine.runAndWait()
                except:
                    pass
            if blocking:
                _speak()
            else:
                t = threading.Thread(target=_speak, daemon=True)
                t.start()
        else:
            # Fallback: try system TTS
            import platform, subprocess
            system = platform.system()
            if system == "Darwin":
                cmd = ["say", "-r", "170", clean[:300]]
                if not blocking:
                    subprocess.Popen(cmd)
                else:
                    subprocess.run(cmd)
            elif system == "Linux":
                subprocess.Popen(["espeak", "-s", "150", clean[:300]],
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def listen_once(self, timeout=5) -> str:
        """Listen for a single command, return text."""
        if not self._available:
            return ""
        import speech_recognition as sr
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
            text = self.recognizer.recognize_google(audio)
            return text.lower()
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except Exception:
            return ""

    def start_wake_word_loop(self):
        """Start background thread listening for wake word."""
        if not self._available:
            return
        self.is_running = True
        t = threading.Thread(target=self._wake_word_loop, daemon=True)
        t.start()

    def stop(self):
        self.is_running = False

    def _wake_word_loop(self):
        """Continuously listen for wake word in background."""
        import speech_recognition as sr
        while self.is_running:
            try:
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.2)
                    try:
                        audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=5)
                        text = self.recognizer.recognize_google(audio).lower()
                        if self.wake_word in text:
                            if self.on_wake:
                                self.on_wake()
                            # Now listen for the actual command
                            self._listen_for_command()
                    except sr.WaitTimeoutError:
                        pass
                    except sr.UnknownValueError:
                        pass
            except Exception:
                time.sleep(1)

    def _listen_for_command(self):
        """Listen for command after wake word detected."""
        import speech_recognition as sr
        if self.on_listening:
            self.on_listening(True)
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=12)
                text = self.recognizer.recognize_google(audio)
                if self.on_command and text.strip():
                    self.on_command(text)
        except sr.WaitTimeoutError:
            pass
        except sr.UnknownValueError:
            pass
        except Exception:
            pass
        finally:
            if self.on_listening:
                self.on_listening(False)
