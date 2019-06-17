from django.views.generic import View
from django.utils import timezone

from django.shortcuts import render,redirect,get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden

from django.shortcuts import get_object_or_404
from django.contrib.staticfiles import finders
import os
from io import BytesIO
from reportlab.platypus.tables import Table, TableStyle, CellStyle, LongTable
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter, A4,  LETTER, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Table, BaseDocTemplate, Frame, PageTemplate, Image, TableStyle, Spacer, SimpleDocTemplate, PageBreak
from reportlab.lib.units import inch, cm, mm 
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from datetime import datetime

from apps.trabaexpe.models import * 
from apps.constancias.models import * 
import string
from django.contrib import messages


# Número de Página -----------------------------------------------------------------------------
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []
 
    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()
 
    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)
 
    def draw_page_number(self, page_count):
        self.setFont("Helvetica-Bold", 7)
        self.drawRightString(25 * mm, 4 * mm + (0.3 * inch),"Página %d de %d" % (self._pageNumber, page_count))


# PDF de Persona -----------------------------------------------------------------------------
def HeaderFooterPersona(canvas,doc):
        canvas.saveState()
        title = "Reporte de Ley Politica"
        canvas.setTitle(title)
        
        Story=[]
        styles = getSampleStyleSheet()
        
        archivo_imagen = finders.find('images/cintillo/1.png')
        canvas.drawImage(archivo_imagen, 30, 720, width=540,height=100,preserveAspectRatio=True)

        fecha = datetime.now().strftime('%d/%m/%Y ')
        # Estilos de Párrafos
        ta_c = ParagraphStyle('parrafos', 
                            alignment = TA_CENTER,
                            fontSize = 10,
                            fontName="Helvetica",
                            )   
       	ta_c1 = ParagraphStyle('parrafos', 
                            alignment = TA_JUSTIFY,
                            fontSize = 14,
                            borderPadding = 20,
                            leading = 18,
                            fontName="Helvetica",

                            )   
        ta_l = ParagraphStyle('parrafos', 
                            alignment = TA_LEFT,
                            fontSize = 15,
                            fontName="Helvetica-Bold",
                            )
        ta_l7 = ParagraphStyle('parrafos', 
                            alignment = TA_CENTER,
                            fontSize = 10,
                            fontName="Helvetica-Bold",
                            )
       	ta_l8 = ParagraphStyle('parrafos', 
                            alignment = TA_CENTER,
                            fontSize = 7,
                            fontName="Helvetica",
                            )
        ta_r = ParagraphStyle('parrafos', 
                            alignment = TA_RIGHT,
                            fontSize = 13,
                            fontName="Helvetica-Bold",
                            )

        # Header
        header = Paragraph("CONSTANCIA ",ta_l)
        w,h = header.wrap(doc.width+250, doc.topMargin)
        header.drawOn(canvas, 245, doc.height -10 + doc.topMargin-120)


        content = """
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Quien suscribe, Jefe de Recursos Humanos  <p/> del Hospital Universitario “Dr. Miguel Oraá” de Guanare, 
        por medio de la presente hago constar  que el Ciudadana(o): <b>{}</b>, Titular de la  
        cédula de identidad <b>V–{}</b>, presta sus servicios en esta Institución como: <b>{}</b> {}, código del Rac: <b>{}</b> siendo su fecha de ingreso desde: <b>{}</b>
        hasta la actualidad. Cotiza Ley de Política Habitacional.
        <br/>
        <br/>
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Constancia que se expide para fines legales en la ciudad de Guanare, a los {}.


        """.format(nombre,cedula,cargo,cargo2,rac,fecha_i,dia)
        header1 = Paragraph(content,ta_c1)
        w,h = header1.wrap(doc.width-50, doc.topMargin)
        header1.drawOn(canvas, 55, doc.height -10 + doc.topMargin-340)

        firma = """
			LCDA. SOVEIDA YOLIMAR PEREZ DE M.<br/>
			Jefe de Recursos Humano  del Hospital Universitario<br/>
			“Dr. Miguel Oraá” de Guanare Edo. Portuguesa<br/>
			Según Oficio DESP-18-0042 De Fecha 23/01/2018<br/>

        """
        header2 = Paragraph(firma,ta_l7)
        w,h = header2.wrap(doc.width-50, doc.topMargin)
        header2.drawOn(canvas, 55, doc.height -10 + doc.topMargin-650)

        final = """
        RUMBO A LA CONSOLIDACIÓN DEL SISTEMA PÚBLICO NACIONAL DE SALUD…<br/>
		”HOSPITAL GENERAL  MIGUEL ORAÁ DE GUANARE EDO PORTUGUESA  AV. LA HILANDERA  URBANIZACIÓN ANDRÉS ELOY BLANCO   GUANARE  –  PORTUGUESA,  RIF:   G   –   20008795 -  1     TELF. (0257)   251-0343 /2517336,  correo: personalmigueloraa@gmil.com.

        """
       	header2 = Paragraph(final,ta_l8)
        w,h = header2.wrap(doc.width-50, doc.topMargin)
        header2.drawOn(canvas, 55, doc.height -10 + doc.topMargin-750)

        

        canvas.restoreState()

def LeyPDF(request):
    response = HttpResponse(content_type='application/pdf')
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    doc = SimpleDocTemplate(buffer,
        pagesizes=letter,
        rightMargin = 30,
        leftMargin= 30,
        topMargin=176.9,
        bottomMargin=50,
        paginate_by=0,
    )
    ta_r = ParagraphStyle('parrafos', 
        alignment = TA_RIGHT,
        fontSize = 13,
        fontName="Helvetica-Bold",
        )
    persona=[]
    styles = getSampleStyleSheet()
    # TABLA NUMERO 1
    count = 0
    data = []
    data.append(['','','','','','',''])
    x = Table(data)
    trabajador = Trabajador.objects.get(usuario=request.user)
    global expediente
    expediente = Expedientes.objects.get(trabajador=trabajador)
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    hoy = str(datetime.now().strftime('%d/%m/%Y ')).split('/')

    fecha1 = hoy[0]+' dias del mes de '+str(meses[int(hoy[1])-1])+' del '+hoy[2]
    print(hoy,fecha1)
    if expediente:
        global nombre,cedula,cargo,cargo2,rac,fecha_i,dia
        rac = trabajador.cod_rac
        cargo = (trabajador.cargos).upper().strip()
        if cargo == 'EMPLEADO (A)':
            cargo2 = 'en el cargo de: <b>'+str((trabajador.empleados).upper().strip())+'</b>'
        if cargo == 'MEDICO (A)':
            cargo2 = 'grado: <b>'+str((trabajador.grado).upper().strip())+'</b>'
        if cargo == 'OBRERO (A)':
            cargo2 = 'en el cargo de: <b>'+str((trabajador.obreros).upper().strip())+'</b>'
        nombre = (trabajador.nomb_trab + ' '+trabajador.ape_trab).upper().strip() 
        cedula = "{:,}".format(trabajador.cedu_trab).replace(',','.')
        fe = str(trabajador.fech_ing_inst).split('-')
        fecha_i = fe[2]+'/'+fe[1]+'/'+fe[0]
        dia = fecha1.strip()
    	
    else:
    	print('error')

    persona.append(x)

    doc.build(persona,onFirstPage=HeaderFooterPersona,onLaterPages=HeaderFooterPersona,canvasmaker=NumberedCanvas)
    response.write(buffer.getvalue())
    buffer.close()

    return response

# PDF de Persona -----------------------------------------------------------------------------
def HeaderFooterTrabajo(canvas,doc):
        canvas.saveState()
        title = "Reporte de Ley Politica"
        canvas.setTitle(title)
        
        Story=[]
        styles = getSampleStyleSheet()
        
        archivo_imagen = finders.find('images/cintillo/1.png')
        canvas.drawImage(archivo_imagen, 30, 720, width=540,height=100,preserveAspectRatio=True)

        fecha = datetime.now().strftime('%d/%m/%Y ')
        # Estilos de Párrafos
        ta_c = ParagraphStyle('parrafos', 
                            alignment = TA_CENTER,
                            fontSize = 10,
                            fontName="Helvetica",
                            )   
        ta_c1 = ParagraphStyle('parrafos', 
                            alignment = TA_JUSTIFY,
                            fontSize = 14,
                            borderPadding = 20,
                            leading = 18,
                            fontName="Helvetica",

                            )   
        ta_l = ParagraphStyle('parrafos', 
                            alignment = TA_LEFT,
                            fontSize = 15,
                            fontName="Helvetica-Bold",
                            )
        ta_l7 = ParagraphStyle('parrafos', 
                            alignment = TA_CENTER,
                            fontSize = 10,
                            fontName="Helvetica-Bold",
                            )
        ta_l8 = ParagraphStyle('parrafos', 
                            alignment = TA_CENTER,
                            fontSize = 7,
                            fontName="Helvetica",
                            )
        ta_r = ParagraphStyle('parrafos', 
                            alignment = TA_RIGHT,
                            fontSize = 13,
                            fontName="Helvetica-Bold",
                            )

        # Header
        header = Paragraph("CONSTANCIA ",ta_l)
        w,h = header.wrap(doc.width+250, doc.topMargin)
        header.drawOn(canvas, 245, doc.height -10 + doc.topMargin-120)


        content = """
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Quien suscribe, Jefe de Recursos Humanos  <p/> del Hospital Universitario “Dr. Miguel Oraá” de Guanare, 
        por medio de la presente hago constar  que el Ciudadana(o): <b>{}</b>, Titular de la  
        cédula de identidad <b>V–{}</b>, presta sus servicios en esta Institución como: <b>{}</b> {}, siendo su fecha de ingreso desde: <b>{}</b>
        hasta la actualidad.
        <br/>
        <br/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Constancia que se expide para fines legales en la ciudad de Guanare, a los {}.


        """.format(nombre,cedula,cargo,cargo2,fecha_i,dia)
        header1 = Paragraph(content,ta_c1)
        w,h = header1.wrap(doc.width-50, doc.topMargin)
        header1.drawOn(canvas, 55, doc.height -10 + doc.topMargin-340)

        firma = """
            LCDA. SOVEIDA YOLIMAR PEREZ DE M.<br/>
            Jefe de Recursos Humano  del Hospital Universitario<br/>
            “Dr. Miguel Oraá” de Guanare Edo. Portuguesa<br/>
            Según Oficio DESP-18-0042 De Fecha 23/01/2018<br/>

        """
        header2 = Paragraph(firma,ta_l7)
        w,h = header2.wrap(doc.width-50, doc.topMargin)
        header2.drawOn(canvas, 55, doc.height -10 + doc.topMargin-650)

        final = """
        RUMBO A LA CONSOLIDACIÓN DEL SISTEMA PÚBLICO NACIONAL DE SALUD…<br/>
        ”HOSPITAL GENERAL  MIGUEL ORAÁ DE GUANARE EDO PORTUGUESA  AV. LA HILANDERA  URBANIZACIÓN ANDRÉS ELOY BLANCO   GUANARE  –  PORTUGUESA,  RIF:   G   –   20008795 -  1     TELF. (0257)   251-0343 /2517336,  correo: personalmigueloraa@gmil.com.

        """
        header2 = Paragraph(final,ta_l8)
        w,h = header2.wrap(doc.width-50, doc.topMargin)
        header2.drawOn(canvas, 55, doc.height -10 + doc.topMargin-750)

        

        canvas.restoreState()

def TrabajoPDF(request):
    response = HttpResponse(content_type='application/pdf')
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    doc = SimpleDocTemplate(buffer,
        pagesizes=letter,
        rightMargin = 30,
        leftMargin= 30,
        topMargin=176.9,
        bottomMargin=50,
        paginate_by=0,
    )
    ta_r = ParagraphStyle('parrafos', 
        alignment = TA_RIGHT,
        fontSize = 13,
        fontName="Helvetica-Bold",
        )
    persona=[]
    styles = getSampleStyleSheet()
    # TABLA NUMERO 1
    count = 0
    data = []
    data.append(['','','','','','',''])
    x = Table(data)
    trabajador = Trabajador.objects.get(usuario=request.user)
    global expediente
    expediente = Expedientes.objects.get(trabajador=trabajador)
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    hoy = str(datetime.now().strftime('%d/%m/%Y ')).split('/')

    fecha1 = hoy[0]+' dias del mes de '+str(meses[int(hoy[1])-1])+' del '+hoy[2]
    print(hoy,fecha1)
    if expediente:
        global nombre,cedula,cargo,cargo2,rac,fecha_i,dia
        rac = trabajador.cod_rac
        cargo = (trabajador.cargos).upper().strip()
        if cargo == 'EMPLEADO (A)':
            cargo2 = 'en el cargo de: <b>'+str((trabajador.empleados).upper().strip())+'</b>'
        if cargo == 'MEDICO (A)':
            cargo2 = 'grado: <b>'+str((trabajador.grado).upper().strip())+'</b>'
        if cargo == 'OBRERO (A)':
            cargo2 = 'en el cargo de: <b>'+str((trabajador.obreros).upper().strip())+'</b>'
        nombre = (trabajador.nomb_trab + ' '+trabajador.ape_trab).upper().strip() 
        cedula = "{:,}".format(trabajador.cedu_trab).replace(',','.')
        fe = str(trabajador.fech_ing_inst).split('-')
        fecha_i = fe[2]+'/'+fe[1]+'/'+fe[0]
        dia = fecha1.strip()
        
    else:
        print('error')

    persona.append(x)

    doc.build(persona,onFirstPage=HeaderFooterTrabajo,onLaterPages=HeaderFooterTrabajo,canvasmaker=NumberedCanvas)
    response.write(buffer.getvalue())
    buffer.close()

    return response


# PDF de Persona -----------------------------------------------------------------------------
def HeaderFooterTrabajadoSueldo(canvas,doc):
        canvas.saveState()
        title = "Reporte de Ley Politica"
        canvas.setTitle(title)
        
        Story=[]
        styles = getSampleStyleSheet()
        
        archivo_imagen = finders.find('images/cintillo/1.png')
        canvas.drawImage(archivo_imagen, 30, 720, width=540,height=100,preserveAspectRatio=True)

        fecha = datetime.now().strftime('%d/%m/%Y ')
        # Estilos de Párrafos
        ta_c = ParagraphStyle('parrafos', 
                            alignment = TA_CENTER,
                            fontSize = 10,
                            fontName="Helvetica",
                            )   
        ta_c1 = ParagraphStyle('parrafos', 
                            alignment = TA_JUSTIFY,
                            fontSize = 14,
                            borderPadding = 20,
                            leading = 18,
                            fontName="Helvetica",

                            )   
        ta_l = ParagraphStyle('parrafos', 
                            alignment = TA_LEFT,
                            fontSize = 15,
                            fontName="Helvetica-Bold",
                            )
        ta_l7 = ParagraphStyle('parrafos', 
                            alignment = TA_CENTER,
                            fontSize = 10,
                            fontName="Helvetica-Bold",
                            )
        ta_l9 = ParagraphStyle('parrafos', 
                            alignment = TA_LEFT,
                            fontSize = 11,
                            fontName="Helvetica-Bold",
                            )
        ta_l8 = ParagraphStyle('parrafos', 
                            alignment = TA_CENTER,
                            fontSize = 7,
                            fontName="Helvetica",
                            )
        ta_r = ParagraphStyle('parrafos', 
                            alignment = TA_RIGHT,
                            fontSize = 13,
                            fontName="Helvetica-Bold",
                            )

        # Header
        header = Paragraph("CONSTANCIA ",ta_l)
        w,h = header.wrap(doc.width+250, doc.topMargin)
        header.drawOn(canvas, 245, doc.height -10 + doc.topMargin-120)


        content = """
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Quien suscribe, Jefe de Recursos Humanos  <p/> del Hospital Universitario “Dr. Miguel Oraá” de Guanare, 
        por medio de la presente hago constar  que el Ciudadana(o): <b>{}</b>, Titular de la  
        cédula de identidad <b>V–{}</b>, presta sus servicios en esta Institución como: <b>{}</b> {}, código del Rac: <b>{}</b> siendo su fecha de ingreso desde: <b>{}</b>
        hasta la actualidad. devengando las siguientes remuneraciones:
        <br/>
        <br/>
        <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>

        <b>Nota: solo para trámites bancarios.</b>
        <br/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Constancia que se expide para fines legales en la ciudad de Guanare, a los {}.


        """.format(nombre,cedula,cargo,cargo2,rac,fecha_i,dia)
        header1 = Paragraph(content,ta_c1)
        w,h = header1.wrap(doc.width-50, doc.topMargin)
        header1.drawOn(canvas, 55, doc.height -10 + doc.topMargin-500)

        data = [
            ['Sueldo Básico Mensual:','Bs. F.',Paragraph(str(sueldo),ta_r)],
            ['Prima Profesionalización:','Bs. F.',Paragraph(str(profesionalizacion),ta_r)],
            ['Prima Antigüedad:','Bs. F.',Paragraph(str(antiguedad),ta_r)],
            [Paragraph('Total:',ta_l9),'Bs. F.',Paragraph(str(total),ta_r)],
        ]
        if prima_d:
            data.insert(3,['Prima Dedicación Exclusiva a la Salud:','Bs. F.',Paragraph(str(profesionalizacion),ta_r)])
        print(cargo)
        if cargo != 'MEDICO (A)':
            data.insert(1,['Compensación:','Bs. F.',Paragraph(str(compensacion),ta_r)])

        header5 = Table(data, colWidths = [185,35,125])

        w,h = header5.wrap(doc.width-115, doc.topMargin)
        header5.drawOn(canvas, 42.5, doc.height -40 + doc.topMargin-383)
        firma = """
            {}.<br/>
            Jefe de Recursos Humano  del Hospital Universitario<br/>
            “Dr. Miguel Oraá” de Guanare Edo. Portuguesa<br/>
            <br/>

        """.format(nombre_l)
        header2 = Paragraph(firma,ta_l7)
        w,h = header2.wrap(doc.width-50, doc.topMargin)
        header2.drawOn(canvas, 55, doc.height -10 + doc.topMargin-650)

        final = """
        RUMBO A LA CONSOLIDACIÓN DEL SISTEMA PÚBLICO NACIONAL DE SALUD…<br/>
        ”HOSPITAL GENERAL  MIGUEL ORAÁ DE GUANARE EDO PORTUGUESA  AV. LA HILANDERA  URBANIZACIÓN ANDRÉS ELOY BLANCO   GUANARE  –  PORTUGUESA,  RIF:   G   –   20008795 -  1     TELF. (0257)   251-0343 /2517336,  correo: personalmigueloraa@gmail.com.

        """
        header2 = Paragraph(final,ta_l8)
        w,h = header2.wrap(doc.width-50, doc.topMargin)
        header2.drawOn(canvas, 55, doc.height -10 + doc.topMargin-750)

        

        canvas.restoreState()

def TrabajoSueldoPDF(request):
    response = HttpResponse(content_type='application/pdf')
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    doc = SimpleDocTemplate(buffer,
        pagesizes=letter,
        rightMargin = 30,
        leftMargin= 30,
        topMargin=176.9,
        bottomMargin=50,
        paginate_by=0,
    )
    ta_r = ParagraphStyle('parrafos', 
        alignment = TA_RIGHT,
        fontSize = 13,
        fontName="Helvetica-Bold",
        )
    persona=[]
    styles = getSampleStyleSheet()
    # TABLA NUMERO 1
    count = 0
    data = []
    data.append(['','','','','','',''])
    x = Table(data)
    trabajador = Trabajador.objects.get(usuario=request.user)
    global expediente
    expediente = Expedientes.objects.get(trabajador=trabajador)
    sueldo_b = Sueldo.objects.filter(expediente=expediente).last()
    print(sueldo_b)
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    hoy = str(datetime.now().strftime('%d/%m/%Y ')).split('/')

    fecha1 = hoy[0]+' dias del mes de '+str(meses[int(hoy[1])-1])+' del '+hoy[2]
    print(hoy,fecha1)
    if sueldo_b == None:
        messages.add_message(request, messages.INFO, "No puede acceder a este reporte, porque no poseé un sueldo cargado.")
        return redirect('Trabaexpe:Admin')
    else:
        if expediente:
            global nombre,cedula,cargo,cargo2,rac,fecha_i,dia,nombre_l,sueldo,compensacion,profesionalizacion,antiguedad,total,prima_d
            rac = trabajador.cod_rac
            cargo = (trabajador.cargos).upper().strip()
            if cargo == 'EMPLEADO (A)':
                cargo2 = 'en el cargo de: <b>'+str((trabajador.empleados).upper().strip())+'</b>'
            if cargo == 'MEDICO (A)':
                cargo2 = 'grado: <b>'+str((trabajador.grado).upper().strip())+'</b>'
            if cargo == 'OBRERO (A)':
                cargo2 = 'en el cargo de: <b>'+str((trabajador.obreros).upper().strip())+'</b>'

            nombre = (trabajador.nomb_trab + ' '+trabajador.ape_trab).upper().strip()
            nombre_l = (expediente.directores.nomb_direc+' '+expediente.directores.apel_direc).upper().strip()
            cedula = "{:,}".format(trabajador.cedu_trab).replace(',','.')
            fe = str(trabajador.fech_ing_inst).split('-')
            fecha_i = fe[2]+'/'+fe[1]+'/'+fe[0]
            dia = fecha1.strip()
            from decimal import Decimal
            from re import sub
            sueldo = Decimal(sub(r'[^\d.]', '', sueldo_b.sueldo))
            if cargo != 'MEDICO (A)':
                compensacion = Decimal(sub(r'[^\d.]', '', sueldo_b.compensasion))
            else:
                compensacion = '0,00'
            prima_d = ''
            profesionalizacion = Decimal(sub(r'[^\d.]', '', sueldo_b.profesionalizacion))
            antiguedad = Decimal(sub(r'[^\d.]', '', sueldo_b.antiguedad))
            total = Decimal(sub(r'[^\d.]', '', sueldo_b.sueldo))+Decimal(sub(r'[^\d.]', '', sueldo_b.compensasion))+Decimal(sub(r'[^\d.]', '', sueldo_b.profesionalizacion))+Decimal(sub(r'[^\d.]', '', sueldo_b.antiguedad))
            print("{:,}".format(total))
        else:
            print('error')

    persona.append(x)

    doc.build(persona,onFirstPage=HeaderFooterTrabajadoSueldo,onLaterPages=HeaderFooterTrabajadoSueldo,canvasmaker=NumberedCanvas)
    response.write(buffer.getvalue())
    buffer.close()

    return response

# PDF de Persona -----------------------------------------------------------------------------
def HeaderFooterVacaDetail(canvas,doc):
        canvas.saveState()
        title = "Reporte de Ley Politica1"
        canvas.setTitle(title)
        
        Story=[]
        styles = getSampleStyleSheet()
        
        archivo_imagen1 = finders.find('images/cintillo/vaca.png')
        archivo_imagen = finders.find('images/cintillo/1.png')
        canvas.drawImage(archivo_imagen1, 30, 20, width=540,height=800,preserveAspectRatio=True)
        canvas.drawImage(archivo_imagen, 30, 720, width=540,height=100,preserveAspectRatio=True)

        fecha = datetime.now().strftime('%d/%m/%Y ')
        # Estilos de Párrafos
        ta_c = ParagraphStyle('parrafos', 
                            alignment = TA_JUSTIFY,
                            fontSize = 10,
                            fontName="Helvetica",
                            )   
        ta_c1 = ParagraphStyle('parrafos', 
                            alignment = TA_JUSTIFY,
                            fontSize = 12,
                            borderPadding = 20,
                            leading = 18,
                            fontName="Helvetica",

                            )
        #fecha
        fecha1 = Paragraph(str(fecha),ta_c)
        w,h = fecha1.wrap(doc.width+250, doc.topMargin)
        fecha1.drawOn(canvas, 505, doc.height -10 + doc.topMargin-40)

        #estatus
        estatus = Paragraph("Estatus: "+str(vacaciones.estatus),ta_c1)
        w,h = estatus.wrap(doc.width+250, doc.topMargin)
        estatus.drawOn(canvas, 455, doc.height -10 + doc.topMargin-70)

        #nombre
        nombre = Paragraph(vacaciones.periodo.expediente.trabajador.nombre_completo(),ta_c1)
        w,h = nombre.wrap(doc.width+250, doc.topMargin)
        nombre.drawOn(canvas, 45, doc.height -10 + doc.topMargin-170)
        #cedula
        cedula = Paragraph(str(vacaciones.periodo.expediente.trabajador.cedu_trab),ta_c1)
        w,h = cedula.wrap(doc.width+250, doc.topMargin)
        cedula.drawOn(canvas, 425, doc.height -10 + doc.topMargin-170)
        #tipo Obrero (a) 
        if vacaciones.periodo.expediente.trabajador.cargos.strip() == 'Empleado (a)':
            cargos = vacaciones.periodo.expediente.trabajador.empleados.upper()
        elif vacaciones.periodo.expediente.trabajador.cargos.strip() == 'Obrero (a)':
            cargos = vacaciones.periodo.expediente.trabajador.obreros.upper()
        else:
            cargos = vacaciones.periodo.expediente.trabajador.cargos.upper()+' GRADO '+vacaciones.periodo.expediente.trabajador.grado

        cargo = Paragraph(str(cargos),ta_c1)
        w,h = cargo.wrap(doc.width+250, doc.topMargin)
        cargo.drawOn(canvas, 45, doc.height -10 + doc.topMargin-205)

        #codigo
        codigo = Paragraph(str(vacaciones.periodo.expediente.trabajador.pk),ta_c1)
        w,h = codigo.wrap(doc.width+250, doc.topMargin)
        codigo.drawOn(canvas, 475, doc.height -10 + doc.topMargin-205)

        #estatus
        if vacaciones.periodo.expediente.trabajador.estat_traba.strip() == 'Fijo':
            val = 43.2
        else:
            val = 104
        est = Paragraph('x',ta_c1)
        w,h = est.wrap(doc.width+250, doc.topMargin)
        est.drawOn(canvas, val, doc.height -10 + doc.topMargin-359)

        #Tipo Reglamentarias Atrasadas Adelantadas
        if vacaciones.tipo_vaca == 'Reglamentarias':
            val = 218.2
        elif vacaciones.tipo_vaca.strip() == 'Atrasadas':
            val = 301.6
        else:
            val = 371.2
        tip = Paragraph('x',ta_c1)
        w,h = tip.wrap(doc.width+250, doc.topMargin)
        tip.drawOn(canvas, val, doc.height -10 + doc.topMargin-360)

        #ingreso p
        entro_i = Paragraph(str(vacaciones.periodo.expediente.trabajador.fech_ing_pub),ta_c1)
        w,h = entro_i.wrap(doc.width+250, doc.topMargin)
        entro_i.drawOn(canvas, 467, doc.height -10 + doc.topMargin-360)
        
        #institucion
        ints = Paragraph(str(vacaciones.periodo.expediente.trabajador.fech_ing_inst),ta_c1)
        w,h = ints.wrap(doc.width+250, doc.topMargin)
        ints.drawOn(canvas, 60, doc.height -10 + doc.topMargin-410)

        #dias
        dias = Paragraph(str(vacaciones.periodo.dias),ta_c1)
        w,h = dias.wrap(doc.width+250, doc.topMargin)
        dias.drawOn(canvas, 175, doc.height -10 + doc.topMargin-410)

        #fecha_i fech_inic 
        fecha_i = Paragraph(str(vacaciones.fech_inic),ta_c1)
        w,h = fecha_i.wrap(doc.width+250, doc.topMargin)
        fecha_i.drawOn(canvas, 227, doc.height -10 + doc.topMargin-410)

        #fecha_i fech_culm
        fecha_f = Paragraph(str(vacaciones.fech_culm),ta_c1)
        w,h = fecha_f.wrap(doc.width+250, doc.topMargin)
        fecha_f.drawOn(canvas, 343, doc.height -10 + doc.topMargin-410)

        #fecha_r
        fecha_f = Paragraph(str(vacaciones.fech_rein),ta_c1)
        w,h = fecha_f.wrap(doc.width+250, doc.topMargin)
        fecha_f.drawOn(canvas, 467, doc.height -10 + doc.topMargin-410)

         #Observacion
        obs = Paragraph(vacaciones.observacion,ta_c)
        w,h = obs.wrap(doc.width+250, doc.topMargin)
        obs.drawOn(canvas, 45, doc.height -10 + doc.topMargin-450)

        canvas.restoreState()

def VacaDetailPDF(request,pk):
    response = HttpResponse(content_type='application/pdf')
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    doc = SimpleDocTemplate(buffer,
        pagesizes=letter,
        rightMargin = 30,
        leftMargin= 30,
        topMargin=176.9,
        bottomMargin=50,
        paginate_by=0,
    )
    ta_r = ParagraphStyle('parrafos', 
        alignment = TA_RIGHT,
        fontSize = 13,
        fontName="Helvetica-Bold",
        )
    persona=[]
    styles = getSampleStyleSheet()
    # TABLA NUMERO 1
    count = 0
    data = []
    data.append(['','','','','','',''])
    x = Table(data)
    trabajador = Trabajador.objects.get(usuario=request.user)
    expediente = Expedientes.objects.get(trabajador=trabajador)
    global vacaciones
    vacaciones = Vacaciones.objects.get(pk=pk)
        
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    hoy = str(datetime.now().strftime('%d/%m/%Y ')).split('/')

    fecha1 = hoy[0]+' dias del mes de '+str(meses[int(hoy[1])-1])+' del '+hoy[2]
    print(hoy,fecha1)

   

    persona.append(x)

    doc.build(persona,onFirstPage=HeaderFooterVacaDetail,onLaterPages=HeaderFooterVacaDetail,canvasmaker=NumberedCanvas)
    response.write(buffer.getvalue())
    buffer.close()

    return response

# PDF de Persona -----------------------------------------------------------------------------
def HeaderFooterDecaDetail(canvas,doc):
        canvas.saveState()
        title = "Reporte de Ley Politica1"
        canvas.setTitle(title)
        
        Story=[]
        styles = getSampleStyleSheet()
        
        archivo_imagen1 = finders.find('images/cintillo/deca.png')
        archivo_imagen = finders.find('images/cintillo/1.png')
        canvas.drawImage(archivo_imagen1, 30, -5, width=540,height=800,preserveAspectRatio=True)
        canvas.drawImage(archivo_imagen, 30, 720, width=540,height=100,preserveAspectRatio=True)

        fecha = datetime.now().strftime('%d/%m/%Y ')
        # Estilos de Párrafos
        ta_c = ParagraphStyle('parrafos', 
                            alignment = TA_JUSTIFY,
                            fontSize = 10,
                            fontName="Helvetica",
                            )   
        ta_c1 = ParagraphStyle('parrafos', 
                            alignment = TA_JUSTIFY,
                            fontSize = 12,
                            borderPadding = 20,
                            leading = 18,
                            fontName="Helvetica",

                            )

        #Tipo Reglamentarias Atrasadas Adelantadas
        if deca.opci.strip() == 'SOLICITUD DE PERMISO':
            val = 55.2
        elif deca.opci.strip() == 'NOTIFICACIÓN DE INASISTENCIA':
            val = 305.6
        tip = Paragraph('x',ta_c1)
        w,h = tip.wrap(doc.width+250, doc.topMargin)
        tip.drawOn(canvas, val, doc.height -10 + doc.topMargin-82)

        #fecha
        fecha1 = Paragraph(str(fecha),ta_c)
        w,h = fecha1.wrap(doc.width+250, doc.topMargin)
        fecha1.drawOn(canvas, 505, doc.height -10 + doc.topMargin-40)

        #fecha_de_solicitud
        fecs = str(deca.date_joined.date()).split('-')
        fecha_d = Paragraph(fecs[2],ta_c)
        w,h = fecha_d.wrap(doc.width+250, doc.topMargin)
        fecha_d.drawOn(canvas, 400, doc.height -10 + doc.topMargin-126)
        fecha_m = Paragraph(fecs[1],ta_c)
        w,h = fecha_m.wrap(doc.width+250, doc.topMargin)
        fecha_m.drawOn(canvas, 465, doc.height -10 + doc.topMargin-126)
        fecha_a = Paragraph(fecs[0],ta_c)
        w,h = fecha_a.wrap(doc.width+250, doc.topMargin)
        fecha_a.drawOn(canvas, 515, doc.height -10 + doc.topMargin-126)

        #estatus
        estatus = Paragraph("Estatus: "+str(deca.estatus),ta_c1)
        w,h = estatus.wrap(doc.width+250, doc.topMargin)
        estatus.drawOn(canvas, 455, doc.height -10 + doc.topMargin-70)

        #nombre
        nombre = Paragraph(deca.expediente.trabajador.nomb_trab,ta_c)
        w,h = nombre.wrap(doc.width+250, doc.topMargin)
        nombre.drawOn(canvas, 45, doc.height -10 + doc.topMargin-190)
        #apellido
        apellido = Paragraph(deca.expediente.trabajador.ape_trab,ta_c)
        w,h = apellido.wrap(doc.width+250, doc.topMargin)
        apellido.drawOn(canvas, 45, doc.height -10 + doc.topMargin-202)
        #cedula
        cedula = Paragraph(str(deca.expediente.trabajador.cedu_trab),ta_c)
        w,h = cedula.wrap(doc.width+250, doc.topMargin)
        cedula.drawOn(canvas, 185, doc.height -10 + doc.topMargin-195)
 
        #tipo Obrero (a) 
        if deca.expediente.trabajador.cargos.strip() == 'Empleado (a)':
            cargos = deca.expediente.trabajador.empleados.upper()
        elif deca.expediente.trabajador.cargos.strip() == 'Obrero (a)':
            cargos = deca.expediente.trabajador.obreros.upper()
        else:
            cargos = deca.expediente.trabajador.cargos.upper()+' GRADO '+deca.expediente.trabajador.grado

        cargo = Paragraph(str(cargos),ta_c)
        w,h = cargo.wrap(doc.width-410, doc.topMargin)
        cargo.drawOn(canvas, 300, doc.height -10 + doc.topMargin-202)
        canvas.restoreState()

        #codigo
        codigo = Paragraph(str(deca.expediente.trabajador.pk),ta_c1)
        w,h = codigo.wrap(doc.width+250, doc.topMargin)
        codigo.drawOn(canvas, 495, doc.height -10 + doc.topMargin-200)

        #Checkbox             
        if deca.carg_libr_nom == 'on':
            alto = 262.2
            ancho = 35.7
        elif deca.enfer == 'on':
            alto = 288.2
            ancho = 35.7
        elif deca.accid == 'on':
            alto = 305.2
            ancho = 35.7
        elif deca.falle_fami_metro == 'on':
            alto = 322.2
            ancho = 35.7
        elif deca.falle_fami_exte == 'on':
            alto = 340.2
            ancho = 35.7
        elif deca.nacim_hij == 'on':
            alto = 356.2
            ancho = 35.7
        elif deca.com_ant_tribu == 'on':
            alto = 373.2
            ancho = 35.7
        elif deca.matrim == 'on':
            alto = 391.2
            ancho = 35.7
        elif deca.pre_natal == 'on':
            alto = 408.2
            ancho = 35.7
        elif deca.post_natal == 'on':
            alto = 425.2
            ancho = 35.7
        elif deca.asis_curs_confe == 'on':
            alto = 262.2
            ancho = 313.7
        elif deca.enfer_fami == 'on':
            alto = 288.2
            ancho = 313.7
        elif deca.estu_acade == 'on':
            alto = 305.2
            ancho = 313.7
        elif deca.dili_pers == 'on':
            alto = 330.2
            ancho = 313.7
        elif deca.otro:
            alto = 348.2
            ancho = 313.7
            otro = Paragraph(deca.otro,ta_c)
            w,h = otro.wrap(doc.width-300, doc.topMargin)
            otro.drawOn(canvas, ancho, doc.height -10 + doc.topMargin-alto-25)
        tip = Paragraph('x',ta_c1)
        w,h = tip.wrap(doc.width+250, doc.topMargin)
        tip.drawOn(canvas, ancho, doc.height -10 + doc.topMargin-alto)
        
        if deca.estatus != 'Pendiente':
            #observacion
            obs = Paragraph(deca.observacion,ta_c)
            w,h = obs.wrap(doc.width+250, doc.topMargin)
            obs.drawOn(canvas, 45, doc.height -10 + doc.topMargin-465)

        #desde
        des = Paragraph(str(deca.fech_solici),ta_c)
        w,h = des.wrap(doc.width+250, doc.topMargin)
        des.drawOn(canvas, 65, doc.height -10 + doc.topMargin-555)

        #hasta
        has = Paragraph(str(deca.fech_fin),ta_c)
        w,h = has.wrap(doc.width+250, doc.topMargin)
        has.drawOn(canvas, 215, doc.height -10 + doc.topMargin-555)

def DecaDetailPDF(request,pk):
    response = HttpResponse(content_type='application/pdf')
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    doc = SimpleDocTemplate(buffer,
        pagesizes=letter,
        rightMargin = 30,
        leftMargin= 30,
        topMargin=176.9,
        bottomMargin=50,
        paginate_by=0,
    )
    ta_r = ParagraphStyle('parrafos', 
        alignment = TA_RIGHT,
        fontSize = 13,
        fontName="Helvetica-Bold",
        )
    persona=[]
    styles = getSampleStyleSheet()
    # TABLA NUMERO 1
    count = 0
    data = []
    data.append(['','','','','','',''])
    x = Table(data)
    global deca
    deca = Descan_Trimes.objects.get(pk=pk)
    print(deca)
        
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    hoy = str(datetime.now().strftime('%d/%m/%Y ')).split('/')

    fecha1 = hoy[0]+' dias del mes de '+str(meses[int(hoy[1])-1])+' del '+hoy[2]
    print(hoy,fecha1)

   

    persona.append(x)

    doc.build(persona,onFirstPage=HeaderFooterDecaDetail,onLaterPages=HeaderFooterDecaDetail,canvasmaker=NumberedCanvas)
    response.write(buffer.getvalue())
    buffer.close()

    return response

# PDF de Alimentos -----------------------------------------------------------------------------
def HeaderFooterDes(canvas,doc):
        canvas.saveState()
        title = "Reporte"
        canvas.setTitle(title)
        
        Story=[]
        styles = getSampleStyleSheet()
        
        archivo_imagen = finders.find('images/cintillo/1.png')
        canvas.drawImage(archivo_imagen, 30, 720, width=540,height=100,preserveAspectRatio=True)

        fecha = datetime.now().strftime('%d/%m/%Y ')
        # Estilos de Párrafos
        ta_c = ParagraphStyle('parrafos', 
                            alignment = TA_CENTER,
                            fontSize = 9,
                            fontName="Helvetica",
                            )   
        ta_l = ParagraphStyle('parrafos', 
                            alignment = TA_LEFT,
                            fontSize = 13,
                            fontName="Helvetica-Bold",
                            )
        ta_l7 = ParagraphStyle('parrafos', 
                            alignment = TA_LEFT,
                            fontSize = 7,
                            fontName="Helvetica-Bold",
                            )
        ta_r = ParagraphStyle('parrafos', 
                            alignment = TA_RIGHT,
                            fontSize = 13,
                            fontName="Helvetica-Bold",
                            )

        # Header
        header = Paragraph("Listado de Descansos Trimestrales ",ta_l,)
        w,h = header.wrap(doc.width+250, doc.topMargin)
        header.drawOn(canvas, 215, doc.height -10 + doc.topMargin-80)

        #header1 = Paragraph("<u>DIRECCIÓN DE AGRICULTURA Y TIERRA</u> ",ta_r,)
        #w,h = header1.wrap(doc.width-115, doc.topMargin)
        #header1.drawOn(canvas, 140, doc.height -10 + doc.topMargin - 2)
        
        P1 = Paragraph('''N°''',ta_c)
        P2 = Paragraph('''Nombre del trabajador''',ta_c)
        P3 = Paragraph('''Fecha inicio''',ta_c)
        P4 = Paragraph('''Fecha Fin''',ta_c)
        P5 = Paragraph('''Tipo''',ta_c)
        P6 = Paragraph('''Estatus''',ta_c)
        data = [[P1, P2, P3, P4,P5,P6]]
        header2 = Table(data, colWidths = [35,120,60,60,160,60])
        header2.setStyle(TableStyle( 
            [   
                ('GRID', (0, -1), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), '#a4bfd4d1'),
                ('ALIGN', (0, 0), (-1, -3), "CENTER"),
            ]
            ))
        w,h = header2.wrap(doc.width-115, doc.topMargin)
        header2.drawOn(canvas, 50, doc.height -40 + doc.topMargin-93)

       

        # FOOTER

        footer4 = Paragraph("Fecha: "+str(fecha),ta_l7)
        w, h = footer4.wrap(doc.width -200, doc.bottomMargin) 
        footer4.drawOn(canvas,doc.height-105, doc.topMargin +625, h)

        canvas.restoreState()

def DescansoPDF(request):
    response = HttpResponse(content_type='application/pdf')
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    doc = SimpleDocTemplate(buffer,
        pagesizes=letter,
        rightMargin = 30,
        leftMargin= 30,
        topMargin=176.9,
        bottomMargin=50,
        paginate_by=0,
    )
    ta_r = ParagraphStyle('parrafos', 
        alignment = TA_RIGHT,
        fontSize = 13,
        fontName="Helvetica-Bold",
        )
    persona=[]
    styles = getSampleStyleSheet()
    # TABLA NUMERO 1
    count = 0
    data = []
    c = Descan_Trimes.objects.all().order_by('-id')
    if c:
        for i in c:
            count =count+1 
            data.append([count,i.expediente.trabajador.nomb_trab,i.fech_solici,i.fech_fin,i.opci,i.estatus])
    else:
        return redirect('Constancias:Listdes_trim')
    print(data)
    x = Table(data, colWidths = [35,120,60,60,160,60])
    x.setStyle(TableStyle(
        [   
            ('GRID', (0, 0), (12, -1), 1, colors.black),
            ('ALIGN',(0,0),(3,-1),'CENTER'),
            ('FONTSIZE', (0, 0), (5, -1), 8),   
        ]
    ))
    persona.append(x)

    doc.build(persona,onFirstPage=HeaderFooterDes,onLaterPages=HeaderFooterDes,canvasmaker=NumberedCanvas)
    response.write(buffer.getvalue())
    buffer.close()

    return response

# PDF de Alimentos -----------------------------------------------------------------------------
def HeaderFooterVac(canvas,doc):
        canvas.saveState()
        title = "Reporte"
        canvas.setTitle(title)
        
        Story=[]
        styles = getSampleStyleSheet()
        
        archivo_imagen = finders.find('images/cintillo/1.png')
        canvas.drawImage(archivo_imagen, 30, 720, width=540,height=100,preserveAspectRatio=True)

        fecha = datetime.now().strftime('%d/%m/%Y ')
        # Estilos de Párrafos
        ta_c = ParagraphStyle('parrafos', 
                            alignment = TA_CENTER,
                            fontSize = 9,
                            fontName="Helvetica",
                            )   
        ta_l = ParagraphStyle('parrafos', 
                            alignment = TA_LEFT,
                            fontSize = 13,
                            fontName="Helvetica-Bold",
                            )
        ta_l7 = ParagraphStyle('parrafos', 
                            alignment = TA_LEFT,
                            fontSize = 7,
                            fontName="Helvetica-Bold",
                            )
        ta_r = ParagraphStyle('parrafos', 
                            alignment = TA_RIGHT,
                            fontSize = 13,
                            fontName="Helvetica-Bold",
                            )

        # Header
        header = Paragraph("Listado de Vacaciones ",ta_l,)
        w,h = header.wrap(doc.width+250, doc.topMargin)
        header.drawOn(canvas, 215, doc.height -10 + doc.topMargin-80)

        #header1 = Paragraph("<u>DIRECCIÓN DE AGRICULTURA Y TIERRA</u> ",ta_r,)
        #w,h = header1.wrap(doc.width-115, doc.topMargin)
        #header1.drawOn(canvas, 140, doc.height -10 + doc.topMargin - 2)
        
        P1 = Paragraph('''N°''',ta_c)
        P2 = Paragraph('''Nombre del trabajador''',ta_c)
        P3 = Paragraph('''Fecha inicio''',ta_c)
        P4 = Paragraph('''Fecha Fin''',ta_c)
        P5 = Paragraph('''Tipo''',ta_c)
        P6 = Paragraph('''Estatus''',ta_c)
        data = [[P1, P2, P3, P4,P5,P6]]
        header2 = Table(data, colWidths = [35,120,60,60,160,60])
        header2.setStyle(TableStyle( 
            [   
                ('GRID', (0, -1), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), '#a4bfd4d1'),
                ('ALIGN', (0, 0), (-1, -3), "CENTER"),
            ]
            ))
        w,h = header2.wrap(doc.width-115, doc.topMargin)
        header2.drawOn(canvas, 50, doc.height -40 + doc.topMargin-93)

       

        # FOOTER

        footer4 = Paragraph("Fecha: "+str(fecha),ta_l7)
        w, h = footer4.wrap(doc.width -200, doc.bottomMargin) 
        footer4.drawOn(canvas,doc.height-105, doc.topMargin +625, h)

        canvas.restoreState()

def VacacionesPDF(request):
    response = HttpResponse(content_type='application/pdf')
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    doc = SimpleDocTemplate(buffer,
        pagesizes=letter,
        rightMargin = 30,
        leftMargin= 30,
        topMargin=176.9,
        bottomMargin=50,
        paginate_by=0,
    )
    ta_r = ParagraphStyle('parrafos', 
        alignment = TA_RIGHT,
        fontSize = 13,
        fontName="Helvetica-Bold",
        )
    persona=[]
    styles = getSampleStyleSheet()
    # TABLA NUMERO 1
    count = 0
    data = []
    c = Vacaciones.objects.all().order_by('-id')
    if c:
        for i in c:
            count =count+1 
            data.append([count,i.periodo.expediente.trabajador.nomb_trab,i.fech_inic,i.fech_culm,i.tipo_vaca,i.estatus])
    else:
        return redirect('Constancias:Listvaca')
    print(data)
    x = Table(data, colWidths = [35,120,60,60,160,60])
    x.setStyle(TableStyle(
        [   
            ('GRID', (0, 0), (12, -1), 1, colors.black),
            ('ALIGN',(0,0),(3,-1),'CENTER'),
            ('FONTSIZE', (0, 0), (5, -1), 8),   
        ]
    ))
    persona.append(x)

    doc.build(persona,onFirstPage=HeaderFooterVac,onLaterPages=HeaderFooterVac,canvasmaker=NumberedCanvas)
    response.write(buffer.getvalue())
    buffer.close()

    return response

# PDF de Alimentos -----------------------------------------------------------------------------
def HeaderFooterVac(canvas,doc):
        canvas.saveState()
        title = "Reporte"
        canvas.setTitle(title)
        
        Story=[]
        styles = getSampleStyleSheet()
        
        archivo_imagen = finders.find('images/cintillo/1.png')
        canvas.drawImage(archivo_imagen, 30, 720, width=540,height=100,preserveAspectRatio=True)

        fecha = datetime.now().strftime('%d/%m/%Y ')
        # Estilos de Párrafos
        ta_c = ParagraphStyle('parrafos', 
                            alignment = TA_CENTER,
                            fontSize = 9,
                            fontName="Helvetica",
                            )   
        ta_l = ParagraphStyle('parrafos', 
                            alignment = TA_LEFT,
                            fontSize = 13,
                            fontName="Helvetica-Bold",
                            )
        ta_l7 = ParagraphStyle('parrafos', 
                            alignment = TA_LEFT,
                            fontSize = 7,
                            fontName="Helvetica-Bold",
                            )
        ta_r = ParagraphStyle('parrafos', 
                            alignment = TA_RIGHT,
                            fontSize = 13,
                            fontName="Helvetica-Bold",
                            )

        # Header
        header = Paragraph("Listado de Vacaciones ",ta_l,)
        w,h = header.wrap(doc.width+250, doc.topMargin)
        header.drawOn(canvas, 215, doc.height -10 + doc.topMargin-80)

        #header1 = Paragraph("<u>DIRECCIÓN DE AGRICULTURA Y TIERRA</u> ",ta_r,)
        #w,h = header1.wrap(doc.width-115, doc.topMargin)
        #header1.drawOn(canvas, 140, doc.height -10 + doc.topMargin - 2)
        
        P1 = Paragraph('''N°''',ta_c)
        P2 = Paragraph('''Nombre del trabajador''',ta_c)
        P3 = Paragraph('''Fecha inicio''',ta_c)
        P4 = Paragraph('''Fecha Fin''',ta_c)
        P5 = Paragraph('''Tipo''',ta_c)
        P6 = Paragraph('''Estatus''',ta_c)
        data = [[P1, P2, P3, P4,P5,P6]]
        header2 = Table(data, colWidths = [35,120,60,60,160,60])
        header2.setStyle(TableStyle( 
            [   
                ('GRID', (0, -1), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), '#a4bfd4d1'),
                ('ALIGN', (0, 0), (-1, -3), "CENTER"),
            ]
            ))
        w,h = header2.wrap(doc.width-115, doc.topMargin)
        header2.drawOn(canvas, 50, doc.height -40 + doc.topMargin-93)

       

        # FOOTER

        footer4 = Paragraph("Fecha: "+str(fecha),ta_l7)
        w, h = footer4.wrap(doc.width -200, doc.bottomMargin) 
        footer4.drawOn(canvas,doc.height-105, doc.topMargin +625, h)

        canvas.restoreState()

def VacacionesPDF(request):
    response = HttpResponse(content_type='application/pdf')
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    doc = SimpleDocTemplate(buffer,
        pagesizes=letter,
        rightMargin = 30,
        leftMargin= 30,
        topMargin=176.9,
        bottomMargin=50,
        paginate_by=0,
    )
    ta_r = ParagraphStyle('parrafos', 
        alignment = TA_RIGHT,
        fontSize = 13,
        fontName="Helvetica-Bold",
        )
    persona=[]
    styles = getSampleStyleSheet()
    # TABLA NUMERO 1
    count = 0
    data = []
    c = Vacaciones.objects.all().order_by('-id')
    if c:
        for i in c:
            count =count+1 
            data.append([count,i.periodo.expediente.trabajador.nomb_trab,i.fech_inic,i.fech_culm,i.tipo_vaca,i.estatus])
    else:
        return redirect('Constancias:Listvaca')
    print(data)
    x = Table(data, colWidths = [35,120,60,60,160,60])
    x.setStyle(TableStyle(
        [   
            ('GRID', (0, 0), (12, -1), 1, colors.black),
            ('ALIGN',(0,0),(3,-1),'CENTER'),
            ('FONTSIZE', (0, 0), (5, -1), 8),   
        ]
    ))
    persona.append(x)

    doc.build(persona,onFirstPage=HeaderFooterVac,onLaterPages=HeaderFooterVac,canvasmaker=NumberedCanvas)
    response.write(buffer.getvalue())
    buffer.close()

    return response

# PDF de Alimentos -----------------------------------------------------------------------------
def HeaderFooterTrab(canvas,doc):
        canvas.saveState()
        title = "Reporte"
        canvas.setTitle(title)
        
        Story=[]
        styles = getSampleStyleSheet()
        
        archivo_imagen = finders.find('images/cintillo/1.png')
        canvas.drawImage(archivo_imagen, 30, 720, width=540,height=100,preserveAspectRatio=True)

        fecha = datetime.now().strftime('%d/%m/%Y ')
        # Estilos de Párrafos
        ta_c = ParagraphStyle('parrafos', 
                            alignment = TA_CENTER,
                            fontSize = 9,
                            fontName="Helvetica",
                            )   
        ta_l = ParagraphStyle('parrafos', 
                            alignment = TA_LEFT,
                            fontSize = 13,
                            fontName="Helvetica-Bold",
                            )
        ta_l7 = ParagraphStyle('parrafos', 
                            alignment = TA_LEFT,
                            fontSize = 7,
                            fontName="Helvetica-Bold",
                            )
        ta_r = ParagraphStyle('parrafos', 
                            alignment = TA_RIGHT,
                            fontSize = 13,
                            fontName="Helvetica-Bold",
                            )

        # Header
        header = Paragraph("Listado de Trabajadores ",ta_l,)
        w,h = header.wrap(doc.width+250, doc.topMargin)
        header.drawOn(canvas, 215, doc.height -10 + doc.topMargin-80)

        #header1 = Paragraph("<u>DIRECCIÓN DE AGRICULTURA Y TIERRA</u> ",ta_r,)
        #w,h = header1.wrap(doc.width-115, doc.topMargin)
        #header1.drawOn(canvas, 140, doc.height -10 + doc.topMargin - 2)
        
        P1 = Paragraph('''N°''',ta_c)
        P2 = Paragraph('''Cedula''',ta_c)
        P3 = Paragraph('''Nombre''',ta_c)
        P4 = Paragraph('''Apellido''',ta_c)
        P5 = Paragraph('''Cargo''',ta_c)
        data = [[P1, P2, P3, P4,P5]]
        header2 = Table(data, colWidths = [35,60,120,120,120])
        header2.setStyle(TableStyle( 
            [   
                ('GRID', (0, -1), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), '#a4bfd4d1'),
                ('ALIGN', (0, 0), (-1, -3), "CENTER"),
            ]
            ))
        w,h = header2.wrap(doc.width-115, doc.topMargin)
        header2.drawOn(canvas,70, doc.height -40 + doc.topMargin-93)

       

        # FOOTER

        footer4 = Paragraph("Fecha: "+str(fecha),ta_l7)
        w, h = footer4.wrap(doc.width -200, doc.bottomMargin) 
        footer4.drawOn(canvas,doc.height-105, doc.topMargin +625, h)

        canvas.restoreState()

def TrabajadoresPDF(request):
    response = HttpResponse(content_type='application/pdf')
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    doc = SimpleDocTemplate(buffer,
        pagesizes=letter,
        rightMargin = 30,
        leftMargin= 30,
        topMargin=176.9,
        bottomMargin=50,
        paginate_by=0,
    )
    ta_r = ParagraphStyle('parrafos', 
        alignment = TA_RIGHT,
        fontSize = 13,
        fontName="Helvetica-Bold",
        )
    persona=[]
    styles = getSampleStyleSheet()
    # TABLA NUMERO 1
    count = 0
    data = []
    c = Trabajador.objects.all().order_by('-id')
    if c:
        for i in c:
            count =count+1 
            data.append([count,i.cedu_trab,i.nomb_trab,i.ape_trab,i.cargos])
    else:
        return redirect('Trabaexpe:Listworker')
    print(data)
    x = Table(data, colWidths = [35,60,120,120,120])
    x.setStyle(TableStyle(
        [   
            ('GRID', (0, 0), (12, -1), 1, colors.black),
            ('ALIGN',(0,0),(3,-1),'CENTER'),
            ('FONTSIZE', (0, 0), (4, -1), 8),   
        ]
    ))
    persona.append(x)

    doc.build(persona,onFirstPage=HeaderFooterTrab,onLaterPages=HeaderFooterTrab,canvasmaker=NumberedCanvas)
    response.write(buffer.getvalue())
    buffer.close()

    return response

# PDF de Alimentos -----------------------------------------------------------------------------
def HeaderFootercam(canvas,doc):
        canvas.saveState()
        title = "Reporte"
        canvas.setTitle(title)
        
        Story=[]
        styles = getSampleStyleSheet()
        
        archivo_imagen = finders.find('images/cintillo/1.png')
        canvas.drawImage(archivo_imagen, 30, 720, width=540,height=100,preserveAspectRatio=True)

        fecha = datetime.now().strftime('%d/%m/%Y ')
        # Estilos de Párrafos
        ta_c = ParagraphStyle('parrafos', 
                            alignment = TA_CENTER,
                            fontSize = 9,
                            fontName="Helvetica",
                            )   
        ta_l = ParagraphStyle('parrafos', 
                            alignment = TA_LEFT,
                            fontSize = 13,
                            fontName="Helvetica-Bold",
                            )
        ta_l7 = ParagraphStyle('parrafos', 
                            alignment = TA_LEFT,
                            fontSize = 7,
                            fontName="Helvetica-Bold",
                            )
        ta_r = ParagraphStyle('parrafos', 
                            alignment = TA_RIGHT,
                            fontSize = 13,
                            fontName="Helvetica-Bold",
                            )

        # Header
        header = Paragraph("Listado de Cambio de Institución ",ta_l,)
        w,h = header.wrap(doc.width+250, doc.topMargin)
        header.drawOn(canvas, 215, doc.height -10 + doc.topMargin-80)

        #header1 = Paragraph("<u>DIRECCIÓN DE AGRICULTURA Y TIERRA</u> ",ta_r,)
        #w,h = header1.wrap(doc.width-115, doc.topMargin)
        #header1.drawOn(canvas, 140, doc.height -10 + doc.topMargin - 2)
        
        P1 = Paragraph('''N°''',ta_c)
        P2 = Paragraph('''Cedula''',ta_c)
        P3 = Paragraph('''Nombre''',ta_c)
        P4 = Paragraph('''Apellido''',ta_c)
        P5 = Paragraph('''Estatus''',ta_c)
        data = [[P1, P2, P3, P4,P5]]
        header2 = Table(data, colWidths = [35,60,120,120,120])
        header2.setStyle(TableStyle( 
            [   
                ('GRID', (0, -1), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), '#a4bfd4d1'),
                ('ALIGN', (0, 0), (-1, -3), "CENTER"),
            ]
            ))
        w,h = header2.wrap(doc.width-115, doc.topMargin)
        header2.drawOn(canvas,70, doc.height -40 + doc.topMargin-93)

       

        # FOOTER

        footer4 = Paragraph("Fecha: "+str(fecha),ta_l7)
        w, h = footer4.wrap(doc.width -200, doc.bottomMargin) 
        footer4.drawOn(canvas,doc.height-105, doc.topMargin +625, h)

        canvas.restoreState()

def CambioPDF(request):
    response = HttpResponse(content_type='application/pdf')
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    doc = SimpleDocTemplate(buffer,
        pagesizes=letter,
        rightMargin = 30,
        leftMargin= 30,
        topMargin=176.9,
        bottomMargin=50,
        paginate_by=0,
    )
    ta_r = ParagraphStyle('parrafos', 
        alignment = TA_RIGHT,
        fontSize = 13,
        fontName="Helvetica-Bold",
        )
    persona=[]
    styles = getSampleStyleSheet()
    # TABLA NUMERO 1
    count = 0
    data = []
    c = Cambio.objects.all().order_by('-id')
    if c:
        for i in c:
            count =count+1 
            data.append([count,i.expediente.trabajador.cedu_trab,i.expediente.trabajador.nomb_trab,i.expediente.trabajador.ape_trab,i.estatus])
    else:
        return redirect('Constancias:Listreti')
    print(data)
    x = Table(data, colWidths = [35,60,120,120,120])
    x.setStyle(TableStyle(
        [   
            ('GRID', (0, 0), (12, -1), 1, colors.black),
            ('ALIGN',(0,0),(3,-1),'CENTER'),
            ('FONTSIZE', (0, 0), (4, -1), 8),   
        ]
    ))
    persona.append(x)

    doc.build(persona,onFirstPage=HeaderFootercam,onLaterPages=HeaderFootercam,canvasmaker=NumberedCanvas)
    response.write(buffer.getvalue())
    buffer.close()

    return response

# PDF de Alimentos -----------------------------------------------------------------------------
def HeaderFooterjub(canvas,doc):
        canvas.saveState()
        title = "Reporte"
        canvas.setTitle(title)
        
        Story=[]
        styles = getSampleStyleSheet()
        
        archivo_imagen = finders.find('images/cintillo/1.png')
        canvas.drawImage(archivo_imagen, 30, 720, width=540,height=100,preserveAspectRatio=True)

        fecha = datetime.now().strftime('%d/%m/%Y ')
        # Estilos de Párrafos
        ta_c = ParagraphStyle('parrafos', 
                            alignment = TA_CENTER,
                            fontSize = 9,
                            fontName="Helvetica",
                            )   
        ta_l = ParagraphStyle('parrafos', 
                            alignment = TA_LEFT,
                            fontSize = 13,
                            fontName="Helvetica-Bold",
                            )
        ta_l7 = ParagraphStyle('parrafos', 
                            alignment = TA_LEFT,
                            fontSize = 7,
                            fontName="Helvetica-Bold",
                            )
        ta_r = ParagraphStyle('parrafos', 
                            alignment = TA_RIGHT,
                            fontSize = 13,
                            fontName="Helvetica-Bold",
                            )

        # Header
        header = Paragraph("Listado de Jubilación ",ta_l,)
        w,h = header.wrap(doc.width+250, doc.topMargin)
        header.drawOn(canvas, 215, doc.height -10 + doc.topMargin-80)

        #header1 = Paragraph("<u>DIRECCIÓN DE AGRICULTURA Y TIERRA</u> ",ta_r,)
        #w,h = header1.wrap(doc.width-115, doc.topMargin)
        #header1.drawOn(canvas, 140, doc.height -10 + doc.topMargin - 2)
        
        P1 = Paragraph('''N°''',ta_c)
        P2 = Paragraph('''Cedula''',ta_c)
        P3 = Paragraph('''Nombre''',ta_c)
        P4 = Paragraph('''Fecha''',ta_c)
        P5 = Paragraph('''Estatus''',ta_c)
        data = [[P1, P2, P3, P4,P5]]
        header2 = Table(data, colWidths = [35,60,120,120,120])
        header2.setStyle(TableStyle( 
            [   
                ('GRID', (0, -1), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), '#a4bfd4d1'),
                ('ALIGN', (0, 0), (-1, -3), "CENTER"),
            ]
            ))
        w,h = header2.wrap(doc.width-115, doc.topMargin)
        header2.drawOn(canvas,70, doc.height -40 + doc.topMargin-93)

       

        # FOOTER

        footer4 = Paragraph("Fecha: "+str(fecha),ta_l7)
        w, h = footer4.wrap(doc.width -200, doc.bottomMargin) 
        footer4.drawOn(canvas,doc.height-105, doc.topMargin +625, h)

        canvas.restoreState()

def JubPDF(request):
    response = HttpResponse(content_type='application/pdf')
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    doc = SimpleDocTemplate(buffer,
        pagesizes=letter,
        rightMargin = 30,
        leftMargin= 30,
        topMargin=176.9,
        bottomMargin=50,
        paginate_by=0,
    )
    ta_r = ParagraphStyle('parrafos', 
        alignment = TA_RIGHT,
        fontSize = 13,
        fontName="Helvetica-Bold",
        )
    persona=[]
    styles = getSampleStyleSheet()
    # TABLA NUMERO 1
    count = 0
    data = []
    c = Jubilacion.objects.all().order_by('-id')
    if c:
        for i in c:
            count =count+1 
            data.append([count,i.expediente.trabajador.cedu_trab,i.expediente.trabajador.nomb_trab,i.fecha_s.date(),i.estatus])
    else:
        return redirect('Constancias:Listjubi')
    print(data)
    x = Table(data, colWidths = [35,60,120,120,120])
    x.setStyle(TableStyle(
        [   
            ('GRID', (0, 0), (12, -1), 1, colors.black),
            ('ALIGN',(0,0),(3,-1),'CENTER'),
            ('FONTSIZE', (0, 0), (4, -1), 8),   
        ]
    ))
    persona.append(x)

    doc.build(persona,onFirstPage=HeaderFooterjub,onLaterPages=HeaderFooterjub,canvasmaker=NumberedCanvas)
    response.write(buffer.getvalue())
    buffer.close()

    return response

# PDF de Alimentos -----------------------------------------------------------------------------
def HeaderFooterseg(canvas,doc):
        canvas.saveState()
        title = "Reporte"
        canvas.setTitle(title)
        
        Story=[]
        styles = getSampleStyleSheet()
        
        archivo_imagen = finders.find('images/cintillo/1.png')
        canvas.drawImage(archivo_imagen, 30, 720, width=540,height=100,preserveAspectRatio=True)

        fecha = datetime.now().strftime('%d/%m/%Y ')
        # Estilos de Párrafos
        ta_c = ParagraphStyle('parrafos', 
                            alignment = TA_CENTER,
                            fontSize = 9,
                            fontName="Helvetica",
                            )   
        ta_l = ParagraphStyle('parrafos', 
                            alignment = TA_LEFT,
                            fontSize = 13,
                            fontName="Helvetica-Bold",
                            )
        ta_l7 = ParagraphStyle('parrafos', 
                            alignment = TA_LEFT,
                            fontSize = 7,
                            fontName="Helvetica-Bold",
                            )
        ta_r = ParagraphStyle('parrafos', 
                            alignment = TA_RIGHT,
                            fontSize = 13,
                            fontName="Helvetica-Bold",
                            )

        # Header
        header = Paragraph("Listado de Seguro Social ",ta_l,)
        w,h = header.wrap(doc.width+250, doc.topMargin)
        header.drawOn(canvas, 215, doc.height -10 + doc.topMargin-80)

        #header1 = Paragraph("<u>DIRECCIÓN DE AGRICULTURA Y TIERRA</u> ",ta_r,)
        #w,h = header1.wrap(doc.width-115, doc.topMargin)
        #header1.drawOn(canvas, 140, doc.height -10 + doc.topMargin - 2)
        
        P1 = Paragraph('''N°''',ta_c)
        P2 = Paragraph('''Cedula''',ta_c)
        P3 = Paragraph('''Nombre''',ta_c)
        P4 = Paragraph('''Fecha''',ta_c)
        P5 = Paragraph('''Tipo''',ta_c)
        P6 = Paragraph('''Estatus''',ta_c)
        data = [[P1, P2, P3, P4,P5,P6]]
        header2 = Table(data, colWidths = [35,60,120,80,80,120])
        header2.setStyle(TableStyle( 
            [   
                ('GRID', (0, -1), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), '#a4bfd4d1'),
                ('ALIGN', (0, 0), (-1, -3), "CENTER"),
            ]
            ))
        w,h = header2.wrap(doc.width-115, doc.topMargin)
        header2.drawOn(canvas,50, doc.height -40 + doc.topMargin-93)

       

        # FOOTER

        footer4 = Paragraph("Fecha: "+str(fecha),ta_l7)
        w, h = footer4.wrap(doc.width -200, doc.bottomMargin) 
        footer4.drawOn(canvas,doc.height-105, doc.topMargin +625, h)

        canvas.restoreState()

def SegPDF(request):
    response = HttpResponse(content_type='application/pdf')
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    doc = SimpleDocTemplate(buffer,
        pagesizes=letter,
        rightMargin = 30,
        leftMargin= 30,
        topMargin=176.9,
        bottomMargin=50,
        paginate_by=0,
    )
    ta_r = ParagraphStyle('parrafos', 
        alignment = TA_RIGHT,
        fontSize = 13,
        fontName="Helvetica-Bold",
        )
    persona=[]
    styles = getSampleStyleSheet()
    # TABLA NUMERO 1
    count = 0
    data = []
    c = Segu_Social.objects.all().order_by('-id')
    if c:
        for i in c:
            count =count+1 
            data.append([count,i.expediente.trabajador.cedu_trab,i.expediente.trabajador.nomb_trab,i.fech_func,i.esta_seg_soc,i.estatus])
    else:
        return redirect('Constancias:Listseg')
    print(data)
    x = Table(data, colWidths = [35,60,120,80,80,120])
    x.setStyle(TableStyle(
        [   
            ('GRID', (0, 0), (12, -1), 1, colors.black),
            ('ALIGN',(0,0),(3,-1),'CENTER'),
            ('FONTSIZE', (0, 0), (5, -1), 8),   
        ]
    ))
    persona.append(x)

    doc.build(persona,onFirstPage=HeaderFooterseg,onLaterPages=HeaderFooterseg,canvasmaker=NumberedCanvas)
    response.write(buffer.getvalue())
    buffer.close()

    return response

# PDF de Alimentos -----------------------------------------------------------------------------
def HeaderFooterpen(canvas,doc):
        canvas.saveState()
        title = "Reporte"
        canvas.setTitle(title)
        
        Story=[]
        styles = getSampleStyleSheet()
        
        archivo_imagen = finders.find('images/cintillo/1.png')
        canvas.drawImage(archivo_imagen, 30, 720, width=540,height=100,preserveAspectRatio=True)

        fecha = datetime.now().strftime('%d/%m/%Y ')
        # Estilos de Párrafos
        ta_c = ParagraphStyle('parrafos', 
                            alignment = TA_CENTER,
                            fontSize = 9,
                            fontName="Helvetica",
                            )   
        ta_l = ParagraphStyle('parrafos', 
                            alignment = TA_LEFT,
                            fontSize = 13,
                            fontName="Helvetica-Bold",
                            )
        ta_l7 = ParagraphStyle('parrafos', 
                            alignment = TA_LEFT,
                            fontSize = 7,
                            fontName="Helvetica-Bold",
                            )
        ta_r = ParagraphStyle('parrafos', 
                            alignment = TA_RIGHT,
                            fontSize = 13,
                            fontName="Helvetica-Bold",
                            )

        # Header
        header = Paragraph("Listado de Pensión ",ta_l,)
        w,h = header.wrap(doc.width+250, doc.topMargin)
        header.drawOn(canvas, 215, doc.height -10 + doc.topMargin-80)

        #header1 = Paragraph("<u>DIRECCIÓN DE AGRICULTURA Y TIERRA</u> ",ta_r,)
        #w,h = header1.wrap(doc.width-115, doc.topMargin)
        #header1.drawOn(canvas, 140, doc.height -10 + doc.topMargin - 2)
        
        P1 = Paragraph('''N°''',ta_c)
        P2 = Paragraph('''Cedula''',ta_c)
        P3 = Paragraph('''Nombre''',ta_c)
        P4 = Paragraph('''Fecha''',ta_c)
        P5 = Paragraph('''Estatus''',ta_c)
        data = [[P1, P2, P3, P4,P5]]
        header2 = Table(data, colWidths = [35,60,120,120,120])
        header2.setStyle(TableStyle( 
            [   
                ('GRID', (0, -1), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), '#a4bfd4d1'),
                ('ALIGN', (0, 0), (-1, -3), "CENTER"),
            ]
            ))
        w,h = header2.wrap(doc.width-115, doc.topMargin)
        header2.drawOn(canvas,70, doc.height -40 + doc.topMargin-93)

       

        # FOOTER

        footer4 = Paragraph("Fecha: "+str(fecha),ta_l7)
        w, h = footer4.wrap(doc.width -200, doc.bottomMargin) 
        footer4.drawOn(canvas,doc.height-105, doc.topMargin +625, h)

        canvas.restoreState()

def PenPDF(request):
    response = HttpResponse(content_type='application/pdf')
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    doc = SimpleDocTemplate(buffer,
        pagesizes=letter,
        rightMargin = 30,
        leftMargin= 30,
        topMargin=176.9,
        bottomMargin=50,
        paginate_by=0,
    )
    ta_r = ParagraphStyle('parrafos', 
        alignment = TA_RIGHT,
        fontSize = 13,
        fontName="Helvetica-Bold",
        )
    persona=[]
    styles = getSampleStyleSheet()
    # TABLA NUMERO 1
    count = 0
    data = []
    c = Pension.objects.all().order_by('-id')
    if c:
        for i in c:
            count =count+1 
            data.append([count,i.expediente.trabajador.cedu_trab,i.expediente.trabajador.nomb_trab,i.fecha_s.date(),i.estatus])
    else:
        return redirect('Constancias:Listjubi')
    print(data)
    x = Table(data, colWidths = [35,60,120,120,120])
    x.setStyle(TableStyle(
        [   
            ('GRID', (0, 0), (12, -1), 1, colors.black),
            ('ALIGN',(0,0),(3,-1),'CENTER'),
            ('FONTSIZE', (0, 0), (4, -1), 8),   
        ]
    ))
    persona.append(x)

    doc.build(persona,onFirstPage=HeaderFooterpen,onLaterPages=HeaderFooterpen,canvasmaker=NumberedCanvas)
    response.write(buffer.getvalue())
    buffer.close()

    return response