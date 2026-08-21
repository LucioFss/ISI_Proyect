from wsgiref.simple_server import make_server #importamos la libreria de wsgi para poder montar servidores
import json
#Usaremos una variable "tasks" con el fin de usarla para almacenar la informacion que posee el servidor
#Es una variable que almacena una lista de diccionarios, cada diccionario tiene la estructura {id : <<numero>>, nombreTarea : <<'Nombre de la tarea'>>, realizada : <<true/false>>}

tasks = [{"id" : 1, "nombreTarea" : "Montar servidor", 'realizado' : False}]

#Definicion que procesara la peticion de el cliente

def process_request(environ, start_response):   #Los campos reciben environ (metodo diccionario) y start_response que es un metodo que estandariza las respuestas de el servidor
    verb = environ['REQUEST_METHOD']   #Guardamos en una variable los diccionarios que contienen los metodos GET,POST,etc.
    path = environ['PATH_INFO']    #Traemos el diccionario con las rutas, como "/tasks" en este caso

    #Verificamos que la entrada de la consulta sea un metodo GET y ademas que quiera todas las tareas en el servidor
    if verb == 'GET' and path == '/tasks' :

        #indicamos el estado de la respuesta y ademas las cabeceras que esta llevara, como el formato de la respuesta y cual es el servidor
        start_response('200 OK',[('Format','application/json'),('Server', 'server_v1')])

        #La lista de tareas se convierte a formato JSON y se almacena en ina variable
        json_return = json.dump(tasks)
        #Convertimos la lista de tareas de formato JSON a Bytes, ya que la red no entiende de caracteres
        return [json_return.encode('utf-8')] #Se envia en forma de lista ya que el servidor espera un iterable con caracteres en bytes dentro


