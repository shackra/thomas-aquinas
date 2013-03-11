***El desarrollo de este proyecto (así como su Wiki y el bugtrack) se lleva acabo en [bitbucket.org](https://bitbucket.org/shackra/thomas-aquinas).***

## ¿Qué cosa?

Bueno, quiero decir que el proyecto es algo así como un motor para desarrollar videojuegos 2D usando Python y SFML debajo del capo. Quiero dedicarme al desarrollo de vídeo juegos como independiente (aka desarrollador indie de vídeo juegos), así que primero debo refactorizar todas esas lineas de codigo que pueden existir entre diferentes títulos en un solo modulo.

## ¿Qué provee Thomas Aquinas?

provee:

* Director de escenas.
* Escenas (Diseñadas en Tiled: Soporta mapas ortográficos o isometricos).
* Entidades (Aun bajo fuerte desarrollo).
* Manejo de configuraciones para juegos (rutas absolutas de archivos, botones del juego, etc).
* Manejador de recursos de audio (música y efectos de sonido: Aun necesitan ser escritos).
* Cargado rápido de escenas hermanas ((¿Se le dice así?) Aun no se modifica código los objetos Escena para hacer esto funcionar).
* algo de IA con [SimpleAI](https://pypi.python.org/pypi/simpleai/0.5.1) (Aunque no vendría mal aprender álgebra y más sobre Inteligencia Artificial)
* Interfaz gráfica con [Librocket](http://librocket.com/) (tengo algo de soporte para SFML con [pylibrocket](https://bitbucket.org/shackra/pylibrocket) aunque la verdad siento que necesitan exponer para Python más de la API de librocket, así el proyecto se puede aprovechar al 100% de sus capacidades).
* Cuando recuerde que más puede hacer Thomas Aquinas, lo agregare a esta lista.

## ¿Thomas Aquinas?

Thomas Aquinas, o precisamente St. Thomas Aquinas (Santo Tomás de Aquino) [Según Wikipedia](https://es.wikipedia.org/wiki/Tom%C3%A1s_de_Aquino): 

![](http://marccortez.com/wp-content/uploads/2012/03/St-Thomas-Aquinas.jpg)

> (en italiano Tommaso D'Aquino) (Roccasecca o Belcastro,1 Italia, 1224/1225 – Abadía de Fossanuova, 7 de marzo de 1274) fue un teólogo y filósofo católico perteneciente a la Orden de Predicadores, el principal representante de la tradición escolástica, y fundador de la escuela tomista de teología y filosofía. Es conocido también como "Doctor Angélico" , "Doctor Común" y " Doctor Universal".
> 
> Es considerado santo por la Iglesia Católica. Su trabajo más conocido es la Suma Teológica, tratado en el cual pretende exponer de modo ordenado la doctrina católica. Canonizado en 1323, fue declarado Doctor de la Iglesia en 1567 y santo patrón de las universidades y centros de estudio católicos en 1880. Su festividad se celebra el 28 de enero.

## Tu proyecto usa la licencia GNU GPL 3 ¿No tienes una versión LGPL?

Ehh... nop, no tengo intenciones de usar doble licenciamiento para mi proyecto. Yo, como usted, estoy interesado en el desarrollo de títulos comerciales, y sin embargo, la trama del software privativo no me convence en lo más mínimo como forma de hacer dinero. Sé que existen motores (¿o frameworks?) mejores que mi proyecto, pero aun así, pienso mantenerme firme en mis principios morales.

## Soy principiante en programación y quiero hacer juegos ¿Debería usar Pygame o SFML o tu motor?

Nop. si esa es tu situación lo mejor que puedo recomendarte es [Pilas Engine](http://pilas-engine.com.ar/), desarrollado por [Hugo Ruscitti](http://www.losersjuegos.com.ar/comunidad/integrantes/hugoruscitti) y la comunidad [LosersJuegos](http://www.losersjuegos.com.ar/) Argentina. Ya me lo agradecerás algún día xd.
