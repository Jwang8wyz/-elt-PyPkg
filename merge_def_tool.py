def fetch_table_columns(cursor, table_name, schema_name, database_name):
    query = f"""
    SELECT COLUMN_NAME
    FROM {database_name}.INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = '{schema_name}'
    AND TABLE_NAME = '{table_name}'
    ORDER BY ORDINAL_POSITION;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [row[0] for row in rows]
    return columns

def generate_merge_sql(source_table, target_table, key_columns, all_columns):
    on_clause = ' AND '.join([f"target.{col} = source.{col}" for col in key_columns])
    insert_columns = ', '.join(all_columns)
    insert_values = ', '.join([f"source.{col}" for col in all_columns])
   
    sql = f"""
    MERGE INTO {target_table} AS target
    USING {source_table} AS source
    ON {on_clause}
    WHEN NOT MATCHED THEN
        INSERT ({insert_columns})
        VALUES ({insert_values});
    """
    return sql
