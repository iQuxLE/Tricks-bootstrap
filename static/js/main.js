// hier findest du alles Javascript, das für die Funktionalität der Seite notwendig ist

// ermöglicht das Abspielen von Videos, die erst nach dem Laden der Seite erstellt werden
$(document).ready(function(){
  // wenn auf einem 'a' tag mit der klasse 'video' geklickt wird 
  $("body").on('mouseover', 'a', function() {
      //  dann wird der href wert in die variable videoSrc gespeichert
      var videoSrc = $(this).attr('href');
      // und in das div mit der id 'video-preview' wird ein video tag mit dem src wert von videoSrc eingefügt
      $("#video-preview").html('<video width="320" height="240" controls><source src="'+ videoSrc +'" type="video/mp4"></video>');
  });
});



$(document).ready(function() {
  // AJAX request
  $.ajax({
    // Zugriff auf den "/uploads" Endpunkt
      url: '/uploads',
      // Zugriffstyp GET
      type: 'GET',
      // keine Daten an den Server senden
      success: function(data) {
        // JSON-formatierte Antwort in ein Array von JavaScript-Objekten konvertieren
          data = JSON.parse(data);
          // For-Loop durchläuft jedes Element des Arrays und hängt es an das HTML-Element mit dem ID "videos" an
          for (var i = 0; i < data.length; i++) {
              $('#videos').append('<a href="/uploads/' + data[i] + '">' + data[i] + '</a><br>');
          }
      }
  });
});

