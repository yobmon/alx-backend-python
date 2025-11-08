class contextmanager:
    def __enter__(self):
        print("Entering the context")
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        print("Exiting the context")
        if exc_type:
            print(f"An exception occurred: {exc_value}")
        return False 
with contextmanager() as cm:
    print("Inside the context")