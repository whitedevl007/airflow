import happybase
connection = happybase.Connection('localhost', port=9090)



def create_hbase_table():
    # Specify the table name
    table_name = "personal"
    families = {
        'column_family': dict()  # Create an empty column family
    }

    # Create the table if it doesn't exist
    
    connection.create_table(table_name, families)
        
create_hbase_table()