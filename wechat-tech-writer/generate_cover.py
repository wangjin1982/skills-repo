import os
import anthropic

# 初始化Claude客户端
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# 生成图片的提示词
prompt = """A stunning tech cover image for AI tools and productivity, featuring:
- Vibrant gradient background from emerald green (#10b981) to bright orange (#f97316)
- Modern 3D geometric elements (cubes, spheres, pyramids) floating in space
- Subtle circuit board patterns and connecting lines in the background
- Glowing particles and light effects
- Main title "AI工具新势力" in large, bold, simplified Chinese characters positioned at the top center
- Subtitle "Claude引领智能工作新时代" in simplified Chinese, positioned below the main title
- Futuristic and professional tech aesthetic
- High quality, sharp details, photorealistic rendering
- 16:9 landscape orientation
- Minimal text, accurate Chinese characters
- Professional magazine cover style"""

# 调用Claude生成图片
message = client.messages.create(
    model="claude-opus-4-5-20251101",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": f"Please generate an image based on this description: {prompt}"
        }
    ]
)

print("Image generation request sent. Check the response for the image.")
print(message.content)
