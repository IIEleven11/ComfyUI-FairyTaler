"""
@author: IIEleven11
@title: ComfyUI FairyTaler Storyboard Nodes
@nickname: FairyTaler
@description: Custom nodes for creating storyboards from Ollama text output. Parse text into scenes, generate images, and compose storyboards with scene consistency options.
"""

try:
    from .storyboard_nodes import NODE_CLASS_MAPPINGS
except ImportError:
    from storyboard_nodes import NODE_CLASS_MAPPINGS

__all__ = ['NODE_CLASS_MAPPINGS']
