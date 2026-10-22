#This is a little application using the the MASSIVE STOCK 
#api ... I think it was called polygon io at some point 
#stock trading data extractor 
import os
from dotenv import load_dotenv


#Load the environment variables from the .env file 
load_dotenv()

massive_key = os.environ.get("MASSIVE_API_KEY")



def main():
    print(massive_key)
    print("come on!")




if __name__ == "__main__":
    main()
    