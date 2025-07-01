"""
Example workflow demonstrating how to use the FairyTaler Storyboard nodes

This is a conceptual example showing how the nodes would be connected in ComfyUI.
The actual workflow would be created in the ComfyUI interface.
"""

# Example Ollama output that would be input to the system
EXAMPLE_OLLAMA_OUTPUT = """
Scene 1:
A girl sits on the front steps of a cabin, lost in thought. A car pulls up to the cabin and parks nearby. The girl remains seated and does not acknowledge the arrival of the car or its occupant. Crows cluster around the porch and the palings, creating a sense of foreboding. There is no food for them but they remain close by.

Scene 2:
The girl continues to work on her homespun as the crows scatter from the sagging eaves and caw loudly at the newcomer. The humidity presses down on the skin of the person stepping out of the car, creating a sense of discomfort and unease. The girl, now alerted by the presence of the stranger, stands up and raises her head to look towards the approaching person.

Scene 3:
The girl introduces herself as "Stranger" and explains that she is in these parts without cause. She has a guarded expression on her face and her body language indicates wariness and unease. Some crows perch nearby, adding to the tension of the scene. The girl makes it clear that the person needs to state their business clearly before she will continue to engage with them.
"""

# Workflow 1: Using individual nodes for maximum control
def workflow_individual_nodes():
    """
    Workflow using individual nodes for maximum control over each step
    """
    # Step 1: Parse the Ollama output into scenes
    # Node: SceneParser
    # Input: ollama_text = EXAMPLE_OLLAMA_OUTPUT
    # Output: scene_1, scene_2, scene_3
    
    # Step 2: Convert each scene to conditioning
    # Node: SceneToConditioning (3 instances)
    # Input: scene_text = scene_1/scene_2/scene_3, clip = your_clip_model
    # Output: conditioning_1, conditioning_2, conditioning_3
    
    # Step 3: Generate images using standard ComfyUI nodes
    # Node: KSampler (3 instances)
    # Input: model, positive=conditioning_1/2/3, negative=empty_conditioning, etc.
    # Output: latent_1, latent_2, latent_3
    
    # Step 4: Decode latents to images
    # Node: VAE Decode (3 instances)
    # Input: samples=latent_1/2/3, vae=your_vae
    # Output: image_1, image_2, image_3
    
    # Step 5: Compose final storyboard
    # Node: StoryboardCompositor
    # Input: image_1, image_2, image_3, layout="vertical", spacing=10, etc.
    # Output: storyboard
    
    pass

# Workflow 2: Using the all-in-one node for simplicity
def workflow_all_in_one():
    """
    Simplified workflow using the FairyTalerStoryboard all-in-one node
    """
    # Step 1: Parse scenes and create text-based storyboard
    # Node: FairyTalerStoryboard
    # Input: ollama_text = EXAMPLE_OLLAMA_OUTPUT
    # Output: scene_1, scene_2, scene_3, text_storyboard
    
    # Step 2: Use scenes with your preferred image generation workflow
    # (Connect scene_1, scene_2, scene_3 to CLIP Text Encode nodes, then to KSampler, etc.)
    
    # Step 3: Connect generated images back to FairyTalerStoryboard for final composition
    # Node: FairyTalerStoryboard
    # Input: ollama_text, image_1, image_2, image_3, layout="horizontal"
    # Output: scene_1, scene_2, scene_3, visual_storyboard
    
    pass

# Example of expected scene parsing results
EXPECTED_PARSED_SCENES = {
    "scene_1": "A girl sits on the front steps of a cabin, lost in thought. A car pulls up to the cabin and parks nearby. The girl remains seated and does not acknowledge the arrival of the car or its occupant. Crows cluster around the porch and the palings, creating a sense of foreboding. There is no food for them but they remain close by.",
    
    "scene_2": "The girl continues to work on her homespun as the crows scatter from the sagging eaves and caw loudly at the newcomer. The humidity presses down on the skin of the person stepping out of the car, creating a sense of discomfort and unease. The girl, now alerted by the presence of the stranger, stands up and raises her head to look towards the approaching person.",
    
    "scene_3": "The girl introduces herself as \"Stranger\" and explains that she is in these parts without cause. She has a guarded expression on her face and her body language indicates wariness and unease. Some crows perch nearby, adding to the tension of the scene. The girl makes it clear that the person needs to state their business clearly before she will continue to engage with them."
}

# ComfyUI workflow connection example (conceptual)
WORKFLOW_CONNECTIONS = {
    "nodes": [
        {
            "id": 1,
            "type": "OllamaGenerate",
            "inputs": {"prompt": "Transform this roleplay text into 3 scenes..."}
        },
        {
            "id": 2,
            "type": "SceneParser",
            "inputs": {"ollama_text": "connect_to_node_1_output"}
        },
        {
            "id": 3,
            "type": "CLIPTextEncode",
            "inputs": {"text": "connect_to_node_2_scene_1"}
        },
        {
            "id": 4,
            "type": "CLIPTextEncode", 
            "inputs": {"text": "connect_to_node_2_scene_2"}
        },
        {
            "id": 5,
            "type": "CLIPTextEncode",
            "inputs": {"text": "connect_to_node_2_scene_3"}
        },
        {
            "id": 6,
            "type": "KSampler",
            "inputs": {"positive": "connect_to_node_3_output"}
        },
        {
            "id": 7,
            "type": "KSampler",
            "inputs": {"positive": "connect_to_node_4_output"}
        },
        {
            "id": 8,
            "type": "KSampler",
            "inputs": {"positive": "connect_to_node_5_output"}
        },
        {
            "id": 9,
            "type": "VAEDecode",
            "inputs": {"samples": "connect_to_node_6_output"}
        },
        {
            "id": 10,
            "type": "VAEDecode",
            "inputs": {"samples": "connect_to_node_7_output"}
        },
        {
            "id": 11,
            "type": "VAEDecode",
            "inputs": {"samples": "connect_to_node_8_output"}
        },
        {
            "id": 12,
            "type": "StoryboardCompositor",
            "inputs": {
                "image_1": "connect_to_node_9_output",
                "image_2": "connect_to_node_10_output", 
                "image_3": "connect_to_node_11_output",
                "layout": "vertical"
            }
        }
    ]
}

if __name__ == "__main__":
    print("This is an example workflow file.")
    print("Use the nodes in ComfyUI interface to create actual workflows.")
    print("\nExample Ollama output:")
    print(EXAMPLE_OLLAMA_OUTPUT)
    print("\nExpected parsed scenes:")
    for scene_id, scene_text in EXPECTED_PARSED_SCENES.items():
        print(f"{scene_id}: {scene_text[:100]}...")
