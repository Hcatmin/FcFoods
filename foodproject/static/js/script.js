var navmobile = document.getElementById("nav-mobile");
var navpc = document.getElementById("nav-pc");
var navsearch = document.getElementById("nav-search");

// var display = navpc.style.display;
var estiloComputado = window.getComputedStyle(navpc);

function responsive_mode() {
  var display = estiloComputado.getPropertyValue('display');
  if (display == "flex") {
    navpc.hidden = false;
    navmobile.hidden = true;
    navsearch.hidden = true;
  }
  else {
    // navpc.style.setProperty('display', 'none'); // Oculta el elemento
    navpc.hidden = true;
    navmobile.hidden = false;
    navsearch.hidden = false;
  }
};

responsive_mode();

window.onresize = responsive_mode;

