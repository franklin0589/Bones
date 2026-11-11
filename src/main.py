
from lib.builder import build_app
from scripts import setup, update 

def main():
    build_app(setup, update)
    
if __name__ == "__main__":
    main()