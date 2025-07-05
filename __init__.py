"""
@author: Eleven
@title: ComfyUI FairyTaler Storyboard Nodes
@nickname: ComfyUI FairyTaler
@description: Turn your AI roleplay into AI generated scenes from every response. Visualize what you read!
"""
from .storyboard_nodes import NODE_CLASS_MAPPINGS
try:
    from .storyboard_nodes import NODE_CLASS_MAPPINGS
except ImportError:
    from storyboard_nodes import NODE_CLASS_MAPPINGS

__all__ = ['NODE_CLASS_MAPPINGS']
