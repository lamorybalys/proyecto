import mysql.connector
import datetime

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="deparweb"
)
consulta = mydb.cursor()
date     = datetime.datetime.now()
fecha    = date.strftime("%Y")
hoy      = date.strftime("%Y-%m-%d")
consulta.execute("(select t.id as id_t,fech_ing_inst,TIMESTAMPDIFF(YEAR,fech_ing_inst,CURDATE()) as edad,DATE(DATE_ADD(fech_ing_inst, INTERVAL 1 YEAR)) as año,e.id as id_exp,TIMESTAMPDIFF(YEAR,fech_ing_inst,CURDATE()) as antiguedad,IF(t.cargos ='Medico (a)',concat(t.cargos,' Grado ',t.grado),t.cargos) as cargo   from trabaexpe_trabajador t inner join trabaexpe_expedientes e on e.trabajador_id=t.id having edad =1 and año='"+str(hoy)+"') union (select t.id,periodo,TIMESTAMPDIFF(YEAR,periodo,CURDATE()) as edad,DATE(DATE_ADD(periodo, INTERVAL 1 YEAR)) as año,expediente_id,TIMESTAMPDIFF(YEAR,t.fech_ing_inst,CURDATE()) as antiguedad,IF(t.cargos ='Medico (a)',concat(t.cargos,' Grado ',t.grado),t.cargos) as cargo from  constancias_periodo c inner join trabaexpe_expedientes e inner join trabaexpe_trabajador t on e.trabajador_id=t.id where c.expediente_id=e.id having edad =1 and año='"+str(hoy)+"');")
resultado = consulta.fetchall()

days_m = ['18','20','22','24','26','28','31','34','37','40','43','46']
days_e = ['18','18','18','18','19','21','21','22','23','24','25','26','27','28','29','30']
days_o = ['20','20','20','20','20','22','22','22','23','24','25','26','27','28','29','30']
def dias(cargo="",antiguedad=""):
  car = cargo.split(' ')

  if car[0] == 'Medico':
    dias  = days_m[int(car[4])-1]

  elif car[0] == 'Empleado':
    if int(antiguedad) <=16:
      dias  = days_e[int(antiguedad)-1]
    else:
      dias  = days_e[15]

  elif car[0] == 'Obrero':
    if int(antiguedad) <=16:
      dias  = days_o[int(antiguedad)-1]
    else:
      dias  = days_o[15]

  return dias
for i in resultado:
    consulta.execute("select DATE_FORMAT(periodo,'%Y') as año from  constancias_periodo x inner join trabaexpe_expedientes e on e.trabajador_id='"+str(i[0])+"' where expediente_id=e.id having año="+str(fecha)+"  order by x.id desc limit 1;")
    query = consulta.fetchall()
    if len(query)<1:
        consulta.execute("insert into constancias_periodo (periodo,expediente_id,dias) values('"+str(i[3])+"',"+str(i[4])+","+str(dias(str(i[6]),str(i[5])))+");")
        mydb.commit()



