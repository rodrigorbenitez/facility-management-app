
status1()

//-------filtro id-------------------//

$(document).ready(function() {
  if ($( "#column" ).val()==""){
    $(document).ready(function(){
      $("#tableInputSearch").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#myTable tr").filter(function() {
          $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
      });
    });

  }
  else{

      $("#tableOS tbody").addClass("search");
      $('#tableInputSearch').keyup(function() {
          var rex = new RegExp($(this).val(), 'i');
          // var $t = $(this).children(":eq(4))");
          $('.search tr ').hide();

          //Recusively filter the jquery object to get results.
          $('.search tr ').filter(function(i, v) {
            var column=$( "#column" ).val();
            //Get the 3rd column object here which is userNamecolumn
              var $t = $(this).children(":eq(" + column + ")");
              return rex.test($t.text());
          }).show();
      })}

 ;

})

//----------------buscador os asignadas------------------------//
  $(document).ready(function(){
    $("#assignedTicketsSearch").on("keyup", function() {
      var value = $(this).val().toLowerCase();
      $(".tbodyAssigned tr").filter(function() {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
      });
    });
  });
  //---------------------buscador os requeridas------------------------//
  $(document).ready(function(){
    $("#petitionerTicketsSearch").on("keyup", function() {
      var value = $(this).val().toLowerCase();
      $(".tbodyRequired tr").filter(function() {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
      });
    });
  });
  //---------------------search bar ------------------------//
  $('#tableInputSearch').on('keyup', function() {
    var input = $(this);
    if(input.val().length === 0) {
        input.addClass('empty');
    } else {
        input.removeClass('empty');
    }
});


//------------------functions-------------------------//

function status1(){
  var x = document.querySelectorAll("#status");
  var $row = document.querySelectorAll("#myTable>tr");
  var $status = document.querySelectorAll("#priority");
  var i;
  for (i = 0; i < x.length; i++) {
    if (x[i].innerText == "pausada"){
      x[i].innerHTML="<i style='color:orange;' class='far fa-pause-circle'></i> Pausada"
      
  }
  else if (x[i].innerText == "cerrada"){
    x[i].innerHTML="<i style='color:red;' class='far fa-times-circle'></i> Cerrada"
    $row[i].classList.add("info")
  }
  else if (x[i].innerText == "abierta"){
    x[i].innerHTML="<i style='color:green' class='fas fa-circle'></i> Abierta"

  }
  else if (x[i].innerText == "en curso"){
    x[i].innerHTML="<i style='color:green' class='far fa-arrow-alt-circle-right'></i> En curso"

  }


}
}
  //---------------------search bar asignadas------------------------//
  $('#assignedTicketsSearch').on('keyup', function() {
    var input = $(this);
    if(input.val().length === 0) {
        input.addClass('empty');
    } else {
        input.removeClass('empty');
    }
});
  //---------------------search bar requeridas------------------------//
  $('#petitionerTicketsSearch').on('keyup', function() {
    var input = $(this);
    if(input.val().length === 0) {
        input.addClass('empty');
    } else {
        input.removeClass('empty');
    }
});

//-------filtro id asignadas-------------------//

$(document).ready(function() {
  if ($( "#column" ).val()==""){
    $(document).ready(function(){
      $("#assignedTicketsSearch").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $(".tbodyAssigned tr").filter(function() {
          $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
      });
    });

  }
  else{

      $("#TableOsAssigned tbody").addClass("search");
      $('#assignedTicketsSearch').keyup(function() {
          var rex = new RegExp($(this).val(), 'i');
          // var $t = $(this).children(":eq(4))");
          $('.search tr ').hide();

          //Recusively filter the jquery object to get results.
          $('.search tr ').filter(function(i, v) {
            var column=$( "#column" ).val();
            //Get the 3rd column object here which is userNamecolumn
              var $t = $(this).children(":eq(" + column + ")");
              return rex.test($t.text());
          }).show();
      })}

 ;

})

//-------filtro id requeridas-------------------//

$(document).ready(function() {
  if ($( "#column2" ).val()==""){
    $(document).ready(function(){
      $("#petitionerTicketsSearch").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $(".tbodyRequired tr").filter(function() {
          $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
      });
    });

  }
  else{

      $("#TableOsRequired tbody").addClass("search");
      $('#petitionerTicketsSearch').keyup(function() {
          var rex = new RegExp($(this).val(), 'i');
          // var $t = $(this).children(":eq(4))");
          $('.search tr ').hide();

          //Recusively filter the jquery object to get results.
          $('.search tr ').filter(function(i, v) {
            var column=$( "#column2" ).val();
            //Get the 3rd column object here which is userNamecolumn
              var $t = $(this).children(":eq(" + column + ")");
              return rex.test($t.text());
          }).show();
      })}

 ;

})

//----------------toggle de mis ordenes-------------------------------//
$("#slideToggle1").click(function(){
  $("#assignedOsContainer").slideToggle()
 })
 $("#slideToggle2").click(function(){
  $("#requiredOsContainer").slideToggle()
 })

 //-------------------------print OS PDF ---------------------------------//

 var doc = new jsPDF()
 var html = $("#containerPrint").html()
 var osNumber = $("#osNumber").text()
 margins = {
  bottom:10,
  top:10,
  left:10,
  right:10
};

 printHtml = () => {
  var pdf = new jsPDF('p', 'pt', 'letter');
  pdf.addHTML($("#containerPrint")[0], function () {
      pdf.save(osNumber+".pdf");
  }, margins);
 }
 
//----------------toggle de navbar User-------------------------------//
$("#user").click(function(){
  $("#logOutDropdown").slideToggle()
 })

//--------------------grafico 1------------------------//

var osAbiertas=$('#osAbiertas').text()
var OsEnCurso=$('#OsEnCurso').text()
var OsPausadas=$('#OsPausadas').text()
var OsCerradas=$('#OsCerradas').text()

var ctx = document.getElementById('myChart').getContext('2d');
var myDoughnutChart = new Chart(ctx, {
  type: 'doughnut',
  data: {
    datasets: [{
        data: [osAbiertas, OsEnCurso, OsPausadas, OsCerradas], backgroundColor: ['rgb(66, 139, 202)', 'rgb(0, 201, 0)', 'rgb(255, 165, 0)', 'rgb(255, 0, 0)']
    }],labels: [
      'Abiertas',
      'En curso',
      'Pausadas',
      'Cerradas'
  ]
}
});
//--------------------grafico 2------------------------//
var media=$('#media').text()
var baja=$('#baja').text()
var alta=$('#alta').text()


var ctx = document.getElementById('myChart2').getContext('2d');
var myDoughnutChart = new Chart(ctx, {
  type: 'doughnut',
  data: {
    datasets: [{
        data: [media, baja, alta], backgroundColor: ['rgb(255, 204, 0)', 'rgb(255, 0, 0)' , 'rgb(66, 139, 202)']
    }],labels: [
      'Prioridad media',
      'Prioridad alta',
      'Prioridad Baja'
  ]
}
});