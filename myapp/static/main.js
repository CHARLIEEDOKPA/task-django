window.addEventListener("DOMContentLoaded",() => {

    let closeMessage = document.getElementById("close-message")
    let goBack = document.getElementById("go-back")

    if(closeMessage) {
        closeMessage.getElementById("close-message").addEventListener("click",() => {
            let message = document.querySelector(".message")
            message.remove()
        })
    }

    if(goBack) {
        goBack.addEventListener(("click"),() => {
           history.back()
        })
    }



})




