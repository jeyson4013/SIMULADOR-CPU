import time

class ProcesoSIGET:
    def __init__(self, pid, tiempo_irrupcion, prioridad_alerta, tamano_datos):
        self.pid = pid
        self.tiempo_irrupcion = tiempo_irrupcion
        self.tiempo_restante = tiempo_irrupcion
        self.prioridad_alerta = prioridad_alerta
        self.tamano_datos = tamano_datos
        # Estados: Nuevo, Listo, En ejecución, Bloqueado, Terminado
        self.estado = "Nuevo"
        print(f"[{self.pid}] Creado con {self.tamano_datos} de datos. Estado: {self.estado}")

    def cambiar_estado(self, nuevo_estado):
        self.estado = nuevo_estado
        print(f"[{self.pid}] Transición a estado: {self.estado}")

def planificacion_prioridad(procesos):
    print("\n--- INICIANDO PLANIFICACIÓN POR PRIORIDAD (Emergencias SIGET) ---")
    # Cambiar de Nuevo a Listo
    for p in procesos:
        p.cambiar_estado("Listo")
        
    # Ordenar procesos por prioridad (menor número = mayor prioridad)
    procesos_ordenados = sorted(procesos, key=lambda x: x.prioridad_alerta)
    
    for p in procesos_ordenados:
        p.cambiar_estado("En ejecución")
        # Simulación de un bloqueo fortuito
        if p.tamano_datos > 50:
            p.cambiar_estado("Bloqueado")
            time.sleep(1) # Simulando tiempo de espera de I/O
            print(f"[{p.pid}] Resolución de bloqueo completada.")
            p.cambiar_estado("Listo")
            p.cambiar_estado("En ejecución")
            
        # Simular ejecución completa
        time.sleep(p.tiempo_irrupcion * 0.1) 
        p.tiempo_restante = 0
        p.cambiar_estado("Terminado")

def planificacion_round_robin(procesos, quantum):
    print(f"\n--- INICIANDO PLANIFICACIÓN ROUND-ROBIN (Datos de rutina) | Quantum: {quantum} ---")
    # Restaurar procesos para la segunda simulación
    for p in procesos:
        p.tiempo_restante = p.tiempo_irrupcion
        p.estado = "Nuevo"
        p.cambiar_estado("Listo")

    cola = procesos.copy()
    
    while cola:
        p = cola.pop(0)
        if p.tiempo_restante > 0:
            p.cambiar_estado("En ejecución")
            
            # Ejecutar por un quantum de tiempo
            tiempo_ejecucion = min(p.tiempo_restante, quantum)
            time.sleep(tiempo_ejecucion * 0.1)
            p.tiempo_restante -= tiempo_ejecucion
            
            if p.tiempo_restante > 0:
                print(f"[{p.pid}] Quantum agotado. Tiempo restante: {p.tiempo_restante}")
                p.cambiar_estado("Listo")
                cola.append(p) # Vuelve al final de la cola
            else:
                p.cambiar_estado("Terminado")

# --- BLOQUE PRINCIPAL DE EJECUCIÓN ---
if __name__ == "__main__":
    # Creación de al menos tres procesos con características variadas
    procesos_siget = [
        ProcesoSIGET(pid="P1_Rutina", tiempo_irrupcion=8, prioridad_alerta=3, tamano_datos=30),
        ProcesoSIGET(pid="P2_Emergencia", tiempo_irrupcion=4, prioridad_alerta=1, tamano_datos=20),
        ProcesoSIGET(pid="P3_CargaPesada", tiempo_irrupcion=10, prioridad_alerta=2, tamano_datos=80)
    ]

    # Ejecución de los dos algoritmos de planificación
    planificacion_prioridad(procesos_siget)
    planificacion_round_robin(procesos_siget, quantum=3)
