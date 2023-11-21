from utils import Compiler, CompilerException

# Create an instance of the Compiler class
compiler = Compiler()

# Enter the language, code, and stdin (if needed) you want to test
language = "python3"
code = "print('Hello, World! 👻')"
stdin = ""  # Optional: add stdin input here if needed

try:
    # Execute the code
    response = compiler.execute(language, code, stdin)

    # Generate output to display the result
    output = compiler.generate_output(response, code)
    print(output)

except CompilerException as e:
    print(f"Error: {e}")
