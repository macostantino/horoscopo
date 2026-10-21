"""Piezas de redacción del motor de horóscopos (voz de astrólogo, segunda persona, sin marcas de género).

Un pronóstico = A (situación + esfuerzo) + B (luz) + C opcional (astros o consejo).
Todas las oraciones se arman con piezas intercambiables; el motor garantiza que ninguna
oración se repita y que dentro de un texto no se repitan ideas ni sujetos.
"""

SIGNS = [
    "ARIES", "TAURO", "GÉMINIS", "CÁNCER", "LEO", "VIRGO",
    "LIBRA", "ESCORPIO", "SAGITARIO", "CAPRICORNIO", "ACUARIO", "PISCIS",
]
CATEGORIES = ["Hoy", "Amor", "Riqueza", "Bienestar"]

# ---- Piezas comunes -----------------------------------------------------------
A_LEADS = [
    "Hoy ", "Este día ", "Durante la jornada ", "Desde temprano ", "Por la mañana ", "Ya desde primera hora ",
    "A media jornada ", "En lo que resta del día ", "Durante estas horas ", "Esta mañana ", "Esta tarde ",
    "En las próximas horas ", "A lo largo del día ", "Con el día recién empezado ",
]
A_FORMS = [
    "tendrás que", "será necesario", "te tocará", "habrá que", "conviene", "deberás",
    "hará falta", "lo mejor será", "vas a tener que", "te conviene",
    "lo ideal será", "harás bien en", "necesitarás", "es momento de", "toca", "no está de más",
    "hay que", "te aconsejo", "te recomiendo", "sería bueno", "sería prudente", "procura", "intenta",
    "no olvides", "vale la pena", "te vendrá bien", "es buen momento para", "haz el esfuerzo de",
]
A_TAILS = [" antes de seguir adelante", " paso a paso", " con serenidad", " aunque cueste al principio"]  # pocas y neutras
B_CONNECTORS = [
    "Pero ", "Aun así, ", "La buena noticia es que ", "Hacia el final del día ", "Más pronto que tarde ",
    "Poco a poco ", "Si te mantienes firme, ", "Al final ", "Antes de lo que piensas ",
    "Con el correr de las horas ", "Cuando menos lo esperes ", "Tarde o temprano ", "Al caer la tarde ",
    "Lo importante es que ", "Con el tiempo ", "Esa misma noche ", "Sin darte cuenta ",
    "En cuestión de horas ", "Por suerte ", "Con algo de paciencia ", "Para tu sorpresa ", "Y al final ",
    "Después de todo, ", "Aunque no lo creas, ", "Casi sin esperarlo ", "De un momento a otro ", "A su debido tiempo ",
    "Si perseveras, ", "Contra todo pronóstico ", "Con un poco de suerte ", "Antes de que te des cuenta ",
    "Por fortuna, ", "En medio de todo, ", "Con la ayuda del tiempo ",
]
B_TAILS = [
    ", justo cuando más lo necesitas", ", y se nota en tu ánimo", ", y eso te da nuevas fuerzas",
    ", y no es poca cosa", ", como un pequeño premio", ", y lo notarás enseguida", ", y vale cada esfuerzo",
    ", y no te lo esperabas", ", y te lo agradecerás", ", y bien que lo necesitabas", ", y te devuelve el ánimo",
    ", como quien recibe un buen regalo", ", y eso cambia el rumbo del día", ", algo que ya no esperabas",
    ", y se siente muy bien", ", y te hacía falta", ", y ya era hora", ", como una pequeña victoria",
    ", como si el día se pusiera de tu parte", 
]
C_PLANETS = ["Venus", "Mercurio", "Marte", "Júpiter", "Saturno", "la Luna", "el Sol", "Neptuno"]
C_LEADS = ["", "", "Hoy ", "Estos días ", "Esta jornada ", "Por estos días ", "Desde temprano ", "Esta vez "]
C_FRAMES = ["favorece", "pone luz sobre", "protege", "da impulso a", "cuida de", "inspira"]
C_TIP_FRAMES = [
    "aprovecha para {x}", "intenta {x}", "trata de {x}", "procura {x}",
    "hazte el favor de {x}", "no te olvides de {x}", "te vendrá bien {x}", "conviene {x}",
]
C_TIP_LEADS = ["", "Un consejo: ", "Además, ", "Y si puedes, "]

# ---- Piezas por categoría -----------------------------------------------------
CONTENT = {
    'Hoy': {
        'sit': [
            'la jornada llega cargada de pendientes',
            'algo que venías postergando reclama por fin tu atención',
            'se cruzan dos compromisos al mismo tiempo',
            'sientes que el día te queda un poco grande',
            'la rutina pesa más de lo habitual',
            'una decisión importante asoma en el horizonte',
            'hay ruido a tu alrededor y cuesta concentrarse',
            'un plan cambia a último momento',
            'empiezas con más dudas que certezas',
            'alguien cercano espera una respuesta tuya',
            'el cansancio de la semana empieza a notarse',
            'tu agenda se llena de pequeñas tareas',
            'te levantas con ganas de cambiar algo',
            'tienes más energía de la que sospechas',
            'una idea que parecía descabellada empieza a cobrar sentido',
            'te cuesta arrancar, aunque tu cabeza ya tiene claro el rumbo',
            'tu paciencia se pone a prueba desde temprano',
            'surge una oportunidad que no tenías prevista',
            'te piden más de lo que puedes dar',
            'sientes que todo ocurre más rápido que tú',
            'una conversación pendiente ronda tu cabeza',
            'el ánimo sube y baja sin demasiada explicación',
            'tienes ante ti un camino que no termina de convencerte',
            'recibes consejos de todos lados',
            'un viejo asunto vuelve a ponerse sobre la mesa',
            'te llega un encargo que no esperabas',
            'notas que cuesta poner orden en tus ideas',
            'te sientes a medio camino entre dos opciones',
            'algo que dabas por resuelto vuelve a moverse',
            'las prisas te acompañan desde la mañana',
            'tienes la sensación de estar dando vueltas en el mismo punto',
            'se acerca una fecha que te inquieta un poco',
            'recuperas el entusiasmo por algo que habías dejado de lado',
            'el entorno te empuja a salir de la rutina',
            'una pequeña discusión amenaza con arruinarte el humor',
            'un tema que parecía menor pide más tiempo del esperado',
            'te sientes con ganas de empezar de nuevo',
            'tu intuición te dice que algo está por cambiar',
            'cargas con un peso que ya no te corresponde',
            'la jornada se presenta más movida de lo que pensabas',
        ],
        'eff': [
            'insistir un poco más de lo previsto',
            'hacer una pausa cuando aparezca la duda',
            'poner límites a lo que te quita energía',
            'dedicar tiempo a un pequeño obstáculo',
            'tomarte tu tiempo para decidir entre dos opciones',
            'tener una conversación incómoda pero necesaria',
            'ordenar prioridades',
            'enfrentar una situación pendiente',
            'sostener el ritmo ante la presión',
            'salir de tu zona de confort',
            'confiar en tus capacidades ante una dificultad',
            'armarte de paciencia con un asunto lento',
            'revisar lo que no te convence',
            'resistir la tentación de rendirte',
            'aceptar ayuda cuando la necesites',
            'atender un imprevisto',
            'dividir una tarea grande en partes pequeñas',
            'dejar de postergar lo importante',
            'reconocer un error y corregirlo',
            'decir no a lo que te distrae',
            'adaptarte a un cambio de planes',
            'perseverar cuando el avance se note poco',
            'evitar comparaciones que te desaniman',
            'terminar una tarea antes de empezar otra',
            'pedir una opinión sincera',
            'soltar el control de algo que no depende de ti',
            'cuidar tus energías durante la tarde',
            'preparar mejor el siguiente paso',
            'buscar una solución distinta a la de siempre',
            'atender un detalle que habías pasado por alto',
            'esperar el momento justo sin desesperar',
            'sostener tu decisión frente a las dudas',
        ],
        'light': [
            'todo empieza a acomodarse',
            'llegará una noticia que te alegra el día',
            'se abre una puerta que parecía cerrada',
            'descubrirás que eras más capaz de lo que creías',
            'recibirás un gesto de apoyo que no esperabas',
            'encontrarás la solución donde menos pensabas',
            'sentirás que el esfuerzo valió la pena',
            'cerrarás con una sonrisa lo que empezó con dudas',
            'el panorama se aclara y respiras con alivio',
            'una persona de confianza te echa una mano',
            'te sorprende lo bien que sale lo que temías',
            'recuperas el control de la situación',
            'aparece una idea que lo cambia todo',
            'tu paciencia da sus primeros frutos',
            'llega un momento de calma que agradecerás',
            'alguien reconoce lo que haces sin que se lo pidas',
            'te vas a dormir con la sensación de haber avanzado',
            'lo que parecía un problema resulta ser una oportunidad',
            'una casualidad feliz juega a tu favor',
            'tendrás un rato para ti y lo disfrutarás de verdad',
            'la suerte te guiña un ojo',
            'se despeja una duda que te venía rondando',
            'descubres que no estabas tan lejos de tu objetivo',
            'se te ocurre justo lo que hacía falta',
            'una buena noticia te devuelve las ganas',
            'sentirás un alivio enorme al soltar lo que pesaba',
            'las cosas se ponen de tu lado',
            'ganas confianza con cada paso que das',
            'se renueva tu fe en lo que estás construyendo',
            'tu esfuerzo empieza a verse',
            'aparece alguien que suma justo a tiempo',
            'termina mejor de lo que empezó',
            'una sorpresa agradable te espera a la vuelta de la esquina',
            'sentirás que vuelves a tener el timón',
            'lo que hoy cuesta mañana será tu mayor orgullo',
            'se confirma que ibas por buen camino',
            'tu ánimo se levanta sin que sepas bien por qué',
            'una risa inesperada te cambia el humor',
            'obtendrás una respuesta que llevabas tiempo esperando',
            'tu intuición acierta y te lo agradecerás',
            'te darás cuenta de cuánto has avanzado',
            'la tensión se disuelve y todo fluye mejor',
            'tomarás una decisión que te devuelve la paz',
            'se cierra un asunto pendiente y respiras hondo',
            'tendrás motivos para celebrar, aunque sea en pequeño',
            'empiezas a ver resultados donde antes solo había dudas',
            'una palabra amable llega en el momento justo',
            'te quedas con el ánimo más liviano de lo que esperabas',
        ],
        'astro': [
            'las decisiones del día',
            'tus ideas',
            'las conversaciones importantes',
            'los planes que tienes entre manos',
            'tu energía',
            'los proyectos nuevos',
            'los pendientes del día',
            'tu intuición',
            'los cambios de planes',
            'los encuentros casuales',
            'tu concentración',
            'la organización de tu agenda',
            'los comienzos',
            'tus iniciativas',
            'las gestiones de último momento',
            'tu estado de ánimo',
            'las sorpresas del día',
            'la búsqueda de soluciones',
            'las charlas con los tuyos',
            'el inicio de algo nuevo',
        ],
        'tips': [
            'tomarte cinco minutos antes de responder',
            'anotar lo que tienes pendiente',
            'empezar por lo más difícil',
            'hablar claro y sin rodeos',
            'dejar el móvil un rato',
            'pedir ayuda sin vergüenza',
            'hacer una pausa a media tarde',
            'revisar tus planes con calma',
            'decir lo que piensas con respeto',
            'escuchar a quien tiene experiencia',
            'guardar energía para la tarde',
            'terminar lo que ya empezaste',
            'confiar un poco más en tu instinto',
            'darte un pequeño gusto al final del día',
            'evitar discusiones innecesarias',
            'ir paso a paso sin querer abarcarlo todo',
            'sonreír aunque cueste',
            'salir a caminar un rato',
            'agradecer algo antes de dormir',
            'poner límites a lo que no te corresponde',
            'empezar con un buen desayuno',
            'dedicar unos minutos a respirar',
            'ser amable contigo',
            'no cargar con lo que no es tuyo',
            'tomar una decisión pequeña y cumplirla',
            'dejar para mañana lo que no sea urgente',
            'aprovechar la mañana para lo importante',
            'preguntar antes de suponer',
            'cerrar el día con algo que te guste',
            'mirar el lado bueno de las cosas',
        ],
    },
    'Amor': {
        'sit': [
            'tu corazón anda algo revuelto',
            'una conversación pendiente con alguien especial pesa en tu ánimo',
            'se acerca alguien con quien conectas de inmediato',
            'te sientes con ganas de dar más de lo que recibes',
            'un malentendido reciente sigue dando vueltas',
            'la distancia con alguien querido se hace notar',
            'hay ternura en el aire, aunque no sepas cómo expresarla',
            'una persona del pasado vuelve a tu pensamiento',
            'te pide el cuerpo un abrazo largo',
            'la rutina en pareja empieza a pedir un cambio',
            'alguien espera que des el primer paso',
            'notas que cuesta decir lo que sientes',
            'tu sensibilidad está a flor de piel',
            'un viejo resentimiento intenta volver',
            'una amistad necesita tu atención',
            'te sientes más cerca de tu familia que de costumbre',
            'el orgullo se interpone entre tú y alguien que quieres',
            'una mirada o un mensaje te remueve por dentro',
            'recibes más cariño del que sabes aceptar',
            'un silencio incómodo se instala entre dos personas',
            'te cuesta separar lo que sientes de lo que imaginas',
            'tienes ganas de plantear algo que llevas tiempo callando',
            'un encuentro casual puede cambiar tu estado de ánimo',
            'hay quien te quiere y no sabes verlo',
            'tu corazón pide calma después de unos días intensos',
            'un plan en compañía se tuerce por un detalle',
            'te debates entre lo que quieres y lo que debes',
            'se reaviva una ilusión que creías dormida',
            'alguien te pide más tiempo del que puedes darle',
            'un gesto tuyo se malinterpreta y genera tensión',
            'la nostalgia te visita sin avisar',
            'una persona cercana atraviesa un mal momento y te necesita',
            'te nace el deseo de sorprender a quien quieres',
            'hay celos o dudas que te cuesta nombrar',
            'una discusión menor puede crecer si no la hablas',
            'sientes que das mucho y recibes poco',
            'el cariño de siempre está ahí, aunque lo des por hecho',
            'te cruzas con alguien que despierta tu curiosidad',
            'un vínculo importante atraviesa un momento de cambio',
            'la pareja y el trabajo compiten por tu tiempo',
        ],
        'eff': [
            'aclarar un malentendido',
            'escuchar antes de responder',
            'dejar atrás un viejo resentimiento',
            'dar el primer paso para reparar una distancia',
            'tener una conversación pendiente',
            'ceder en algo pequeño',
            'pedir perdón si hace falta',
            'expresar lo que te cuesta decir',
            'poner límites con cariño',
            'equilibrar tus necesidades con las de otra persona',
            'aceptar que no todo depende de ti',
            'tender un puente después de un silencio',
            'respetar los tiempos de quien quieres',
            'soltar una expectativa que no se cumplió',
            'mostrar tu vulnerabilidad',
            'hablar con calma en un momento tenso',
            'reconocer un error propio',
            'perdonar sin guardar rencor',
            'dedicar más tiempo a quien lo necesita',
            'aprender a pedir ayuda',
            'tolerar una diferencia de opiniones',
            'cuidar el vínculo con constancia',
            'separar lo que sientes de lo que supones',
            'respirar antes de reaccionar',
            'entender que el cariño se construye de a poco',
            'dejar de postergar una charla importante',
            'revisar lo que esperas de una relación',
            'reconocer lo que te hace feliz',
            'dar espacio cuando hace falta',
            'animarte a decir lo que piensas',
            'no tomar como personal un mal momento',
            'recordar lo bueno cuando haya tensión',
        ],
        'light': [
            'una palabra sincera lo arregla todo',
            'recibirás un abrazo que vale por mil palabras',
            'la conversación pendiente sale mejor de lo que temías',
            'alguien te sorprende con un detalle lleno de cariño',
            'el cariño vuelve a fluir con naturalidad',
            'se disipa el malentendido y reina la calma',
            'llega un mensaje que te hace sonreír',
            'sentirás que alguien te entiende de verdad',
            'un reencuentro te llena el corazón',
            'la complicidad regresa y te regala un buen rato',
            'descubres que te quieren más de lo que pensabas',
            'se acorta la distancia con quien extrañas',
            'una charla sincera abre una etapa más serena',
            'alguien responde a tu ternura con otra aún mayor',
            'el orgullo se rinde y gana el cariño',
            'una mirada cómplice te dice todo lo que necesitabas oír',
            'tu pareja o tus amigos te dan una alegría inesperada',
            'se confirma que tu cariño es correspondido',
            'te reconcilias con alguien importante',
            'tu corazón se aligera como si te quitaras un peso de encima',
            'vuelve la risa compartida',
            'un gesto pequeño marca una gran diferencia',
            'nace una conexión que promete ser duradera',
            'sentirás que estás exactamente donde quieres estar',
            'alguien te dice justo lo que querías escuchar',
            'te sorprende lo bien que expresas lo que sientes',
            'el cariño de los tuyos te envuelve como un abrigo',
            'la ilusión se renueva y con ella las ganas de cuidar lo que tienes',
            'un perdón sincero cierra una herida antigua',
            'se despejan las dudas y ves con claridad lo que sientes',
            'recibes una invitación que te devuelve la ilusión',
            'compartes una velada tranquila que te sienta de maravilla',
            'la ternura gana la partida a la discusión',
            'alguien especial te hace sentir en casa',
            'se fortalece un lazo que creías debilitado',
            'recuerdas por qué quieres a quien quieres',
            'una sonrisa tuya desarma cualquier tensión',
            'llega un detalle que no esperabas y te emociona',
            'se abre la posibilidad de empezar de nuevo con alguien',
            'el amor te recuerda que a veces basta con estar',
            'tu sinceridad es recibida con los brazos abiertos',
            'una noche de charla te acerca más que meses enteros',
            'disfrutas de un cariño sin condiciones',
            'llega la reconciliación que tanto esperabas',
            'te llenas de ganas de cuidar y dejarte cuidar',
            'un abrazo en el momento justo lo cambia todo',
            'alguien cercano te agradece de corazón lo que haces',
            'la paz vuelve a tus relaciones más queridas',
            'terminas con una sensación de cariño compartido',
        ],
        'astro': [
            'las conversaciones sinceras',
            'los encuentros con quien quieres',
            'las reconciliaciones',
            'los gestos de cariño',
            'la complicidad en pareja',
            'las amistades de siempre',
            'los reencuentros',
            'las charlas pendientes',
            'la ternura cotidiana',
            'los vínculos familiares',
            'los primeros pasos en el amor',
            'las declaraciones sinceras',
            'los perdones necesarios',
            'las citas improvisadas',
            'la confianza entre dos personas',
            'los mensajes que se esperaban',
            'la convivencia',
            'los acuerdos en pareja',
            'las sorpresas afectivas',
            'el diálogo con los tuyos',
        ],
        'tips': [
            'decir hoy lo que sientes',
            'regalar un abrazo sin motivo',
            'escuchar sin interrumpir',
            'dedicarle un rato de calidad a quien quieres',
            'enviar ese mensaje que tienes pendiente',
            'agradecer a quien te cuida',
            'dejar el orgullo a un lado',
            'preguntar cómo está esa persona especial',
            'planear algo sencillo en compañía',
            'no dar por hecho el cariño',
            'mirar a los ojos al conversar',
            'pedir perdón si corresponde',
            'reírte un rato con alguien querido',
            'recordar un buen momento compartido',
            'dar espacio a quien lo necesita',
            'cuidar los pequeños detalles',
            'hablar de lo que te molesta con calma',
            'abrirte a conocer gente nueva',
            'llamar a alguien que extrañas',
            'evitar reproches innecesarios',
            'mostrar interés por los demás',
            'regalar una palabra amable',
            'compartir una comida sin prisas',
            'no guardar rencores',
            'valorar lo que ya tienes en el amor',
            'dejar que otros te cuiden',
            'hacer las paces con el pasado',
            'cocinar algo rico para alguien querido',
            'contar lo que te ilusiona',
            'confiar un poco más',
        ],
    },
    'Riqueza': {
        'sit': [
            'el trabajo se acumula sobre tu escritorio',
            'una propuesta interesante asoma en el horizonte',
            'te toca ordenar unas cuentas que andaban descuidadas',
            'un gasto inesperado altera tus planes',
            'se acerca una reunión importante',
            'tienes un proyecto a medio camino que necesita impulso',
            'alguien te pide que asumas más responsabilidad',
            'el dinero parece escurrirse entre los dedos',
            'una negociación se alarga más de lo previsto',
            'recibes una idea que podría mejorar tus ingresos',
            'hay cambios en tu entorno laboral',
            'tu talento empieza a llamar la atención',
            'un plazo se acerca y aún queda mucho por hacer',
            'te surge la duda entre quedarte donde estás o probar algo nuevo',
            'un trámite se demora más de lo razonable',
            'sientes que trabajas mucho y el reconocimiento tarda',
            'se presenta una oportunidad para aprender algo útil',
            'te ofrecen un trato que conviene mirar con lupa',
            'tus finanzas piden un poco de orden',
            'alguien del trabajo te complica una tarea',
            'el panorama económico se muestra algo incierto',
            'hay un compromiso que no te conviene del todo',
            'te llega la tentación de una compra impulsiva',
            'un contacto olvidado reaparece con novedades',
            'tienes que decidir con los números en la mano',
            'el ritmo laboral se acelera sin previo aviso',
            'alguien exige más de lo acordado',
            'un proyecto personal reclama tiempo y dinero',
            'tu esfuerzo de los últimos meses empieza a notarse',
            'surge un imprevisto en un papeleo importante',
            'te cuesta decir que no a un pedido extra',
            'tu economía pide paciencia y cálculo',
            'un ahorro tuyo puede ponerse a trabajar',
            'el equipo necesita que tomes la iniciativa',
            'una inversión de tiempo empieza a mostrar resultados',
            'se cruzan dos prioridades laborales',
            'un error pequeño amenaza con volverse grande',
            'te proponen colaborar en algo nuevo',
            'una deuda pendiente pesa más de lo que admites',
            'las cuentas del mes se ajustan más de lo esperado',
        ],
        'eff': [
            'revisar cada detalle antes de comprometerte',
            'resistir la tentación de gastar sin necesidad',
            'cumplir con un plazo ajustado',
            'rehacer una parte del trabajo',
            'adaptarte a un cambio de planes',
            'defender tus ideas con argumentos sólidos',
            'replantear prioridades tras un gasto inesperado',
            'asumir una responsabilidad extra',
            'sostener un proyecto exigente',
            'mantener la serenidad en una negociación lenta',
            'aprender de un pequeño tropiezo',
            'dosificar tus fuerzas',
            'gestionar un trámite que se demora',
            'poner orden en tus cuentas',
            'decir que no a un compromiso que no te conviene',
            'pedir una segunda opinión',
            'estudiar mejor una propuesta',
            'ahorrar un poco más de lo habitual',
            'organizar mejor tu tiempo',
            'enfrentar una tarea que venías postergando',
            'cuidar tu reputación profesional',
            'tener una conversación difícil con un colega',
            'ser constante aunque los resultados tarden',
            'controlar los impulsos a la hora de comprar',
            'prepararte mejor para una reunión',
            'resolver un problema antes de que crezca',
            'priorizar lo importante sobre lo urgente',
            'pedir lo que consideras justo',
            'mantener la disciplina en tus metas',
            'tener paciencia con los resultados',
            'comparar opciones antes de gastar',
            'no comprometerte con más de lo que puedes abarcar',
        ],
        'light': [
            'llegará un reconocimiento que llevabas tiempo esperando',
            'se cierra un trato que te conviene',
            'los números empiezan a cuadrar',
            'aparece una oportunidad económica que no esperabas',
            'tu trabajo bien hecho abre una puerta nueva',
            'recibes una buena noticia sobre tus ingresos',
            'un contacto te acerca justo la propuesta que necesitabas',
            'ves con claridad cómo ordenar tus gastos',
            'se resuelve ese trámite que te quitaba el sueño',
            'tu esfuerzo se traduce en un resultado concreto',
            'alguien confía en tu criterio y te lo hace saber',
            'descubres una forma de ahorrar sin renunciar a lo importante',
            'tu proyecto despega con más fuerza de la esperada',
            'consigues el acuerdo que parecía imposible',
            'llega un pago que alivia tus cuentas',
            'tu prudencia te ahorra un disgusto',
            'te ofrecen algo que encaja con tus planes',
            'se afianza tu posición en el trabajo',
            'una idea tuya es bien recibida',
            'el panorama económico se aclara y ganas tranquilidad',
            'tu constancia convence hasta a los más escépticos',
            'se abre un camino para crecer profesionalmente',
            'cierras con la lista de tareas completa',
            'alguien valora tu dedicación con hechos',
            'aparece una ayuda que acelera tu proyecto',
            'tus decisiones prudentes empiezan a dar fruto',
            'te das cuenta de que tu situación es más sólida de lo que pensabas',
            'un ingreso extra llega en el momento justo',
            'la negociación termina a tu favor',
            'se aclara un asunto de dinero que te preocupaba',
            'tu perseverancia convierte un tropiezo en aprendizaje',
            'consigues el respaldo que necesitabas',
            'te felicitan por un trabajo que dabas por rutinario',
            'tu reputación sale fortalecida',
            'se concreta una colaboración prometedora',
            'tu plan de ahorro empieza a dar resultados',
            'recibes una propuesta que mejora tu situación',
            'ganas la confianza de quien toma las decisiones',
            'todo el trabajo previo se transforma en un avance visible',
            'se despeja el camino hacia una meta importante',
            'un cambio laboral resulta mejor de lo que temías',
            'el dinero rinde más de lo previsto',
            'tu esfuerzo atrae a las personas indicadas',
            'concluyes un proyecto con la satisfacción del deber cumplido',
            'llega una recompensa por tu constancia',
            'un nuevo comienzo profesional se perfila con buenos augurios',
            'tu criterio te da la razón',
            'te dan luz verde para avanzar',
        ],
        'astro': [
            'las negociaciones del día',
            'los asuntos de dinero',
            'los proyectos nuevos',
            'los acuerdos laborales',
            'las decisiones económicas',
            'los trámites pendientes',
            'las reuniones importantes',
            'el trabajo en equipo',
            'tus ahorros',
            'las propuestas profesionales',
            'las gestiones con papeles',
            'los contactos laborales',
            'las inversiones prudentes',
            'los pagos pendientes',
            'las ideas emprendedoras',
            'el orden de tus cuentas',
            'las conversaciones sobre sueldos',
            'los cambios de trabajo',
            'los negocios en marcha',
            'las metas profesionales',
        ],
        'tips': [
            'anotar tus gastos de la semana',
            'revisar tus cuentas sin miedo',
            'hacer una lista de prioridades',
            'leer bien la letra pequeña',
            'consultar con alguien de confianza antes de firmar',
            'ahorrar aunque sea una pequeña cantidad',
            'agradecer una colaboración',
            'delegar lo que no es esencial',
            'planificar la semana con antelación',
            'evitar compras impulsivas',
            'mostrar tus avances a quien corresponde',
            'dedicar tiempo a aprender algo útil',
            'cuidar tus contactos profesionales',
            'poner fecha a una meta',
            'dejar claras las condiciones de un acuerdo',
            'dar seguimiento a ese correo pendiente',
            'descansar antes de una decisión grande',
            'pensar a largo plazo',
            'comparar antes de gastar',
            'guardar copia de lo importante',
            'reconocer el trabajo de tu equipo',
            'terminar lo que dejaste a medias',
            'no prometer más de lo que puedes cumplir',
            'preparar con tiempo tu próxima reunión',
            'separar un poco de dinero para imprevistos',
            'preguntar sin miedo',
            'enfocarte en una cosa a la vez',
            'revisar tus suscripciones',
            'buscar una fuente extra de ingresos',
            'celebrar un logro, por pequeño que sea',
        ],
    },
    'Bienestar': {
        'sit': [
            'el cuerpo te pide frenar un poco',
            'te cuesta conciliar el sueño últimamente',
            'la cabeza no deja de dar vueltas',
            'tu energía anda algo baja',
            'sientes tensión acumulada en los hombros',
            'el estrés se instala sin que lo notes',
            'tienes ganas de moverte y despejarte',
            'la mente pide silencio',
            'tu ánimo cambia de un momento a otro',
            'has descuidado tus rutinas sanas',
            'necesitas aire fresco y un poco de sol',
            'una preocupación te roba la tranquilidad',
            'tu cuerpo agradece cualquier gesto de cuidado',
            'hay cansancio acumulado de días intensos',
            'te cuesta desconectar de las obligaciones',
            'tu apetito y tu humor van de la mano',
            'sientes que necesitas un cambio de ritmo',
            'la ansiedad asoma cuando piensas en lo que viene',
            'estás más sensible de lo habitual',
            'te falta tiempo para ti',
            'un dolor pequeño te recuerda que debes cuidarte',
            'sientes la necesidad de poner orden en tus hábitos',
            'el ritmo de la semana te pasa factura',
            'tu mente va más rápido que tu cuerpo',
            'te rondan pensamientos que no te hacen bien',
            'has estado exigiéndote demasiado',
            'el silencio y la calma te llaman',
            'tu cuerpo pide agua, descanso y buena comida',
            'hay momentos del día en que te ganan las prisas',
            'te sientes con ganas de retomar el ejercicio',
            'la falta de pausas empieza a notarse',
            'una emoción intensa te atraviesa sin permiso',
            'el cansancio te juega malas pasadas',
            'sientes que tu energía necesita recargarse',
            'tienes la cabeza llena de listas y pendientes',
            'tu sueño no es tan reparador como quisieras',
            'estás a punto de empezar un hábito nuevo',
            'las pantallas te roban más tiempo del que quisieras',
            'tu cuerpo te da señales que no conviene ignorar',
            'buscas un rato de calma en medio del ruido',
        ],
        'eff': [
            'mantener la constancia en una rutina saludable',
            'reconocer el cansancio acumulado',
            'decir no para proteger tu tranquilidad',
            'respirar con calma en momentos de tensión',
            'dormir y alimentarte con más cuidado',
            'soltar una preocupación poco a poco',
            'vencer la pereza del primer paso',
            'confiar en tu fuerza aunque dudes',
            'cambiar un viejo hábito',
            'gestionar el estrés con pequeños gestos',
            'detenerte a recuperar fuerzas',
            'reconocer una emoción intensa',
            'escuchar a tu cuerpo aunque prefieras seguir',
            'sostener la confianza en un momento de inquietud',
            'desconectarte un rato de las pantallas',
            'hidratarte y moverte más',
            'poner orden en tus horarios de descanso',
            'pedir ayuda cuando todo pesa',
            'aceptar que no puedes con todo',
            'reservar tiempo para ti',
            'evitar la autoexigencia excesiva',
            'enfrentar un miedo pequeño',
            'dejar de postergar un chequeo médico',
            'moderar el ritmo de trabajo',
            'alejarte de lo que te agota',
            'mantener una rutina de ejercicio',
            'practicar la calma cuando algo te altera',
            'aprender a decir basta a tiempo',
            'cuidar tus pensamientos',
            'perdonarte un error',
            'no abandonar tu rutina un día difícil',
            'darte permiso para descansar',
        ],
        'light': [
            'un descanso a tiempo te devuelve las fuerzas',
            'tu cuerpo responde y te sientes con más energía',
            'la calma vuelve a instalarse en tu cabeza',
            'duermes con una tranquilidad que hacía tiempo no tenías',
            'un paseo corto te cambia el humor',
            'sientes que la tensión se deshace poco a poco',
            'respiras hondo y todo se ve más claro',
            'un rato para ti te devuelve el equilibrio',
            'tu ánimo se levanta con cosas sencillas',
            'descubres que cuidarte te sienta de maravilla',
            'se despeja la mente y vuelves a concentrarte',
            'el cuerpo te lo agradece con un buen día',
            'una buena charla te quita un peso de encima',
            'la ansiedad cede y llega la serenidad',
            'recuperas las ganas de moverte',
            'tu energía se recarga cuando menos lo esperas',
            'un baño caliente o una infusión te devuelve la paz',
            'tu hábito nuevo empieza a notarse en tu ánimo',
            'te dedicas un momento y sientes que renaces',
            'vuelves a conectar con lo que te hace bien',
            'aprendes a soltar lo que no puedes controlar',
            'tu sueño mejora y con él tu humor',
            'una sonrisa franca te alivia más que cualquier remedio',
            'el aire fresco te despeja las ideas',
            'encuentras un ritmo que te sienta bien',
            'tu cuerpo y tu mente por fin se ponen de acuerdo',
            'te sorprende lo bien que te sienta decir que no',
            'la tranquilidad llega cuando dejas de exigirte tanto',
            'sientes una ligereza que no sentías hacía semanas',
            'el cansancio da paso a una agradable sensación de logro',
            'un rato de silencio te devuelve la claridad',
            'te reencuentras con tu buen humor',
            'una comida tranquila te reconforta',
            'tu mente se aquieta y tu cuerpo se relaja',
            'percibes que tu energía fluye de nuevo',
            'el movimiento te devuelve la alegría',
            'una pausa bien aprovechada lo cambia todo',
            'se disuelve esa preocupación que te pesaba',
            'recuperas la confianza en tu propio cuerpo',
            'la gratitud te llena de buena energía',
            'un gesto de autocuidado marca la diferencia',
            'te levantas con una calma renovadora',
            'tu mente despejada te regala buenas ideas',
            'sientes que el equilibrio vuelve a ti',
            'encuentras paz en lo más simple',
            'tu bienestar mejora con cada pequeño cambio',
            'te acuestas en paz y con el cuerpo en calma',
            'una energía luminosa te acompaña hasta la noche',
            'entiendes que descansar también es avanzar',
        ],
        'astro': [
            'el descanso',
            'la calma mental',
            'tus rutinas sanas',
            'los paseos al aire libre',
            'el sueño reparador',
            'tu energía vital',
            'las pausas del día',
            'la respiración consciente',
            'el ejercicio suave',
            'la alimentación equilibrada',
            'los momentos de silencio',
            'tu equilibrio emocional',
            'los hábitos nuevos',
            'el autocuidado',
            'la relajación',
            'los ratos de desconexión',
            'la serenidad de tu mente',
            'tu bienestar general',
            'las actividades al sol',
            'tu paz interior',
        ],
        'tips': [
            'beber más agua durante el día',
            'salir a caminar al aire libre',
            'dormir unos minutos más',
            'estirar el cuerpo al levantarte',
            'comer despacio y sin pantallas',
            'apagar el móvil una hora antes de dormir',
            'respirar hondo cuando sientas tensión',
            'hacer una pausa cada tanto',
            'probar una infusión caliente por la noche',
            'dedicar diez minutos a no hacer nada',
            'escuchar tu música favorita',
            'tomar un poco de sol',
            'dejar un hueco libre en la agenda',
            'anotar lo que te preocupa y soltarlo',
            'bailar en casa como si nadie te viera',
            'hablar con alguien de confianza',
            'cenar algo ligero',
            'cuidar tu postura frente al ordenador',
            'reír con ganas',
            'evitar el café a última hora',
            'ordenar un rincón de tu casa',
            'practicar un minuto de silencio',
            'ventilar tu espacio',
            'mirar el cielo un momento',
            'acostarte a una hora razonable',
            'pasar tiempo con quien te hace bien',
            'dejar de lado las quejas por hoy',
            'agradecer a tu cuerpo lo que hace por ti',
            'regalarte un momento de calma',
            'estirar las piernas cada hora',
        ],
    },
}


# ---- Ampliación de Amor: amistades, familia, citas y nostalgia (no solo pareja) ----------
CONTENT["Amor"]["sit"] += [
    "una amistad de años te pide un momento de calidad",
    "una cita o un encuentro social te llena de expectativas",
    "tu familia reclama un poco más de tu presencia",
    "te acuerdas de alguien con mucha nostalgia",
    "alguien de tu círculo de amistades atraviesa un mal momento",
    "una reunión familiar despierta emociones encontradas",
    "te invitan a una salida que te hace dudar",
    "un viejo conocido reaparece en tu vida",
    "alguien de tu familia espera noticias tuyas",
    "sientes que tu círculo de amistades necesita renovarse",
    "un recuerdo de la infancia te llena de ternura",
    "te cuesta decidir si das una segunda oportunidad",
    "una persona nueva despierta tu interés, aunque no sepas por qué",
]
CONTENT["Amor"]["light"] += [
    "alguien querido te sorprende con una llamada",
    "la familia se reúne y todo se siente más liviano",
    "una cita inesperada te devuelve la ilusión",
    "una amistad se fortalece con una charla sincera",
    "la nostalgia se convierte en una sonrisa",
    "un lazo familiar se estrecha y te llena de calidez",
    "alguien nuevo en tu vida te transmite confianza",
    "recuperas el contacto con alguien que extrañabas",
    "un brindis con los tuyos deja un recuerdo hermoso",
    "una segunda oportunidad resulta mejor de lo esperado",
    "descubres quiénes están de verdad a tu lado",
    "una salida con amistades te recarga de alegría",
]
CONTENT["Amor"]["eff"] += [
    "dedicar tiempo a una amistad que lo necesita",
    "llamar a alguien de tu familia",
    "aceptar una invitación que te da pereza",
    "dejar atrás una nostalgia que pesa",
    "dar una segunda oportunidad con la cabeza fría",
    "soltar una amistad que ya no suma",
    "tomar la iniciativa en una cita",
    "reservar un rato para tu círculo cercano",
]
CONTENT["Amor"]["tips"] += [
    "organizar una reunión con tus amistades",
    "llamar a tus padres o a tus hermanos",
    "aceptar esa invitación pendiente",
    "mirar fotos que te hagan sonreír",
    "escribirle a alguien con quien perdiste contacto",
    "preparar una cena para los tuyos",
]
CONTENT["Amor"]["astro"] += [
    "las amistades de toda la vida",
    "las reuniones familiares",
    "las primeras citas",
    "los recuerdos que se reencuentran",
]
for _cat, _lists in CONTENT.items():
    for _k, _v in _lists.items():
        assert len(_v) == len(set(_v)), (_cat, _k)


# ---- Ampliación de vocabulario (todas las categorías) ----------------------------------------
def _L(s):
    return [x.strip() for x in s.strip().split("\n") if x.strip()]


_EXT = {
    "Hoy": {
        "sit": _L("""
el reloj parece correr más deprisa que de costumbre
un cruce de caminos te obliga a elegir rumbo
te rodea cierta confusión que pide paciencia
la agenda te exige malabares
una noticia inesperada sacude tu calendario
aparece un obstáculo menor justo cuando creías tenerlo todo controlado
tus pensamientos van y vienen sin encontrar reposo
hay un asunto espinoso que ya no puedes esquivar
un compromiso adquirido a la ligera pide cuentas
sientes el impulso de abandonar una tarea a medias
una duda ajena intenta colarse en tus planes
percibes que falta un último empujón para cerrar un tema
la prisa de los demás amenaza con contagiarte
una corazonada insiste en llamar tu atención
"""),
        "eff": _L("""
mantener el pulso firme ante lo imprevisto
deslindar lo urgente de lo accesorio
enfriar la cabeza antes de contestar
resistir el impulso de abandonar a medias
cerrar un frente abierto antes de abrir otro
hacerte tiempo para lo que de verdad cuenta
mirar de frente algo que venías eludiendo
dosificar tu entusiasmo para llegar con fuerzas a la noche
desconfiar de las soluciones demasiado fáciles
sostener tu postura sin alzar la voz
"""),
        "light": _L("""
cada pieza encuentra por fin su lugar
un golpe de suerte te allana el camino
la intuición te sopla justo la respuesta correcta
el nudo que te apretaba empieza a aflojarse
descubres que el esfuerzo tenía sentido
un rayo de claridad ilumina lo que parecía confuso
te sorprende la rapidez con que se resuelve un asunto
alguien dice la palabra exacta y todo cambia
el cansancio se transforma en satisfacción
se despeja el horizonte y vuelves a ver el rumbo
consigues dar el paso que llevabas semanas postergando
el día te regala un pequeño triunfo
la balanza se inclina a tu favor
termina por salir mejor de lo que imaginabas
"""),
        "tips": _L("""
regalarte un respiro a media mañana
poner en orden tu escritorio antes de empezar
confiar en tu primera impresión
dejar un margen para los imprevistos
hacer una sola cosa a la vez
escribir tres prioridades al despertar
brindar por algo pequeño al caer la noche
desconectar las notificaciones un rato
"""),
        "astro": _L("""
las corazonadas del día
los asuntos que parecían estancados
las decisiones rápidas
los acuerdos de última hora
las ideas que despiertan al alba
"""),
    },
    "Amor": {
        "sit": _L("""
el silencio de alguien querido te intriga
una declaración pendiente te quema por dentro
la timidez frena un gesto que deseas hacer
un reencuentro anunciado te acelera el pulso
alguien te mira con una ternura que no habías notado
una promesa hecha hace tiempo pide ser cumplida
un detalle pequeño te hace dudar de las intenciones ajenas
la dulzura de un recuerdo te arrulla
un lazo que creías roto se tensa otra vez
sientes que el afecto circula mejor entre risas
"""),
        "eff": _L("""
bajar la guardia con quien te quiere
decir lo que callas con tacto
reconocer el cariño que ya recibes
dejar de ensayar discursos y hablar desde el corazón
contener los celos antes de que crezcan
poner de tu parte para romper el silencio
aceptar que el afecto no se exige
regalar tu atención completa a quien te habla
"""),
        "light": _L("""
una mirada basta para disipar las dudas
la sinceridad vuelve a tender puentes
el afecto florece donde menos lo esperabas
una carta, un mensaje o una visita te llena de dicha
se derrite el hielo entre dos personas
la confianza se renueva con un gesto sencillo
descubres un cariño silencioso que estaba a tu lado
un abrazo largo repara más de lo que imaginabas
el cortejo avanza con una dulzura que te desarma
la risa compartida borra el malestar
alguien te elige sin dudarlo
el perdón llega como una brisa fresca
"""),
        "tips": _L("""
escribir una nota cariñosa
invitar a alguien a un café sin motivo
abrazar con ganas
recordar una fecha que importa a alguien
dar las gracias por un favor antiguo
dedicar una canción a quien quieres
"""),
        "astro": _L("""
los gestos de ternura
las confidencias entre dos
las promesas de afecto
los lazos que se estrechan
"""),
    },
    "Riqueza": {
        "sit": _L("""
una cifra en rojo te quita el sueño
el reloj de la oficina corre en tu contra
una oferta tentadora trae letra pequeña
la competencia te pisa los talones
te cambian las reglas del juego a mitad de camino
alguien clave retrasa una respuesta que esperas
una reunión sin objetivo claro consume tu energía
se multiplican las llamadas y los correos
tus gastos fijos hacen su aparición poco amistosa
te piden un favor profesional que no figura en tu agenda
una inversión pide más paciencia de la prevista
recibes una crítica que sientes injusta
un proyecto en equipo se estanca por falta de acuerdos
estrenas una responsabilidad que te queda algo grande
"""),
        "eff": _L("""
contar dos veces antes de firmar
argumentar con datos y no con impulsos
poner por escrito lo acordado
afinar el presupuesto de la semana
agendar tiempo para tus asuntos de dinero
defender tu valor sin regatearlo
investigar antes de apostar
aguantar la presión sin perder la sonrisa
cortar los gastos hormiga
aprender de un error ajeno sin criticarlo
"""),
        "light": _L("""
una puerta profesional se entreabre
tu cuenta respira con un alivio inesperado
el reconocimiento llega de quien menos esperabas
se firma un acuerdo con cláusulas a tu favor
un cliente satisfecho abre otras puertas
tu propuesta se impone entre las demás
el mercado te sonríe por un instante
encuentras una vía de ahorro que no veías
la perseverancia se transforma en ingresos
una ventaja competitiva sale a la luz
tus números muestran una tendencia alentadora
un aliado inesperado respalda tu idea
consigues cerrar el mes con un saldo favorable
el esfuerzo callado recibe su aplauso
"""),
        "tips": _L("""
guardar los comprobantes en orden
reservar una parte de lo que ganas
consultar a alguien con experiencia
negociar con la calma de quien no tiene prisa
fijar un tope de gastos semanal
actualizar tu currículum
agradecer a quien confía en ti
aprender una herramienta nueva de trabajo
"""),
        "astro": _L("""
los balances y las cuentas
las ofertas que llegan
los contratos por firmar
las alianzas profesionales
los ingresos extra
"""),
    },
    "Bienestar": {
        "sit": _L("""
una molestia leve se instala en la espalda
el insomnio te visita con insistencia
añoras un paisaje abierto y un poco de silencio
el cuerpo reclama sol y movimiento
una racha de comidas desordenadas empieza a notarse
los nervios se acumulan en el estómago
la mente se llena de ventanas abiertas
un exceso de cafeína te acelera
te duele la nuca de tanto sostener la tensión
estás a un paso de tocar tu límite
la ciudad te pesa y quieres escapar un rato
un dolor de cabeza amenaza con arruinarte la tarde
tu energía se agota antes de lo habitual
notas el cuerpo pesado y el ánimo apagado
"""),
        "eff": _L("""
escuchar la señal del cansancio antes de que grite
acostarte más temprano por una vez
hacer pausas visuales lejos de la pantalla
suavizar la rutina sin abandonarla
tomar el sol unos minutos
reducir el café sin dramatizar
masajear tu cuello con paciencia
hacer del descanso una prioridad real
cenar liviano y sin prisa
respirar contando hasta cuatro
"""),
        "light": _L("""
el cuerpo se afloja como si soltara una cuerda
tu cabeza se despeja como el cielo después de la lluvia
descansas profundamente y despiertas con ganas
el aire nuevo te llena de vitalidad
un masaje o un estiramiento te renueva
tu pulso se serena y tu ánimo se aligera
el sueño regresa como un viejo conocido
una caminata te devuelve la lucidez
te reconcilias con tu ritmo natural
sientes que respiras hasta el fondo
un baño tibio te devuelve la calma
la energía vuelve a correr por tus venas
el dolor cede y reaparece la sonrisa
un amanecer tranquilo te recibe con alegría
"""),
        "tips": _L("""
tomar un té sin mirar el teléfono
estirar los hombros cada hora
salir a ver el cielo un minuto
ir a la cama sin pantallas
comer una fruta de temporada
caminar con calzado cómodo
cerrar los ojos y contar hasta diez
regar una planta con calma
"""),
        "astro": _L("""
los ciclos de sueño
el pulso de tu cuerpo
los ratos de ocio
la salud de tu espalda
las caminatas de la tarde
"""),
    },
}
for _cat, _d in _EXT.items():
    for _k, _v in _d.items():
        CONTENT[_cat][_k] += _v
for _cat, _lists in CONTENT.items():
    for _k, _v in _lists.items():
        assert len(_v) == len(set(_v)), (_cat, _k)

# Piezas comunes ampliadas
C_PLANETS += ["Urano", "Plutón", "la Luna nueva", "la Luna creciente"]
C_FRAMES += ["despierta", "ilumina", "armoniza", "acompaña", "alienta", "bendice"]
C_LEADS += ["Durante estas horas ", "A lo largo del día ", "Con la caída de la tarde "]
A_LEADS += ["Con la mañana por delante ", "Entre una cosa y otra ", "En la recta final del día "]
B_CONNECTORS += ["Mucho antes del final ", "Cuando se asiente el polvo ", "Si todo marcha como parece, ", "En el último tramo del día "]
# Condicionales de una sola oración: "Si logras <esfuerzo>, <luz>."
COND_LEADS = [
    "Si logras", "Si te animas a", "Cuando consigas", "Si te decides a", "En cuanto logres",
    "Una vez que logres", "Si te das permiso para", "Si te propones",
    "A poco que consigas", "Cuando logres", "Si te atreves a", "Apenas logres", "Tan pronto como logres",
    "Si decides", "Siempre que logres", "Si pones empeño en", "En el momento en que logres",
    "Cuando te animes a", "Si consigues", "Si das el paso de", "Si vences la duda y puedes",
]


# ---- Segundo lote de vocabulario ------------------------------------------------------------
_EXT2 = {
    "Hoy": {
        "sit": _L("""
una racha de indecisión te hace girar en círculos
el ambiente está cargado de expectativas ajenas
una tarea rutinaria esconde un detalle delicado
el entusiasmo inicial se enfría a media mañana
un plan largamente soñado pide por fin un calendario
se te acumulan los mensajes por responder
una charla de pasillo cambia tu manera de ver un asunto
un hábito viejo intenta ganarte la partida
"""),
        "light": _L("""
el viento cambia de dirección y sopla a tu favor
la jornada cierra con un aplauso discreto
un detalle insignificante resulta ser la clave
la recompensa asoma por la puerta de atrás
todo vuelve a su cauce con sorprendente facilidad
alguien inesperado aparece con la solución
recuperas el hilo y el entusiasmo
una sonrisa ajena te contagia el buen ánimo
"""),
        "eff": _L("""
dividir el día en pequeños tramos alcanzables
decidir con la almohada lo que no urge
separar el ruido de lo esencial
bajar las expectativas para disfrutar del camino
rescatar lo útil de una mala idea
agradecer una ayuda antes de pedir otra
"""),
    },
    "Amor": {
        "sit": _L("""
un mensaje sin responder pesa más de lo debido
la ternura asoma en lo cotidiano, aunque pase inadvertida
una conversación a medias se queda flotando en el aire
te intimida la idea de mostrarte vulnerable
alguien cercano necesita tu oído más que tu consejo
una broma mal interpretada enfría el ambiente
las fotos de otros tiempos remueven tu sensibilidad
hay una invitación a la que no sabes qué responder
"""),
        "light": _L("""
un malentendido se disuelve entre carcajadas
la mesa compartida se llena de afecto
se te acerca alguien con la sonrisa que esperabas
el diálogo fluye como un río manso
un reproche se convierte en una caricia verbal
recibes una muestra de cariño en el momento exacto
se renueva la complicidad con quien camina a tu lado
un gesto amable abre un capítulo luminoso
"""),
        "eff": _L("""
tomar aire antes de responder a un reproche
dar crédito a las buenas intenciones
mirar el lado tierno de una discusión
dar a cada afecto el tiempo que merece
decir gracias sin letra pequeña
transformar un reclamo en una petición clara
"""),
    },
    "Riqueza": {
        "sit": _L("""
una factura inesperada altera tu balance mensual
se acerca la fecha de entrega de un trabajo clave
alguien con quien trabajas cambia las condiciones pactadas
las cifras no terminan de cuadrar
tu ambición choca con una norma rígida
un cambio de puesto se insinúa en el aire
te llega una propuesta de negocio poco convencional
los plazos se estrechan y las dudas se agrandan
"""),
        "light": _L("""
una transferencia o un premio te sonríe
una cifra clave se corrige a tu favor
se abre un cupo que parecía agotado
quien dirige reconoce tu labor
el balance del mes sorprende gratamente
alguien valora tu criterio con una oferta concreta
una colaboración da frutos antes de lo previsto
tus ahorros crecen con una pequeña sorpresa
"""),
        "eff": _L("""
cuidar la letra chica de cada trato
cultivar la paciencia del sembrador
revisar tu ruta de ingresos con lápiz en mano
evitar prometer plazos imposibles
dar un paso atrás para ver el mapa completo
cerrar tratos solo cuando estés conforme
"""),
    },
    "Bienestar": {
        "sit": _L("""
las piernas piden caminar y la agenda lo impide
el estómago te avisa que algo no te cae bien
una contractura te recuerda que existes
el ruido del entorno te agota los sentidos
hay más café que agua en tu rutina
duermes poco y sueñas demasiado
un cansancio sordo se esconde tras tu sonrisa
tu postura delata las horas frente a la pantalla
"""),
        "light": _L("""
el agua fresca te devuelve la claridad
el cuerpo agradece el descanso con una ráfaga de energía
el sol de la tarde te abraza
una infusión caliente cierra el día con dulzura
tu espalda se relaja y la tensión se disipa
el silencio te regala un instante de paz profunda
una carcajada libera lo que la tensión guardaba
la ligereza vuelve a tus pasos
"""),
        "eff": _L("""
hidratarte aunque no tengas sed
estirar la espalda sin apuro
cerrar los ojos un minuto cada tarde
salir a que te dé el aire antes de decidir
caminar de forma consciente unos minutos
respetar tu horario de sueño aunque tengas planes
"""),
    },
}
for _cat, _d in _EXT2.items():
    for _k, _v in _d.items():
        CONTENT[_cat][_k] += _v
for _cat, _lists in CONTENT.items():
    for _k, _v in _lists.items():
        assert len(_v) == len(set(_v)), (_cat, _k)
