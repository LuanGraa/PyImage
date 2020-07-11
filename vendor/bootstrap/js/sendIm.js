function sendFile(file) {
    var data = new FormData();
    data.append("image", file);
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "processImg");
    xhr.upload.addEventListener("progress", updateProgress, false);
    xhr.send(data);
}
function updateProgress(evt){
    if(evt.loaded == evt.total)
        alert("Your picture has been uploaded!");
}
function updatePhoto(event){
    var reader = new FileReader();
    reader.onload = function(event){
        //Criar uma imagem
        var img = new Image();
        img.src = event.target.result;
    }
    reader.readAsDataURL(event.target.files[0]);
    sendFile(event.target.files[0]);

    //Libertar recursos da imagem seleccionada
    windowURL.revokeObjectURL(picURL);
  }
