//Las siguientes tres lineas hacen que el Zoom funcione al cambiar las imagenes del slider
document.getElementById('img-container').addEventListener('mouseover', function(){
    imageZoom('featured')
})

function imageZoom(imgID){
    let img = document.getElementById(imgID)
    let lens = document.getElementById('lens')

    lens.style.backgroundImage = `url( ${img.src} )`

    let ratio = 2

    lens.style.backgroundSize = (img.width * ratio) + 'px '+ (img.height * ratio) + 'px'

    img.addEventListener("mousemove", moveLens)
    lens.addEventListener("mousemove", moveLens)
    img.addEventListener("touchmove", moveLens)


    function moveLens(){
        /* Function sets sets position of lens over image and background image of lens
        1 - Get cursor position
        2 - Set top anf left position using cursor position - lens width & height / 2
        3 - Set lens top/left positions based on cursor results
        4 - Set lens background position & invert
        5 - Set lens bounds
        */

        //1 -
        let pos = getCursor()
        //console.log('pos:', pos)

        //2 -
        let positionLeft = pos.x - (lens.offsetWidth / 4)
        let positionTop = pos.y - (lens.offsetHeight / 4)

        //5 -
        if (positionLeft < 0){
            positionLeft= 0
        }

        if (positionTop < 0){
            positionTop = 0
        }

        if (positionLeft > img.width - lens.offsetWidth / 2){
            positionLeft = img.width -lens.offsetWidth / 2
        }

        if (positionTop > img.height - lens.offsetHeight / 2){
            positionTop = img.height - lens.offsetHeight / 2
        }

        //3 -
        lens.style.left = positionLeft + 'px';
        lens.style.top = positionTop + 'px';

        //4 -
        lens.style.backgroundPosition = "-" + (pos.x * ratio) + 'px -' + (pos.y * ratio) + 'px'


    }

    function getCursor(){
        /* Function gets position of mouse in dom and bounds of image to know where mouse is over image when moved
        1 - Set "e" to window events
        2 - Get bounds of image
        3 - Set x position of mouse on image using pagex/pageY  - bounds.left/bounds.top
        4 - Return x and y coordinates for mouse position on image
        */

        let e = window.event
        let bounds = img.getBoundingClientRect()
        //console.log('e:', e)
        //console.log('bounds:', bounds)
        let x = e.pageX - bounds.left
        let y = e.pageY - bounds.top
        x = x - window.pageXOffset;
        y = y - window.pageYOffset;

        return {'x':x, 'y':y}
    }
}


