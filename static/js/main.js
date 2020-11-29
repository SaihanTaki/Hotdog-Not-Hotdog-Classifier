
if (document.readyState !== 'loading') {
    eventHandler()
  } else {
    document.addEventListener('DOMContentLoaded', eventHandler);
  }

// --------------------------- Event Handler Function --------------------------------------------

  function eventHandler(event) {

    // Init
    var imageSection = document.querySelector('.image-section')
    imageSection.style.display = 'none'
    var loader = document.querySelector('.loader')
    loader.style.display = 'none'
    var result = document.querySelector('#result')
    result.style.display = 'none'



    // Upload Preview
    function readURL(input){
        if (input.files && input.files[0]){
            var reader = new FileReader();
            reader.onload = function (e) {
                var imagePreview = document.querySelector('#imagePreview')
                imagePreview.style.backgroundImage = 'url(' + e.target.result + ')'
                imagePreview.style.display = 'block'
                fadeIn(imagePreview, 650)
            }
            reader.readAsDataURL(input.files[0])
        }
    }

    imageUpload = document.querySelector("#imageUpload")
    imageUpload.addEventListener('change',function () {
        var imageSection = document.querySelector('.image-section')
        imageSection.style.display = 'block'
        var btnPredict = document.querySelector('#btn-predict')
        btnPredict.style.display = 'block'
        var result = document.querySelector('#result')
        result.textContent = ''
        result.style.display = 'none'
        readURL(this);
    })




    // Predict
    var btnPredict = document.getElementById('btn-predict')
    btnPredict .addEventListener('click', function (){

        var formData = new FormData(document.getElementById('upload-file'))
        //Show loading animation
        var btn = document.getElementById('btn-predict')
        btn.style.display = 'none'
        var loader = document.querySelector('.loader')
        loader.style.display = 'block'

        //Make prediction by calling api /predict
        async function predict(){
          try{
              const response = await fetch("/predict",{
                method : "POST",
                body: formData
              })
      
              const data = await response.text()
              var loader = document.querySelector('.loader')
              loader.style.display = 'none'
              var result = document.querySelector('#result')
              result.style.display = 'block'
              fadeIn(result,600)
              result.textContent = 'Result: '+ data
              console.log('Success!... Result: '+data)
          }
          catch(e) {
              console.log(e)
              var loader = document.querySelector('.loader')
              loader.style.display = 'none'
              var result = document.querySelector('#result')
              fadeIn(result,600)
              result.textContent = 'Something Wrong!'
          }
      }

        predict()

    })
}



// ------------------------ Helper Function -------------------------------------------------------------------
function fadeIn(elem, ms) {
    elem.style.opacity = 0;
  
    if (ms) {
      let opacity = 0;
      const timer = setInterval(function() {
        opacity += 50 / ms;
        if (opacity >= 1) {
          clearInterval(timer);
          opacity = 1;
        }
        elem.style.opacity = opacity;
      }, 50);
    } else {
      elem.style.opacity = 1;
    }
  }






  


        // //Make prediction by calling api /predict
        // fetch("/predict",{
        //   method : "POST",
        //   body: formData
        // }).then(function(response
        //   ){
        //     return response.text()
        //   }).then(function(data){
        //         var loader = document.querySelector('.loader')
        //         loader.style.display = 'none'
        //         var result = document.querySelector('#result')
        //         result.style.display = 'block'
        //         fadeIn(result,600) 
        //         result.textContent = 'Result: '+ data
        //         console.log('Success!..Result : '+ data)
        //   })