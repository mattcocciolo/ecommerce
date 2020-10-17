var updatebtns = document.getElementsByClassName('update-cart')

for (var i = 0; i < updatebtns.length; i++){
    updatebtns[i].addEventListener('click', function(){
        var productid = this.dataset.product
        var action = this.dataset.action
        console.log('productid:', productid, 'action:', action,)

        console.log('User:', user)
        if (user == 'AnonymousUser'){
            addCookieItem(productid, action)
        }else{
            updateuserorder(productid, action)
        }
    })
}

function addCookieItem(productid, action){
    console.log('El usuario no esta autenticado...')

    if (action == "add"){
        if (cart[productid] == undefined){
            cart[productid] = {'quantity':1}
        }else{
            cart[productid]['quantity'] += 1
        }
    }

    if (action == "remove"){
        cart[productid]['quantity'] -=1
        if (cart[productid]['quantity'] <= 0){
            console.log('Borrar Item')
            delete cart[productid]
        }
    }
    console.log('Cart:', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
    location.reload()
}

function updateuserorder(productid, action){
    console.log('El ususario esta autenticado, enviando datos... ')

    var url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'productid': productid, 'action': action}),
    })
    .then((response) =>{
        return response.json()
    })
    .then((data) =>{
        console.log('data:', data)
        location.reload()
    });
}
