"""
ComfyUI FairyTaler Storyboard Nodes

This package provides nodes for creating storyboards from Ollama text output.

Nodes included:
- SceneParser: Parses Ollama text into 3 separate scene descriptions
- SceneToConditioning: Converts scene text to CLIP conditioning
- ThreeSceneGenerator: Generates placeholder images for 3 scenes
- StoryboardCompositor: Combines 3 images into a storyboard layout
- FairyTalerStoryboard: All-in-one node for complete storyboard creation

Usage:
1. Connect Ollama Generate node output to SceneParser or FairyTalerStoryboard
2. Use the scene descriptions with image generation nodes
3. Combine the generated images with StoryboardCompositor
"""

try:
    from .storyboard_nodes import (
        SceneParser,
        SceneToConditioning,
        ThreeSceneGenerator,
        StoryboardCompositor,
        FairyTalerStoryboard
    )
except ImportError:
    # Fallback for direct execution
    from storyboard_nodes import (
        SceneParser,
        SceneToConditioning,
        ThreeSceneGenerator,
        StoryboardCompositor,
        FairyTalerStoryboard
    )

# Node mappings for ComfyUI registration
NODE_CLASS_MAPPINGS = {
    "SceneParser": SceneParser,
    "SceneToConditioning": SceneToConditioning,
    "ThreeSceneGenerator": ThreeSceneGenerator,
    "StoryboardCompositor": StoryboardCompositor,
    "FairyTalerStoryboard": FairyTalerStoryboard,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SceneParser": "Scene Parser",
    "SceneToConditioning": "Scene to Conditioning",
    "ThreeSceneGenerator": "Three Scene Generator",
    "StoryboardCompositor": "Storyboard Compositor",
    "FairyTalerStoryboard": "FairyTaler Storyboard",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
