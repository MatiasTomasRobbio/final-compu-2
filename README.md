# final-compu-2 # Poker Game App

## Descripción
Esta es una aplicacion de un juego poker de modalidad texas hol' em con un chat incluido. Con arquitectura cliente servidor , permite crear una sala a la cual los clientes se conectan mediante sockets e interactuan mediante consola. Ademas incluye una sala de chat que se lanza automaticamente cuando se conecta a la sala de juego

## Instalación


1. Clona el repositorio: `git clone https://github.com/MatiasTomasRobbio/final-compu-2`
2. Instalar dependecias en caso de ser necesario segun la version de python que este usando

### INSTRUCIONES 

Servidor:

Para correr el servidor (el cual crea una sala) debe navegar hasta la carpeta poker_game_app/server y correr el archivo server.py el cuale recibe los siguientes argumentos

--host: Especifica el host en el que se escuchará. Si no se define, se establece por defecto en 'localhost'.
--game_port, -g: Especifica el puerto en el que el proceso del juego de póker escuchará. [REQUERIDO]
--chat_port, -c: Especifica el puerto en el que el proceso de chat escuchará. Si no se define, se establecerá por defecto en el puerto siguiente al puerto del juego.
--starting_stack: Especifica la pila inicial para cada jugador. Si no se define, se establece por defecto en 1000 y no puede ser igual a 0.
--num_players, -n: Especifica el número de jugadores para iniciar el juego el cual no puede ser menor a 2. Si no se define, se establece por defecto en 3.

 El servidor inicia y crea la sala de chat, y luego espera las conexiones de los jugadores hasta que el numero de jugadores conectados sea el ingresado. Una vez alcanzado el numero de jugadores comienza el juego. Este termina una vez que todos los jugadores menos 1 se queda sin dinero



 Cliente:

 Para correr el juego como cliente debe navegar hasta la carpeta poker_game_app/client y correr el archvio game_client.py el cual recibe los siguientes argumentos

 --server_ip, -s: Especifica la direccion ip del servidor al cual se desea conectar. Si no se define, se establece por defecto en 'localhost'.
 --name, -n: Especifica el nombre que va a utilizar en la partida. Si el nombre ya esta usado deberia intentar nuevamente con otro nombre [REQUERIDO]
 --port, -p: Especifica el puerto del servidor [REQUERIDO]

 El cliente se conecta a la sala del juego donde podra interactuar. Ademas se abrira otra ventana con el chat donde podra chatear con los demas jugadores de la sala.
