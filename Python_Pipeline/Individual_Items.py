from dataclasses import dataclass, field
from typing import List

@dataclass
class NewsItem:
    title: str = ""
    category: str = ""
    url: List[str] = field(default_factory=list)   # multiple article links
    content: str = ""                              # combined text
    summary: str = ""                              # summarized version
    script: str = ""                               # podcast script
    audio_file: str = ""                           # local path to audio
