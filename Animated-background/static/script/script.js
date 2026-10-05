let ws = new WebSocket("ws://127.0.0.1:8000/ws");

ws.addEventListener("message", function(e) {
    let cards= document.querySelector(".container");
    
    let colors = e.data.split('-')
    console.log(`linear-gradient(to bottom,${colors[0]}, ${colors[1]})`)
    cards.style.background = `linear-gradient(to bottom,${colors[0]}, ${colors[1]})`;
    
} );

function mouseEvent(element){
    element.addEventListener("mouseover", (e) => {

        if (e.target.classList.contains("src")) {
            ws.send(e.target.getAttribute("src"));
            
            
        };
    })
}

let cards = document.getElementById("cards-main");

mouseEvent(cards);