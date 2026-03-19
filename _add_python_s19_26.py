"""Add sections 19-26 to gen_python_basics.py."""
import sys
sys.path.insert(0, r"c:\Users\seany\Documents\All Codes\Data Science Study Path")
from _inserter import insert_sections

FILE = r"c:\Users\seany\Documents\All Codes\Data Science Study Path\gen_python_basics.py"
MARKER = "]  # end SECTIONS"

def ec(code):
    return (code.replace('\\', '\\\\')
                .replace('"', '\\"')
                .replace('\n', '\\n')
                .replace("'", "\\'"))

def make_pb(num, title, desc, examples, rw_title, rw_scenario, rw_code,
            pt, pd_text, ps):
    """Build a section dict string for gen_python_basics format."""
    ex_lines = []
    for i, ex in enumerate(examples):
        comma = ',' if i < len(examples) - 1 else ''
        ex_lines.append(
            f'        {{"label": "{ec(ex["label"])}", "code": "{ec(ex["code"])}"}}{comma}'
        )
    ex_block = '\n'.join(ex_lines)
    return (
        f'{{\n'
        f'"title": "{num}. {title}",\n'
        f'"desc": "{ec(desc)}",\n'
        f'"examples": [\n{ex_block}\n    ],\n'
        f'"rw": {{\n'
        f'    "title": "{ec(rw_title)}",\n'
        f'    "scenario": "{ec(rw_scenario)}",\n'
        f'    "code": "{ec(rw_code)}"\n'
        f'}},\n'
        f'"practice": {{\n'
        f'    "title": "{ec(pt)}",\n'
        f'    "desc": "{ec(pd_text)}",\n'
        f'    "starter": "{ec(ps)}"\n'
        f'}}\n'
        f'}},\n\n'
    )

# ── Section 19: Functional Programming ──────────────────────────────────────
s19 = make_pb(19, "Functional Programming",
    "Python supports functional programming with map(), filter(), reduce(), and functools. These let you transform data declaratively without explicit loops.",
    [
        {"label": "map() and filter() for data transformation",
         "code":
"""nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# map() applies a function to every element
squares = list(map(lambda x: x**2, nums))
print("Squares:", squares)

# filter() keeps elements where function returns True
evens = list(filter(lambda x: x % 2 == 0, nums))
print("Evens:", evens)

# Chaining: square the even numbers
result = list(map(lambda x: x**2, filter(lambda x: x % 2 == 0, nums)))
print("Squared evens:", result)

# map with multiple iterables
a, b = [1, 2, 3], [10, 20, 30]
sums = list(map(lambda x, y: x + y, a, b))
print("Pairwise sums:", sums)"""},
        {"label": "functools.reduce() and partial()",
         "code":
"""from functools import reduce, partial

nums = [1, 2, 3, 4, 5]

# reduce() accumulates a result across an iterable
total = reduce(lambda acc, x: acc + x, nums)
print("Sum via reduce:", total)

product = reduce(lambda acc, x: acc * x, nums)
print("Product:", product)

# partial() freezes some arguments of a function
def power(base, exp):
    return base ** exp

square = partial(power, exp=2)
cube   = partial(power, exp=3)

print("5 squared:", square(5))
print("3 cubed:  ", cube(3))

# partial with data processing
def scale(value, factor=1.0, offset=0.0):
    return value * factor + offset

normalize = partial(scale, factor=0.1, offset=-0.5)
data = [0, 5, 10, 15, 20]
print("Normalized:", list(map(normalize, data)))"""},
        {"label": "Higher-order functions and function pipelines",
         "code":
"""from functools import reduce

# A function that returns a function
def make_multiplier(n):
    return lambda x: x * n

double = make_multiplier(2)
triple = make_multiplier(3)

print("double(7):", double(7))
print("triple(7):", triple(7))

# Build a pipeline of transformations
def pipeline(*funcs):
    def apply(data):
        return reduce(lambda v, f: f(v), funcs, data)
    return apply

process = pipeline(
    lambda x: [v for v in x if v > 0],    # keep positives
    lambda x: list(map(lambda v: v**0.5, x)),  # sqrt
    lambda x: [round(v, 2) for v in x],   # round
)

data = [-3, 4, 9, -1, 16, 25]
print("Input:", data)
print("Output:", process(data))"""}
    ],
    rw_title="Sales Data Cleaner",
    rw_scenario="A data pipeline uses functional tools to clean and transform a list of raw sales records without mutating state.",
    rw_code=
"""from functools import reduce, partial

records = [
    {"item": "apple",  "qty": 3,  "price": 1.20, "valid": True},
    {"item": "banana", "qty": -1, "price": 0.50, "valid": False},
    {"item": "cherry", "qty": 10, "price": 2.00, "valid": True},
]

# Filter valid records
valid = list(filter(lambda r: r["valid"] and r["qty"] > 0, records))

# Map to compute total
with_total = list(map(lambda r: {**r, "total": r["qty"] * r["price"]}, valid))

# Reduce to grand total
grand = reduce(lambda acc, r: acc + r["total"], with_total, 0.0)

for r in with_total:
    print(f'  {r["item"]:8s}: ${r["total"]:.2f}')
print(f"Grand total: ${grand:.2f}")""",
    pt="Functional Data Processor",
    pd_text="Write a function process_data(numbers) that uses ONLY map(), filter(), and reduce() (no loops): remove negatives, multiply each by 3, return the sum. Then create a partial called process_small that pre-filters values below 100 before calling process_data.",
    ps=
"""from functools import reduce, partial

def process_data(numbers):
    # Step 1: filter out negatives with filter()
    # Step 2: multiply each by 3 with map()
    # Step 3: sum with reduce()
    pass

# Test
print(process_data([1, -2, 3, -4, 5]))  # expect 27

def keep_small(numbers, limit=100):
    return [n for n in numbers if abs(n) < limit]

process_small = partial(process_data, ...)  # TODO: use partial with keep_small
"""
)

# ── Section 20: Itertools in Depth ──────────────────────────────────────────
s20 = make_pb(20, "Itertools in Depth",
    "The itertools module provides fast, memory-efficient tools for working with iterables. Essential for combinatorics, grouping, and chaining data streams.",
    [
        {"label": "chain, islice, cycle, repeat for sequence control",
         "code":
"""import itertools

# chain: join multiple iterables
combined = list(itertools.chain([1, 2], [3, 4], [5]))
print("chain:", combined)

# islice: slice an iterable (works on generators too)
first5 = list(itertools.islice(range(100), 5))
print("islice first 5:", first5)

skip3_take4 = list(itertools.islice(range(100), 3, 7))
print("islice [3:7]:", skip3_take4)

# cycle: repeat sequence infinitely — take 7
colors = list(itertools.islice(itertools.cycle(['R', 'G', 'B']), 7))
print("cycle 7:", colors)

# repeat: repeat a value n times
zeros = list(itertools.repeat(0, 5))
print("repeat:", zeros)

# accumulate: running totals
import itertools
data = [1, 3, 2, 5, 4]
running = list(itertools.accumulate(data))
print("accumulate (sum):", running)"""},
        {"label": "combinations, permutations, product",
         "code":
"""import itertools

items = ['A', 'B', 'C']

# combinations: order does not matter, no repeats
combs = list(itertools.combinations(items, 2))
print("combinations(2):", combs)

# permutations: order matters
perms = list(itertools.permutations(items, 2))
print("permutations(2):", perms)

# product: Cartesian product (like nested loops)
colors = ['red', 'blue']
sizes  = ['S', 'M', 'L']
variants = list(itertools.product(colors, sizes))
print("product:", variants)

# product with repeat: like rolling dice twice
dice = list(itertools.product(range(1, 4), repeat=2))
print("dice pairs:", dice[:6], "...")

print(f"Combinations: {len(combs)}, Permutations: {len(perms)}, Product: {len(dice)}")"""},
        {"label": "groupby and takewhile/dropwhile",
         "code":
"""import itertools

# groupby: group consecutive elements by a key
# NOTE: input must be sorted by the key first!
data = [
    {"dept": "eng",  "name": "Alice"},
    {"dept": "eng",  "name": "Bob"},
    {"dept": "sales","name": "Carol"},
    {"dept": "sales","name": "Dave"},
    {"dept": "hr",   "name": "Eve"},
]
data.sort(key=lambda x: x["dept"])

for dept, members in itertools.groupby(data, key=lambda x: x["dept"]):
    names = [m["name"] for m in members]
    print(f"  {dept}: {names}")

# takewhile: take elements while condition is True
nums = [2, 4, 6, 1, 8, 10]
taken = list(itertools.takewhile(lambda x: x % 2 == 0, nums))
print("takewhile even:", taken)  # stops at 1

# dropwhile: skip elements while condition is True
dropped = list(itertools.dropwhile(lambda x: x % 2 == 0, nums))
print("dropwhile even:", dropped)  # starts from 1"""}
    ],
    rw_title="Grid Search Parameter Iterator",
    rw_scenario="A machine learning hyperparameter search uses itertools.product to enumerate all combinations of parameters without nested loops.",
    rw_code=
"""import itertools

param_grid = {
    "learning_rate": [0.01, 0.1, 0.001],
    "max_depth":     [3, 5, 7],
    "n_estimators":  [50, 100],
}

keys = list(param_grid.keys())
values = list(param_grid.values())

configs = list(itertools.product(*values))
print(f"Total configs: {len(configs)}")

for i, combo in enumerate(itertools.islice(configs, 3)):
    cfg = dict(zip(keys, combo))
    print(f"  Config {i+1}: {cfg}")
print("  ...")""",
    pt="Itertools Combinatorics",
    pd_text="Write a function all_pairs(items) using itertools.combinations that returns all unique pairs. Write team_schedules(teams) using itertools.permutations(teams, 2) for home/away matchups. Write batch(iterable, n) using islice that yields chunks of size n.",
    ps=
"""import itertools

def all_pairs(items):
    # Return list of all unique 2-element combinations
    pass

def team_schedules(teams):
    # Return list of (home, away) tuples for all matchups
    pass

def batch(iterable, n):
    # Yield successive n-sized chunks from iterable
    it = iter(iterable)
    while True:
        chunk = list(itertools.islice(it, n))
        if not chunk:
            break
        yield chunk

# Tests
print(all_pairs(['A','B','C','D']))   # 6 pairs
print(len(team_schedules(['X','Y','Z'])))  # 6 matchups
print(list(batch(range(10), 3)))     # [[0,1,2],[3,4,5],[6,7,8],[9]]
"""
)

# ── Section 21: Closures & Scoping ──────────────────────────────────────────
s21 = make_pb(21, "Closures & Scoping",
    "Python resolves names using the LEGB rule (Local, Enclosing, Global, Built-in). Closures capture variables from enclosing scopes and are the foundation of decorators and factories.",
    [
        {"label": "LEGB scoping rule",
         "code":
"""x = "global"

def outer():
    x = "enclosing"

    def inner():
        x = "local"
        print("inner sees:", x)       # local

    inner()
    print("outer sees:", x)           # enclosing

outer()
print("module sees:", x)              # global

# Built-in scope: Python's built-in names (len, print, etc.)
print("built-in len:", len([1,2,3]))  # 3

# global keyword — modify a global from inside a function
counter = 0
def increment():
    global counter
    counter += 1

increment()
increment()
print("counter:", counter)  # 2

# nonlocal keyword — modify an enclosing variable
def make_counter():
    count = 0
    def inc():
        nonlocal count
        count += 1
        return count
    return inc

c = make_counter()
print(c(), c(), c())  # 1 2 3"""},
        {"label": "Closure factories",
         "code":
"""# A closure captures variables from its defining scope

def make_adder(n):
    # n is captured in the closure
    def add(x):
        return x + n
    return add

add5  = make_adder(5)
add10 = make_adder(10)
print("add5(3):", add5(3))   # 8
print("add10(3):", add10(3)) # 13

# Each closure has its own cell
print("Different objects:", add5 is not add10)  # True

# Closure with mutable state
def make_accumulator():
    total = 0
    def accumulate(value):
        nonlocal total
        total += value
        return total
    return accumulate

acc = make_accumulator()
for v in [10, 25, 5, 60]:
    print(f"  +{v} -> running total: {acc(v)}")"""},
        {"label": "Late binding and closure gotcha",
         "code":
"""# Common closure gotcha: late binding in loops
# All closures share the SAME variable i

funcs_bad = [lambda: i for i in range(5)]
print("Late binding:", [f() for f in funcs_bad])  # [4, 4, 4, 4, 4]!

# Fix 1: capture current value as default argument
funcs_good = [lambda i=i: i for i in range(5)]
print("Default arg fix:", [f() for f in funcs_good])  # [0, 1, 2, 3, 4]

# Fix 2: use a factory function
def make_func(i):
    def f():
        return i
    return f

funcs_factory = [make_func(i) for i in range(5)]
print("Factory fix:", [f() for f in funcs_factory])  # [0, 1, 2, 3, 4]

# Inspecting closure cells
import inspect
def outer(x):
    def inner():
        return x * 2
    return inner

fn = outer(7)
print("Closure cell value:", fn.__closure__[0].cell_contents)  # 7"""}
    ],
    rw_title="Configurable Validator Factory",
    rw_scenario="A data validation system uses closures to create reusable validators with baked-in limits, avoiding class overhead.",
    rw_code=
"""def make_range_validator(min_val, max_val, field="value"):
    def validate(x):
        if not (min_val <= x <= max_val):
            raise ValueError(f"{field} {x} out of range [{min_val}, {max_val}]")
        return True
    return validate

def make_str_validator(max_len, allowed_chars=None):
    def validate(s):
        if len(s) > max_len:
            raise ValueError(f"String too long: {len(s)} > {max_len}")
        if allowed_chars and not all(c in allowed_chars for c in s):
            raise ValueError(f"Invalid characters in: {s!r}")
        return True
    return validate

validate_age   = make_range_validator(0, 120, "age")
validate_score = make_range_validator(0.0, 1.0, "score")
validate_name  = make_str_validator(50, allowed_chars="abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ")

tests = [(validate_age, 25), (validate_score, 0.85), (validate_name, "Alice Smith")]
for validator, val in tests:
    try:
        print(f"  OK: {val!r}")
        validator(val)
    except ValueError as e:
        print(f"  FAIL: {e}")""",
    pt="Memoize with Closure",
    pd_text="Write a function memoize(func) that returns a new function. The new function caches results in a dict (stored in a closure). It should handle any positional arguments as the cache key. Test it with a slow Fibonacci function and verify the cache speeds it up.",
    ps=
"""def memoize(func):
    cache = {}   # closure variable
    def wrapper(*args):
        # TODO: if args in cache, return cached result
        # TODO: otherwise, call func(*args), store, return
        pass
    return wrapper

@memoize
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)

import time
t0 = time.time()
print(fib(35))     # should be fast after memoize
print(f"Time: {time.time()-t0:.4f}s")
"""
)

# ── Section 22: Decorators in Depth ─────────────────────────────────────────
s22 = make_pb(22, "Decorators in Depth",
    "Decorators wrap functions or classes to add behavior without modifying their source. Master stacked, parameterized, and class-based decorators.",
    [
        {"label": "Stacked decorators and functools.wraps",
         "code":
"""import functools, time

def timer(func):
    @functools.wraps(func)  # preserves __name__, __doc__
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"[timer] {func.__name__} took {(time.perf_counter()-t0)*1000:.2f}ms")
        return result
    return wrapper

def logger(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[logger] calling {func.__name__} with args={args}, kwargs={kwargs}")
        return func(*args, **kwargs)
    return wrapper

# Decorators apply bottom-up: logger wraps timer-wrapped function
@logger
@timer
def compute(n):
    return sum(range(n))

result = compute(100_000)
print("Result:", result)
print("Name preserved:", compute.__name__)  # compute, not wrapper"""},
        {"label": "Parameterized decorators (decorator factories)",
         "code":
"""import functools

def retry(times=3, exceptions=(Exception,)):
    # Outer function receives decorator arguments
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    print(f"  Attempt {attempt} failed: {e}")
                    if attempt == times:
                        raise
        return wrapper
    return decorator

attempt_count = 0

@retry(times=3, exceptions=(ValueError,))
def unstable_fetch(url):
    global attempt_count
    attempt_count += 1
    if attempt_count < 3:
        raise ValueError(f"Connection failed (attempt {attempt_count})")
    return f"Data from {url}"

result = unstable_fetch("https://api.example.com")
print("Got:", result)"""},
        {"label": "Class-based decorators",
         "code":
"""import functools

class CallCounter:
    # A class-based decorator that counts calls
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func  = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"[CallCounter] {self.func.__name__} called {self.count}x")
        return self.func(*args, **kwargs)

@CallCounter
def add(a, b):
    return a + b

add(1, 2)
add(3, 4)
add(5, 6)
print("Total calls:", add.count)  # 3

# Decorator that works on both functions and methods
class validate_positive:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func

    def __call__(self, *args, **kwargs):
        for arg in args:
            if isinstance(arg, (int, float)) and arg < 0:
                raise ValueError(f"Expected positive, got {arg}")
        return self.func(*args, **kwargs)

@validate_positive
def sqrt(x):
    return x ** 0.5

print(sqrt(9))   # 3.0
try:    sqrt(-1)
except ValueError as e: print("Caught:", e)"""}
    ],
    rw_title="Rate Limiter Decorator",
    rw_scenario="A web scraper applies a rate-limiting decorator to avoid overloading target servers, with configurable calls-per-second.",
    rw_code=
"""import functools, time

def rate_limit(calls_per_second=1):
    min_interval = 1.0 / calls_per_second
    last_called = [0.0]  # mutable container to allow mutation in closure

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            wait = min_interval - elapsed
            if wait > 0:
                print(f"  Rate limit: waiting {wait:.2f}s")
                time.sleep(wait)
            last_called[0] = time.time()
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(calls_per_second=2)
def fetch(url):
    return f"Response from {url}"

urls = ["http://a.com", "http://b.com", "http://c.com"]
for url in urls:
    print(fetch(url))""",
    pt="Cache Decorator with TTL",
    pd_text="Write a parameterized decorator @cache(ttl=60) that caches function results for ttl seconds. After the TTL expires, re-call the function and refresh the cache. Use a dict with (args, timestamp) as cache entries. Test with a function that returns time.time() so you can observe expiry.",
    ps=
"""import functools, time

def cache(ttl=60):
    def decorator(func):
        store = {}  # {args: (result, timestamp)}
        @functools.wraps(func)
        def wrapper(*args):
            now = time.time()
            if args in store:
                result, ts = store[args]
                if now - ts < ttl:
                    print(f"  [cache hit] age={now-ts:.1f}s")
                    return result
            # TODO: call func, store result with timestamp, return result
            pass
        return wrapper
    return decorator

@cache(ttl=2)
def get_value(key):
    return f"{key}:{time.time():.2f}"

print(get_value("x"))
print(get_value("x"))  # should be cache hit
time.sleep(2.1)
print(get_value("x"))  # should re-fetch after TTL
"""
)

# ── Section 23: Abstract Base Classes & Protocols ───────────────────────────
s23 = make_pb(23, "Abstract Base Classes & Protocols",
    "ABCs enforce interface contracts at class creation time. Protocols (PEP 544) enable structural subtyping — duck typing with type-checker support.",
    [
        {"label": "abc.ABC and @abstractmethod",
         "code":
"""from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass

    @abstractmethod
    def perimeter(self) -> float:
        pass

    def describe(self):
        # Concrete method shared by all subclasses
        return f"{type(self).__name__}: area={self.area():.2f}, perimeter={self.perimeter():.2f}"

class Circle(Shape):
    def __init__(self, r): self.r = r
    def area(self): return 3.14159 * self.r ** 2
    def perimeter(self): return 2 * 3.14159 * self.r

class Rectangle(Shape):
    def __init__(self, w, h): self.w, self.h = w, h
    def area(self): return self.w * self.h
    def perimeter(self): return 2 * (self.w + self.h)

for shape in [Circle(5), Rectangle(4, 6)]:
    print(shape.describe())

# Cannot instantiate ABC directly
try:
    s = Shape()
except TypeError as e:
    print("Cannot instantiate:", e)"""},
        {"label": "typing.Protocol for structural subtyping",
         "code":
"""from typing import Protocol, runtime_checkable

@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> str: ...
    def get_color(self) -> str: ...

# Any class with draw() and get_color() satisfies Drawable
# No explicit inheritance required!
class Circle:
    def draw(self): return "O"
    def get_color(self): return "red"

class Square:
    def draw(self): return "[]"
    def get_color(self): return "blue"

class TextLabel:
    def draw(self): return "TEXT"
    def get_color(self): return "black"

def render(item: Drawable) -> str:
    return f"Drawing {item.draw()} in {item.get_color()}"

shapes = [Circle(), Square(), TextLabel()]
for s in shapes:
    print(render(s))
    print(f"  isinstance check: {isinstance(s, Drawable)}")"""},
        {"label": "__subclasshook__ and virtual subclasses",
         "code":
"""from abc import ABC, abstractmethod

class Sized(ABC):
    @abstractmethod
    def __len__(self): ...

    @classmethod
    def __subclasshook__(cls, C):
        # Automatically treat ANY class with __len__ as Sized
        if cls is Sized:
            if any("__len__" in B.__dict__ for B in C.__mro__):
                return True
        return NotImplemented

# list, dict, str all have __len__ — they are virtual subclasses
print(isinstance([], Sized))    # True
print(isinstance({}, Sized))    # True
print(isinstance("hi", Sized))  # True
print(isinstance(42, Sized))    # False

# Register a virtual subclass without inheritance
class SparseVector:
    def __init__(self, data): self.data = data
    def __len__(self): return len(self.data)

print(isinstance(SparseVector({0: 1.0}), Sized))  # True
print(issubclass(SparseVector, Sized))             # True"""}
    ],
    rw_title="Plugin Architecture with ABC",
    rw_scenario="A data pipeline enforces that all data sources implement a common interface using ABC, then iterates over any registered source.",
    rw_code=
"""from abc import ABC, abstractmethod
from typing import Iterator, Any

class DataSource(ABC):
    @abstractmethod
    def connect(self) -> bool: ...
    @abstractmethod
    def read(self) -> Iterator[Any]: ...
    @abstractmethod
    def close(self) -> None: ...

    def stream(self):
        if self.connect():
            yield from self.read()
            self.close()

class CSVSource(DataSource):
    def __init__(self, rows):
        self.rows = rows
    def connect(self):
        print("CSV: opening"); return True
    def read(self):
        return iter(self.rows)
    def close(self):
        print("CSV: closed")

class APISource(DataSource):
    def __init__(self, data):
        self.data = data
    def connect(self):
        print("API: authenticated"); return True
    def read(self):
        return iter(self.data)
    def close(self):
        print("API: session ended")

for src in [CSVSource([1,2,3]), APISource(["a","b"])]:
    for record in src.stream():
        print(" ", record)""",
    pt="Serializable Protocol",
    pd_text="Define a Protocol called Serializable with methods to_dict() -> dict and classmethod from_dict(cls, d: dict). Implement it on a Product(name, price, qty) class. Write a function save_all(items) that checks isinstance(item, Serializable) before converting each item to dict.",
    ps=
"""from typing import Protocol, runtime_checkable
from dataclasses import dataclass

@runtime_checkable
class Serializable(Protocol):
    def to_dict(self) -> dict: ...
    # Note: classmethods in Protocols are tricky — just include to_dict for now

@dataclass
class Product:
    name: str
    price: float
    qty: int

    def to_dict(self):
        # TODO: return {"name": ..., "price": ..., "qty": ...}
        pass

    @classmethod
    def from_dict(cls, d: dict):
        # TODO: return cls(d["name"], d["price"], d["qty"])
        pass

def save_all(items):
    results = []
    for item in items:
        if isinstance(item, Serializable):
            results.append(item.to_dict())
        else:
            print(f"Skipped: {item!r} is not Serializable")
    return results

products = [Product("apple", 1.2, 50), Product("banana", 0.5, 200)]
print(save_all(products))
"""
)

# ── Section 24: Descriptors & Properties ────────────────────────────────────
s24 = make_pb(24, "Descriptors & Properties",
    "Descriptors control attribute access via __get__, __set__, __delete__. The property() built-in is the most common descriptor. __slots__ reduces memory overhead.",
    [
        {"label": "property getter, setter, deleter",
         "code":
"""class Temperature:
    def __init__(self, celsius=0):
        self._celsius = celsius  # private storage

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError(f"Temperature {value} below absolute zero!")
        self._celsius = value

    @celsius.deleter
    def celsius(self):
        print("Resetting temperature to 0")
        self._celsius = 0

    @property
    def fahrenheit(self):
        # Read-only computed property
        return self._celsius * 9/5 + 32

t = Temperature(25)
print(f"{t.celsius}C = {t.fahrenheit}F")

t.celsius = 100
print(f"Boiling: {t.celsius}C = {t.fahrenheit}F")

del t.celsius
print(f"Reset: {t.celsius}C")

try:
    t.celsius = -300
except ValueError as e:
    print("Caught:", e)"""},
        {"label": "Descriptor protocol (__get__, __set__, __delete__)",
         "code":
"""class Validated:
    # A reusable descriptor for validated attributes
    def __init__(self, min_val=None, max_val=None):
        self.min_val = min_val
        self.max_val = max_val
        self.name = None  # set by __set_name__

    def __set_name__(self, owner, name):
        self.name = name  # called when class is defined

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self  # class-level access returns descriptor itself
        return obj.__dict__.get(self.name, None)

    def __set__(self, obj, value):
        if self.min_val is not None and value < self.min_val:
            raise ValueError(f"{self.name} must be >= {self.min_val}, got {value}")
        if self.max_val is not None and value > self.max_val:
            raise ValueError(f"{self.name} must be <= {self.max_val}, got {value}")
        obj.__dict__[self.name] = value

class Person:
    age    = Validated(min_val=0, max_val=150)
    salary = Validated(min_val=0)

    def __init__(self, name, age, salary):
        self.name   = name
        self.age    = age
        self.salary = salary

p = Person("Alice", 30, 75000)
print(f"{p.name}: age={p.age}, salary={p.salary}")
try:
    p.age = -5
except ValueError as e:
    print("Caught:", e)"""},
        {"label": "__slots__ for memory efficiency",
         "code":
"""import sys

class PointNormal:
    def __init__(self, x, y):
        self.x, self.y = x, y

class PointSlots:
    __slots__ = ('x', 'y')   # declare allowed attributes
    def __init__(self, x, y):
        self.x, self.y = x, y

n = PointNormal(1.0, 2.0)
s = PointSlots(1.0, 2.0)

print(f"Without slots: {sys.getsizeof(n)} bytes, has __dict__: {hasattr(n, '__dict__')}")
print(f"With    slots: {sys.getsizeof(s)} bytes, has __dict__: {hasattr(s, '__dict__')}")

# Slots prevents adding arbitrary attributes
try:
    s.z = 3.0
except AttributeError as e:
    print("Cannot add:", e)

# Memory comparison with many instances
normal_mem = sum(sys.getsizeof(PointNormal(i, i)) for i in range(1000))
slots_mem  = sum(sys.getsizeof(PointSlots(i, i))  for i in range(1000))
print(f"1000 objects — normal: {normal_mem} bytes, slots: {slots_mem} bytes")
print(f"Slots saves: {normal_mem - slots_mem} bytes ({(1-slots_mem/normal_mem)*100:.1f}%)")"""}
    ],
    rw_title="Validated Configuration Class",
    rw_scenario="A configuration system uses descriptors to validate settings when they are set, providing clear error messages without if-statement clutter in __init__.",
    rw_code=
"""class TypedAttr:
    def __init__(self, expected_type, default=None):
        self.expected_type = expected_type
        self.default = default
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None: return self
        return obj.__dict__.get(self.name, self.default)

    def __set__(self, obj, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"{self.name} must be {self.expected_type.__name__}, "
                f"got {type(value).__name__}"
            )
        obj.__dict__[self.name] = value

class AppConfig:
    host     = TypedAttr(str, "localhost")
    port     = TypedAttr(int, 8080)
    debug    = TypedAttr(bool, False)
    timeout  = TypedAttr(float, 30.0)

cfg = AppConfig()
cfg.host    = "0.0.0.0"
cfg.port    = 443
cfg.debug   = True
cfg.timeout = 5.0

print(f"Config: {cfg.host}:{cfg.port} debug={cfg.debug} timeout={cfg.timeout}s")

try:
    cfg.port = "8080"  # wrong type!
except TypeError as e:
    print("Caught:", e)""",
    pt="Unit-Enforced Measurement",
    pd_text="Create a descriptor class UnitFloat(unit, min_val, max_val) that stores a float and records its unit. On __get__, return a namedtuple (value, unit). Create a class Measurement with descriptors for temperature (unit='C', min=-273.15), pressure (unit='Pa', min=0), and humidity (unit='%', min=0, max=100).",
    ps=
"""from collections import namedtuple

class UnitFloat:
    Reading = namedtuple("Reading", ["value", "unit"])

    def __init__(self, unit, min_val=None, max_val=None):
        self.unit    = unit
        self.min_val = min_val
        self.max_val = max_val
        self.name    = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None: return self
        val = obj.__dict__.get(self.name)
        # TODO: return UnitFloat.Reading(val, self.unit) if val is not None else None
        pass

    def __set__(self, obj, value):
        # TODO: validate type is float or int, validate min/max, store
        pass

class Measurement:
    temperature = UnitFloat("C", min_val=-273.15)
    pressure    = UnitFloat("Pa", min_val=0)
    humidity    = UnitFloat("%", min_val=0, max_val=100)

m = Measurement()
m.temperature = 22.5
m.pressure    = 101325.0
m.humidity    = 65.0
print(m.temperature)  # Reading(value=22.5, unit='C')
print(m.humidity)
"""
)

# ── Section 25: Memory Management & Profiling ────────────────────────────────
s25 = make_pb(25, "Memory Management & Profiling",
    "Python manages memory via reference counting and a cyclic garbage collector. Use sys, gc, tracemalloc, and cProfile to find memory leaks and performance bottlenecks.",
    [
        {"label": "sys.getsizeof, id(), and reference counting",
         "code":
"""import sys

# Basic sizes
for obj in [0, 1, 255, 2**100, 3.14, "hi", "hello world", [], [1,2,3], {}, {"a":1}]:
    print(f"  {repr(obj):<25} {sys.getsizeof(obj):>6} bytes")

# id() returns memory address
a = [1, 2, 3]
b = a          # same object
c = a.copy()   # different object

print("a is b:", a is b)  # True
print("a is c:", a is c)  # False
print("id(a)==id(b):", id(a) == id(b))  # True

# Small integers are cached
x, y = 100, 100
print("100 is 100:", x is y)  # True (cached)

x, y = 1000, 1000
print("1000 is 1000:", x is y)  # False (not cached)

# Nested containers: getsizeof is shallow!
lst = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print("Shallow size:", sys.getsizeof(lst))   # just the list object"""},
        {"label": "gc module and reference cycles",
         "code":
"""import gc

print("GC enabled:", gc.isenabled())
print("GC thresholds:", gc.get_threshold())  # (700, 10, 10)

# Reference cycle: a -> b -> a, both become unreachable
class Node:
    def __init__(self, name):
        self.name = name
        self.ref = None

a = Node("A")
b = Node("B")
a.ref = b  # a -> b
b.ref = a  # b -> a (cycle!)

# Delete our references
del a, b

before = gc.collect(0)
print(f"GC collected {before} objects in gen-0")

# Check what gc is tracking
tracked = gc.get_count()
print("GC counts (gen0, gen1, gen2):", tracked)

# Use __del__ to observe collection
class Tracked:
    def __del__(self):
        print(f"  {self!r} collected")

x = Tracked()
del x           # collected immediately (refcount -> 0)
gc.collect()    # collect cycles"""},
        {"label": "tracemalloc and cProfile",
         "code":
"""import tracemalloc, cProfile, io, pstats

# --- tracemalloc: trace memory allocations ---
tracemalloc.start()

snapshot1 = tracemalloc.take_snapshot()
big_list = [i**2 for i in range(10_000)]
snapshot2 = tracemalloc.take_snapshot()

stats = snapshot2.compare_to(snapshot1, "lineno")
for stat in stats[:3]:
    print(f"  {stat}")

tracemalloc.stop()
del big_list

# --- cProfile: find slow functions ---
def slow_sum(n):
    return sum(i**2 for i in range(n))

def fast_sum(n):
    return n * (n-1) * (2*n-1) // 6  # formula

pr = cProfile.Profile()
pr.enable()
slow_sum(50_000)
fast_sum(50_000)
pr.disable()

sio = io.StringIO()
ps  = pstats.Stats(pr, stream=sio).sort_stats("cumulative")
ps.print_stats(5)
print(sio.getvalue())"""}
    ],
    rw_title="Memory Leak Detector",
    rw_scenario="A long-running service monitors its own memory usage between requests to detect leaks early.",
    rw_code=
"""import tracemalloc, sys

def deep_size(obj, seen=None):
    # Recursively estimate size of a container
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum(deep_size(v, seen) for v in obj.values())
        size += sum(deep_size(k, seen) for k in obj.keys())
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes)):
        size += sum(deep_size(i, seen) for i in obj)
    return size

# Simulate a request that leaks memory
cache = {}

def handle_request(key, data):
    cache[key] = data  # intentional "leak" into global cache
    return len(data)

tracemalloc.start()
snap1 = tracemalloc.take_snapshot()

for i in range(5):
    handle_request(f"req_{i}", list(range(1000)))

snap2 = tracemalloc.take_snapshot()
top = snap2.compare_to(snap1, "lineno")[:2]
for stat in top:
    print(f"  Memory diff: {stat}")
print(f"Cache deep size: {deep_size(cache):,} bytes")
tracemalloc.stop()""",
    pt="Profile and Optimize",
    pd_text="Write two versions of a function that finds all prime numbers up to n: (1) trial_division(n) using a simple loop, (2) sieve(n) using the Sieve of Eratosthenes. Use timeit to benchmark both for n=10000. Use cProfile to show which lines of trial_division are slowest.",
    ps=
"""import cProfile, timeit

def trial_division(n):
    primes = []
    for num in range(2, n+1):
        if all(num % i != 0 for i in range(2, int(num**0.5)+1)):
            primes.append(num)
    return primes

def sieve(n):
    is_prime = [True] * (n+1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5)+1):
        if is_prime[i]:
            for j in range(i*i, n+1, i):
                is_prime[j] = False
    return [i for i, p in enumerate(is_prime) if p]

N = 10_000

# Benchmark
t1 = timeit.timeit(lambda: trial_division(N), number=3)
t2 = timeit.timeit(lambda: sieve(N), number=3)
print(f"trial_division: {t1:.3f}s")
print(f"sieve:          {t2:.3f}s")
print(f"Speedup: {t1/t2:.1f}x")

# Profile trial_division
cProfile.run("trial_division(5000)", sort="cumulative")
"""
)

# ── Section 26: Logging Best Practices ──────────────────────────────────────
s26 = make_pb(26, "Logging Best Practices",
    "Use the logging module instead of print() for production code. It supports levels, handlers, formatters, and log rotation — all configurable without code changes.",
    [
        {"label": "Basic logging setup and levels",
         "code":
"""import logging

# Configure root logger
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)-8s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)

logger = logging.getLogger("myapp")

# Five standard levels (low to high)
logger.debug("Detailed info for debugging")
logger.info("Normal operation: user logged in")
logger.warning("Something unexpected but not fatal")
logger.error("A failure occurred — function returned None")
logger.critical("Service is down!")

# Log exceptions with traceback
try:
    result = 1 / 0
except ZeroDivisionError:
    logger.exception("Division failed")  # includes traceback

# Extra context
user_id = 42
logger.info("Processing order", extra={"user": user_id})

# Check effective level
print("Effective level:", logger.getEffectiveLevel())  # 10 = DEBUG"""},
        {"label": "Multiple handlers and formatters",
         "code":
"""import logging, io

logger = logging.getLogger("pipeline")
logger.setLevel(logging.DEBUG)
logger.handlers.clear()  # avoid duplicate handlers in notebooks

# Handler 1: console with simple format
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)  # console only shows WARNING+
ch.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))

# Handler 2: "file" (using StringIO here for demo)
log_buffer = io.StringIO()
fh = logging.StreamHandler(log_buffer)
fh.setLevel(logging.DEBUG)   # file gets everything
fh.setFormatter(logging.Formatter(
    "%(asctime)s %(levelname)-8s [%(funcName)s:%(lineno)d] %(message)s",
    datefmt="%H:%M:%S"
))

logger.addHandler(ch)
logger.addHandler(fh)

def process(data):
    logger.debug("Starting process with %d items", len(data))
    logger.info("Processing...")
    if not data:
        logger.warning("Empty input")
    logger.debug("Done")

process([1, 2, 3])
process([])

print("--- File log ---")
print(log_buffer.getvalue())"""},
        {"label": "Logger hierarchy and module-level loggers",
         "code":
"""import logging

# Best practice: use __name__ as logger name
# This creates a hierarchy: "myapp" -> "myapp.db" -> "myapp.db.query"

root = logging.getLogger()
app  = logging.getLogger("myapp")
db   = logging.getLogger("myapp.db")
qry  = logging.getLogger("myapp.db.query")

# Set up root handler for the demo
logging.basicConfig(
    level=logging.DEBUG,
    format="%(name)-20s %(levelname)s: %(message)s"
)

# Child loggers propagate to parent by default
app.setLevel(logging.INFO)
db.setLevel(logging.DEBUG)   # db subtree shows DEBUG

app.info("App started")
app.debug("This won't show — app is INFO level")
db.debug("DB connection established")
qry.debug("SELECT * FROM users")

# Disable propagation to avoid double-logging
# child_logger.propagate = False

# Silence noisy third-party libraries
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("boto3").setLevel(logging.WARNING)
print("Third-party loggers silenced")"""}
    ],
    rw_title="Pipeline Logger",
    rw_scenario="A data processing pipeline uses structured logging to track progress, errors, and timing without print statements.",
    rw_code=
"""import logging, time, io

def setup_logger(name, level=logging.DEBUG):
    log = logging.getLogger(name)
    log.setLevel(level)
    if not log.handlers:
        h = logging.StreamHandler()
        h.setFormatter(logging.Formatter(
            "%(asctime)s %(name)s %(levelname)-8s %(message)s",
            datefmt="%H:%M:%S"
        ))
        log.addHandler(h)
    return log

log = setup_logger("etl")

def extract(source):
    log.info("Extracting from %s", source)
    data = list(range(100))  # simulated data
    log.debug("Extracted %d records", len(data))
    return data

def transform(data):
    log.info("Transforming %d records", len(data))
    t0 = time.time()
    result = [x * 2 for x in data if x % 5 != 0]
    log.debug("Transform took %.3fs, %d records remain", time.time()-t0, len(result))
    return result

def load(data, target):
    log.info("Loading %d records to %s", len(data), target)
    # Simulate occasional error
    if len(data) > 70:
        log.warning("Large batch — consider chunking")
    log.info("Load complete")

try:
    d = extract("sales.csv")
    d = transform(d)
    load(d, "warehouse")
except Exception:
    log.exception("Pipeline failed")""",
    pt="Log Analyzer",
    pd_text="Write a function parse_log_line(line) that extracts timestamp, level, and message from a log line like '12:34:56 WARNING myapp: disk 90% full'. Write analyze_logs(lines) that counts occurrences of each level and returns a dict like {'WARNING': 3, 'ERROR': 1}. Use the logging module to emit a summary.",
    ps=
"""import logging, re
from collections import Counter

def parse_log_line(line):
    # Pattern: HH:MM:SS LEVEL name: message
    pattern = r"(\\d{2}:\\d{2}:\\d{2}) (\\w+) (\\S+): (.+)"
    m = re.match(pattern, line)
    if m:
        return {"time": m.group(1), "level": m.group(2),
                "name": m.group(3), "msg": m.group(4)}
    return None

def analyze_logs(lines):
    # TODO: parse each line, count levels, return Counter dict
    pass

sample_logs = [
    "12:00:01 INFO myapp: started",
    "12:00:02 DEBUG myapp.db: query took 0.1s",
    "12:00:03 WARNING myapp: memory 80% full",
    "12:00:04 ERROR myapp: connection refused",
    "12:00:05 WARNING myapp: retry 1/3",
]

counts = analyze_logs(sample_logs)
print("Level counts:", counts)
"""
)

# ── Assemble and insert ──────────────────────────────────────────────────────
all_sections = s19 + s20 + s21 + s22 + s23 + s24 + s25 + s26

result = insert_sections(FILE, MARKER, all_sections)
if result:
    print("SUCCESS: sections 19-26 added to gen_python_basics.py")
else:
    print("FAILED: check marker and file")
