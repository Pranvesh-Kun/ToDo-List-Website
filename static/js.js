function myFunction() {
  // Get the checkbox
  var checkBox = document.getElementById("checkbox");
  // Get the output text
  var text = document.getElementById("1");

  if (checkBox.checked == true){
    text.style.display = ”text-decoration:line-through”;
  }
}