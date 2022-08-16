# PROYECTO SISTEMAS OPERATIVOS
# CICLO BÁSICO DE INSTRUCCIÓN
# AGOSTO 2022
# ----------------------------
# HECHO POR:
# ALESSANDRO DIAZ GARCIA 1940983
# JUAN MANUEL CASTILLO 1941563
# ALEJANDRO MARROQUIN 1942529

# Capacidad de memoria de 5000 posiciones
memoria_principal = []
for x in range(5000):
    memoria_principal.append(0)

# Contador de Programa
pc = None
# Registro de Control de Instrucciones
icr = None
# Registro de Acceso a Memoria
mar = None
# Registro de Datos de Memoria
mdr = None

unidad_control = None
acumulador = None
alu = None


def status():
    print("--------\nPC:", pc, " ICR:", icr, "\nMAR:", mar, " MDR:", mdr, "\nUC:", unidad_control, "\nAC:",
          acumulador,
          " ALU:", alu)


def leer_instruccion():
    with open('entrada.txt') as f:
        lines = f.readlines()

    global pc
    pc = 4000  # Valor del PC predefinido
    i = 4000
    # Las instrucciones se alojan en la memoria principal desde la dirección 4000
    for x in lines:
        memoria_principal[i] = x
        i = i + 1
    do_pc()


# FETCH STAGE
# Tiene cargada dirección de la siguiente instrucción,
# Le pasa el contenido al MAR
def do_pc():
    global mar
    mar = pc
    do_mar()


# Contiene la dirección de RAM en la que desea leer o escribir
def do_mar():
    global mdr, pc
    i = pc + 1
    if memoria_principal[i] != 0:
        pc = pc + 1

    if unidad_control is not None:
        if unidad_control.split()[0] == "LDR":
            mdr = memoria_principal[mar]
            do_mdr()
        else:
            mdr = memoria_principal[mar]
            do_mdr()
    else:
        mdr = memoria_principal[mar]
        do_mdr()
        do_icr()


# Contiene los datos que ha leído de la RAM o desea escribir en la RAM
def do_mdr():
    global icr
    icr = mdr
    do_icr()


# Tiene la última instrucción obtenida
def do_icr():
    global unidad_control
    unidad_control = icr

    do_uc()


# LDR: Toma el valor en D y lo pone en el acumulador
def do_ldr():
    global mar, mdr, acumulador
    mar = extraer_direccion(unidad_control.split()[1])
    mdr = memoria_principal[mar]
    acumulador = mdr

    do_pc()


# ADD, SUB, DIV, MUL, BEQ
# ADD D1 NULL NULL,
# Suma el valor de D1 al valor cargado en el acumulador.
# ADD D1 D3 NULL
# Carga el valor de D1 en el acumulador y lo suma con el valor en D3
# ADD D1 D3 D4
# Igual al anterior, pero pone el resultado en D4
def do_operation():
    global alu, mar, mdr, acumulador

    if unidad_control.split()[3] != "NULL":
        acumulador = memoria_principal[int(extraer_direccion(unidad_control.split()[1]))]
        alu = acumulador
        mar = extraer_direccion(unidad_control.split()[2])
        mdr = memoria_principal[int(mar)]
        acumulador = mdr
    elif unidad_control.split()[2] != "NULL":
        acumulador = memoria_principal[int(extraer_direccion(unidad_control.split()[1]))]
        alu = acumulador
        mar = extraer_direccion(unidad_control.split()[2])
        mdr = memoria_principal[int(mar)]
        acumulador = mdr
    else:
        alu = acumulador
        mar = extraer_direccion(unidad_control.split()[1])
        mdr = memoria_principal[int(mar)]
        acumulador = mdr

    if unidad_control.split()[0] == "ADD":
        alu = acumulador + alu
    # SUB: Resta el valor en D al valor cargado en el acumulador
    # Similar a ADD pero resta
    elif unidad_control.split()[0] == "SUB" or unidad_control.split()[0] == "BEQ":
        alu = acumulador - alu
    elif unidad_control.split()[0] == "MUL":
        alu = acumulador * alu
    elif unidad_control.split()[0] == "DIV":
        alu = acumulador / alu

    acumulador = alu
    if unidad_control.split()[0] == "BEQ":
        if acumulador == 0:
            if unidad_control.split()[3] != "NULL":
                memoria_principal[int(extraer_direccion(unidad_control.split()[3]))] = acumulador
            elif unidad_control.split()[2] != "NULL":
                memoria_principal[int(extraer_direccion(unidad_control.split()[2]))] = acumulador
            elif unidad_control.split()[1] != "NULL":
                memoria_principal[int(extraer_direccion(unidad_control.split()[1]))] = acumulador
    elif unidad_control.split()[3] != "NULL":
        memoria_principal[int(extraer_direccion(unidad_control.split()[3]))] = alu

    alu = 0
    do_pc()


# INC: Incrementar en 1 el valor de D. INC D3 NULL NULL.
# DEC: Decrementar en 1 el valor de D. DEC D3 NULL NULL.
def do_inc_dec():
    global alu, mar, mdr, acumulador

    mar = extraer_direccion(unidad_control.split()[1])
    mdr = memoria_principal[int(mar)]
    acumulador = mdr

    if unidad_control.split()[0] == "INC":
        alu = acumulador + 1
    elif unidad_control.split()[0] == "DEC":
        alu = acumulador - 1

    acumulador = alu
    memoria_principal[int(extraer_direccion(unidad_control.split()[1]))] = acumulador


# Mover. Cargar el valor de D2 a D10 y limpiar D2. MOV D2 D10 NULL.
def do_mov():
    global mar, mdr
    mar = extraer_direccion(unidad_control.split()[1])
    mdr = memoria_principal[int(mar)]
    memoria_principal[int(mar)] = 0

    mar = extraer_direccion(unidad_control.split()[2])
    memoria_principal[int(mar)] = mdr


# STR: Lee lo que hay en el acumulador y lo guarda en la dirección D indicada
def do_str():
    global mar, mdr
    mar = extraer_direccion(unidad_control.split()[1])
    mdr = acumulador
    memoria_principal[mar] = mdr


def extraer_direccion(direccion):
    direccion_final = direccion.replace("D", "")
    return int(direccion_final)


# Muestra el valor en la dirección o registro indicado.
# SHW D2, SHW ACC, SHW ICR, SHW MAR, SHW MDR, SHW UC.
def do_shw():
    if unidad_control.split()[1] == "ACC":
        print(acumulador)
    elif unidad_control.split()[1] == "ICR":
        print(icr)
    elif unidad_control.split()[1] == "MAR":
        print(mar)
    elif unidad_control.split()[1] == "MDR":
        print(mdr)
    elif unidad_control.split()[1] == "UC":
        print(unidad_control)
    else:
        print(memoria_principal[extraer_direccion(unidad_control.split()[1])])


# DECODE STAGE
def do_uc():
    if type(unidad_control.split()[0]) == str:
        # EXECUTE STAGE
        if unidad_control.split()[0] == "SET":
            # SET: Guarda X en D
            memoria_principal[extraer_direccion(unidad_control.split()[1])] = int(unidad_control.split()[2])
        elif unidad_control.split()[0] == "LDR":
            do_ldr()
        elif unidad_control.split()[0] == "ADD":
            do_operation()
        elif unidad_control.split()[0] == "SUB":
            do_operation()
        elif unidad_control.split()[0] == "MUL":
            do_operation()
        elif unidad_control.split()[0] == "DIV":
            do_operation()
        elif unidad_control.split()[0] == "INC":
            do_inc_dec()
        elif unidad_control.split()[0] == "DEC":
            do_inc_dec()
        elif unidad_control.split()[0] == "MOV":
            do_mov()
        elif unidad_control.split()[0] == "BEQ":
            do_operation()
        elif unidad_control.split()[0] == "STR":
            do_str()
        elif unidad_control.split()[0] == "SHW":
            do_shw()
        elif unidad_control.split()[0] == "END":
            quit()

    do_pc()


(leer_instruccion())