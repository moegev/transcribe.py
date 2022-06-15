Hi, my name is Moe Gevirtz. I am a linguist and budding data scientist at Deepgram. 
I have learned what I know of programming and Python by writing scripts that make use of Deepgram's API's and Hotpepper to solve problems.
morris@deepgram.com
Slack: @moe

I saw a need for a better transcription wrapper. 
This script allows me to transcribe audio more easily that writing a CURL command (which I find clumsy to do). 

Having written many similar scripts, I decided one hot Berkeley Saturday evening to write a better wrapper. This is more adaptable than the others I have written. Sure, it's still the work of an untrained amateur. Yet, I have incorporated design features that I have learned over the last year of programming. 

My own personal goal is to create a simple machine that allows me to answer MORE AND MORE questions about digital speech data and  it's textual representations. 

*------------------------------------------------------------------------*
Future Functionality (that I have thought about)
*------------------------------------------------------------------------*

transcribe.py -- (the main script for now) allow ability use ANY of deepgram's speech models incl. diarizers, transliteration.  Add much more detail to metadata. Make sure it can handle any file Deepgram can handle .mp3, .ogg etc. 

text_stats.py -- tools  learn about some of the important text features of the audio - basic stats: distribution, word count, low accuracy areas, silence time, AAAs, words that don't fit a particular dictionary, etc.

lang_detect.py -- wrapper for DG lang detect, my own personal (high cost) language detector, moe's codeswitching tool. 

audio_wav analzued

Connect with other DG tools, such as WER tools.  Do model comparisons easily.  

What would you like to add?


Write me and let me know. 
Best, 

Moe

PYTHON PACKAGES YOU NEED:

import os
import argparse
import json
from requests_toolbelt.utils import dump
import requests