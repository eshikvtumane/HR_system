$(document).ready(function(){
    //$('input:text:second').focus();

     $('input').bind("keydown", function(e) {
        var n = $("input").length;
        if (e.which == 13)
        { //Enter key
          e.preventDefault(); //Skip default behavior of the enter key
          var nextIndex = $('input').index(this) + 1;
          if(nextIndex < n)
            $('input')[nextIndex].focus();
          else
          {
            $('input')[nextIndex-1].blur();
            $('#btnSubmit').click();
          }
        }
      });
});

