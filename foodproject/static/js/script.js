const navmobile = document.getElementById("nav-mobile");
const navpc = document.getElementById("nav-pc");
const pcard = document.getElementById("popular");


if (window.innerWidth >= 992  ) {
  navmobile.hidden = true;
  navpc.hidden = false;
}
else {
  navmobile.hidden = false;
  navpc.hidden = true;
}

function responsiveNav() {
  if (window.innerWidth >= 992  ) {
    navmobile.hidden = true;
    navpc.hidden = false;
  }
  else {
    navmobile.hidden = false;
    navpc.hidden = true;
  }
}



window.onresize = responsiveNav;

