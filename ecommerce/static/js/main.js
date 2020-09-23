
// Esconde o muestra el usuario en la navbar dependiendo si esta o no autenticado
if (user != 'AnonymousUser'){
                document.getElementById('ini-session').classList.add("hidden");
                document.getElementById('hello-user').classList.remove("hidden");
                document.getElementById('close-session').classList.remove("hidden");
                }


