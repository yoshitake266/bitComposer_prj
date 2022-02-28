var box = document.getElementById('box'),
    p = document.createElement('p'),
    text = document.createTextNode("test"),
    textcreate = document.getElementById('textcreate'),
    textdelete = document.getElementById('textdelete'),
    textcolorchange = document.getElementById('textcolorchange'),
    textchange = document.getElementById('textchange');
  
    function bluecolor() {
      box.style.backgroundColor = "blue";
    }
    function redcolor() {
      box.style.backgroundColor = "red";
    }
    function greencolor() {
      box.style.backgroundColor = "green";
    }
    function clearText() {
      var textForm = document.getElementById("form1");
      textForm.value = '';
    }
    
    function clearTextarea() {
      var textareaForm = document.getElementById("form2");
      textareaForm.value = '';
    }

    function clearTexs(){
      var textareaForm = document.getElementById("form2");
      textareaForm.value = value = slice(0,-1)
      return value
      }
      