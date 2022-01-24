(function(){
  var canvas = document.getElementById('canvas'),
      context = canvas.getContext('2d'),
      video = document.getElementById('video'),
      photoBtn = document.getElementById('photoBtn'),
      vendorUrl = window.URL || window.webkitURL;

  navigator.getMedia = navigator.getUserMedia ||
                       navigator.webkitgetUserMedia||
                       navigator.mozgetUserMedia||
                       navigator.msgetUserMedia;
  navigator.getMedia({
    video:true,
    audio:false
  }, function(stream){
    //video.src= vendorUrl.createObjectURL(stream);
    video.srcObject= stream;
    video.play();
  }, function(error){
    //An error occured
    //error.code
  });
/*
video.addEventListener('play', function()
  {
    draw(this,context, 380,300);
  }, false);

function draw(video,context,width,height){
    context.drawImage(video,0,0,width,height);
    setTimeout(draw, 10, video, context, width, height);
}
*/

/*
$target_dir = "uploads/";
$target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);
$uploadOk = 1;
$imageFileType = strtolower(pathinfo($target_file,PATHINFO_EXTENSION));
*/
function download(dataUrl, filename) {
    var download = document.createElement('a');
    download.href = dataUrl;
    download.target = 'static/image_data';
    download.download = filename;
    var evt = document.createEvent('MouseEvents');
    evt.initMouseEvent('click', true, true, window, 1, 0, 0, 0, 0,
                       false, false, false, false, 0, null);
    download.dispatchEvent(evt);

    var saved_url = download.target + '/' +filename;
    return saved_url;
}


photoBtn.addEventListener('click', function(){
  canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
  image_data_url = canvas.toDataURL('image/jpeg');
  console.log(image_data_url);

  calculateBtn.addEventListener('click', function(){
    download(image_data_url,'fish');
  });
  /*
  move_uploaded_file($_FILES["fileToUpload"]["image_data_url"], $target_file;
  $tempImage = $_FILES["fileToUpload"]["name"];
  $_SESSION["tempImage"] = "uploads/".$tempImage;
  */
  //save to uploads##
  // data url of the image
});

})();
