# LLM Prompt Examples for Automatic Constant Extraction

This document provides example prompts to use with your LLM (Ollama) to get both scenes and constants automatically.

## 🎯 Basic Prompt Template

```
Transform this roleplay text into 3 scenes for a storyboard. Also provide scene constants for character and setting consistency.

[Your roleplay text here]

Please format your response as:

Constants: [character age, appearance, setting, style/mood]

Scene 1: [scene description]
Scene 2: [scene description]
Scene 3: [scene description]
```

## 📝 Example Prompts

### Example 1: Direct Constants Format
```
Transform this roleplay text into 3 scenes for a storyboard. Also provide scene constants for character and setting consistency.

A girl sits on the front steps slaughtering time. She seems lost in thought, for she does not raise her head when your car pulls up to her cabin. She only continues to work on her homespun. Around her, crows cluster on the porch and the palings. There's no food, yet they cluster anyway. When you get out of the car, they scatter to the sagging eaves and caw at you. Humidity presses on your skin. Alerted by the crows, the girl raises her head as you approach. She's young. Her eyes are a murky blue, her left bruised and swollen. Welts pepper her arms. There is a pause, then she stands. "Stranger," she says. "Folks don't usually wander 'round these hollers without cause." There's a guardedness about her, a wariness reminiscent of a wild animal. As if sensing her unease, some crows perch by her feet. "Best make your business clear."

Please format as:
Constants: [character and setting details]
Scene 1: [description]
Scene 2: [description]
Scene 3: [description]
```

### Example 2: Detailed Format
```
Create a 3-scene storyboard from this text. Include character and setting constants for consistency.

[Your text here]

Format:
Character Description: [age, appearance, demeanor]
Setting Description: [location, atmosphere, style]
Scene 1: [action and description]
Scene 2: [action and description]
Scene 3: [action and description]
```

### Example 3: Bullet Point Format
```
Transform this into 3 storyboard scenes with consistency guidelines:

[Your text here]

Please provide:
For consistency across all scenes:
• Character: [details]
• Setting: [details]
• Style: [mood/aesthetic]

Scene 1: [description]
Scene 2: [description]
Scene 3: [description]
```

## 🎨 Expected LLM Response Examples

### Response Format 1: Direct Constants
```
Constants: 1 girl around 25 years old, homeless looking, at a cabin in the woods, gloomy and country aesthetic

Scene 1:
A girl sits on the front steps of a cabin, lost in thought. A car pulls up to the cabin and parks nearby. The girl remains seated and does not acknowledge the arrival of the car or its occupant. Crows cluster around the porch and the palings, creating a sense of foreboding.

Scene 2:
The girl continues to work on her homespun as the crows scatter from the sagging eaves and caw loudly at the newcomer. The humidity presses down on the skin of the person stepping out of the car, creating a sense of discomfort and unease. The girl, now alerted by the presence of the stranger, stands up and raises her head to look towards the approaching person.

Scene 3:
The girl introduces herself as "Stranger" and explains that she is in these parts without cause. She has a guarded expression on her face and her body language indicates wariness and unease. Some crows perch nearby, adding to the tension of the scene. The girl makes it clear that the person needs to state their business clearly before she will continue to engage with them.
```

### Response Format 2: Descriptive Format
```
Character Description: A young woman around 25 years old with a weathered, homeless appearance and guarded demeanor

Setting Description: Isolated cabin in the woods with a dark, gloomy country aesthetic

Scene 1: [scene content]
Scene 2: [scene content]
Scene 3: [scene content]
```

## 💡 Tips for Better Results

### Character Constants Should Include:
- Age and gender
- Physical appearance
- Clothing style
- Demeanor/personality traits
- Any distinctive features

### Setting Constants Should Include:
- Location type (cabin, city, etc.)
- Time period or era
- Weather/atmosphere
- Architectural style
- Color palette/mood

### Style Constants Should Include:
- Art style (realistic, stylized, etc.)
- Mood (dark, bright, mysterious, etc.)
- Aesthetic (country, urban, fantasy, etc.)
- Lighting (dim, bright, dramatic, etc.)

## 🔧 Integration with ComfyUI Nodes

1. **Use the prompt** → Get LLM response with constants
2. **Feed to SceneParser** → Automatically extracts constants and scenes
3. **Constants applied** → Each scene gets the consistent details
4. **Generate images** → Better consistency across all 3 scenes

## 🚀 Advanced Prompting

For even better results, you can be more specific:

```
Create a 3-scene storyboard optimized for image generation. Include detailed constants for visual consistency.

[Your text]

Provide:
Visual Constants: [specific details for image models - age, hair, clothing, setting, lighting, style]
Scene 1: [detailed visual description]
Scene 2: [detailed visual description]  
Scene 3: [detailed visual description]

Focus on visual elements that will help maintain character and setting consistency across all generated images.
```

This approach ensures your storyboards have maximum visual consistency!
