// Esconde o muestra el usuario en la navbar dependiendo si esta o no autenticado
if (user != 'AnonymousUser'){
                document.getElementById('ini-session').classList.add("hidden");
                document.getElementById('hello-user').classList.remove("hidden");
                document.getElementById('close-session').classList.remove("hidden");
                }

// Coockie para comprar sin tener un usuario registrado
var user = '{{request.user}}'
function getToken(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getToken('csrftoken');

function getCookie(name){
    //Parte la cadena de cookies y obtiene todos los pares name = value en un array
    var cookieArr = document.cookie.split(";");

    //Itera entre los elementos del array
    for(var i = 0; i < cookieArr.length; i++){
        var cookiePair = cookieArr[i].split("=");

        /* elimina espacios en blanco al comienzo del nombre de la cookie
        y lo compararlo con la cadena dada */
        if(name == cookiePair[0].trim()){
            //Decodifica el valor de la cookie y lo devuelve
            return decodeURIComponent(cookiePair[1]);
        }
    }
    //retorna null si no lo encuentra
    return null;
}

var cart = JSON.parse(getCookie('cart'));
if(cart == undefined){
    cart = {};
    console.log('Cart Creada!', cart);
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
}
console.log('Cart:', cart);