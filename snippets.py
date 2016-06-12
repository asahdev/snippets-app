import psycopg2
import logging
import argparse

# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)
logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect(database="snippets")
logging.debug("Database connection established.")


def put(name, snippet):
    """Store a snippet with an associated name."""
    logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
    cursor = connection.cursor()
    command = "insert into snippets values (%s, %s)"
    cursor.execute(command, (name, snippet))
    connection.commit()
    logging.debug("Snippet stored successfully.")
    return name, snippet


def get(name):
    """Retrieve the snippet with a given name"""
    logging.info("Get function used to get values of {!r}".format(name))
    cursor = connection.cursor()
    command = "select keyword, message from snippets where keyword='%s'" %(name)
    cursor.execute(command)
    result = cursor.fetchone()
    connection.commit()
    logging.debug("Snippet retrived successfully.")
    return result



def main():
    """Main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="Name of the snippet")
    put_parser.add_argument("snippet", help="Snippet text")
     
    #Subparser for the get command
    logging.debug("Constructing put subparser")
    get_parser = subparsers.add_parser("get", help="Store a snippet")
    get_parser.add_argument("name", help="Name of the snippet")

    arguments = parser.parse_args()
    arguments = vars(arguments)
    command = arguments.pop("command")
    if command == "put":
      name, snippet = put(**arguments)
      print("Stored {!r} as {!r}".format(snippet, name))
    elif command == "get":
      snippet = get(**arguments)
      print("Retrieved snippet: {!r}".format(snippet))

  
if __name__ == "__main__":
    main()
