import asyncio

from marimo import MarimoIslandGenerator

generator = MarimoIslandGenerator.from_file("src/data-files/bf-images-stack.py")
app = asyncio.run(generator.build())
body = generator.render_body(style="margin: auto; max-width: 100%;")
print(body)
