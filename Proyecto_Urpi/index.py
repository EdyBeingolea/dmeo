from flask import Flask, render_template, request, Response
import pyodbc 
import cv2
app = Flask(__name__)

Server_name = "DESKTOP-2G3QD7I"
Databases = "urpi"
Usuario = "sa"
Contraseña= "tasayco2004"


width = 440  # Define el ancho deseado
height = 300 

# camra live
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
face_detector = cv2.CascadeClassifier(cv2.data.haarcascades +
     "haarcascade_frontalface_default.xml")

def generate():
    while True:
        ret, frame = cap.read()
        if ret:
               frame = cv2.resize(frame, (width, height))
               gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
               faces = face_detector.detectMultiScale(gray, 3, 5)
        
               (flag, encodedImage) = cv2.imencode(".jpg", frame, (cv2.IMWRITE_JPEG_QUALITY, 70))

               if not flag:
                    continue
               yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                    bytearray(encodedImage) + b'\r\n')
        
               
@app.route("/live")
def live():
     return render_template("videolive.html")
 
@app.route("/video_feed")
def video_feed():
     return Response(generate(),
          mimetype = "multipart/x-mixed-replace; boundary=frame")




# FIN DE  LA CAMARA LIVE 


@app.route('/')
def incio():
    return render_template('inicio.html')

@app.route('/Menu')
def menu():
    return render_template('index.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/nosotros')
def acerca_nosotros():
    return render_template('nosotros.html')


try:
    connection = pyodbc.connect(
        'DRIVER={SQL Server};SERVER='+Server_name+';DATABASE='+Databases+';UID='+Usuario+';PWD='+Contraseña)
    
except Exception as ex:
    print(ex)

@app.route('/consultas', methods=['POST'])
def procesar_consulta():
    
    if request.method == 'POST':
        usuario = request.form['usuario']
        correo = request.form['correo']
        mensaje = request.form['mensaje']
        
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Consulta (USUARIO, EMAIL, MENSAJE) VALUES (?, ?, ?)", (usuario, correo, mensaje))
        connection.commit()
        cursor.close()
        
        return render_template('inicio.html')

if __name__ == '__main__':
    app.run(debug=False)
        
cap.release()
