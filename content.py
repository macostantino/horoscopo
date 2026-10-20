"""Gramática de frases del motor de horóscopos.

Cada pronóstico se compone de oraciones armadas con piezas intercambiables
(todas en segunda persona y sin marcas de género):
  s1 = situación del día        -> "{lead}, {sujeto} {verbo} {complemento}."
  s2 = esfuerzo / dificultad    -> "{prefijo}{forma} {esfuerzo}{cola}."
  s3 = luz / resolución         -> "{tiempo}, {sujeto} {verbo} {complemento}."
  s4 = cierre opcional          -> de la categoría o propio del signo.
La "cabeza" de cada oración (complemento, esfuerzo, objeto) se reparte en ciclo
para que no se repita dentro del mismo signo y mes.
"""

SIGNS = [
    "ARIES", "TAURO", "GÉMINIS", "CÁNCER", "LEO", "VIRGO",
    "LIBRA", "ESCORPIO", "SAGITARIO", "CAPRICORNIO", "ACUARIO", "PISCIS",
]
CATEGORIES = ["Hoy", "Amor", "Riqueza", "Bienestar"]

# ---- Piezas comunes -------------------------------------------------------
S1_LEADS = [
    "Hoy", "Desde temprano", "Durante esta jornada", "A lo largo del día",
    "En las próximas horas", "Al comenzar la jornada", "Hacia el mediodía",
    "Con el correr de las horas", "En este día", "Por la mañana",
]
S1_VERBS = ["te invita a", "te ayuda a", "te impulsa a", "te anima a", "te prepara para", "te da fuerza para"]

S2_FORMS = ["tendrás que", "será necesario", "te tocará", "habrá que", "conviene", "deberás"]
S2_PREFIXES = [
    "", "En algún momento, ", "Por la tarde, ", "Más de una vez, ", "Aunque cueste, ",
    "Si hace falta, ", "Llegado el caso, ", "Durante el día, ", "Más allá del cansancio, ", "Aunque dudes, ",
]
S2_TAILS = [
    "", " antes de seguir adelante", " aunque cueste al principio", " sin perder la calma",
    " aunque el camino sea lento", " sin rendirte a mitad de camino", " aunque no sea sencillo",
    " dando un paso a la vez", " con humildad y firmeza", " sin apresurarte",
    " y confiar en el proceso", " pensando en lo que viene",
]

S3_TIMES = [
    "Al final", "Finalmente", "Con el paso de las horas", "Hacia el atardecer",
    "Antes de que termine el día", "Más pronto de lo que crees", "Cuando menos lo esperes",
    "Poco a poco", "Al caer la tarde", "Tras el esfuerzo",
]
S3_VERBS = ["te regala", "te trae", "te deja", "se convierte en", "da paso a", "te acerca a"]

S4_VERBS = ["Cuida", "Valora", "Celebra", "Agradece", "Aprovecha", "Honra", "Disfruta", "Protege", "Reconoce"]
S4_TAILS = [
    "", " hoy mismo", " con calma", " sin culpa", " con gratitud", " de corazón",
    " a tu manera", " sin prisa", " cada vez que puedas", " durante todo el día",
    " con todo tu ser", " en cada momento",
]

# ---- Piezas por categoría -------------------------------------------------
CONTENT = {
    "Hoy": {
        "s1_subj": [
            "tu energía", "tu intuición", "tu entorno", "tu capacidad de decisión",
            "tu manera de ver las cosas", "tu determinación", "tu creatividad", "tu rutina",
            "tu estado de ánimo", "tu mente", "tu espíritu", "tu confianza",
        ],
        "s1_comp": [
            "empezar algo nuevo", "ordenar lo pendiente", "ver las cosas con otros ojos",
            "avanzar con paso firme", "tomar decisiones con claridad", "retomar un proyecto olvidado",
            "aprovechar las oportunidades que llegan", "confiar en tu propio criterio",
            "dar el primer paso sin miedo", "disfrutar de los pequeños logros",
            "escuchar lo que realmente importa", "mirar el futuro con optimismo",
            "abrirte a nuevas ideas", "poner en marcha lo que soñaste", "cuidar lo que más valoras",
            "cerrar un ciclo que ya cumplió su función", "probar un camino distinto",
            "valorar lo que ya has conseguido", "hablar con claridad de lo que necesitas",
            "cuidar tu tiempo con más conciencia", "animarte a pedir lo que mereces",
            "enfrentar un pendiente sin demora", "apoyarte en quienes confían en ti",
            "mantener la calma cuando todo se acelera", "celebrar un avance que pasó inadvertido",
            "crear algo con tus propias manos", "dejar que la intuición te oriente",
            "terminar lo que empezaste", "descubrir un talento olvidado",
            "construir una rutina que te haga bien", "compartir una buena idea",
            "apostar por lo que te entusiasma",
        ],
        "s2_effort": [
            "insistir un poco más de lo previsto", "hacer una pausa cuando aparezca la duda",
            "poner límites a lo que te quita energía", "dedicar tiempo a un pequeño obstáculo",
            "tomarte tu tiempo para decidir entre dos opciones", "tener una conversación incómoda pero necesaria",
            "ordenar prioridades", "enfrentar una situación pendiente", "sostener el ritmo ante la presión",
            "salir de tu zona de confort", "confiar en tus capacidades ante una dificultad",
            "armarte de paciencia con un asunto lento", "revisar lo que no te convence",
            "resistir la tentación de rendirte", "aceptar ayuda cuando la necesites", "atender un imprevisto",
            "dividir una tarea grande en partes pequeñas", "dejar de postergar lo importante",
            "reconocer un error y corregirlo", "decir no a lo que te distrae", "adaptarte a un cambio de planes",
            "perseverar cuando el avance se note poco", "evitar comparaciones que te desaniman",
            "terminar una tarea antes de empezar otra", "pedir una opinión sincera",
            "soltar el control de algo que no depende de ti", "cuidar tus energías durante la tarde",
            "preparar mejor el siguiente paso", "buscar una solución distinta a la de siempre",
            "atender un detalle que habías pasado por alto", "esperar el momento justo sin desesperar",
            "sostener tu decisión frente a las dudas",
        ],
        "s3_subj": [
            "tu esfuerzo", "tu perseverancia", "tu constancia", "tu paciencia", "tu valentía", "tu dedicación",
            "tu confianza", "tu actitud positiva", "tu determinación", "tu capacidad de adaptación",
            "tu insistencia", "tu serenidad",
        ],
        "s3_comp": [
            "una grata sorpresa", "un momento de calma y alegría", "una sensación de logro", "una buena noticia",
            "la serenidad que buscabas", "una oportunidad inesperada", "nuevas ganas de seguir",
            "un resultado mejor del esperado", "la confianza que necesitabas", "un aprendizaje valioso",
            "una sonrisa sincera", "una puerta que parecía cerrada", "un orgullo merecido",
            "un respiro muy bien ganado", "una claridad nueva", "una alegría que no esperabas",
            "el reconocimiento de alguien cercano", "una tarde luminosa", "un comienzo prometedor",
            "la satisfacción de haber dado lo mejor", "una fuerza renovada", "un final feliz para la jornada",
            "un cambio que veías lejos", "la prueba de que eres capaz", "un alivio que se siente en el pecho",
            "una razón más para creer en ti", "un día que vale la pena recordar", "una paz que te acompaña",
            "nuevas posibilidades a tu alcance", "el broche de oro que esperabas", "un empujón de optimismo",
            "una victoria pequeña pero valiosa",
        ],
        "s4_obj": [
            "cada pequeño avance", "tu ritmo", "lo que ya tienes", "tu descanso de esta noche",
            "los gestos amables", "los pequeños logros", "tu energía", "tu intuición", "tu fortaleza",
            "el apoyo de los tuyos", "la calma que llega", "tus ganas de seguir", "tu tiempo",
            "lo que ya has logrado", "tus ideas", "cada oportunidad", "tu capacidad de empezar de nuevo",
            "los buenos momentos", "tu optimismo", "tu manera de ser",
        ],
    },
    "Amor": {
        "s1_subj": [
            "tu corazón", "tu vida afectiva", "tu forma de querer", "tu sensibilidad", "tu ternura",
            "tu sinceridad", "tu magnetismo personal", "tu manera de escuchar", "tu calidez",
            "tu generosidad", "tu intuición emocional", "tu mundo interior",
        ],
        "s1_comp": [
            "abrir tu corazón sin miedo", "expresar lo que sientes", "compartir tiempo de calidad con quien quieres",
            "cuidar los pequeños detalles", "escuchar con atención a quienes te rodean",
            "reconectar con alguien especial", "mostrarte tal como eres", "dar y recibir cariño",
            "fortalecer un vínculo importante", "valorar a quienes suman en tu vida", "hablar con honestidad",
            "regalar una palabra amable", "acercarte a alguien que extrañas", "disfrutar de la compañía de los tuyos",
            "confiar en el cariño que recibes", "agradecer a quien siempre está", "romper el hielo con alguien",
            "planear algo lindo en compañía", "recordar por qué elegiste a quien quieres",
            "dedicar un mensaje afectuoso", "hacer las paces con un viejo conflicto", "dejarte sorprender por el amor",
            "cuidar a quienes te cuidan", "dar un abrazo que hacía falta", "mostrar interés genuino por los demás",
            "compartir una risa con alguien querido", "perdonar y seguir adelante",
            "celebrar lo que une a tu familia", "apreciar una amistad de años", "hablar desde el corazón",
            "tener paciencia con tus emociones", "construir confianza día a día",
        ],
        "s2_effort": [
            "aclarar un malentendido", "escuchar antes de responder", "dejar atrás un viejo resentimiento",
            "dar el primer paso para reparar una distancia", "tener una conversación pendiente",
            "ceder en algo pequeño", "pedir perdón si hace falta", "expresar lo que te cuesta decir",
            "poner límites con cariño", "equilibrar tus necesidades con las de otra persona",
            "aceptar que no todo depende de ti", "tender un puente después de un silencio",
            "respetar los tiempos de quien quieres", "soltar una expectativa que no se cumplió",
            "mostrar tu vulnerabilidad", "hablar con calma en un momento tenso", "reconocer un error propio",
            "perdonar sin guardar rencor", "dedicar más tiempo a quien lo necesita", "aprender a pedir ayuda",
            "tolerar una diferencia de opiniones", "cuidar el vínculo con constancia",
            "separar lo que sientes de lo que supones", "respirar antes de reaccionar",
            "entender que el cariño se construye de a poco", "dejar de postergar una charla importante",
            "revisar lo que esperas de una relación", "reconocer lo que te hace feliz",
            "dar espacio cuando hace falta", "animarte a decir lo que piensas",
            "no tomar como personal un mal momento", "recordar lo bueno cuando haya tensión",
        ],
        "s3_subj": [
            "tu sinceridad", "tu paciencia", "tu ternura", "tu gesto de cariño", "tu constancia", "tu valentía",
            "tu empatía", "tu generosidad", "tu disposición a escuchar", "tu esfuerzo por entender",
            "tu honestidad", "tu calidez",
        ],
        "s3_comp": [
            "un abrazo sincero", "una conversación llena de ternura", "un momento de complicidad",
            "una sonrisa que lo cambia todo", "una conexión más profunda", "una muestra de cariño inesperada",
            "la armonía que buscabas", "un mensaje que te alegra el día", "una etapa afectiva más serena",
            "un vínculo más fuerte", "una reconciliación sentida", "un instante para recordar",
            "la calma que tanto querías", "un detalle que te hace sentir especial", "una cercanía renovada",
            "un cariño que se multiplica", "una charla que sana", "un reencuentro emocionante",
            "una invitación inesperada", "un gesto que te llega al alma", "la certeza de que te quieren",
            "una ternura que te envuelve", "una mirada cómplice", "un perdón que alivia", "una promesa sincera",
            "una noche tranquila en buena compañía", "un cariño que nunca se fue", "una paz compartida",
            "una risa que contagia a todos", "un apoyo que te emociona", "una confianza que se renueva",
            "el calor de un hogar lleno de afecto",
        ],
        "s4_obj": [
            "cada gesto de cariño", "tu tiempo con quienes quieres", "los momentos de complicidad",
            "tu capacidad de perdonar", "el cariño que recibes", "tu corazón abierto", "las palabras sinceras",
            "la compañía de los tuyos", "lo que sientes", "los pequeños detalles", "la ternura que das",
            "tu sensibilidad", "el amor que te rodea", "una buena charla", "tu forma de querer",
            "las risas compartidas", "tu disposición a escuchar", "los abrazos sinceros",
            "la confianza que construyes", "el vínculo con quienes importan",
        ],
    },
    "Riqueza": {
        "s1_subj": [
            "tu capacidad de organización", "tu economía", "tu trabajo", "tu creatividad profesional",
            "tu perseverancia", "tu criterio para los negocios", "tu red de contactos", "tu talento",
            "tu visión a largo plazo", "tu disciplina", "tu iniciativa", "tu preparación",
        ],
        "s1_comp": [
            "avanzar en un proyecto postergado", "cerrar un acuerdo favorable", "ordenar tus finanzas",
            "aprovechar una oportunidad profesional", "proponer una idea que destaque", "negociar con claridad",
            "planificar con inteligencia", "revisar tus gastos con calma", "mostrar lo que sabes hacer",
            "colaborar con un buen equipo", "tomar decisiones económicas seguras",
            "empezar un proyecto que te entusiasma", "fortalecer tu estabilidad", "dar un paso hacia tus metas",
            "ganar la confianza de quienes deciden", "ampliar tus conocimientos profesionales",
            "ahorrar con un objetivo claro", "delegar lo que no es tu fuerte", "mejorar un proceso de tu trabajo",
            "explorar una fuente de ingresos distinta", "pedir un reconocimiento que mereces",
            "presentar una propuesta bien pensada", "construir una relación laboral de confianza",
            "cumplir una meta que te propusiste", "tomar la iniciativa en un equipo", "poner en orden tu papeleo",
            "pensar en inversiones prudentes", "formarte en algo que te apasiona",
            "resolver un asunto financiero pendiente", "consolidar lo que ya funciona",
            "ganar visibilidad con tu trabajo", "cerrar el día con tareas completas",
        ],
        "s2_effort": [
            "revisar cada detalle antes de comprometerte", "resistir la tentación de gastar sin necesidad",
            "cumplir con un plazo ajustado", "rehacer una parte del trabajo", "adaptarte a un cambio de planes",
            "defender tus ideas con argumentos sólidos", "replantear prioridades tras un gasto inesperado",
            "asumir una responsabilidad extra", "sostener un proyecto exigente",
            "mantener la serenidad en una negociación lenta", "aprender de un pequeño tropiezo",
            "dosificar tus fuerzas", "gestionar un trámite que se demora", "poner orden en tus cuentas",
            "decir que no a un compromiso que no te conviene", "pedir una segunda opinión",
            "estudiar mejor una propuesta", "ahorrar un poco más de lo habitual", "organizar mejor tu tiempo",
            "enfrentar una tarea que venías postergando", "cuidar tu reputación profesional",
            "tener una conversación difícil con un colega", "ser constante aunque los resultados tarden",
            "controlar los impulsos a la hora de comprar", "prepararte mejor para una reunión",
            "resolver un problema antes de que crezca", "priorizar lo importante sobre lo urgente",
            "pedir lo que consideras justo", "mantener la disciplina en tus metas",
            "tener paciencia con los resultados", "comparar opciones antes de gastar",
            "no comprometerte con más de lo que puedes abarcar",
        ],
        "s3_subj": [
            "tu constancia", "tu dedicación", "tu esfuerzo", "tu perseverancia", "tu prudencia", "tu preparación",
            "tu disciplina", "tu iniciativa", "tu trabajo bien hecho", "tu capacidad de adaptación", "tu visión",
            "tu compromiso",
        ],
        "s3_comp": [
            "un reconocimiento merecido", "una oportunidad económica prometedora", "una buena noticia laboral",
            "un resultado mejor del esperado", "una propuesta interesante", "un acuerdo favorable",
            "una base firme para crecer", "la tranquilidad que buscabas", "un avance concreto",
            "un ingreso que alivia", "nuevas puertas profesionales", "una sensación de progreso real",
            "un logro que celebrar", "una recompensa que llevabas tiempo esperando",
            "la confianza de quienes te rodean", "un futuro más estable", "una nueva fuente de ingresos",
            "un respaldo que no esperabas", "un aumento en tu seguridad económica", "una oportunidad de crecer",
            "una alianza provechosa", "un proyecto que despega", "la valoración de tu equipo",
            "un balance más favorable", "una puerta abierta en el trabajo", "un salto de calidad en lo que haces",
            "una etapa de abundancia", "un pago que llega a tiempo", "un plan que da frutos", "una meta cumplida",
            "una idea que se convierte en proyecto", "un respiro en tus cuentas",
        ],
        "s4_obj": [
            "tu esfuerzo diario", "cada pequeño avance", "tu preparación", "los buenos contactos",
            "tu tiempo de trabajo", "lo que ya has logrado", "tus ahorros", "tu reputación",
            "las oportunidades que llegan", "tu constancia", "tus ideas", "la estabilidad que construyes",
            "tu criterio", "el apoyo de tu equipo", "tus metas", "los frutos de tu trabajo",
            "tu capacidad de aprender", "los acuerdos justos", "tu prosperidad", "las decisiones prudentes",
        ],
    },
    "Bienestar": {
        "s1_subj": [
            "tu cuerpo", "tu mente", "tu energía vital", "tu estado de ánimo", "tu sensibilidad", "tu espíritu",
            "tu respiración", "tu descanso", "tu equilibrio interior", "tu vitalidad", "tu serenidad", "tu intuición",
        ],
        "s1_comp": [
            "bajar el ritmo y disfrutar del presente", "renovar un buen hábito", "salir a caminar al aire libre",
            "reconectar con lo que te da calma", "dormir y alimentarte mejor", "escuchar las señales de tu cuerpo",
            "dedicarte un momento para ti", "soltar una preocupación", "respirar con calma", "aprender algo nuevo",
            "moverte un poco más", "rodearte de lo que te hace bien", "cuidar tu descanso", "practicar la gratitud",
            "encontrar equilibrio entre descanso y acción", "dormir mejor esta noche", "hidratarte con más atención",
            "estirar el cuerpo con suavidad", "observar tus pensamientos sin juzgarlos",
            "apagar el ruido y escuchar tu interior", "comer con más conciencia", "reír con ganas",
            "salir de la rutina por un rato", "tomar sol y aire fresco", "ordenar tu espacio y tu mente",
            "meditar unos minutos", "poner música que te levante el ánimo", "bailar o moverte sin pensar",
            "cultivar pensamientos amables", "dejar el celular un rato", "disfrutar de una comida tranquila",
            "conectar con la naturaleza",
        ],
        "s2_effort": [
            "mantener la constancia en una rutina saludable", "reconocer el cansancio acumulado",
            "decir no para proteger tu tranquilidad", "respirar con calma en momentos de tensión",
            "dormir y alimentarte con más cuidado", "soltar una preocupación poco a poco",
            "vencer la pereza del primer paso", "confiar en tu fuerza aunque dudes", "cambiar un viejo hábito",
            "gestionar el estrés con pequeños gestos", "detenerte a recuperar fuerzas",
            "reconocer una emoción intensa", "escuchar a tu cuerpo aunque prefieras seguir",
            "sostener la confianza en un momento de inquietud", "desconectarte un rato de las pantallas",
            "hidratarte y moverte más", "poner orden en tus horarios de descanso", "pedir ayuda cuando todo pesa",
            "aceptar que no puedes con todo", "reservar tiempo para ti", "evitar la autoexigencia excesiva",
            "enfrentar un miedo pequeño", "dejar de postergar un chequeo médico", "moderar el ritmo de trabajo",
            "alejarte de lo que te agota", "mantener una rutina de ejercicio",
            "practicar la calma cuando algo te altera", "aprender a decir basta a tiempo", "cuidar tus pensamientos",
            "perdonarte un error", "no abandonar tu rutina un día difícil", "darte permiso para descansar",
        ],
        "s3_subj": [
            "tu constancia", "tu serenidad", "tu autocuidado", "tu paciencia", "tu confianza",
            "tu respiración tranquila", "tu decisión de cuidarte", "tu descanso", "tu perseverancia",
            "tu actitud positiva", "tu calma", "tu gratitud",
        ],
        "s3_comp": [
            "una renovada ligereza", "una sonrisa genuina", "una energía que se contagia", "un descanso reparador",
            "un instante de claridad", "la paz que buscabas", "una vitalidad inesperada", "un ánimo más luminoso",
            "una sensación de equilibrio", "una alegría tranquila", "una fuerza interior renovada",
            "un bienestar que se nota", "una noche de sueño profundo", "la calma que necesitabas",
            "un cuerpo más liviano", "un momento de verdadera armonía", "un cuerpo agradecido", "una mente despejada",
            "un suspiro de alivio", "una energía que vuelve", "una mañana renovada", "un corazón en paz",
            "una calma profunda", "una risa que libera", "una sensación de hogar en ti",
            "una confianza más firme en tu cuerpo", "un equilibrio que se sostiene", "una paz que se queda",
            "un amanecer más liviano", "un ánimo que se levanta", "una armonía entre mente y cuerpo",
            "un respiro que renueva",
        ],
        "s4_obj": [
            "tu descanso", "tu respiración", "los momentos de calma", "tu cuerpo", "tu energía",
            "los paseos al aire libre", "tu tranquilidad", "un buen sueño", "tus rutinas sanas", "tu equilibrio",
            "las pausas a tiempo", "tu salud", "tu paz interior", "los hábitos que te hacen bien",
            "la alegría sencilla", "tu mente en calma", "el silencio que te repara", "tu ánimo",
            "el tiempo para ti", "la compañía que te hace bien",
        ],
    },
}

# ---- Cierres propios de cada signo ---------------------------------------
SIGN_LEADS = ["Hoy", "Hoy más que nunca", "Esta vez", "Ahora", "En este momento", "Sin duda", "Como siempre", "Una vez más"]
SIGN_PREDICATES = [
    "abre caminos donde otros dudan", "marca la diferencia", "inspira a quienes te rodean",
    "ilumina cada paso que das", "te lleva más lejos de lo que imaginas", "te acompaña como una fuerza silenciosa",
    "te guía con acierto", "atrae buenas noticias", "contagia entusiasmo a tu entorno",
    "transforma los obstáculos en oportunidades", "te regala confianza", "despierta lo mejor de ti",
    "siembra buenos resultados", "te sostiene cuando todo se mueve", "hace brillar lo que tocas",
    "te abre puertas inesperadas", "convierte lo difícil en aprendizaje", "trae calma a quienes te rodean",
]
SIGN_SUBJECTS = {
    "ARIES": ["tu espíritu de Aries", "tu iniciativa ariana", "tu determinación", "tu energía pionera",
              "tu impulso de fuego", "tu coraje", "tu liderazgo natural", "tu entusiasmo ariano"],
    "TAURO": ["tu paciencia taurina", "tu constancia de Tauro", "tu serenidad de tierra", "tu firmeza",
              "tu lealtad", "tu gusto por lo bello", "tu perseverancia", "tu sentido práctico taurino"],
    "GÉMINIS": ["tu curiosidad geminiana", "tu ingenio de Géminis", "tu facilidad para comunicar", "tu mente ágil",
                "tu versatilidad", "tu chispa", "tu don de la palabra", "tu adaptabilidad geminiana"],
    "CÁNCER": ["tu sensibilidad canceriana", "tu intuición de Cáncer", "tu ternura", "tu empatía",
               "tu memoria del corazón", "tu capacidad de cuidar", "tu instinto protector", "tu mundo emocional de Cáncer"],
    "LEO": ["tu brillo de Leo", "tu generosidad leonina", "tu corazón de león", "tu carisma",
            "tu liderazgo", "tu nobleza", "tu alegría contagiosa", "tu confianza leonina"],
    "VIRGO": ["tu mirada atenta de Virgo", "tu dedicación al detalle", "tu espíritu servicial", "tu mente analítica",
              "tu practicidad virginiana", "tu humildad", "tu afán de mejora", "tu criterio de Virgo"],
    "LIBRA": ["tu sentido del equilibrio libriano", "tu diplomacia", "tu encanto de Libra", "tu amabilidad",
              "tu gusto por la armonía", "tu mirada justa", "tu elegancia natural", "tu capacidad de conciliar"],
    "ESCORPIO": ["tu intensidad escorpiana", "tu fuerza de renacer", "tu intuición profunda", "tu pasión",
                 "tu resiliencia", "tu mirada penetrante", "tu lealtad de Escorpio", "tu magnetismo escorpiano"],
    "SAGITARIO": ["tu optimismo sagitariano", "tu espíritu aventurero", "tu fe en el futuro", "tu sinceridad",
                  "tu sed de aprender", "tu entusiasmo de Sagitario", "tu visión amplia", "tu energía viajera"],
    "CAPRICORNIO": ["tu disciplina capricorniana", "tu constancia de Capricornio", "tu sentido del deber", "tu ambición",
                    "tu madurez", "tu paciencia de montaña", "tu responsabilidad", "tu determinación capricorniana"],
    "ACUARIO": ["tu originalidad acuariana", "tu espíritu libre", "tu visión de futuro", "tu mente inventiva",
                "tu generosidad humanitaria", "tu independencia", "tu creatividad de Acuario", "tu forma única de pensar"],
    "PISCIS": ["tu imaginación pisciana", "tu compasión", "tu sensibilidad de Piscis", "tu intuición",
               "tu creatividad fluida", "tu mundo interior", "tu capacidad de soñar", "tu empatía pisciana"],
}
