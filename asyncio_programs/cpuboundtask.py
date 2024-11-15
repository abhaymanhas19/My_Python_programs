import hashlib
import os
import string
import time
import random
import asyncio
from concurrent.futures import ThreadPoolExecutor
def random_password(length: int) -> bytes:
    ascii_lowercase = string.ascii_lowercase.encode()
    return b''.join(bytes(random.choice(ascii_lowercase)) for _ in range(length))
    
passwords = [random_password(10) for _ in range(10000)]
def hash(password: bytes) -> str:
    salt = os.urandom(16)
    return str(hashlib.scrypt(password, salt=salt, n=2048, p=1, r=8))
start = time.time()

def main():
    end = time.time()
    # loop = asyncio.get_running_loop()
    # tasks = []
    with ThreadPoolExecutor() as pool:
        results=pool.map(hash,passwords)
        futures = [pool.submit(hash,password)  for password in passwords]
        for future in futures:
            future.result()
        # for password in passwords:
            # tasks.append(loop.run_in_executor(pool,hash,password))
            
        # await asyncio.gather(*tasks)
    end = time.time()
    print(end - start)
        
# for password in passwords:
#     hash(password)
# end = time.time()
# print(end - start)
# asyncio.run(main())
main()