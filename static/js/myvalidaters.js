// funcion para validar el correo
function caracteresCorreoValido(email, alert){
    var user = $(email).val();
    var caract = new RegExp(/^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/);

    if (caract.test(user) == false){
        $(alert).html('Correo incorrecto debe ser ejemplo@gmail.com').slideDown(500);
        $(user).onfocus();
        return false;
    }else{
        $(alert).slideUp(200);
        return true;
    }
}

$("#formValidate").validate({
    rules: {
        cod_seg_soc:"required",
        expediente:"required",
        trami_pens:"required",
        esta_seg_soc:"required",
        fech_func:"required",
        estado_civil:"required",
        trabajador:"required",
        directores:"required",
        cedula: {
            required: true,
            minlength: 9
        },
    },
    
    //For custom messages
    messages: {
        cod_seg_soc:"Colocar codigo",
        estado_civil:"Seleccione estado civil",
        trabajador:"Seleccione trabajador",
        directores:"Seleccione director",
        expediente:"Seleccionar expediente",
        trami_pens:"Seleccionar si esta pensionado",
        esta_seg_soc:"Seleccionar estatus",
        fech_func:"Selecionar una fecha",
        cedula:{
            required: "Colocar cedula",
            minlength: "maximo 9 numeros"
        },
    },
    errorElement : 'div',
    errorPlacement: function(error, element) {
      var placement = $(element).data('error');
      if (placement) {
        $(placement).append(error)
      } else {
        error.insertAfter(element);
      }
    }
 });