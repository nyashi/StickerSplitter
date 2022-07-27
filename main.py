from flask import Flask, render_template, request,send_file
#from werkzeug import secure_filename
from io import BytesIO
from PIL import Image
from PIL import UnidentifiedImageError
from zipfile import ZipFile,ZipInfo as zi,ZIP_DEFLATED
app = Flask(__name__)
import os,time
@app.route('/')
def upload_file2():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      i=BytesIO()
      i.seek(0)
      f.save(i)
      try:
          a=Image.open(i).convert('RGBA')
      except UnidentifiedImageError:
          return "No se pudo determinar el tipo de imagen"


      a=a.resize((1024,1024),Image.Resampling.LANCZOS)
      b=a.crop((0,0,512,512))
      c=a.crop((512,0,1024,512))

      d=a.crop((0,512,512,1024))
      z=a.crop((512,512,1024,1024))
      e=BytesIO()
      f=BytesIO()
      g=BytesIO()
      h=BytesIO()
      b.save(e,'PNG')
      c.save(f,'PNG')
      d.save(g,'PNG')
      z.save(h,'PNG')
      myxip=BytesIO()
      [x.seek(0) for x in [e,f,g,h]]
      images=[x.getvalue() for x in [e,f,g,h]]
      file=ZipFile(myxip,'w')
      for i,imagen in enumerate(images):
         data = zi(f"{i}.png")
         data.date_time = time.localtime(time.time())[:6]
         data.compress_type = ZIP_DEFLATED
         file.writestr(data,imagen)
      file.close()
      myxip.seek(0)
      

      
      return send_file(myxip,as_attachment=True,attachment_name="sticker.zip")
		
if __name__ == '__main__':
    app.run("0.0.0.0")
