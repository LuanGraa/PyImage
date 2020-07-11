#.------..------.
#|L.--. ||G.--. |
#| :/\: || :/\: |
#| (__) || :\/: |
#| '--'L|| '--'G|
#`------'`------'

import os.path
import cherrypy
import sqlite3
import requests
import json

import re
import webcolors
from PIL import Image
cherrypy.config.update({'server.socket_port': 10016,})
baseDir = os.path.dirname(os.path.abspath(__file__))
config = {
  "/":     { "tools.staticdir.root": baseDir },
  "/js":   { "tools.staticdir.on": True,
             "tools.staticdir.dir": "js" },
  "/css":  { "tools.staticdir.on": True,
             "tools.staticdir.dir": "css" },
  "/html": { "tools.staticdir.on": True,
             "tools.staticdir.dir": "html" },
  "/vendor": { "tools.staticdir.on": True,
             "tools.staticdir.dir": "vendor" },
  "/scss": { "tools.staticdir.on": True,
             "tools.staticdir.dir": "scss" },
  "/img": { "tools.staticdir.on": True,
             "tools.staticdir.dir": "img" },
  "/imgInput": { "tools.staticdir.on": True,
             "tools.staticdir.dir": "imgInput" },
  "/imgOutput": { "tools.staticdir.on": True,
             "tools.staticdir.dir": "imgOutput" },
}

def corDominante(image):

    w, h = image.size
    pixels = image.getcolors(w * h)

    pixelFrequente = pixels[0]

    for count, colour in pixels:
        if count > pixelFrequente[0]:
            pixelFrequente = (count, colour)

    return pixelFrequente[1]

def closestColor(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

class Root:



    indexHTML = """<!DOCTYPE html>
    <html lang="en">

    <head>

      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
      <meta name="description" content="">
      <meta name="author" content="">

      <title>PyImage</title>

      <!-- Bootstrap core CSS -->
      <link href="vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet">

      <!-- Custom fonts for this template -->
      <link href="vendor/fontawesome-free/css/all.min.css" rel="stylesheet">
      <link rel="stylesheet" href="vendor/simple-line-icons/css/simple-line-icons.css">
      <link href="https://fonts.googleapis.com/css?family=Lato" rel="stylesheet">
      <link href="https://fonts.googleapis.com/css?family=Catamaran:100,200,300,400,500,600,700,800,900" rel="stylesheet">
      <link href="https://fonts.googleapis.com/css?family=Muli" rel="stylesheet">

      <!-- Plugin CSS -->
      <link rel="stylesheet" href="device-mockups/device-mockups.min.css">

      <!-- Custom styles for this template -->
      <link href="css/new-age.css" rel="stylesheet">

    </head>

    <body id="page-top">

      <!-- Navigation -->
      <nav class="navbar navbar-expand-lg navbar-light fixed-top" id="mainNav">
        <div class="container">
          <a class="navbar-brand js-scroll-trigger" href="#page-top"><img src="img/python.png" width=40px height=40px>PyImage</a>
          <button class="navbar-toggler navbar-toggler-right" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
            Menu
            <i class="fas fa-bars"></i>
          </button>
          <div class="collapse navbar-collapse" id="navbarResponsive">
            <ul class="navbar-nav ml-auto">
              <li class="nav-item">
                <a class="nav-link js-scroll-trigger" href="/put">Upload</a>
              </li>
              <li class="nav-item">

                <a class="nav-link js-scroll-trigger" href="#"   data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                Listar
                </a>
                <div class="dropdown show">
                <div class="dropdown-menu" aria-labelledby="dropdownMenuLink">
                <a class="dropdown-item" href="/listar">Imagens</a>
                <a class="dropdown-item" href="/listarObj">Objetos</a>
                </div>
                </div>
              </li>
              <li class="nav-item">

                <a class="nav-link js-scroll-trigger" href="#"   data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                JSON
                </a>
                <div class="dropdown show">
                <div class="dropdown-menu" aria-labelledby="dropdownMenuLink">
                <a class="dropdown-item" href="/list?type=names&color=empty&name=empty">Objetos</a>
                <a class="dropdown-item" href="/list?type=detected&color=empty&name=empty">Objetos e originais</a>
                <a class="dropdown-item" href="/listByName">Pesquisar por nome</a>
                <a class="dropdown-item" href="/listByNameAndColor">Pesquisar por nome e cor</a>
                </div>
                </div>
              </li>
              <li class="nav-item">
                <a class="nav-link js-scroll-trigger" href="/dumpinfo">Pesquisar</a>
              </li>
              <li class="nav-item">
                <a class="nav-link js-scroll-trigger" href="/Sobre">Sobre</a>
              </li>
            </ul>
          </div>
        </div>
      </nav>

      <header class="masthead">
        <div class="container h-100">
          <div class="row h-100">
            <div class="col-lg-7 my-auto">
              <div class="header-content mx-auto">
                <h1 class="mb-5"><img src="img/python.png" width=50px height=50px>PyImage<br></h1><h2> A aplicação que permite processar as imagens via Python e SQLite3 </h2>
                <a href="/put" class="btn btn-outline btn-xl js-scroll-trigger">Upload</a>
              </div>
            </div>
            <div class="col-lg-5 my-auto">
              <div class="device-container">
                <div class="device-mockup iphone6_plus portrait white">
                  <div class="device">
                    <div class="screen">
                      <!-- Demo image for screen mockup, you can put an image here, some HTML, an animation, video, or anything else! -->
                      <img src="img/reconhecimento-facial.png" class="img-fluid" alt="">
                    </div>
                    <div class="button">
                      <!-- You can hook the "home button" to some JavaScript events or just remove it -->
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </header>



      <section class="features" id="features">
        <div class="container">
          <div class="section-heading text-center">
            <h2>Como usar?</h2>
            <p class="text-muted">Veja aqui as suas funcionabilidades!</p>
            <hr>
          </div>
          <div class="row">
            <div class="col-lg-4 my-auto">
              <div class="device-container">
                <div class="device-mockup iphone6_plus portrait white">
                  <div class="device">
                    <div class="screen">
                      <!-- Demo image for screen mockup, you can put an image here, some HTML, an animation, video, or anything else! -->
                      <img src="img/demo-screen-1.jpg" class="img-fluid" alt="">
                    </div>
                    <div class="button">
                      <!-- You can hook the "home button" to some JavaScript events or just remove it -->
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="col-lg-8 my-auto">
              <div class="container-fluid">
                <div class="row">
                  <div class="col-lg-6">
                    <div class="feature-item">
                      <i class="icon-screen-smartphone text-primary"></i>
                      <h3>Design Responsivo</h3>
                      <p class="text-muted">Pronto para ser utilizado em qualquer dispositivo</p>
                    </div>
                  </div>
                  <div class="col-lg-6">
                    <div class="feature-item">
                      <i class="icon-camera text-primary"></i>
                      <h3>Reconhecimento rápido</h3>
                      <p class="text-muted">É capaz de reconhecer cores e objetos com precisão</p>
                    </div>
                  </div>
                </div>
                <div class="row">
                  <div class="col-lg-6">
                    <div class="feature-item">
                      <i class="icon-present text-primary"></i>
                      <h3>Uso gratuito</h3>
                      <p class="text-muted">Desde sempre este aplicativo é grátis e pode ser usado em qualquer que seja a circunstância!</p>
                    </div>
                  </div>
                  <div class="col-lg-6">
                    <div class="feature-item">
                      <i class="icon-lock-open text-primary"></i>
                      <h3>Open Source</h3>
                      <p class="text-muted">Código livre que pode ser editado e melhorado</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="cta">
        <div class="cta-content">
          <div class="container">
            <h2>A evolução do <br> Reconhecimento!</h2>
            <a href="/put" class="btn btn-outline btn-xl js-scroll-trigger">Upload</a>
          </div>
        </div>
        <div class="overlay"></div>
      </section>



      <footer>
        <div class="container">
          <p>Pyimage</p>

        </div>
      </footer>

      <!-- Bootstrap core JavaScript -->
      <script src="vendor/jquery/jquery.min.js"></script>
      <script src="vendor/bootstrap/js/bootstrap.bundle.min.js"></script>

      <!-- Plugin JavaScript -->
      <script src="vendor/jquery-easing/jquery.easing.min.js"></script>

      <!-- Custom scripts for this template -->
      <script src="js/new-age.min.js"></script>

    </body>

    </html>
"""

    @cherrypy.expose
    def index(self):
       return Root.indexHTML

    def header(self):
        return """<!DOCTYPE html>
          <html lang="en">
          <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
          <meta name="description" content="">
          <meta name="author" content="">
          <title>Bare - Start Bootstrap Template</title>
          <!-- Bootstrap core CSS -->
          <link href="vendor/bootstrap/css/bootstrap.css" rel="stylesheet">
        </head>
        <body>
          <!-- Navigation -->
          <nav class="navbar navbar-expand-lg navbar-dark bg-dark static-top">
            <div class="container">
              <a class="navbar-brand" href="/put">Voltar</a>
              <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
              </button>
              <div class="collapse navbar-collapse" id="navbarResponsive">
                <ul class="navbar-nav ml-auto">
                </ul>
              </div>
            </div>
          </nav>
          <!-- Page Content -->
          <div class="container">
            <div class="row">
              <div class="col-lg-12 text-center">

                <h1 class="mt-5">Imagem enviada com sucesso!</h1>
                <p class="lead">Objetos identificados:</p>
                <br>"""


    def footer(self):
        return """</div>
                </div>
                    </div>
                    <!-- Bootstrap core JavaScript -->
                    <script src="vendor/jquery/jquery.slim.min.js"></script>
                    <script src="vendor/bootstrap/js/bootstrap.js"></script>
                    </body>
                    </html>"""

    @cherrypy.expose
    def processImg(self,customFile):
        session = requests.Session()
        URL="http://image-dnn-sgh-jpbarraca.ws.atnog.av.it.pt/process"
        print(type(customFile))
        imgPath = 'imgInput/' + customFile
        with open(imgPath, 'rb') as f:
            file = {'img': f.read()}
        r = session.post(url=URL, files=file, data=dict(thr=0.5))
        if r.status_code == 200:
            yield self.header()
            i = 0
            db = sqlite3.connect("Pyimagedb.db", timeout=5)
            curs = db.cursor()
            curs2 = db.cursor()
            insrRes = curs.execute("INSERT INTO pyimage (imgPath,objDet,objExt) VALUES (?,?,?)",(imgPath,"","",))
            ogId = curs.lastrowid
            db.commit()
            for objects in r.json():
                i += 1
                strObjects = str(objects["box"])
                line = re.sub(r'[{\'}]', '', strObjects)
                numbers = re.findall(r'\b\d+\b', line)
                numbersint = list(map(int, numbers))
                dims = tuple(numbersint)
                imgFull = Image.open(imgPath)
                imgObj = imgFull.crop(dims)
                color = corDominante(imgObj)
                yield """<h3>Objeto {}:</h3>
                <p class="lead">Classe : {}</p>
                <p class="lead">Dimensões : {}</p>
                <p class="lead">Confiança : {}%</p>
                <hr>""".format(i,objects["class"] ,line,objects["confidence"]*100)

                imgObjPath = "imgOutput/{}obj{}.jpg".format(ogId,i)
                imgObj.save(imgObjPath)
                result = curs2.execute("INSERT INTO objects (objectN,objPath,confidence,originalId,dimensions,color) VALUES (?,?,?,?,?,?)",(objects["class"],imgObjPath,objects["confidence"]*100,ogId,line,closestColor(color)))
                db.commit()
            yield self.footer()

            imgRes = curs.execute("SELECT objectN FROM objects WHERE originalId = ?",(ogId,))
            imgResVals = re.sub(r'[{\'\]\[\)\(}]', '',str(imgRes.fetchall()))
            db.commit()
            print(curs.lastrowid)
            updateid = curs.execute("UPDATE pyimage SET objDet = ?,objExt = ? WHERE id = ?",(imgResVals,imgResVals,ogId,))
            db.commit()
            db.close()

    @cherrypy.expose
    def put(self):
       puthtml = """<!DOCTYPE html>
       <html lang="en">
       <head>
         <meta charset="utf-8">
         <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
         <meta name="description" content="">
         <meta name="author" content="">
         <title>Upload</title>
         <!-- Bootstrap core CSS -->
         <link href="vendor/bootstrap/css/bootstrap.css" rel="stylesheet">
       </head>
       <body>
         <!-- Navigation -->
         <nav class="navbar navbar-expand-lg navbar-dark bg-dark static-top">
           <div class="container">
             <a class="navbar-brand" href="/">Voltar</a>
             <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
               <span class="navbar-toggler-icon"></span>
             </button>
             <div class="collapse navbar-collapse" id="navbarResponsive">
               <ul class="navbar-nav ml-auto">
               </ul>
             </div>
           </div>
         </nav>
         <!-- Page Content -->
         <div class="container">
           <div class="row">
             <div class="col-lg-12 text-center">
               <h1 class="mt-5">Enviar imagem:</h1>
               <p class="lead">Escolha uma imagem a ser enviada</p>
               <form action="processImg" method="GET" >
               <div class="paymentWrap">
							<div class="btn-group paymentBtnGroup btn-group-justified" data-toggle="buttons">
					            <label class="btn paymentMethod active">
					            	<div class="method race"></div>
					                <input type="radio"  name="customFile" value="race.jpg" checked>
					            </label>
					            <label class="btn paymentMethod">
					            	<div class="method car"></div>
					                <input type="radio" name="customFile" value="car.jpg">
					            </label>
					            <label class="btn paymentMethod">
				            		<div class="method city"></div>
					                <input type="radio" name="customFile" value="city.jpg">
					            </label>
					             <label class="btn paymentMethod">
				             		<div class="method boat"></div>
					                <input type="radio" name="customFile" value="boat.jpg">
					            </label>
					            <label class="btn paymentMethod">
				            		<div class="method dog"></div>
					                <input type="radio" name="customFile" value="dog.jpg">
					            </label>
                                <label class="btn paymentMethod">
				            		<div class="method group"></div>
					                <input type="radio" name="customFile" value="group.jpg">
					            </label>
                                <label class="btn paymentMethod">
				            		<div class="method cat"></div>
					                <input type="radio" name="customFile" value="cat.jpg">
					            </label>
                                <label class="btn paymentMethod">
				            		<div class="method duck"></div>
					                <input type="radio" name="customFile" value="duck.jpg">
					            </label>


					        </div>
				</div>

                <br>
                <br>
                <hr>
                <input type="submit" value="Enviar" class="btn btn-success">

               </form>
             </div>
           </div>
         </div>

         <!-- Bootstrap core JavaScript -->
         <script src="vendor/jquery/jquery.slim.min.js"></script>
         <script src="vendor/bootstrap/js/bootstrap.js"></script>

       </body>

       </html>
       """

       return puthtml

    def listHeader(self):
        return """<!DOCTYPE html>
        <html lang="en">

        <head>

          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
          <meta name="description" content="">
          <meta name="author" content="">

          <title>Lista</title>

          <!-- Bootstrap core CSS -->
          <link href="vendor/bootstrap/css/bootstrap.css" rel="stylesheet">

        </head>

        <body>

          <!-- Navigation -->
          <nav class="navbar navbar-expand-lg navbar-dark bg-dark static-top">
            <div class="container">
              <a class="navbar-brand" href="/">Voltar</a>
            </div>
          </nav>


          <!-- Page Content -->
          <div class="container">
            <div class="row">
              <div class="col-lg-12 text-center">
                <h1 class="mt-5">Imagens:</h1>
                <p class="lead">Imagens registadas no servidor</p>
                <hr>
                <section class="details-card">
     <div class="container">
         <div class="row">"""

    def listFooter(self):
        return """
                            </div>
                        </div>
                    </section>
                 </div>
               </div>
             </div>

             <!-- Bootstrap core JavaScript -->
             <script src="vendor/jquery/jquery.slim.min.js"></script>
             <script src="//cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
             <script src="vendor/bootstrap/js/bootstrap.bundle.min.js"></script>

           </body>

           </html>
    """

    def listJsonHeader(self):
        return """<!DOCTYPE html>
        <html lang="en">

        <head>

          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
          <meta name="description" content="">
          <meta name="author" content="">

          <title>Lista</title>

          <!-- Bootstrap core CSS -->
          <link href="vendor/bootstrap/css/bootstrap.css" rel="stylesheet">

        </head>

        <body>

          <!-- Navigation -->
          <nav class="navbar navbar-expand-lg navbar-dark bg-dark static-top">
            <div class="container">
              <a class="navbar-brand" href="/">Voltar</a>
            </div>
          </nav>


          <!-- Page Content -->
          <div class="container">
            <div class="row">
              <div class="col-lg-12 text-center">
                <h1 class="mt-5">Json</h1>
                <p class="lead">objeto JSON:</p>
                <hr>
                <section class="details-card">
                </div>
     <div class="container">
         <div class="row">"""


    def listObjHeader(self):
        return """<!DOCTYPE html>
        <html lang="en">

        <head>

          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
          <meta name="description" content="">
          <meta name="author" content="">

          <title>Lista</title>

          <!-- Bootstrap core CSS -->
          <link href="vendor/bootstrap/css/bootstrap.css" rel="stylesheet">

        </head>

        <body>

          <!-- Navigation -->
          <nav class="navbar navbar-expand-lg navbar-dark bg-dark static-top">
            <div class="container">
              <a class="navbar-brand" href="/">Voltar</a>
            </div>
          </nav>


          <!-- Page Content -->
          <div class="container">
            <div class="row">
              <div class="col-lg-12 text-center">
                <h1 class="mt-5">Objetos:</h1>
                <p class="lead">Objetos identificados no servidor</p>
                <br>
                <p class="lead">Nível mínimo de confiança:</p>
                <form action="listTreshold" method="GET">
                <input type="text" name="confidenceTxt">
                 <br>
                 <br>
                 <input type="submit" value="Pesquisar" class="btn btn-info">

                </form>
                <hr>
                <section class="details-card">
     <div class="container">
         <div class="row">"""

    def listObjFooter(self):
        return """
                            </div>
                        </div>
                    </section>
                 </div>
               </div>
             </div>

             <!-- Bootstrap core JavaScript -->
             <script src="vendor/jquery/jquery.slim.min.js"></script>
             <script src="//cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
             <script src="vendor/bootstrap/js/bootstrap.bundle.min.js"></script>

           </body>

           </html>
    """

    @cherrypy.expose
    def listarObj(self):
        yield self.listObjHeader()
        db = sqlite3.connect("Pyimagedb.db", timeout=5)
        curs5 = db.cursor()
        result = curs5.execute("SELECT * FROM objects ORDER BY idObj")
        rows = result.fetchall()
        i = 0
        for row in rows:
            yield """<div class="col-md-4">
                <div class="card-content">
                    <div class="card-img">
                        <img src="{}" alt="img">
                        <span>ID: {}</span>
                    </div>
                    <div class="card-desc">
                        <h5>Objetos:</h5>
                        <h6>Classe: <p class="lead">{}</p></h6>
                        <h6>Confidence:  <p class="lead">{}%</p></h6>
                        <h6>Img original:  <p class="lead">{}</p></h6>
                        <h6>Dimensões:  <p class="lead">{}</p></h6>
                        <h6>Cor:  <p class="lead">{}</p></h6>
                        <br>
                    </div>
                </div>
            </div>""".format(str(row[2]),str(row[0]),row[1],row[3],row[4],row[5],row[6])
        yield self.listFooter()

    @cherrypy.expose
    def listTreshold(self,confidenceTxt):
        yield self.listObjHeader()
        db = sqlite3.connect("Pyimagedb.db", timeout=5)
        curs5 = db.cursor()
        result = curs5.execute("SELECT * FROM objects WHERE confidence >= ? ORDER BY idObj",(confidenceTxt,))
        rows = result.fetchall()
        i = 0
        for row in rows:
            yield """<div class="col-md-4">
                <div class="card-content">
                    <div class="card-img">
                        <img src="{}" alt="img">
                        <span>ID: {}</span>
                    </div>
                    <div class="card-desc">
                        <h5>Objetos:</h5>
                        <h6>Classe: <p class="lead">{}</p></h6>
                        <h6>Confidence:  <p class="lead">{}%</p></h6>
                        <h6>Img original:  <p class="lead">{}</p></h6>
                        <h6>Dimensões:  <p class="lead">{}</p></h6>
                        <h6>Cor:  <p class="lead">{}</p></h6>
                        <br>
                    </div>
                </div>
            </div>""".format(str(row[2]),str(row[0]),row[1],row[3],row[4],row[5],row[6])
        yield self.listFooter()


    @cherrypy.expose
    def moreDetailsHeader(self):
        return """<!DOCTYPE html>
        <html lang="en">

        <head>

          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
          <meta name="description" content="">
          <meta name="author" content="">

          <title>Lista</title>

          <!-- Bootstrap core CSS -->
          <link href="vendor/bootstrap/css/bootstrap.css" rel="stylesheet">

        </head>

        <body>

          <!-- Navigation -->
          <nav class="navbar navbar-expand-lg navbar-dark bg-dark static-top">
            <div class="container">
              <a class="navbar-brand" href="/listar">Voltar</a>
            </div>
          </nav>


          <!-- Page Content -->
          <div class="container">
            <div class="row">
              <div class="col-lg-12 text-center">
                <h1 class="mt-5">Detalhes</h1>
                <p class="lead">Objetos identificados:</p>
                <hr>
                <section class="details-card">
     <div class="container">
         <div class="row">"""

    @cherrypy.expose
    def get(self,id):
        yield self.moreDetailsHeader()
        db = sqlite3.connect("Pyimagedb.db", timeout=5)
        curs4 = db.cursor()
        print(id)
        objectRes = curs4.execute("SELECT * FROM objects WHERE originalId = ?",(id,))
        rowsobj = objectRes.fetchall()
        o = 0
        for row in rowsobj:
            o += 1
            yield """<div class="col-md-4">
                <div class="card-content">
                    <div class="card-img">
                        <img src="{}" alt="img">

                    </div>
                    <div class="card-desc">
                        <h5>Objeto {}:</h5>
                        <h6>Classe: <p class="lead">{}</p></h6>
                        <h6>Confiança: <p class="lead">{}%</p></h6>
                        <h6>Dimensões: <p class="lead">{}</p></h6>
                        <h6>Cor dominante: <p class="lead">{}</p></h6>

                    </div>
                </div>
            </div>""".format(row[2],o,row[1] ,row[3],row[5],row[6])
        yield self.moreDetailsFooter()

    @cherrypy.expose
    def moreDetailsFooter(self):
        return """
                            </div>
                        </div>
                    </section>
                 </div>
               </div>
             </div>

             <!-- Bootstrap core JavaScript -->
             <script src="vendor/jquery/jquery.slim.min.js"></script>
             <script src="//cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
             <script src="vendor/bootstrap/js/bootstrap.bundle.min.js"></script>

           </body>

           </html>
    """

    @cherrypy.expose
    def listar(self):
        yield self.listHeader()
        db = sqlite3.connect("Pyimagedb.db", timeout=5)
        curs3 = db.cursor()
        result = curs3.execute("SELECT * FROM pyimage ORDER BY id")
        rows = result.fetchall()
        i = 0
        for row in rows:

            name = str(row[1]).split("/")[1]
            clean = str(row[2]).replace(",","")

            yield """<div class="col-md-4">
                <div class="card-content">
                    <div class="card-img">
                        <img src="{}" alt="{}">
                        <span>{}</span>
                    </div>
                    <div class="card-desc">
                        <h5>Objetos:</h5>
                        <h6>{}</h6>,
                        <br>
                        <a href="/get?id={}" class="btn-card">Ver mais</a>

                    </div>
                </div>
            </div>""".format(str(row[1]),str(row[1]),name,clean,row[0])
        yield self.listFooter()

    @cherrypy.expose
    def dumpinfo(self):
        return """<!DOCTYPE html>
        <html lang="en">

        <head>

          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
          <meta name="description" content="">
          <meta name="author" content="">

          <title>Pesquisar</title>

          <!-- Bootstrap core CSS -->
          <link href="vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet">

        </head>

        <body>

          <!-- Navigation -->
          <nav class="navbar navbar-expand-lg navbar-dark bg-dark static-top">
            <div class="container">
              <a class="navbar-brand" href="/">Voltar</a>
              <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
              </button>
              <div class="collapse navbar-collapse" id="navbarResponsive">
                <ul class="navbar-nav ml-auto">


                </ul>
              </div>
            </div>
          </nav>

          <!-- Page Content -->
          <div class="container">
            <div class="row">
              <div class="col-lg-12 text-center">
                <h1 class="mt-5">Pesquisa de imagens</h1>
                <p class="lead">Selecionar imagens por nome e cor</p>
                <form action="processSearch" method="GET">

                 <input type="text" name="Squery" placeholder="Ex: Car Red">
                 <br>
                 <br>
                 <input type="submit" value="Pesquisar" class="btn btn-info">

                </form>
              </div>
            </div>
          </div>

          <!-- Bootstrap core JavaScript -->
          <script src="vendor/jquery/jquery.slim.min.js"></script>
          <script src="vendor/bootstrap/js/bootstrap.bundle.min.js"></script>

        </body>

        </html>
 """

    def searchHeader(self):
        return """<!DOCTYPE html>
        <html lang="en">

        <head>

          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
          <meta name="description" content="">
          <meta name="author" content="">

          <title>Lista</title>

          <!-- Bootstrap core CSS -->
          <link href="vendor/bootstrap/css/bootstrap.css" rel="stylesheet">

        </head>

        <body>

          <!-- Navigation -->
          <nav class="navbar navbar-expand-lg navbar-dark bg-dark static-top">
            <div class="container">
              <a class="navbar-brand" href="/">Voltar</a>
            </div>
          </nav>


          <!-- Page Content -->
          <div class="container">
            <div class="row">
              <div class="col-lg-12 text-center">
                <h1 class="mt-5">Resultados:</h1>

                <hr>
                <section class="details-card">
     <div class="container">
         <div class="row">"""

    @cherrypy.expose
    def processSearch(self,Squery):
        yield self.searchHeader()
        db = sqlite3.connect("Pyimagedb.db", timeout=5)
        SqueryL = Squery.split(" ")
        Squery1 = "%" + SqueryL[0] + "%"
        Squery2 = "%" + SqueryL[1] + "%"
        curs5 = db.cursor()
        result = curs5.execute("SELECT * FROM objects WHERE objectN LIKE ? AND color LIKE ? ORDER BY idObj",(Squery1,Squery2,))
        rows = result.fetchall()
        i = 0
        for row in rows:
            yield """<div class="col-md-4">
                <div class="card-content">
                    <div class="card-img">
                        <img src="{}" alt="img">
                        <span>ID: {}</span>
                    </div>
                    <div class="card-desc">
                        <h5>Objetos:</h5>
                        <h6>Classe: <p class="lead">{}</p></h6>
                        <h6>Confidence:  <p class="lead">{}%</p></h6>
                        <h6>Img original:  <p class="lead">{}</p></h6>
                        <h6>Dimensões:  <p class="lead">{}</p></h6>
                        <h6>Cor:  <p class="lead">{}</p></h6>
                        <br>
                    </div>
                </div>
            </div>""".format(str(row[2]),str(row[0]),row[1],row[3],row[4],row[5],row[6])
        yield self.listFooter()

    @cherrypy.expose
    def listByName(self):
        return """<!DOCTYPE html>
        <html lang="en">

        <head>

          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
          <meta name="description" content="">
          <meta name="author" content="">

          <title>Pesquisar - JSON</title>

          <!-- Bootstrap core CSS -->
          <link href="vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet">

        </head>

        <body>

          <!-- Navigation -->
          <nav class="navbar navbar-expand-lg navbar-dark bg-dark static-top">
            <div class="container">
              <a class="navbar-brand" href="/">Voltar</a>
              <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
              </button>
              <div class="collapse navbar-collapse" id="navbarResponsive">
                <ul class="navbar-nav ml-auto">


                </ul>
              </div>
            </div>
          </nav>

          <!-- Page Content -->
          <div class="container">
            <div class="row">
              <div class="col-lg-12 text-center">
                <h1 class="mt-5">Gerar JSON</h1>
                <p class="lead">Gerar JSON por nome </p>
                <form action="list" method="GET">
                <input type="text" name="name" placeholder="Ex: Car">
                 <input type="hidden" name="type" value="detected">
                 <input type="hidden" name="color" value="empty">
                 <br>
                 <br>
                 <input type="submit" value="Gerar" class="btn btn-info">

                </form>
              </div>
            </div>
          </div>

          <!-- Bootstrap core JavaScript -->
          <script src="vendor/jquery/jquery.slim.min.js"></script>
          <script src="vendor/bootstrap/js/bootstrap.bundle.min.js"></script>

        </body>

        </html>
 """

    @cherrypy.expose
    def listByNameAndColor(self):
        return """<!DOCTYPE html>
        <html lang="en">

        <head>

          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
          <meta name="description" content="">
          <meta name="author" content="">

          <title>Pesquisar - JSON</title>

          <!-- Bootstrap core CSS -->
          <link href="vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet">

        </head>

        <body>

          <!-- Navigation -->
          <nav class="navbar navbar-expand-lg navbar-dark bg-dark static-top">
            <div class="container">
              <a class="navbar-brand" href="/">Voltar</a>
              <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
              </button>
              <div class="collapse navbar-collapse" id="navbarResponsive">
                <ul class="navbar-nav ml-auto">


                </ul>
              </div>
            </div>
          </nav>

          <!-- Page Content -->
          <div class="container">
            <div class="row">
              <div class="col-lg-12 text-center">
                <h1 class="mt-5">Gerar JSON</h1>
                <p class="lead">Gerar JSON por nome e cor </p>
                <form action="list" method="GET">
                <input type="text" name="name" placeholder="Nome ">
                <br>
                <br>
                 <input type="text" name="color" placeholder="Cor">
                 <input type="hidden" name="type" value="detected">
                 <hr>
                 <br>
                 <br>

                 <input type="submit" value="Gerar" class="btn btn-info">

                </form>
              </div>
            </div>
          </div>

          <!-- Bootstrap core JavaScript -->
          <script src="vendor/jquery/jquery.slim.min.js"></script>
          <script src="vendor/bootstrap/js/bootstrap.bundle.min.js"></script>

        </body>

        </html>
 """

    @cherrypy.expose
    def Sobre(self):
        return """<!DOCTYPE html>
        <html lang="en">

        <head>

          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
          <meta name="description" content="">
          <meta name="author" content="">

          <title>Sobre</title>

          <!-- Bootstrap core CSS -->
          <link href="vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet">

        </head>

        <body>

          <!-- Navigation -->
          <nav class="navbar navbar-expand-lg navbar-dark bg-dark static-top">
            <div class="container">
              <a class="navbar-brand" href="/">Voltar</a>
              <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
              </button>
              <div class="collapse navbar-collapse" id="navbarResponsive">
                <ul class="navbar-nav ml-auto">


                </ul>
              </div>
            </div>
          </nav>

          <!-- Page Content -->
          <div class="container">
            <div class="row">
              <div class="col-lg-12 text-center">
                <h1 class="mt-5">Sobre:</h1>
                <p class="lead"></p>
                <div class="card card-body bg-light">
                Grupo: Luan Graça(91755), João Alves(89197), João Marcos(91749), Luiz Felipe(91257)<br>
                <br>
                Repositório Usado: <a href="https://code.ua.pt/projects/labi2019-p2-g16">https://code.ua.pt/git/labi2019-p2-g16</a>
                <br>
                Diretório no servidor XCOA: <a href="https://xcoa.av.it.pt/labi2019-p2-g16">https://xcoa.av.it.pt/labi2019-p2-g16</a>
                </div>
              </div>
            </div>
          </div>

          <!-- Bootstrap core JavaScript -->
          <script src="vendor/jquery/jquery.slim.min.js"></script>
          <script src="vendor/bootstrap/js/bootstrap.bundle.min.js"></script>

        </body>

        </html>
 """

    @cherrypy.expose
    def list(self,type,color,name):
        db = sqlite3.connect("Pyimagedb.db", timeout=5)
        curs3 = db.cursor()
        result = curs3.execute("SELECT * FROM objects")
        rows = result.fetchall()
        if type == "names" and color == "empty" and name == "empty" :
            yield self.listJsonHeader()
            jsonList = []
            for row in rows:
                jsonList.append({'id': row[0],'tipo': row[1],'ficheiro':row[2],'confian&ccedil;a': row[3],'id ficheiro original': row[4],'dimens&otilde;es': row[5],'cor': row[6]})
            yield """<div class="card card-body bg-light">
                     <pre>{}</pre>
                     </div>""".format(json.dumps(jsonList, indent=4, sort_keys=True))
            yield self.listObjFooter()
        if type == "detected" and color == "empty" and name == "empty" :
            yield self.listJsonHeader()
            jsonList = []
            for row in rows:
                jsonList.append({'id': row[0],'tipo': row[1],'ficheiro':row[2],'confian&ccedil;a': row[3],'id ficheiro original': row[4],'dimens&otilde;es': row[5],'cor': row[6]})
            yield """<div class="card card-body bg-light">
                     <pre>{}</pre>
                     </div>""".format(json.dumps(jsonList, indent=4, sort_keys=True))
            yield self.listObjFooter()
        if type == "detected" and color == "empty" and name != "empty" :
            name = "%" + name + "%"
            result2 = curs3.execute("SELECT * FROM objects WHERE objectN LIKE ?",(name,))
            rows = result2.fetchall()
            yield self.listJsonHeader()
            jsonList = []
            for row in rows:
                jsonList.append({'id': row[0],'tipo': row[1],'ficheiro':row[2],'confian&ccedil;a': row[3],'id ficheiro original': row[4],'dimens&otilde;es': row[5],'cor': row[6]})
            yield """<div class="card card-body bg-light">
                     <pre>{}</pre>
                     </div>""".format(json.dumps(jsonList, indent=4, sort_keys=True))
            yield self.listObjFooter()
        if type == "detected" and color != "empty" and name != "empty" :
            name = "%" + name + "%"
            color = "%" + color + "%"
            result3 = curs3.execute("SELECT * FROM objects WHERE objectN LIKE ? AND color LIKE ?",(name,color,))
            rows = result3.fetchall()
            yield self.listJsonHeader()
            jsonList = []
            for row in rows:
                jsonList.append({'id': row[0],'tipo': row[1],'ficheiro':row[2],'confian&ccedil;a': row[3],'id ficheiro original': row[4],'dimens&otilde;es': row[5],'cor': row[6]})
            yield """<div class="card card-body bg-light">
                     <pre>{}</pre>
                     </div>""".format(json.dumps(jsonList, indent=4, sort_keys=True))
            yield self.listObjFooter()








cherrypy.quickstart(Root(), "/", config)
