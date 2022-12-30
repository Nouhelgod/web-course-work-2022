var ticketNumber = document.getElementById("ticketNumber").textContent
var status = document.getElementById("status").textContent
var url = window.location.href

console.log(url)

if(status == 'ожидание') {
    setTimeout( function(){
        location.reload()
    }, 5000)
}
