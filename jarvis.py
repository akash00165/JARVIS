#!/usr/bin/env python3
"""
J.A.R.V.I.S - Just A Rather Very Intelligent System
Main entry point
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.app_window import JarvisApp

if __name__ == "__main__":
    app = JarvisApp()
    app.run()
