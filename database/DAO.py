from database.DB_connect import DBConnect
from model.metodo import Metodo
from model.prodotto import Prodotto
from model.vendita import Vendita


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllMetodi():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                from go_methods"""
        cursor.execute(query)
        for row in cursor:
            result.append(
                Metodo(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllProdotti(method, year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select gp.* 
                    from go_products gp, go_daily_sales gds 
                    where gds.Product_number = gp.Product_number 
                    and gds.Order_method_code = %s
                    and year(gds.`Date`) = %s
                    group by gp.Product_number """
        cursor.execute(query, (method, year, ))
        for row in cursor:
            result.append(
                Prodotto(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllProfit(year, method):
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """select distinct gds.Product_number as prodotto,sum(Unit_sale_price*Quantity) as prezzo
                            from go_daily_sales gds
                            where year( gds.`Date` )=%s and gds.Order_method_code=%s
                            group by gds.Product_number """

        cursor.execute(query, (year, method))

        for row in cursor:
            result[row["prodotto"]] = row["prezzo"]

        cursor.close()
        conn.close()
        return result
