#!/usr/bin/env python3
"""
Test script for the automatic constant extraction feature

This demonstrates how the LLM can provide both scenes and suggested constants.
"""

import re

def test_auto_constant_extraction():
    """Test the automatic constant extraction from LLM output"""
    
    print("🤖 Automatic Constant Extraction Test")
    print("=" * 60)
    
    # Example LLM outputs with different constant formats
    test_cases = [
        {
            "name": "Direct Constants Format",
            "text": """
Constants: 1 girl around 25 years old, homeless looking, at a cabin in the woods, gloomy and country aesthetic

Scene 1:
A girl sits on the front steps of a cabin, lost in thought. A car pulls up to the cabin and parks nearby.

Scene 2:
The girl continues to work on her homespun as the crows scatter from the sagging eaves.

Scene 3:
"Stranger," she says. "Folks don't usually wander 'round these hollers without cause."
"""
        },
        {
            "name": "Scene Constants Format",
            "text": """
Scene Constants: Young woman, 25 years old, weathered appearance, rural cabin setting, dark atmospheric mood

Scene 1:
A girl sits on the front steps of a cabin, lost in thought. A car pulls up to the cabin and parks nearby.

Scene 2:
The girl continues to work on her homespun as the crows scatter from the sagging eaves.

Scene 3:
"Stranger," she says. "Folks don't usually wander 'round these hollers without cause."
"""
        },
        {
            "name": "Character Description Format",
            "text": """
Character Description: A homeless-looking girl around 25 years old with a guarded demeanor

Setting Description: Isolated cabin in the woods with a gloomy, country aesthetic

Scene 1:
A girl sits on the front steps of a cabin, lost in thought. A car pulls up to the cabin and parks nearby.

Scene 2:
The girl continues to work on her homespun as the crows scatter from the sagging eaves.

Scene 3:
"Stranger," she says. "Folks don't usually wander 'round these hollers without cause."
"""
        },
        {
            "name": "Bullet Point Format",
            "text": """
For consistency across all scenes:
• Character: 25-year-old girl, homeless appearance, wary demeanor
• Setting: Remote cabin in the woods
• Style: Dark, gloomy country aesthetic

Scene 1:
A girl sits on the front steps of a cabin, lost in thought. A car pulls up to the cabin and parks nearby.

Scene 2:
The girl continues to work on her homespun as the crows scatter from the sagging eaves.

Scene 3:
"Stranger," she says. "Folks don't usually wander 'round these hollers without cause."
"""
        },
        {
            "name": "Note Format",
            "text": """
Scene 1:
A girl sits on the front steps of a cabin, lost in thought. A car pulls up to the cabin and parks nearby.

Scene 2:
The girl continues to work on her homespun as the crows scatter from the sagging eaves.

Scene 3:
"Stranger," she says. "Folks don't usually wander 'round these hollers without cause."

Note: For consistency throughout all scenes, maintain: 1 girl around 25 years old, homeless looking, at a cabin in the woods, gloomy and country aesthetic
"""
        },
        {
            "name": "No Explicit Constants (Fallback Test)",
            "text": """
Scene 1:
A 25-year-old girl with a homeless appearance sits on the front steps of a cabin in the woods. The atmosphere is gloomy with a country aesthetic. A car pulls up to the cabin and parks nearby.

Scene 2:
The girl continues to work on her homespun as the crows scatter from the sagging eaves.

Scene 3:
"Stranger," she says. "Folks don't usually wander 'round these hollers without cause."
"""
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Test Case {i}: {test_case['name']}")
        print("-" * 50)
        print("Input:")
        print(test_case['text'])
        
        extracted = extract_constants_from_text(test_case['text'], debug=True)
        
        print(f"\n✅ Extracted Constants: '{extracted}'")
        print("=" * 60)

def extract_constants_from_text(text, debug=False):
    """Extract suggested constants from LLM output (mirrors the node logic)"""
    
    if debug:
        print("🔍 Searching for constants...")
    
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
                if debug:
                    print(f"📍 Found with pattern: {pattern[:30]}...")
                break
    
    # Fallback: Look for character descriptions in the first scene
    if not extracted_constants:
        if debug:
            print("🔄 Using fallback extraction from first scene...")
        
        scene_pattern = r"Scene\s*1:\s*(.*?)(?=Scene\s*2:|$)"
        scene_match = re.search(scene_pattern, text, re.DOTALL | re.IGNORECASE)
        
        if scene_match:
            first_scene = scene_match.group(1).strip()
            # Look for descriptive elements that could be constants
            descriptive_patterns = [
                r"(\d+\s*(?:-year-old|years?\s+old)\s+(?:girl|boy|woman|man|person)[^.]*?)",
                r"((?:at|in)\s+(?:a|the)\s+[^.]*?(?:cabin|house|building|location)[^.]*?)",
                r"([^.]*?(?:aesthetic|style|mood|atmosphere)[^.]*?)",
            ]
            
            potential_constants = []
            for pattern in descriptive_patterns:
                matches = re.findall(pattern, first_scene, re.IGNORECASE)
                potential_constants.extend(matches)
            
            if potential_constants:
                extracted_constants = ", ".join(potential_constants[:3])  # Take first 3 elements
                if debug:
                    print(f"📝 Fallback found: {extracted_constants}")
    
    return extracted_constants

def main():
    """Run the automatic constant extraction tests"""
    test_auto_constant_extraction()
    
    print("\n🎯 Summary:")
    print("The automatic constant extraction feature can handle:")
    print("✅ Direct 'Constants:' declarations")
    print("✅ 'Scene Constants:' format")
    print("✅ 'Character Description:' format")
    print("✅ Bullet point lists")
    print("✅ Note sections")
    print("✅ Fallback extraction from scene content")
    print("\n💡 Recommended LLM prompt addition:")
    print("'Please also provide scene constants for character and setting consistency.'")

if __name__ == "__main__":
    main()
