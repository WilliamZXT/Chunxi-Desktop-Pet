"""Application icon derived from the approved neutral frame, no new drawing."""
from pathlib import Path
from PIL import Image

desktop=Path(__file__).resolve().parents[1]
source=Image.open(desktop.parent/'shared/sprites/spring-v13.webp').convert('RGBA').crop((0,0,192,208))
source=source.crop(source.getbbox())
sizes=[16,24,32,48,64,128,256]
images=[]
for size in sizes:
    image=Image.new('RGBA',(size,size))
    figure=source.copy()
    figure.thumbnail((max(1,round(size*.9)),max(1,round(size*.9))),Image.Resampling.NEAREST)
    image.alpha_composite(figure,((size-figure.width)//2,(size-figure.height)//2))
    images.append(image)
images[-1].save(desktop/'assets/chunxi.ico',format='ICO',sizes=[(s,s) for s in sizes],append_images=images[:-1])
images[-1].save(desktop/'assets/chunxi-icon.png')
print('Icon saved from approved pixels.')
