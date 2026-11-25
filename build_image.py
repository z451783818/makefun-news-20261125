from PIL import Image, ImageDraw, ImageFont
import os
W=H=1024
img=Image.new("RGB",(W,H),(245,242,235))
d=ImageDraw.Draw(img)
def font(size,bold=False):
    p="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(p,size)
def wrap(text,f,maxw,draw):
    words=text.split(); lines=[]; cur=""
    for w in words:
        t=(cur+" "+w).strip()
        if draw.textlength(t,font=f)<=maxw: cur=t
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines
# header
d.rectangle([0,0,W,118],fill=(18,32,62))
d.text((32,18),"WORLD NEWS",font=font(44,True),fill=(255,255,255))
d.text((32,72),"TUESDAY 25 NOVEMBER 2026",font=font(26),fill=(255,200,80))
d.text((W-32,30),"5 STORIES",font=font(28,True),fill=(255,255,255),anchor="ra")
d.text((W-32,72),"ONE IMAGE",font=font(26),fill=(255,200,80),anchor="ra")
panels=[
 ("SHENZHOU-24 LAUNCHES","China launches Shenzhou-24 with Pakistan's Muhammad Zeeshan Ali, the first foreigner aboard Tiangong.",(0,90,70)),
 ("CARTAGENA HOSTAGES FREED","All hostages rescued as forces storm a Cartagena supermarket. About 30 were seized on Tuesday.",(178,34,34)),
 ("ZELENSKIY CONFIRMS SHIP STRIKE","Ukraine's president confirms Kyiv hit a Russian cargo ship in the Gulf of Finland.",(20,80,140)),
 ("GIULIANI GETS MEDAL OF FREEDOM","Trump awards the top US civilian honour to Rudy Giuliani.",(120,70,0)),
 ("ASIAN STOCKS SELL OFF","Nikkei falls 2.9% as Asian markets slide on fresh US tariff threats.",(0,110,90)),
]
# layout: panel0 full width, then 2x2
boxes=[(24,140,1000,320),(24,344,488,620),(536,344,1000,620),(24,644,488,956),(536,644,1000,956)]
for (title,body,color),(x0,y0,x1,y1) in zip(panels,boxes):
    d.rounded_rectangle([x0,y0,x1,y1],radius=18,fill=(255,255,255),outline=color,width=4)
    d.rectangle([x0,y0,x1,y0+8],fill=color)
    # simple icon: coloured circle with number
    idx=panels.index((title,body,color))+1
    d.ellipse([x0+18,y0+24,x0+66,y0+72],fill=color)
    d.text((x0+42,y0+28),str(idx),font=font(30,True),fill=(255,255,255),anchor="ma")
    # title
    tf=font(30,True) if (x1-x0)>400 else font(26,True)
    lines=wrap(title,tf,x1-x0-36,d)
    y=y0+84
    for ln in lines:
        d.text((x0+18,y),ln,font=tf,fill=(20,20,20)); y+=36
    bf=font(22)
    for ln in wrap(body,bf,x1-x0-36,d):
        d.text((x0+18,y),ln,font=bf,fill=(60,60,60)); y+=30
d.text((32,988),"Sources: Reuters / Al Jazeera / Xinhua / SCMP, 25 Nov 2026",font=font(18),fill=(100,100,100))
out=os.path.expanduser("~/workspace/makefun-news-20261125/asset.png")
img.save(out,format="PNG",optimize=True)
print(out, os.path.getsize(out))
