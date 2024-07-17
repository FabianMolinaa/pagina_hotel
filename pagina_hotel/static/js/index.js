// Función para mostrar una ciudad específica cuando se hace clic en un botón
function openCity(evt, cityName) {
    var i, tabcontent, tablinks;
    
    // Oculta todos los elementos con clase "tabcontent"
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    
    // Remueve la clase "active" de todos los elementos con clase "tablinks"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    
    // Muestra la pestaña (ciudad) actual y agrega la clase "active" al botón que abrió la pestaña
    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.className += " active";
}

// Obtiene el elemento con id="defaultOpen" y simula un clic en él al cargar la página
document.getElementById("defaultOpen").click();  