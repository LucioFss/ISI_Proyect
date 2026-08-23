from wsgiref.simple_server import make_server #importamos la libreria de wsgi para poder montar servidores
import json
#Usaremos una variable "tasks" con el fin de usarla para almacenar la informacion que posee el servidor
#Es una variable que almacena una lista de diccionarios, cada diccionario tiene la estructura {id : <<numero>>, nombreTarea : <<'Nombre de la tarea'>>, realizada : <<true/false>>}
list_task = []
#Definicion que procesara la peticion de el cliente

def process_request(environ, start_response):   #Los campos reciben environ (metodo diccionario) y start_response que es un metodo que estandariza las respuestas de el servidor
    verb = environ['REQUEST_METHOD']   #Guardamos en una variable los diccionarios que contienen los metodos GET,POST,etc.
    path = environ['PATH_INFO']    #Traemos el diccionario con las rutas, como "/tasks" en este caso

    #Metodo que permite obtener todas las tareas de la lista de tareas
    if verb == 'GET' and path == '/tasks' :

        #indicamos el estado de la respuesta y ademas las cabeceras que esta llevara, como el formato de la respuesta y cual es el servidor
        start_response('200 OK',[('Content-Type','application/json'),('Server', 'server_v1')])
        
        #La lista de tareas se convierte a formato JSON y se almacena en ina variable
        jsonReturn = json.dumps(list_task)

        #Convertimos la lista de tareas de formato JSON a Bytes, ya que la red no entiende de caracteres
        return [jsonReturn.encode('utf-8')] #Se envia en forma de lista ya que el servidor espera un iterable con caracteres en bytes dentro

    #Metodo que permite agregar a la lista de tareas una nueva lista de tareas
    elif verb == 'POST' and path == '/tasks' : 
        #Usaremos try-catch para controlar si el input es vacio
        try:

            inpunt_Length = int(environ.get('CONTENT_LENGTH', 0)) #Obtenemos el tamaño de la lista de entrada
        except(ValueError): #ValueError surge cuando el valor es texto y no se puede pasar a numero, TypeError puede aparecer si no exist la cabecera de la peticion 
            inpunt_Length = 0   
        
        #Leemos el input y tomamos su contenido en JSON decodificado en UTF-8
        read_input = environ['wsgi.input'].read(inpunt_Length)  #Primero permitimos leer el contenido de la request (environ['wsgi.input']) y luego lo leemos hasta input_Length

        #Inicializamos como un diccionario la variable que almacenara el diccionario proveniente de el metodo ejecutado por el cliente
        values_input = {} 

        #ahora vamos a traducir de UTF-8 para pasarlo de JSON a valores, diccionarios mas especificamente
        values_input = json.loads(read_input.decode('utf-8'))
        new_id = str(len(list_task) + 1)
        new_task = {'id' : new_id, 'title' : values_input.get('title'), 'done' : values_input.get('done')}
        list_task.append(new_task)

        #Se realiza la respuesta
        start_response('201 Created',[('Content-Type','application/json'),('Server', 'server_v1')])
        jsonReturn = json.dumps(new_task)
        return [jsonReturn.encode('utf-8')]

    #Metodo que permite el obtener una tarea de la lista de tareas con el id ingresado en la ruta
    elif verb == 'GET' and path.startswith('/tasks/') :
        split_path = path.split('/') #Separamos en terminos por '/' la ruta y formamos una lista

        #Obtenemos el id que esta alojada en la ruta
        id_input = split_path[-1]

        #Si el valor que venia con la ruta era un entero entonces buscamos en list_task la tarea que posee el id que buscamos
        for task in list_task :
            if id_input == task['id'] :
                #Si encontramos la tarea con ese id, preparamos la respuesta, pasamos json la tarea y la codificamos a bytes UTF-8
                start_response('200 OK', [('Content-Type', 'application/json')])
                jsonReturn = json.dumps(task)
                return [jsonReturn.encode('utf-8')]

        #Si no se encontro la tarea con el id ingresado, se retorna un error 404
            start_response("404 Not Found", [('Content-Type', 'application/json')])
            return [b'{"error" : "id no encontrado"}']

    #Metodo que permite reemplazar valores de una tarea con el id colocado en la ruta
    elif verb == 'PATCH' and path.startswith('/tasks/') :
        split_path = path.split('/')

        #Obtenemos el id que esta alojada en la ruta
        id_input = split_path[-1]
        
        #Usaremos try-catch para controlar si el input es vacio
        try:
            inpunt_Length = int(environ.get('CONTENT_LENGTH', 0))

        except ValueError :
            inpunt_Length = 0

        #Delimitamos lo que debe de leerse de la entrada, que es todo
        read_input = environ['wsgi.input'].read(inpunt_Length)

        #Desconvertimos la entrada de bytes a texto, y luego lo quitamos el formato json
        values_input = json.loads(read_input.decode('utf-8'))

        #Se busca la tarea con el mismo valor de id de entrada
        for task in list_task :
            if id_input == task['id'] : 

                #Tomamos cada key de el diccionario de entrada con su valor, exeptuando el id
                for key, value in values_input.items() :
                    if key != 'id' :
                        task[key] = value

                #Una vez modificados los valores de la tarea, retornamos que la operacion se realizo con exito y la tarea modificada
                start_response('200 OK', [('Content-Type', 'application/json')])
                jsonReturn = json.dumps(task)
                return [jsonReturn.encode('utf-8')]

        #Si no se encontro la tarea con el id ingresado, se retorna un error 404
        start_response("404 Not Found", [('Content-Type', 'application/json')])
        return [b'{"error" : "id no encontrado"}']
    
    #Metodo que elimina una tarea segun el id ingresado en la ruta
    elif verb == 'DELETE' and path.startswith('/tasks/'):
        #Tratamos a la ruta con el fin de obtener el id en ella
        split_path = path.split('/')

        #Obtenemos el id que esta alojada en la ruta
        id_input = split_path[-1]

        #Se busca la tarea con el mismo valor de id de entrada
        for task in list_task :
            #Se compara el id de entrada con el de una tarea existente en la lista de taeas
            if id_input == task['id'] :
                #Si se encontro se remueve la tarea con el id buscado
                list_task.remove(task)

                #Retornamos el codigo y la cabecera de un retorno vacio
                start_response("204 No Content",[])
                return [b'']
            
        #Si no se encontro la tarea con el id ingresado, se retorna un error 404
        start_response("404 Not Found", [('Content-Type', 'application/json')])
        return [b'{"error" : "id no encontrado"}']
    
    else :
        start_response('404 Not Found', [('Content-Type', 'application/json')])
        return [b'{"error": "Ruta o Verbo no encontrado"}']

#Declaramos el nombre del host del servidor
HOSTNAME = 'localhost'
#Declaramos el puerto
PORTNUMBER = 9292
if __name__ == '__main__' :
    print("Inicializando servidor...")
    server = make_server(HOSTNAME,PORTNUMBER,process_request)
    print(f"Servidor inicializado y funcionando en https://{HOSTNAME}:{PORTNUMBER}/ usa Ctrl + c para pararlo")
    server.serve_forever()