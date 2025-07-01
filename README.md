# FairyTaler Storyboard Nodes

This package provides ComfyUI nodes for creating 3-scene storyboards from Ollama text output.

## Installation

1. Copy the `storyboard_nodes.py` and `__init__.py` files to your ComfyUI custom nodes directory
2. Restart ComfyUI
3. The nodes will appear under the "FairyTaler/Storyboard" category

## Nodes

### 1. SceneParser
**Purpose**: Parses Ollama text output into 3 separate scene descriptions

**Inputs**:
- `ollama_text` (STRING): The text output from an Ollama Generate node
- `debug` (enable/disable): Enable debug printing

**Outputs**:
- `scene_1`, `scene_2`, `scene_3` (STRING): Individual scene descriptions

### 2. SceneToConditioning
**Purpose**: Converts scene text to CLIP conditioning for use with sampling nodes

**Inputs**:
- `scene_text` (STRING): A scene description
- `clip` (CLIP): CLIP model for text encoding
- `debug` (enable/disable): Enable debug printing

**Outputs**:
- `conditioning` (CONDITIONING): CLIP conditioning for the scene

### 3. ThreeSceneGenerator
**Purpose**: Generates placeholder images for 3 scenes (for testing/demo)

**Inputs**:
- `scene_1`, `scene_2`, `scene_3` (STRING): Scene descriptions
- `model`, `clip`, `vae`: Standard ComfyUI model inputs
- Various generation parameters (width, height, steps, cfg, seed, etc.)
- `debug` (enable/disable): Enable debug printing

**Outputs**:
- `image_1`, `image_2`, `image_3` (IMAGE): Generated placeholder images

### 4. StoryboardCompositor
**Purpose**: Combines 3 images into a single storyboard layout

**Inputs**:
- `image_1`, `image_2`, `image_3` (IMAGE): The 3 scene images
- `layout` (vertical/horizontal/grid): How to arrange the images
- `spacing` (INT): Pixels between images
- `background_color` (STRING): Background color name
- `add_labels` (enable/disable): Add "Scene 1", "Scene 2", "Scene 3" labels
- `debug` (enable/disable): Enable debug printing

**Outputs**:
- `storyboard` (IMAGE): Combined storyboard image

### 5. FairyTalerStoryboard (All-in-One)
**Purpose**: Complete storyboard creation from Ollama text

**Inputs**:
- `ollama_text` (STRING): The text output from an Ollama Generate node
- Layout and styling options (same as StoryboardCompositor)
- `image_1`, `image_2`, `image_3` (IMAGE, optional): If provided, creates visual storyboard

**Outputs**:
- `scene_1`, `scene_2`, `scene_3` (STRING): Parsed scene descriptions
- `storyboard` (IMAGE): Combined storyboard (visual if images provided, text-based if not)

## Example Workflow

### Basic Workflow:
1. **Ollama Generate** → `ollama_text`
2. **SceneParser** → `scene_1`, `scene_2`, `scene_3`
3. **CLIP Text Encode** (3x) → `conditioning_1`, `conditioning_2`, `conditioning_3`
4. **KSampler** (3x) → `latent_1`, `latent_2`, `latent_3`
5. **VAE Decode** (3x) → `image_1`, `image_2`, `image_3`
6. **StoryboardCompositor** → `storyboard`

### Simplified Workflow:
1. **Ollama Generate** → `ollama_text`
2. **FairyTalerStoryboard** → `scene_1`, `scene_2`, `scene_3`, `storyboard`
3. Use the scene descriptions with your preferred image generation workflow
4. Connect the generated images back to **FairyTalerStoryboard** for final composition

## Example Input/Output

### Input (from Ollama):
```
Scene 1:
A girl sits on the front steps of a cabin, lost in thought. A car pulls up to the cabin and parks nearby...

Scene 2:
The girl continues to work on her homespun as the crows scatter from the sagging eaves...

Scene 3:
The girl introduces herself as "Stranger" and explains that she is in these parts without cause...
```

### Output:
- Three separate scene descriptions for image generation
- A combined storyboard image with all three scenes arranged according to your layout preference

## Tips

1. **For best results**: Use the individual nodes for maximum control over the image generation process
2. **For quick testing**: Use the FairyTalerStoryboard all-in-one node
3. **Layout options**: 
   - Vertical: Scenes stacked top to bottom
   - Horizontal: Scenes side by side
   - Grid: 2x2 layout with 3 scenes
4. **Debug mode**: Enable to see parsing details and troubleshoot issues
