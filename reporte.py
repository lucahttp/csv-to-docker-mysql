
    def makeReport(slef,query_name,query):
        # https://stackoverflow.com/questions/4899832/sqlite-function-to-format-numbers-with-leading-zeroes
        # https://tiebing.blogspot.com/2011/07/sqlite-3-string-to-integer-conversion.html
        """
        CAST(substr('00'||residencia_provincia_id,-2) || substr('000'||residencia_departamento_id,-3) as integer) AS ID,
        """
        sql_string = """
        SELECT residencia_departamento_nombre  AS "Departamento Residencia",residencia_provincia_nombre  AS "Provincia Residencia", 
        substr('00'||residencia_provincia_id,-2) || substr('000'||residencia_departamento_id,-3) AS ID,
        substr('000'||residencia_departamento_id,-3) AS "ID Departamento",
        substr('00'||residencia_provincia_id,-2) AS "ID Provincia",
        count(*) AS "Total Test",
        sum(case when clasificacion_resumen="Confirmado" then 1 else 0 end) AS Confirmados,
        sum(case when clasificacion LIKE "%No Activo%" then 1 else 0 end) AS Recuperados,
        (sum(case when clasificacion_resumen="Confirmado" then 1 else 0 end)-sum(case when clasificacion LIKE "%No Activo%" then 1 else 0 end))Activos,
        sum(case when clasificacion = "Caso confirmado - Fallecido" then 1 else 0 end) AS Fallecidos
        FROM mydb
        GROUP BY residencia_departamento_nombre
        ORDER BY "residencia_provincia_id" ASC,"residencia_departamento_nombre" ASC,"residencia_departamento_nombre" ASC;
        """
        sql_string = query
        gg = pd.read_sql(sql_string, self.conn)
        print()
        #return self.makeReport(gg, "fullreport")
        gg = gg
        report_name = "fullreport"
        report_name = query_name
        #def makeReport(self, gg, report_name):
        import json
        # print(type(gg))
        #gg = gg.set_index(0)
        print(type(gg))
        gg.to_csv(report_name+".csv", encoding='latin1', index=False)
        #json.dumps(parsed, indent=4, ensure_ascii=False)
        # gg.set_index(list(gg)[0])
        gg = gg.set_index(gg.columns[0])
        gg.set_index(gg.columns.tolist()[0])
        #json.dumps(parsed, indent=4)

        result = gg.to_json(orient="index")
        parsed = json.loads(result)
        resultado = gg.to_json(orient="index")
        gg.to_json(report_name+".json", orient='table',
                   force_ascii=False, indent=4)

        # Works
        #out = json.dumps(parsed, indent=4, ensure_ascii=False)
        #gg.to_csv('report.csv', encoding='utf-8', index=False)

        #result = gg.to_json(orient="index")

        parsed = json.loads(result)

        json.dumps(parsed, indent=4)
        # print(resultado)
        return resultado