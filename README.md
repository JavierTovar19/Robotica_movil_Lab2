# Robotica_movil_Lab2

## Descripción:

### Nodo:
 Este laboratorio consiste en el control de una tortuga en el entorno de ROS, para ello se utiliza el lenguaje de programación Python y la librería rospy.

 Con la creación de una clase bot, la cual contiene las propiedades propias de un robot, como la posición, velocidad y orientación, y los metodos necesarios para el control de la tortuga.

 En la clase, se inicializa un nodo denominado **control** el cual se suscribe al topico **/turtle1/pose** para obtener la posición de la tortuga y publica en el topico **/turtle1/cmd_vel** para controlar la velocidad de la tortuga. esta configuración se observa a continuación:

 ![Grafo de nodos](.img/rosgraph.png)

 ### Clase bot:
   La clase bot, contiene los siguientes comportamientos:
   - **__init__**: Inicializa el nodo y los tópicos
   - **callback_pose**: Callback para obtener la posición de la tortuga
   - **move**: Método para mover la tortuga con velocidad lineal y angular
   - **goto**: Método para mover la tortuga a un objetivo

  ### Logica aplicada:
  El bot se mueve en una trayectoria lineal a velocidad constante, hasta que su posición absoluta se aproxima a uno de los muros, lo cual se evalua mediante la siguiente condición:

  $$ 
   x \notin (1, 10) \lor y \notin (1, 10)
  $$ 

  En cuanto el bot detecta que se encuentra fuera del area delimitada por los muros, entra en un estado de giro, en el cual se conserva la velocidad lineal, pero se añade una velocidad angular optimizandola de acuerdo al angulo en el cual se encuentra orientado el bot.

## Diagrama de flujo:

### Maquina de estados:
El comportamiento del robot, conserva una velocidad lineal constante y determina una velocidad angular basada en una dirección optima de movimiento, la cual se calcula mediante la diferencia entre el angulo actual y el angulo objetivo.

$$
\theta_{error} =tan^{-1}\left(\frac{\sin(\theta_{obj} - \theta_{act})}{\cos(\theta_{obj} - \theta_{act})}\right)
$$

Al usar la funcion de numpy arctan2, se obtiene el angulo mapeado correctamente en el cuadrante deseado, lo que permite determinar la dirección del giro optimo.

![Maquina de estados](.img/maquna_est_alg.svg)

### Desiciones del bot:
Con el algoritmo implementado, el angulo objetivo se determina mediante la siguiente lógica:

$$
\begin{array}{|c|c|c|c|}
\hline
\text{Posicion en X} & \text{Posicion en Y} & \text{Dirección deseada} & \text{Angulo Obj (°)} \\
\hline
\text{>10} & \text{>10} & \text{[-1,-1]} & \text{-135} \\
\text{<1} & \text{>10} & \text{[1,-1]} & \text{-45} \\
\text{>10} & \text{<1} & \text{[-1,1]} & \text{135} \\
\text{<1} & \text{<1} & \text{[1,1]} & \text{45} \\
\text{>=1 <=10} & \text{>10} & \text{[0,-1]} & \text{-90} \\
\text{>=1 <=10} & \text{<1} & \text{[0,1]} & \text{90} \\
\text{>10} & \text{>=1 <=10} & \text{[-1,0]} & \text{180} \\
\text{<1} & \text{>=1 <=10} & \text{[1,0]} & \text{0} \\
\text{>=1 <=10} & \text{>=1 <=10} & \text{[-,-]} & \text{-} \\
\hline
\end{array}
$$

## Comandos ejecutados:

Importante, en caso de actualizar python, se debe modificar el constructor de catkin_make para que pueda usar la versión de python deseada, el cual se puede añadir a .bashrc y es el siguiente:

```bash
alias jcatkin_make='catkin_make -DPYTHON_EXECUTABLE=/usr/bin/python3.8'
```


Terminal 1:
```bash
catkin_make
chmod +x src/turtu/scripts/*.py
roscore
```
Terminal 2:
```bash
rosrun turtlesim turtlesim_node
```
Terminal 3:
```bash
source devel/setup.bash
rosrun turtu clases.py
```

![Comandos](.img/comandos.png)
## Simulación:

![Simulación](.img/Ejecucion_colors.png)

## Video de ejecución:

Se usa el comando personalizado **jcatkin_make** para compilar el proyecto.

<video controls src=".img/Ejecución_video.mp4" title="Title"></video>
