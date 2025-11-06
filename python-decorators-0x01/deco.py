def greet_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        # 2. Call the original function
        print("Something is happening after the function is called.")
    return wrapper # 3. Return the new, decorated function

# Use the @ syntax for the decorator
@greet_decorator
def say_hello():
    print("Hello!")
say_hello()  # 4. Call the decorated function