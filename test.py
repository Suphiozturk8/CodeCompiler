
from utils import Compiler

r = Compiler()

try:
    response = r.(
        "python3",
        "print('Hello')")

    print(response)
except Exception as e:
    print(e)
    exit(-1)

print("\nTest completed")
exit(0)
