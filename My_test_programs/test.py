d="<p><strong> Python® – the language of today and tomorrow</strong></p><p><br />Python is the gift that keeps on giving. The more you understand Python, the more you can do in the 21st Century. As simple as that.</p><h2>What</h2><p>Python is a widely-used, interpreted, object-oriented, and high-level programming language with dynamic semantics, used for general-purpose programming. It’s everywhere, and people use numerous Python-powered devices on a daily basis, whether they realize it or not.</p><h2>Who</h2><p>Python was created by <a href=\"https://gvanrossum.github.io/\" target=\"_blank\">Guido van Rossum</a>, and first released on February 20, 1991. While you may know the python as a large snake, the name of the Python programming language comes from an old BBC television comedy sketch series called <em>Monty Python’s Flying Circus</em>.</p><p>One of the amazing features of Python is the fact that it is actually one person’s work. Usually, new programming languages are developed and published by large companies employing lots of professionals, and due to copyright rules, it is very hard to name any of the people involved in the project. Python is an exception.</p><p>Of course, Guido van Rossum did not develop and evolve all the Python components himself. The speed with which Python has spread around the world is a result of the continuous work of thousands (very often anonymous) programmers, testers, users (many of them aren’t IT specialists) and enthusiasts, but it must be said that the very first idea (the seed from which Python sprouted) came to one head – Guido’s.</p><p>Python is maintained by the <a href=\"https://www.python.org/psf-landing/\" target=\"_blank\">Python Software Foundation</a>, a non-profit membership organization and a community devoted to developing, improving, expanding, and popularizing the Python language and its environment.</p><h2>Why</h2><p>Python is omnipresent, and people use numerous Python-powered devices on a daily basis, whether they realize it or not. There are billions of lines of code written in Python, which means almost unlimited opportunities for code reuse and learning from well-crafted examples. What’s more, there is a large and very active Python community, always happy to help.</p><p>There are also a couple of factors that make Python great for learning:</p><ul><li>It is easy to learn – the time needed to learn Python is shorter than for many other languages; this means that it’s possible to start the actual programming faster;</li><li>It is easy to use for writing new software – it’s often possible to write code faster when using Python;</li><li>It is easy to obtain, install and deploy – Python is free, open and multiplatform; not all languages can boast that.</li></ul><p>Programming skills prepare you for careers in almost any industry, and are required if you want to continue to more advanced and higher-paying software development and engineering roles. Python is the programming language that opens more doors than any other. With a solid knowledge of Python, you can work in a multitude of jobs and a multitude of industries. And the more you understand Python, the more you can do in the 21st Century. Even if you don’t need it for work, you will find it useful to know.</p><h2>Where</h2><p>Python is the programming language that opens more doors than any other. With a solid knowledge of Python, you can work in a multitude of jobs and a multitude of industries. And even if you don’t need it for work, you will still find it useful to know to speed certain things up or develop a deeper understanding of other concepts.</p><p>Python is a great choice for career paths related to software development, engineering, DevOps, machine learning, data analytics, web development, and testing. What's more, there are also many jobs outside the IT industry that use Python. Since our lives are becoming more computerized every day, and the computer and technology areas previously associated only with technically gifted people are now opening up to non-programmers, Python has become one of the must-have tools in the toolbox of educators, managers, data scientists, data analysts, economists, psychologists, artists, and even secretaries.</p><h2><strong>How</strong></h2><p><strong>Learn, certify, and succeed!</strong> How great would it be to write your own computer program? Python is a multi-paradigm programming language used by startups and tech giants like Google, Facebook, Cisco, Netflix, and more. With intuitive, readable syntax, Python is a great first programming language to learn. Get started with the <a href=\"https://edube.org/study/pe1\" target=\"_blank\">Python Essentials 1</a> course and prepare for the PCEP certification exam. If you already know the core fundamentals of Python, progress to <a href=\"https://edube.org/study/pe2\" target=\"_blank\">Python Essentials 2</a>, and prepare for the PCAP certification exam. If you work with Python and need to advance to more specialized areas of programming, pick our professional-series courses and prepare for the PCPP and specialization-track certifications.</p>"

from collections import deque
import re
import tiktoken
tokenizer = tiktoken.get_encoding("cl100k_base")
import nltk
nltk.download('punkt_tab')
nltk.download('punkt')


def chunk_text(text: str, max_token_count: int = 500):
    html_split_pattern = re.compile(r'(?:<p[^>]*>|</p>|<br\s*/?>|\n)+', flags=re.IGNORECASE)
    if not isinstance(text, str):
        raise TypeError("Text must be a string.")
    if not isinstance(max_token_count, int) or max_token_count <= 0:
        raise ValueError("max_token_count must be a positive integer.")
    
    segments = [seg.strip() for seg in html_split_pattern.split(text) if seg.strip()]

    token_cache = {}
    chunks = []
    chunk_queue = deque()
    tokens_in_chunk = 0
    overlap_queue = deque(maxlen=5)


    def get_token_count(s: str) -> int:
        if s not in token_cache:
            token_cache[s] = len(tokenizer.encode(s))
        return token_cache[s]
    
    def flush_chunk():
        nonlocal chunk_queue, tokens_in_chunk
        if chunk_queue:
            chunks.append(" ".join(chunk_queue))
            last_overlap = list(overlap_queue)
            chunk_queue = deque(last_overlap)
            tokens_in_chunk = sum(get_token_count(tok) for tok in chunk_queue)


    for segment in segments:
        seg_count = get_token_count(segment)
        # if seg_count <= max_token_count:
        #     # If adding this segment exceeds max, flush and start new
        #     if tokens_in_chunk + seg_count > max_token_count:
        #         flush_chunk()
        #     chunk_queue.append(segment)
        #     tokens_in_chunk += seg_count
        #     overlap_queue.append(segment)
        # else:
            # Segment too large: split into words
        words = nltk.word_tokenize(segment)
        sub_queue = deque()
        sub_count = 0
        for word in words:
            wc = get_token_count(word)
            if sub_count + wc > max_token_count:
                chunks.append(" ".join(sub_queue))
                tail = list(sub_queue)[-5:]
                sub_queue = deque(tail)
                sub_count = sum(get_token_count(w) for w in sub_queue)
            sub_queue.append(word)
            sub_count += wc
        if sub_queue:
            chunks.append(" ".join(sub_queue))

    if chunk_queue:
        chunks.append(" ".join(chunk_queue))

    return chunks

print(chunk_text(d))