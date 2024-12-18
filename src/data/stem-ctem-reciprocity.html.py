import asyncio

from marimo import MarimoIslandGenerator

generator = MarimoIslandGenerator.from_file("src/data-files/stem-ctem-reciprocity.py")
app = asyncio.run(generator.build())
body = generator.render_body(style="margin: auto; max-width: 100%;")
print(body)
