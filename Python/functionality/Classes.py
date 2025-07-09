class MyClass:
    # Class attribute (shared across all instances)
    class_variable = "I am a class variable"

    # Constructor: the __init__ method is a special method called when an instance is created.
    def __init__(self, instance_variable=class_variable):
        # Instance variable (unique to each instance)
        self.instance_variable = instance_variable
        print("hello")

    # Method (function defined within the class)
    def instance_method(self):
        print("This is an instance method.")
        print(f"Instance variable: {self.instance_variable}")


# Create an instance of MyClass and pass a value for the instance variable
my_instance = MyClass()

# Call the instance method on this object
my_instance.instance_method()
