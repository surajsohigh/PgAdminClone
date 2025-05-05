from django.shortcuts import HttpResponse
from django.db import connection, DatabaseError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.utils import ProgrammingError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser

# Default home page
def home(request):
    return HttpResponse("Welcome")    

# Get all table name stored in the database
@api_view(["GET"])
def list_tables(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema='public'
                """
            )
            tables = [row[0] for row in cursor.fetchall()]
        return Response({"tables": tables}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": "Failed to retrieve tables."}, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Get all columns for the given table
@api_view(["GET"])
def get_table_data(request, table_name):
    try:
        if not table_name.isidentifier():
            return Response({"error": "Invalid table name."}, 
                            status=status.HTTP_400_BAD_REQUEST)

        with connection.cursor() as cursor:
            query = f"SELECT * FROM public.\"{table_name}\" LIMIT 100"  # safer for Postgres
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()

        return Response([dict(zip(columns, row)) for row in rows], 
                        status=status.HTTP_200_OK)

    except ProgrammingError as e:
        return Response({"error": "Invalid table or query."}, 
                        status=status.HTTP_400_BAD_REQUEST)

    except DatabaseError as e:
        return Response({"error": "Database error."}, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        return Response({"error": "Internal server error."}, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Function to execute SQL Query
@api_view(["POST"])
def execute_query(request):
    sql = request.data.get("sql", "").strip()

    if not sql:
        return Response({"error": "SQL query is required."}, 
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)

            if cursor.description:
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()
                result = [dict(zip(columns, row)) for row in rows]
                return Response({"rows": result}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Query executed, no result set."}, 
                                status=status.HTTP_200_OK)

    except DatabaseError as db_err:
        return Response(
            {"error": "Query execution failed."},
            status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response(
            {"error": "Internal server error."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Get all columns name for the given table
@api_view(["GET"])
def get_table_columns(request, table_name):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = %s
                ORDER BY ordinal_position
            """, [table_name])
            columns = cursor.fetchall()
        
        result = [{"name": col[0], "type": col[1]} for col in columns]

        if not result:
            return Response(
                {"message": f"No columns found for table '{table_name}'."},
                status=status.HTTP_404_NOT_FOUND)

        return Response(result, status=status.HTTP_200_OK)
    
    except DatabaseError as db_err:
        return Response(
            {"error": "Database query failed."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        # logger.error(f"Unexpected error in get_table_columns: {str(e)}", exc_info=True)
        return Response(
            {"error": "Internal server error."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)




# import logging
# logger = logging.getLogger(__name__)
