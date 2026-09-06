from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess, textwrap, shutil

W,H,FPS=512,910,24
BG,FG,LIME,MUTED="#0F1114","#F2F2F2","#C6FF00","#6B6F76"
OUT=Path("output"); FR=OUT/"frames"; OUT.mkdir(exist_ok=True); FR.mkdir(exist_ok=True)

SCENES=[
(0.00,9.75,"DECISION QUESTION","Quando acquisisci una piattaforma che vale perché è neutrale, come ottieni i benefici del controllo senza distruggere la fiducia che ne alimenta il valore?"),
(9.75,21.00,"THE CASE","NVIDIA ha concordato l’acquisizione di Hugging Face per 12,93 miliardi di dollari."),
(21.00,28.30,"SCALE","Hugging Face è una piattaforma aperta usata da oltre 18 milioni di sviluppatori e più di 200.000 aziende."),
(28.30,40.20,"THE TENSION","NVIDIA può rafforzarne infrastruttura e affidabilità. Ma Hugging Face serve anche modelli, cloud e processori concorrenti."),
(40.20,53.20,"THE TRADE-OFF","Integrare infrastruttura, sicurezza e capacità di investimento mantenendo credibilmente neutrali accesso, interoperabilità e libertà di scelta."),
(53.20,61.70,"DECISION","Il controllo crea valore soltanto se non compromette il motivo per cui utenti e partner partecipano alla piattaforma."),
(61.70,70.00,"NOW WHAT","Prima della chiusura, misura entrambe le cose: benefici dell’integrazione e continuità di una scelta reale.")
]

def font(bold=False,size=28):
    p="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(p,size)

def wrapped(draw,text,x,y,f,fill,width,spacing=9):
    for line in textwrap.wrap(text,width=width):
        draw.text((x,y),line,font=f,fill=fill)
        y=draw.textbbox((x,y),line,font=f)[3]+spacing

def make_scene(i,label,body,path):
    img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)
    d.rounded_rectangle((34,42,42,196),radius=4,fill=LIME)
    d.text((58,44),"DECISIONOS",font=font(True,20),fill=FG)
    d.text((58,72),"M010.3 • CONTROLLED REPLAY",font=font(False,18),fill=MUTED)
    d.text((36,232),label,font=font(True,20),fill=LIME)
    bf=font(True,42) if i in (0,5) else font(False,27)
    wrapped(d,body,36,285,bf,FG,22 if i in (0,5) else 29,11)
    d.line((36,824,476,824),fill="#2A2D31",width=2)
    d.text((36,842),"Infrastructure smoke test — not Founder Gate",font=font(False,16),fill=MUTED)
    img.save(path)

if not shutil.which("ffmpeg"):
    raise SystemExit("ffmpeg not found")

items=[]
for i,(s,e,label,body) in enumerate(SCENES):
    p=FR/f"scene_{i:02d}.png"; make_scene(i,label,body,p); items.append((p,e-s))

cf=OUT/"concat.txt"
with cf.open("w",encoding="utf-8") as f:
    for p,dur in items:
        f.write(f"file '{p.resolve()}'\n")
        f.write(f"duration {dur:.6f}\n")
    f.write(f"file '{items[-1][0].resolve()}'\n")

out=OUT/"DecisionOS_M0103_NVIDIA_VISUAL_SMOKE_TEST.mp4"
subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(cf),"-vf",f"fps={FPS},format=yuv420p","-c:v","libx264","-pix_fmt","yuv420p","-movflags","+faststart",str(out)],check=True)
print(out)
