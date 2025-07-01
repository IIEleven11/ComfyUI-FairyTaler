#!/usr/bin/env python3
"""
Example demonstrating the Scene Constants feature for character/setting consistency

This shows how your specific example would work with scene constants applied.
"""

def demonstrate_scene_constants():
    """Demonstrate the scene constants feature with your example"""
    
    print("🎬 FairyTaler Scene Constants Feature Demo")
    print("=" * 60)
    
    # Your original Ollama output
    original_ollama_output = """
Scene 1:
A girl sits on the front steps of a cabin, lost in thought. A car pulls up to the cabin and parks nearby. The girl remains seated and does not acknowledge the arrival of the car or its occupant. Crows cluster around the porch and the palings, creating a sense of foreboding. There is no food for them but they remain close by.

Scene 2:
The girl continues to work on her homespun as the crows scatter from the sagging eaves and caw loudly at the newcomer. The humidity presses down on the skin of the person stepping out of the car, creating a sense of discomfort and unease. The girl, now alerted by the presence of the stranger, stands up and raises her head to look towards the approaching person.

Scene 3:
The girl introduces herself as "Stranger" and explains that she is in these parts without cause. She has a guarded expression on her face and her body language indicates wariness and unease. Some crows perch nearby, adding to the tension of the scene. The girl makes it clear that the person needs to state their business clearly before she will continue to engage with them.
"""
    
    # Your suggested scene constants
    scene_constants = "1 girl around 25 years old, homeless looking, at a cabin in the woods, gloomy and country aesthetic"
    
    print("📝 Original Ollama Output:")
    print(original_ollama_output)
    
    print(f"🎯 Scene Constants to Apply:")
    print(f'"{scene_constants}"')
    
    print("\n" + "=" * 60)
    print("🔄 Processing with Scene Constants...")
    print("=" * 60)
    
    # Simulate the parsing (simplified version)
    import re
    
    scene_pattern = r"Scene\s*(\d+):\s*(.*?)(?=Scene\s*\d+:|$)"
    matches = re.findall(scene_pattern, original_ollama_output, re.DOTALL | re.IGNORECASE)
    
    original_scenes = ["", "", ""]
    for match in matches:
        scene_num = int(match[0]) - 1
        if 0 <= scene_num < 3:
            original_scenes[scene_num] = match[1].strip()
    
    # Apply constants with different configurations
    configurations = [
        ("beginning", "natural", "🎬 Best for Image Generation"),
        ("end", "descriptive", "📝 Best for Narrative Flow"),
        ("both", "natural", "🔒 Maximum Consistency")
    ]
    
    for position, format_type, description in configurations:
        print(f"\n{description}")
        print(f"Position: {position} | Format: {format_type}")
        print("-" * 50)
        
        enhanced_scenes = apply_constants(original_scenes, scene_constants, position, format_type)
        
        for i, scene in enumerate(enhanced_scenes):
            print(f"\n🎭 Scene {i+1} (Enhanced):")
            print(f"'{scene}'")
    
    print("\n" + "=" * 60)
    print("✨ Benefits of Scene Constants:")
    print("=" * 60)
    print("✅ Character consistency across all scenes")
    print("✅ Setting details maintained throughout")
    print("✅ Art style consistency for image generation")
    print("✅ Reduced need for manual prompt engineering")
    print("✅ Better results from image models")
    
    print("\n💡 Recommended Settings:")
    print("- Position: 'beginning' (for image generation)")
    print("- Format: 'natural' (for proper flow)")
    print("- Include: age, appearance, location, style/mood")

def apply_constants(scenes, constants, position, format_type):
    """Apply scene constants (mirrors the node logic)"""
    
    # Format the constants
    if format_type == "tags":
        formatted_constants = constants
    elif format_type == "descriptive":
        if not constants.endswith('.'):
            formatted_constants = constants + "."
        else:
            formatted_constants = constants
    else:  # natural
        formatted_constants = constants
        if not constants.endswith(('.', ',', ';')):
            formatted_constants = constants + ","
    
    # Apply to each scene
    enhanced_scenes = []
    for scene in scenes:
        if not scene:
            enhanced_scenes.append(scene)
            continue
            
        if position == "beginning":
            enhanced_scene = f"{formatted_constants} {scene}"
        elif position == "end":
            enhanced_scene = f"{scene} {formatted_constants}"
        else:  # both
            enhanced_scene = f"{formatted_constants} {scene} {formatted_constants}"
        
        enhanced_scenes.append(enhanced_scene)
    
    return enhanced_scenes

if __name__ == "__main__":
    demonstrate_scene_constants()
