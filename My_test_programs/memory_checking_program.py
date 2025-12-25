import psutil
def mem_mb():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)

def log_mem(label: str):
    print(f"[MEM] {label}: {mem_mb():.2f} MB")