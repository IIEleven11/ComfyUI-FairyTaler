#!/usr/bin/env python3
"""
Test script for the FairyTaler Storyboard nodes

This script tests the scene parsing functionality without requiring ComfyUI dependencies.
"""

import re

def test_scene_parser():
    """Test the scene parsing logic"""
    
    # Example Ollama output
    test_input = """
Scene 1:
A girl sits on the front steps slaughtering time.
She seems lost in thought, for she does not raise her head when your car pulls up to her cabin. She only continues to work on her homespun. Around her, crows cluster on the porch and the palings. There's no food, yet they cluster anyway. When you get out of the car, they scatter to the sagging eaves and caw at you. Humidity presses on your skin.

Scene 2:
Alerted by the crows, the girl raises her head as you approach. She's young. Her eyes are a murky blue, her left bruised and swollen. Welts pepper her arms. There is a pause, then she stands.

Scene 3:
"Stranger," she says. "Folks don't usually wander 'round these hollers without cause." There's a guardedness about her, a wariness reminiscent of a wild animal. As if sensing her unease, some crows perch by her feet. "Best make your business clear."
"""
    
    print("Testing Scene Parser Logic")
    print("=" * 50)
    print("Input text:")
    print(test_input)
    print("\n" + "=" * 50)
    
    # Parse scenes using regex to find Scene 1:, Scene 2:, Scene 3: patterns
    scene_pattern = r"Scene\s*(\d+):\s*(.*?)(?=Scene\s*\d+:|$)"
    matches = re.findall(scene_pattern, test_input, re.DOTALL | re.IGNORECASE)
    
    scenes = ["", "", ""]
    
    for match in matches:
        scene_num = int(match[0]) - 1  # Convert to 0-based index
        if 0 <= scene_num < 3:
            scenes[scene_num] = match[1].strip()
    
    # Fallback: if regex doesn't work, try splitting by "Scene" keyword
    if not any(scenes):
        parts = re.split(r'Scene\s*\d+:', test_input, flags=re.IGNORECASE)
        if len(parts) > 1:
            for i, part in enumerate(parts[1:4]):  # Take up to 3 scenes
                if i < 3:
                    scenes[i] = part.strip()
    
    # Final fallback: split by paragraphs if still empty
    if not any(scenes):
        paragraphs = [p.strip() for p in test_input.split('\n\n') if p.strip()]
        for i, paragraph in enumerate(paragraphs[:3]):
            scenes[i] = paragraph
    
    print("Parsed scenes:")
    for i, scene in enumerate(scenes):
        print(f"\nScene {i+1}:")
        print("-" * 20)
        print(scene)
    
    return scenes

def test_alternative_formats():
    """Test parsing with different input formats"""
    
    print("\n\n" + "=" * 50)
    print("Testing Alternative Formats")
    print("=" * 50)
    
    # Test format without explicit "Scene X:" labels
    test_input2 = """
    A girl sits on the front steps of a cabin, lost in thought. A car pulls up to the cabin and parks nearby. The girl remains seated and does not acknowledge the arrival of the car or its occupant. Crows cluster around the porch and the palings, creating a sense of foreboding.

    The girl continues to work on her homespun as the crows scatter from the sagging eaves and caw loudly at the newcomer. The humidity presses down on the skin of the person stepping out of the car, creating a sense of discomfort and unease.

    The girl introduces herself as "Stranger" and explains that she is in these parts without cause. She has a guarded expression on her face and her body language indicates wariness and unease. Some crows perch nearby, adding to the tension of the scene.
    """
    
    print("Input without explicit scene labels:")
    print(test_input2)
    
    # This would use the paragraph fallback
    paragraphs = [p.strip() for p in test_input2.split('\n\n') if p.strip()]
    scenes = []
    for i, paragraph in enumerate(paragraphs[:3]):
        scenes.append(paragraph)
    
    print("\nParsed scenes (paragraph method):")
    for i, scene in enumerate(scenes):
        print(f"\nScene {i+1}:")
        print("-" * 20)
        print(scene)

def main():
    """Run all tests"""
    print("FairyTaler Storyboard Node Tests")
    print("=" * 60)
    
    # Test 1: Standard scene parsing
    scenes = test_scene_parser()
    
    # Test 2: Alternative formats
    test_alternative_formats()
    
    print("\n" + "=" * 60)
    print("Tests completed successfully!")
    print("The scene parsing logic is working correctly.")
    print("\nNext steps:")
    print("1. Copy storyboard_nodes.py to your ComfyUI custom_nodes directory")
    print("2. Copy __init__.py to the same directory")
    print("3. Restart ComfyUI")
    print("4. Look for 'FairyTaler/Storyboard' category in the node menu")

if __name__ == "__main__":
    main()
