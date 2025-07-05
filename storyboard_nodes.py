import re
import torch
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import io


class SceneParser:
    """
    A node that takes Ollama text output and parses it into 3 separate scene descriptions
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "ollama_text": ("STRING", {
                    "multiline": True,
                    "default": ""
                }),
                "debug": (["enable", "disable"],),
            },
            "optional": {
                "scene_constants": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "e.g., 1kombat wombat, super ninja skillz, sick and xtreme asthetic"
                }),
                "constants_position": (["beginning", "end", "both"],),
                "constants_format": (["natural", "tags", "descriptive"],),
            },
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("scene_1", "scene_2", "scene_3", "extracted_constants")
    FUNCTION = "parse_scenes"
    CATEGORY = "FairyTaler/Storyboard"

    def parse_scenes(self, ollama_text, debug, scene_constants="", constants_position="beginning", constants_format="natural"):
        if debug == "enable":
            print(f"[SceneParser] Input text:\n{ollama_text}")
            if scene_constants:
                print(f"[SceneParser] Scene constants: {scene_constants}")
                print(f"[SceneParser] Constants position: {constants_position}")
                print(f"[SceneParser] Constants format: {constants_format}")

        # Parse scenes using regex to find Scene 1:, Scene 2:, Scene 3: patterns
        scene_pattern = r"Scene\s*(\d+):\s*(.*?)(?=Scene\s*\d+:|$)"
        matches = re.findall(scene_pattern, ollama_text, re.DOTALL | re.IGNORECASE)

        scenes = ["", "", ""]

        for match in matches:
            scene_num = int(match[0]) - 1  # Convert to 0-based index
            if 0 <= scene_num < 3:
                scenes[scene_num] = match[1].strip()

        # Fallback: if regex doesn't work, try splitting by "Scene" keyword
        if not any(scenes):
            parts = re.split(r'Scene\s*\d+:', ollama_text, flags=re.IGNORECASE)
            if len(parts) > 1:
                for i, part in enumerate(parts[1:4]):  # Take up to 3 scenes
                    if i < 3:
                        scenes[i] = part.strip()

        # Final fallback: split by paragraphs if still empty
        if not any(scenes):
            paragraphs = [p.strip() for p in ollama_text.split('\n\n') if p.strip()]
            for i, paragraph in enumerate(paragraphs[:3]):
                scenes[i] = paragraph

        # Extract constants from LLM output
        extracted_constants = self._extract_constants_from_text(ollama_text, debug)

        # Use extracted constants if no manual constants provided, otherwise use manual ones
        final_constants = scene_constants.strip() if scene_constants and scene_constants.strip() else extracted_constants

        # Apply scene constants if available
        if final_constants:
            scenes = self._apply_scene_constants(scenes, final_constants, constants_position, constants_format, debug)

        if debug == "enable":
            print(f"[SceneParser] Extracted constants: {extracted_constants}")
            print(f"[SceneParser] Final constants used: {final_constants}")
            print(f"[SceneParser] Final scenes with constants applied:")
            for i, scene in enumerate(scenes):
                print(f"Scene {i+1}: {scene[:150]}...")

        return (scenes[0], scenes[1], scenes[2], extracted_constants)

    def _apply_scene_constants(self, scenes, constants, position, format_type, debug):
        """Apply scene constants to each scene based on the specified format and position"""

        if debug == "enable":
            print(f"[SceneParser] Applying constants in {format_type} format at {position}")

        # Format the constants based on the selected format
        if format_type == "tags":
            # Format as comma-separated tags
            formatted_constants = constants
        elif format_type == "descriptive":
            # Format as a descriptive sentence
            if not constants.endswith('.'):
                formatted_constants = constants + "."
            else:
                formatted_constants = constants
        else:  # natural
            # Use as-is but ensure proper punctuation
            formatted_constants = constants
            if not constants.endswith(('.', ',', ';')):
                formatted_constants = constants + ","

        # Apply constants to each scene
        enhanced_scenes = []
        for i, scene in enumerate(scenes):
            if not scene:  # Skip empty scenes
                enhanced_scenes.append(scene)
                continue

            if position == "beginning":
                enhanced_scene = f"{formatted_constants} {scene}"
            elif position == "end":
                enhanced_scene = f"{scene} {formatted_constants}"
            else:  # both
                enhanced_scene = f"{formatted_constants} {scene} {formatted_constants}"

            enhanced_scenes.append(enhanced_scene)

            if debug == "enable":
                print(f"[SceneParser] Enhanced scene {i+1}: {enhanced_scene[:100]}...")

        return enhanced_scenes

    def _extract_constants_from_text(self, text, debug):
        """Extract suggested constants from LLM output using various patterns"""

        if debug == "enable":
            print(f"[SceneParser] Extracting constants from LLM text...")

        # Patterns to look for constants in the LLM output
        constant_patterns = [
            # Direct patterns
            r"Constants?:\s*(.*?)(?:\n\n|\nScene|\n[A-Z]|$)",
            r"Scene Constants?:\s*(.*?)(?:\n\n|\nScene|\n[A-Z]|$)",
            r"Character Constants?:\s*(.*?)(?:\n\n|\nScene|\n[A-Z]|$)",
            r"Setting Constants?:\s*(.*?)(?:\n\n|\nScene|\n[A-Z]|$)",
            r"Consistent Elements?:\s*(.*?)(?:\n\n|\nScene|\n[A-Z]|$)",
            r"Shared Details?:\s*(.*?)(?:\n\n|\nScene|\n[A-Z]|$)",

            # Descriptive patterns
            r"(?:For consistency|To maintain consistency|Consistent across all scenes?):\s*(.*?)(?:\n\n|\nScene|\n[A-Z]|$)",
            r"(?:Character|Setting|Style) (?:description|details?):\s*(.*?)(?:\n\n|\nScene|\n[A-Z]|$)",
            r"(?:Overall|General) (?:setting|character|aesthetic):\s*(.*?)(?:\n\n|\nScene|\n[A-Z]|$)",

            # Bullet point patterns
            r"[•\-\*]\s*(?:Character|Setting|Style|Constants?):\s*(.*?)(?:\n|\n\n|$)",

            # Parenthetical patterns
            r"\((?:Constants?|Consistent elements?|For all scenes?):\s*(.*?)\)",

            # Note patterns
            r"Note:\s*(?:.*?(?:constant|consistent|throughout|all scenes)).*?:\s*(.*?)(?:\n\n|\nScene|\n[A-Z]|$)",
        ]

        extracted_constants = ""

        for pattern in constant_patterns:
            matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)
            if matches:
                # Take the first match and clean it up
                constants = matches[0].strip()
                # Remove extra whitespace and newlines
                constants = re.sub(r'\s+', ' ', constants)
                # Remove trailing punctuation that might interfere
                constants = re.sub(r'[.!?]+$', '', constants)

                if constants and len(constants) > 10:  # Ensure it's substantial
                    extracted_constants = constants
                    if debug == "enable":
                        print(f"[SceneParser] Found constants with pattern: {pattern[:50]}...")
                        print(f"[SceneParser] Extracted: {constants}")
                    break

        # Fallback: Look for character descriptions in the first scene
        if not extracted_constants:
            # Try to extract character/setting info from the first scene
            scene_pattern = r"Scene\s*1:\s*(.*?)(?=Scene\s*2:|$)"
            scene_match = re.search(scene_pattern, text, re.DOTALL | re.IGNORECASE)

            if scene_match:
                first_scene = scene_match.group(1).strip()
                # Look for descriptive elements that could be constants
                descriptive_patterns = [
                    r"(\d+\s+(?:girl|boy|woman|man|person)[^.]*?(?:years?\s+old|looking|appearance)[^.]*?)",
                    r"((?:at|in)\s+(?:a|the)\s+[^.]*?(?:cabin|house|building|location)[^.]*?)",
                    r"([^.]*?(?:aesthetic|style|mood|atmosphere)[^.]*?)",
                ]

                potential_constants = []
                for pattern in descriptive_patterns:
                    matches = re.findall(pattern, first_scene, re.IGNORECASE)
                    potential_constants.extend(matches)

                if potential_constants:
                    extracted_constants = ", ".join(potential_constants[:3])  # Take first 3 elements
                    if debug == "enable":
                        print(f"[SceneParser] Fallback extraction from first scene: {extracted_constants}")

        if debug == "enable":
            if extracted_constants:
                print(f"[SceneParser] Successfully extracted constants: {extracted_constants}")
            else:
                print(f"[SceneParser] No constants found in LLM output")

        return extracted_constants


class SceneToConditioning:
    """
    A node that takes a scene description and converts it to conditioning for use with sampling nodes
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "scene_text": ("STRING", {
                    "multiline": True,
                    "default": ""
                }),
                "clip": ("CLIP",),
                "debug": (["enable", "disable"],),
            },
        }

    RETURN_TYPES = ("CONDITIONING",)
    RETURN_NAMES = ("conditioning",)
    FUNCTION = "encode_scene"
    CATEGORY = "FairyTaler/Storyboard"

    def encode_scene(self, scene_text, clip, debug):
        if debug == "enable":
            print(f"[SceneToConditioning] Encoding scene: {scene_text[:100]}...")

        # Encode the text using CLIP
        tokens = clip.tokenize(scene_text)
        cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)

        # Create conditioning object in ComfyUI format
        conditioning = [[cond, {"pooled_output": pooled}]]

        if debug == "enable":
            print(f"[SceneToConditioning] Created conditioning with shape: {cond.shape}")

        return (conditioning,)


class ThreeSceneGenerator:
    """
    A comprehensive node that takes 3 scene texts and generates 3 images using sampling
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "scene_1": ("STRING", {
                    "multiline": True,
                    "default": ""
                }),
                "scene_2": ("STRING", {
                    "multiline": True,
                    "default": ""
                }),
                "scene_3": ("STRING", {
                    "multiline": True,
                    "default": ""
                }),
                "model": ("MODEL",),
                "clip": ("CLIP",),
                "vae": ("VAE",),
                "width": ("INT", {
                    "default": 512,
                    "min": 64,
                    "max": 2048,
                    "step": 8
                }),
                "height": ("INT", {
                    "default": 512,
                    "min": 64,
                    "max": 2048,
                    "step": 8
                }),
                "steps": ("INT", {
                    "default": 20,
                    "min": 1,
                    "max": 100,
                    "step": 1
                }),
                "cfg": ("FLOAT", {
                    "default": 7.0,
                    "min": 1.0,
                    "max": 20.0,
                    "step": 0.1
                }),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xffffffffffffffff
                }),
                "sampler_name": (["euler", "euler_ancestral", "heun", "dpm_2", "dpm_2_ancestral", "lms", "dpm_fast", "dpm_adaptive", "dpmpp_2s_ancestral", "dpmpp_sde", "dpmpp_2m", "ddim", "uni_pc", "uni_pc_bh2"],),
                "scheduler": (["normal", "karras", "exponential", "sgm_uniform", "simple", "ddim_uniform"],),
                "debug": (["enable", "disable"],),
            },
            "optional": {
                "negative_prompt": ("STRING", {
                    "multiline": True,
                    "default": ""
                }),
            },
        }

    RETURN_TYPES = ("IMAGE", "IMAGE", "IMAGE")
    RETURN_NAMES = ("image_1", "image_2", "image_3")
    FUNCTION = "generate_three_scenes"
    CATEGORY = "FairyTaler/Storyboard"

    def generate_three_scenes(self, scene_1, scene_2, scene_3, model, clip, vae, width, height, steps, cfg, seed, sampler_name, scheduler, debug, negative_prompt=""):
        if debug == "enable":
            print(f"[ThreeSceneGenerator] This node outputs conditioning for use with sampling nodes.")
            print(f"[ThreeSceneGenerator] For actual image generation, connect the conditioning outputs to KSampler nodes.")

        # This is a simplified version that outputs conditioning
        # In practice, users should connect these to KSampler and VAEDecode nodes
        scenes = [scene_1, scene_2, scene_3]
        conditionings = []

        for i, scene_text in enumerate(scenes):
            if debug == "enable":
                print(f"[ThreeSceneGenerator] Processing scene {i+1}: {scene_text[:50]}...")

            # Encode positive conditioning
            tokens = clip.tokenize(scene_text)
            cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
            conditioning = [[cond, {"pooled_output": pooled}]]
            conditionings.append(conditioning)

        # For now, return placeholder images - users should use proper sampling workflow
        # Create simple colored placeholder images to show the concept works
        placeholder_images = []
        colors = [(255, 100, 100), (100, 255, 100), (100, 100, 255)]  # Red, Green, Blue

        for i, color in enumerate(colors):
            # Create a simple colored image as placeholder
            img_array = np.full((height, width, 3), color, dtype=np.uint8)
            img_tensor = torch.from_numpy(img_array.astype(np.float32) / 255.0).unsqueeze(0)
            placeholder_images.append(img_tensor)

            if debug == "enable":
                print(f"[ThreeSceneGenerator] Created placeholder image {i+1} with color {color}")

        return (placeholder_images[0], placeholder_images[1], placeholder_images[2])


class StoryboardCompositor:
    """
    A node that takes 3 images and combines them into a single storyboard layout
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image_1": ("IMAGE",),
                "image_2": ("IMAGE",),
                "image_3": ("IMAGE",),
                "layout": (["vertical", "horizontal", "grid"],),
                "spacing": ("INT", {
                    "default": 10,
                    "min": 0,
                    "max": 100,
                    "step": 1
                }),
                "background_color": ("STRING", {
                    "default": "white"
                }),
                "add_labels": (["enable", "disable"],),
                "debug": (["enable", "disable"],),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("storyboard",)
    FUNCTION = "compose_storyboard"
    CATEGORY = "FairyTaler/Storyboard"

    def compose_storyboard(self, image_1, image_2, image_3, layout, spacing, background_color, add_labels, debug):
        if debug == "enable":
            print(f"[StoryboardCompositor] Creating {layout} storyboard with {spacing}px spacing")
        
        # Convert tensors to PIL Images
        def tensor_to_pil(tensor):
            # Convert from tensor format [batch, height, width, channels] to PIL
            if len(tensor.shape) == 4:
                tensor = tensor[0]  # Remove batch dimension
            
            # Convert from [0,1] float to [0,255] uint8
            if tensor.dtype == torch.float32:
                tensor = (tensor * 255).clamp(0, 255).byte()
            
            # Convert to numpy and then PIL
            np_image = tensor.cpu().numpy()
            return Image.fromarray(np_image)
        
        pil_images = [tensor_to_pil(img) for img in [image_1, image_2, image_3]]
        
        # Get dimensions
        img_width, img_height = pil_images[0].size
        
        # Calculate storyboard dimensions based on layout
        if layout == "vertical":
            board_width = img_width
            board_height = img_height * 3 + spacing * 2
        elif layout == "horizontal":
            board_width = img_width * 3 + spacing * 2
            board_height = img_height
        else:  # grid (2x2 with 3 images)
            board_width = img_width * 2 + spacing
            board_height = img_height * 2 + spacing
        
        # Add space for labels if enabled
        label_height = 30 if add_labels == "enable" else 0
        if layout == "vertical":
            board_height += label_height * 3
        elif layout == "horizontal":
            board_height += label_height
        else:  # grid
            board_height += label_height * 2
        
        # Create the storyboard canvas
        storyboard = Image.new('RGB', (board_width, board_height), background_color)
        
        # Position images based on layout
        positions = []
        if layout == "vertical":
            positions = [
                (0, 0),
                (0, img_height + spacing + label_height),
                (0, (img_height + spacing + label_height) * 2)
            ]
        elif layout == "horizontal":
            positions = [
                (0, label_height),
                (img_width + spacing, label_height),
                ((img_width + spacing) * 2, label_height)
            ]
        else:  # grid
            positions = [
                (0, label_height),
                (img_width + spacing, label_height),
                (0, img_height + spacing + label_height * 2)
            ]
        
        # Paste images
        for i, (img, pos) in enumerate(zip(pil_images, positions)):
            storyboard.paste(img, pos)
            
            # Add labels if enabled
            if add_labels == "enable":
                draw = ImageDraw.Draw(storyboard)
                try:
                    font = ImageFont.load_default()
                except:
                    font = None
                
                label_text = f"Scene {i + 1}"
                if layout == "vertical":
                    label_pos = (5, pos[1] - 25)
                elif layout == "horizontal":
                    label_pos = (pos[0] + 5, 5)
                else:  # grid
                    if i < 2:
                        label_pos = (pos[0] + 5, 5)
                    else:
                        label_pos = (pos[0] + 5, img_height + spacing + label_height + 5)
                
                draw.text(label_pos, label_text, fill="black", font=font)
        
        # Convert back to tensor format
        storyboard_array = np.array(storyboard).astype(np.float32) / 255.0
        storyboard_tensor = torch.from_numpy(storyboard_array).unsqueeze(0)  # Add batch dimension
        
        if debug == "enable":
            print(f"[StoryboardCompositor] Created storyboard with dimensions: {storyboard.size}")
        
        return (storyboard_tensor,)


class FairyTalerStoryboard:
    """
    A comprehensive node that takes Ollama output and creates a complete 3-scene storyboard
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "ollama_text": ("STRING", {
                    "multiline": True,
                    "default": ""
                }),
                "layout": (["vertical", "horizontal", "grid"],),
                "spacing": ("INT", {
                    "default": 10,
                    "min": 0,
                    "max": 100,
                    "step": 1
                }),
                "background_color": ("STRING", {
                    "default": "white"
                }),
                "add_labels": (["enable", "disable"],),
                "debug": (["enable", "disable"],),
            },
            "optional": {
                "image_1": ("IMAGE",),
                "image_2": ("IMAGE",),
                "image_3": ("IMAGE",),
                "scene_constants": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "e.g., 1 girl around 25 years old, homeless looking, at a cabin in the woods, gloomy and country aesthetic"
                }),
                "constants_position": (["beginning", "end", "both"],),
                "constants_format": (["natural", "tags", "descriptive"],),
            },
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "IMAGE", "STRING")
    RETURN_NAMES = ("scene_1", "scene_2", "scene_3", "storyboard", "extracted_constants")
    FUNCTION = "create_storyboard"
    CATEGORY = "FairyTaler/Storyboard"

    def create_storyboard(self, ollama_text, layout, spacing, background_color, add_labels, debug, image_1=None, image_2=None, image_3=None, scene_constants="", constants_position="beginning", constants_format="natural"):
        if debug == "enable":
            print(f"[FairyTalerStoryboard] Creating complete storyboard from Ollama text")

        # Parse scenes using the same logic as SceneParser
        scene_pattern = r"Scene\s*(\d+):\s*(.*?)(?=Scene\s*\d+:|$)"
        matches = re.findall(scene_pattern, ollama_text, re.DOTALL | re.IGNORECASE)

        scenes = ["", "", ""]

        for match in matches:
            scene_num = int(match[0]) - 1  # Convert to 0-based index
            if 0 <= scene_num < 3:
                scenes[scene_num] = match[1].strip()

        # Fallback: if regex doesn't work, try splitting by "Scene" keyword
        if not any(scenes):
            parts = re.split(r'Scene\s*\d+:', ollama_text, flags=re.IGNORECASE)
            if len(parts) > 1:
                for i, part in enumerate(parts[1:4]):  # Take up to 3 scenes
                    if i < 3:
                        scenes[i] = part.strip()

        # Final fallback: split by paragraphs if still empty
        if not any(scenes):
            paragraphs = [p.strip() for p in ollama_text.split('\n\n') if p.strip()]
            for i, paragraph in enumerate(paragraphs[:3]):
                scenes[i] = paragraph

        # Extract constants from LLM output (reuse the logic from SceneParser)
        extracted_constants = self._extract_constants_from_text(ollama_text, debug)

        # Use extracted constants if no manual constants provided, otherwise use manual ones
        final_constants = scene_constants.strip() if scene_constants and scene_constants.strip() else extracted_constants

        # Apply scene constants if available
        if final_constants:
            scenes = self._apply_scene_constants(scenes, final_constants, constants_position, constants_format, debug)

        if debug == "enable":
            print(f"[FairyTalerStoryboard] Extracted constants: {extracted_constants}")
            print(f"[FairyTalerStoryboard] Final constants used: {final_constants}")
            print(f"[FairyTalerStoryboard] Final scenes with constants applied:")
            for i, scene in enumerate(scenes):
                print(f"Scene {i+1}: {scene[:100]}...")

        # If images are provided, create storyboard; otherwise just return scenes
        if image_1 is not None and image_2 is not None and image_3 is not None:
            # Use the same logic as StoryboardCompositor
            def tensor_to_pil(tensor):
                if len(tensor.shape) == 4:
                    tensor = tensor[0]  # Remove batch dimension

                if tensor.dtype == torch.float32:
                    tensor = (tensor * 255).clamp(0, 255).byte()

                np_image = tensor.cpu().numpy()
                return Image.fromarray(np_image)

            pil_images = [tensor_to_pil(img) for img in [image_1, image_2, image_3]]

            # Get dimensions
            img_width, img_height = pil_images[0].size

            # Calculate storyboard dimensions based on layout
            if layout == "vertical":
                board_width = img_width
                board_height = img_height * 3 + spacing * 2
            elif layout == "horizontal":
                board_width = img_width * 3 + spacing * 2
                board_height = img_height
            else:  # grid (2x2 with 3 images)
                board_width = img_width * 2 + spacing
                board_height = img_height * 2 + spacing

            # Add space for labels if enabled
            label_height = 30 if add_labels == "enable" else 0
            if layout == "vertical":
                board_height += label_height * 3
            elif layout == "horizontal":
                board_height += label_height
            else:  # grid
                board_height += label_height * 2

            # Create the storyboard canvas
            storyboard = Image.new('RGB', (board_width, board_height), background_color)

            # Position images based on layout
            positions = []
            if layout == "vertical":
                positions = [
                    (0, 0),
                    (0, img_height + spacing + label_height),
                    (0, (img_height + spacing + label_height) * 2)
                ]
            elif layout == "horizontal":
                positions = [
                    (0, label_height),
                    (img_width + spacing, label_height),
                    ((img_width + spacing) * 2, label_height)
                ]
            else:  # grid
                positions = [
                    (0, label_height),
                    (img_width + spacing, label_height),
                    (0, img_height + spacing + label_height * 2)
                ]

            # Paste images
            for i, (img, pos) in enumerate(zip(pil_images, positions)):
                storyboard.paste(img, pos)

                # Add labels if enabled
                if add_labels == "enable":
                    draw = ImageDraw.Draw(storyboard)
                    try:
                        font = ImageFont.load_default()
                    except:
                        font = None

                    label_text = f"Scene {i + 1}"
                    if layout == "vertical":
                        label_pos = (5, pos[1] - 25)
                    elif layout == "horizontal":
                        label_pos = (pos[0] + 5, 5)
                    else:  # grid
                        if i < 2:
                            label_pos = (pos[0] + 5, 5)
                        else:
                            label_pos = (pos[0] + 5, img_height + spacing + label_height + 5)

                    draw.text(label_pos, label_text, fill="black", font=font)

            # Convert back to tensor format
            storyboard_array = np.array(storyboard).astype(np.float32) / 255.0
            storyboard_tensor = torch.from_numpy(storyboard_array).unsqueeze(0)  # Add batch dimension

            if debug == "enable":
                print(f"[FairyTalerStoryboard] Created storyboard with dimensions: {storyboard.size}")
        else:
            # Create a placeholder storyboard with text
            storyboard = Image.new('RGB', (800, 600), background_color)
            draw = ImageDraw.Draw(storyboard)
            try:
                font = ImageFont.load_default()
            except:
                font = None

            draw.text((10, 10), "Connect images to create visual storyboard", fill="black", font=font)
            draw.text((10, 40), f"Scene 1: {scenes[0][:50]}...", fill="black", font=font)
            draw.text((10, 70), f"Scene 2: {scenes[1][:50]}...", fill="black", font=font)
            draw.text((10, 100), f"Scene 3: {scenes[2][:50]}...", fill="black", font=font)

            storyboard_array = np.array(storyboard).astype(np.float32) / 255.0
            storyboard_tensor = torch.from_numpy(storyboard_array).unsqueeze(0)

        return (scenes[0], scenes[1], scenes[2], storyboard_tensor, extracted_constants)

    def _apply_scene_constants(self, scenes, constants, position, format_type, debug):
        """Apply scene constants to each scene based on the specified format and position"""

        if debug == "enable":
            print(f"[FairyTalerStoryboard] Applying constants in {format_type} format at {position}")

        # Format the constants based on the selected format
        if format_type == "tags":
            # Format as comma-separated tags
            formatted_constants = constants
        elif format_type == "descriptive":
            # Format as a descriptive sentence
            if not constants.endswith('.'):
                formatted_constants = constants + "."
            else:
                formatted_constants = constants
        else:  # natural
            # Use as-is but ensure proper punctuation
            formatted_constants = constants
            if not constants.endswith(('.', ',', ';')):
                formatted_constants = constants + ","

        # Apply constants to each scene
        enhanced_scenes = []
        for i, scene in enumerate(scenes):
            if not scene:  # Skip empty scenes
                enhanced_scenes.append(scene)
                continue

            if position == "beginning":
                enhanced_scene = f"{formatted_constants} {scene}"
            elif position == "end":
                enhanced_scene = f"{scene} {formatted_constants}"
            else:  # both
                enhanced_scene = f"{formatted_constants} {scene} {formatted_constants}"

            enhanced_scenes.append(enhanced_scene)

            if debug == "enable":
                print(f"[FairyTalerStoryboard] Enhanced scene {i+1}: {enhanced_scene[:100]}...")

        return enhanced_scenes

    def _extract_constants_from_text(self, text, debug):
        """Extract suggested constants from LLM output using various patterns"""

        if debug == "enable":
            print(f"[FairyTalerStoryboard] Extracting constants from LLM text...")

        # Patterns to look for constants in the LLM output
        constant_patterns = [
            # Direct patterns
            r"Constants?:\s*(.*?)(?:\n\n|\nScene|\n[A-Z]|$)",
            r"Scene Constants?:\s*(.*?)(?:\n\n|\nScene|\n[A-Z]|$)",
            r"Character Constants?:\s*(.*?)(?:\n\n|\nScene|\n[A-Z]|$)",
            r"Setting Constants?:\s*(.*?)(?:\n\n|\nScene|\n[A-Z]|$)",
            r"Consistent Elements?:\s*(.*?)(?:\n\n|\nScene|\n[A-Z]|$)",
            r"Shared Details?:\s*(.*?)(?:\n\n|\nScene|\n[A-Z]|$)",

            # Descriptive patterns
            r"(?:For consistency|To maintain consistency|Consistent across all scenes?):\s*(.*?)(?:\n\n|\nScene|\n[A-Z]|$)",
            r"(?:Character|Setting|Style) (?:description|details?):\s*(.*?)(?:\n\n|\nScene|\n[A-Z]|$)",
            r"(?:Overall|General) (?:setting|character|aesthetic):\s*(.*?)(?:\n\n|\nScene|\n[A-Z]|$)",

            # Bullet point patterns
            r"[•\-\*]\s*(?:Character|Setting|Style|Constants?):\s*(.*?)(?:\n|\n\n|$)",

            # Parenthetical patterns
            r"\((?:Constants?|Consistent elements?|For all scenes?):\s*(.*?)\)",

            # Note patterns
            r"Note:\s*(?:.*?(?:constant|consistent|throughout|all scenes)).*?:\s*(.*?)(?:\n\n|\nScene|\n[A-Z]|$)",
        ]

        extracted_constants = ""

        for pattern in constant_patterns:
            matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)
            if matches:
                # Take the first match and clean it up
                constants = matches[0].strip()
                # Remove extra whitespace and newlines
                constants = re.sub(r'\s+', ' ', constants)
                # Remove trailing punctuation that might interfere
                constants = re.sub(r'[.!?]+$', '', constants)

                if constants and len(constants) > 10:  # Ensure it's substantial
                    extracted_constants = constants
                    if debug == "enable":
                        print(f"[FairyTalerStoryboard] Found constants with pattern: {pattern[:50]}...")
                        print(f"[FairyTalerStoryboard] Extracted: {constants}")
                    break

        # Fallback: Look for character descriptions in the first scene
        if not extracted_constants:
            # Try to extract character/setting info from the first scene
            scene_pattern = r"Scene\s*1:\s*(.*?)(?=Scene\s*2:|$)"
            scene_match = re.search(scene_pattern, text, re.DOTALL | re.IGNORECASE)

            if scene_match:
                first_scene = scene_match.group(1).strip()
                # Look for descriptive elements that could be constants
                descriptive_patterns = [
                    r"(\d+\s+(?:girl|boy|woman|man|person)[^.]*?(?:years?\s+old|looking|appearance)[^.]*?)",
                    r"((?:at|in)\s+(?:a|the)\s+[^.]*?(?:cabin|house|building|location)[^.]*?)",
                    r"([^.]*?(?:aesthetic|style|mood|atmosphere)[^.]*?)",
                ]

                potential_constants = []
                for pattern in descriptive_patterns:
                    matches = re.findall(pattern, first_scene, re.IGNORECASE)
                    potential_constants.extend(matches)

                if potential_constants:
                    extracted_constants = ", ".join(potential_constants[:3])  # Take first 3 elements
                    if debug == "enable":
                        print(f"[FairyTalerStoryboard] Fallback extraction from first scene: {extracted_constants}")

        if debug == "enable":
            if extracted_constants:
                print(f"[FairyTalerStoryboard] Successfully extracted constants: {extracted_constants}")
            else:
                print(f"[FairyTalerStoryboard] No constants found in LLM output")

        return extracted_constants


# Node mappings for ComfyUI
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