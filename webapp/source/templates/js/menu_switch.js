function bouton_menu_1_clicked() {
	document.getElementsByClassName("menu_1")[0].style.display='block';
	document.getElementsByClassName("menu_2")[0].style.display='none';
	document.getElementsByClassName("menu_3")[0].style.display='none';
	document.getElementsByClassName("menu_4")[0].style.display='none';
}

function bouton_menu_2_clicked() {
	document.getElementsByClassName("menu_1")[0].style.display='none';
	document.getElementsByClassName("menu_2")[0].style.display='block';
	document.getElementsByClassName("menu_3")[0].style.display='none';
	document.getElementsByClassName("menu_4")[0].style.display='none';
}

function bouton_menu_3_clicked() {
	document.getElementsByClassName("menu_1")[0].style.display='none';
	document.getElementsByClassName("menu_2")[0].style.display='none';
	document.getElementsByClassName("menu_3")[0].style.display='block';
	document.getElementsByClassName("menu_4")[0].style.display='none';
}

function bouton_menu_4_clicked() {
	document.getElementsByClassName("menu_1")[0].style.display='none';
	document.getElementsByClassName("menu_2")[0].style.display='none';
	document.getElementsByClassName("menu_3")[0].style.display='none';
	document.getElementsByClassName("menu_4")[0].style.display='block';
}

document.getElementsByClassName("bouton_menu_1")[0].addEventListener("click", bouton_menu_1_clicked);
document.getElementsByClassName("bouton_menu_2")[0].addEventListener("click", bouton_menu_2_clicked);
document.getElementsByClassName("bouton_menu_3")[0].addEventListener("click", bouton_menu_3_clicked);
document.getElementsByClassName("bouton_menu_4")[0].addEventListener("click", bouton_menu_4_clicked);

bouton_menu_1_clicked();