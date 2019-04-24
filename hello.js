function greetMe(yourName) {
    greetMe('world');
}

function displayText() {
    document.getElementById("demo").innerHTML = "Hello I was clicked!";
}

function demoParagraphCreation() {
    for (let i = 1; i <= 10; i++) {
        var pgraph = document.createElement("p");
        p.innerHTML = "No of paragraph: " + i;
        document.body.appendChild(pgraph);
    }

}