setTimeout(() => {
    document.getElementById("close-message").addEventListener("click",() => {
        let message = document.querySelector(".message")
        message.remove()
    })
},3000)

