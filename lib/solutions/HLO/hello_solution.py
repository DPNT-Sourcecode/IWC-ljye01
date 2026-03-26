
class HelloSolution:
    
    # friend_name = unicode string
    def hello(self, friend_name):
        return f"Hello, {friend_name}!"

if __name__ == "__main__":
    print(HelloSolution().hello("Ekin"))
