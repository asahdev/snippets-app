import sys
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
    try:
      command = "insert into snippets values (%s, %s)"
      cursor.execute(command, (name, snippet))
    except  psycopg2.IntegrityError as e:
      connection.rollback()
      command = "update snippets set message=%s where keyword=%s"
      cursor.execute(command, (snippet, name))
    connection.commit()
    return name, snippet


def get(name):
    """Retrieve the snippet with a given name"""
    logging.info("Get function used to get values of {!r}".format(name))
    with connection, connection.cursor() as cursor:
      cursor.execute("select message from snippets where keyword=%s", (name,))
      row = cursor.fetchone()
    logging.debug("Snippet retrived successfully.")
    return row

def catalog():
   """Retrive all the keywords"""
   with connection, connection.cursor() as cursor:
      cursor.execute("select keyword from snippets;")
      row = cursor.fetchall()
   logging.debug("all keywords displayed")
   return row

def search(search_var):
  """search for a keyword in snippets"""
  with connection, connection.cursor() as cursor:
    cursor.execute("select * from snippets where message like {!r}".format(search_var))
    row = cursor.fetchone()
    logging.debug("Snippet retrived successfully.")
    return row

#   logging.info("Funcation to get value of all keywords")
#   cursor = connection.cursor()
#   command = "select * from snippets;"
#   a = cursor.execute(command)
#   connection.commit()
#   print(a)

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

    #Subparser for the all command
    logging.debug("Constructing all subparser")
    all_parser = subparsers.add_parser("all", help="show all keywords")

    #subparser for the search command
    logging.debug("Constructing search subparser")
    search_parser = subparsers.add_parser("search", help="search a keyword in messages")
    search_parser.add_argument("search_var", help="Keyword to search")

#    print(len(sys.argv))
#    if len(sys.argv) <= 1:
#      print("No argument provided")
    
    arguments = parser.parse_args(sys.argv[1:])
#    arguments = parser.parse_args()
    arguments = vars(arguments)
    command = arguments.pop("command")
    if command == None:
      print("Testing out")
    elif command == "put":
      name, snippet = put(**arguments)
      print("Stored {!r} as {!r}".format(snippet, name))
    elif command == "all":
      keywords = catalog(search_var)
      print("All Keyword are ",(keywords))
    elif command == "search":
      search_var = search(**arguments)
      print("The result is ",(search_var))
    elif command == "get":
      snippet = get(**arguments)
      if snippet == None:
        print("No snippet available")
      else:
         print("Retrieved snippet: {!r}".format(snippet))

  
if __name__ == "__main__":
  main()
