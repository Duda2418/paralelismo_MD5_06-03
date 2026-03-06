import hashlib
import time
import threading
from multiprocessing import Process, Manager

HASH_ALVO = "ca6ae33116b93e57b87810a27296fc36"
TOTAL = 10**9

# --- EXECUÇÃO COM THREADS ---
encontrado_threads = False
senha_encontrada_threads = None
lock_threads = threading.Lock()

def worker_thread(inicio, fim):
    global encontrado_threads, senha_encontrada_threads
    for i in range(inicio, fim):
        if encontrado_threads:
            return
        tentativa = f"{i:09d}"
        hash_md5 = hashlib.md5(tentativa.encode()).hexdigest()
        if hash_md5 == HASH_ALVO:
            with lock_threads:
                encontrado_threads = True
                senha_encontrada_threads = tentativa
            return

def executar_threads(num_threads):
    global encontrado_threads, senha_encontrada_threads
    encontrado_threads = False
    senha_encontrada_threads = None
    print(f"\n===== EXECUÇÃO COM {num_threads} THREADS =====")
    inicio = time.time()
    threads = []
    bloco = TOTAL // num_threads
    for i in range(num_threads):
        inicio_intervalo = i * bloco
        fim_intervalo = TOTAL if i == num_threads - 1 else (i + 1) * bloco
        t = threading.Thread(target=worker_thread, args=(inicio_intervalo, fim_intervalo))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    fim = time.time()
    print(f"Senha encontrada ({num_threads} threads):", senha_encontrada_threads)
    print("Tempo:", fim - inicio, "segundos")
    return fim - inicio

# --- EXECUÇÃO COM PROCESSOS ---
def worker_process(inicio, fim, encontrado, senha_encontrada):
    for i in range(inicio, fim):
        if encontrado.value:
            return
        tentativa = f"{i:09d}"
        hash_md5 = hashlib.md5(tentativa.encode()).hexdigest()
        if hash_md5 == HASH_ALVO:
            senha_encontrada.value = tentativa
            encontrado.value = True
            return

def executar_processos(num_processos):
    print(f"\n===== EXECUÇÃO COM {num_processos} PROCESSOS =====")
    inicio = time.time()
    manager = Manager()
    encontrado = manager.Value('b', False)
    senha_encontrada = manager.Value('s', "")
    processos = []
    bloco = TOTAL // num_processos
    for i in range(num_processos):
        inicio_intervalo = i * bloco
        fim_intervalo = TOTAL if i == num_processos - 1 else (i + 1) * bloco
        p = Process(target=worker_process, args=(inicio_intervalo, fim_intervalo, encontrado, senha_encontrada))
        processos.append(p)
        p.start()
    for p in processos:
        p.join()
    fim = time.time()
    print(f"Senha encontrada ({num_processos} processos):", senha_encontrada.value)
    print("Tempo:", fim - inicio, "segundos")
    return fim - inicio

# --- EXECUÇÃO SERIAL ---
def executar_serial():
    print("\n===== EXECUÇÃO SERIAL =====")
    inicio = time.time()
    senha = None
    for i in range(TOTAL):
        tentativa = f"{i:09d}"
        hash_md5 = hashlib.md5(tentativa.encode()).hexdigest()
        if hash_md5 == HASH_ALVO:
            senha = tentativa
            break
    fim = time.time()
    print("Senha encontrada (serial):", senha)
    print("Tempo serial:", fim - inicio, "segundos")
    return fim - inicio

# --- MAIN ---
if __name__ == "__main__":
    print("Hash alvo:", HASH_ALVO)

    # Serial
    tempo_serial = executar_serial()

    # Threads
    tempo_2_threads = executar_threads(2)
    tempo_4_threads = executar_threads(4)
    tempo_8_threads = executar_threads(8)
    tempo_12_threads = executar_threads(12)

    # Processos
    tempo_2_proc = executar_processos(2)
    tempo_4_proc = executar_processos(4)
    tempo_8_proc = executar_processos(8)
    tempo_12_proc = executar_processos(12)

    print("\n===== SPEEDUP THREADS =====")
    print("2 threads:", tempo_serial / tempo_2_threads)
    print("4 threads:", tempo_serial / tempo_4_threads)
    print("8 threads:", tempo_serial / tempo_8_threads)
    print("12 threads:", tempo_serial / tempo_12_threads)

    print("\n===== SPEEDUP PROCESSOS =====")
    print("2 processos:", tempo_serial / tempo_2_proc)
    print("4 processos:", tempo_serial / tempo_4_proc)
    print("8 processos:", tempo_serial / tempo_8_proc)
    print("12 processos:", tempo_serial / tempo_12_proc)