import asyncpg
import asyncio
from asyncpg import Record
from typing import List

async def main():
    # Making connection 
    connection = await asyncpg.connect(host="",user="",password="",database="",port="")
    version = connection.get_server_version()
    
    #creating tables in database.
    statements=[]="list of table querieres"
    print('Creating the product database...')
    for statement in statements:
        status = await connection.execute(statement)
        print(status)
    print('Finished creating the product database!')
    
    
    # Inserting data in postgres asynchronous
    await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'Levis')")
    await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'Seven')")

    # Fetching rows from database
    brand_query = 'SELECT brand_id, brand_name FROM brand'
    results: List[Record] = await connection.fetch(brand_query)
    
    
    # Executemany is a courtine that execute many sql question in one go . "insert brands is the Sql quesries and brands is the list of tuple"
    # internally execute many run a for loop to run queris
    insert_brands = "INSERT INTO brand VALUES(DEFAULT, $1)"
    await connection.executemany(insert_brands, "brands")
    #connection close 
    await connection.close()
asyncio.run(main())





# how to run conncurrenly sql queries for that we need to create_pool  we need user create_pool instead of connect

async def query_product(pool):
    async with pool.acquire() as connection:
        return await connection.fetchrow("product_query")
                                    
async def main1():
   async with asyncpg.create_pool(host='127.0.0.1',port=5432,user='postgres',password='password',database='products',min_size=6,max_size=6) as pool:
       await asyncio.gather(query_product(pool),query_product(pool))
       
asyncio.run(main1())