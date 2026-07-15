from enum import Enum

class ConversationStatus(str, Enum):
    STARTED = "started"
    COMPLETED = "completed"
    FAILED = "failed"

class ConversationProvider(str, Enum):
    RETELL = "retell"
    VAPI = "vapi"
    ELEVENLABS = "elevenlabs"