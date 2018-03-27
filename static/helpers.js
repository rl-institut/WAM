
function toggle_divs(divs, value) {
  // Given an array of elements, function shows element with index "value"
  // and hides the other elements
  for (i = 0; i < divs.length; i++) {
    if ( divs[i] != null ) {
      if ( i == value ) {
        $(divs[i]).show();
      } else {
        $(divs[i]).hide();
      }
    }
  }
};