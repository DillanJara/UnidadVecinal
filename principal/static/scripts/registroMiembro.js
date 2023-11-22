/* PREVISUALIZACION IMAGEN */
function filePreview(input) {
    let extension = /(.jpg|.jpeg|.png)$/i;
    let nombreArchivo = $("#input-btn").val()
    if(!extension.exec(nombreArchivo)) {
        Swal.fire({
            "title": "Uups!",
            "text": "Debes selecionar un archivo png o jpg",
            "icon": "error"
        })
        nombreArchivo = '';
        return false;
    }
    else {
        if(input.files && input.files[0]) {
            let reader = new FileReader();
            reader.onload = function (e) {
                $('#previewImagen').html("<img class='img-thumbnail' src='"+e.target.result+"' alt='No se pudo Cargar la Imagen'>");
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
}

$('#input-btn').change(function() {
    filePreview(this);
});

const uploadField = document.getElementById('input-btn');

uploadField.onchange = function () {
    if (this.files[0].size > 1000000) {
        Swal.fire({
            "title": "Uups!",
            "text": "El tamaño maximo para la imagen es de 10mb.",
            "icon": "error"
        })
        this.value = '';
    }
};