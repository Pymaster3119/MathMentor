//Latex
function processMath() {
    if (window.MathJax && MathJax.typeset) {
        MathJax.typeset(); 
    }
}

//Update the subject when asked
document.getElementById("submitButton").addEventListener("click", () => {
    const subjectval = document.getElementById("subject").value;

    fetch("/api", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({subject:subjectval})
    })
    .then(response => {
        console.log("Result was " + (response.ok ? "okay": "not okay"));
        console.log(response.json());
    });
});

//Update the questions
async function fetchQuestion() {
    const response = await fetch('/question.txt');
    const text = (await response.text()).replace(/<br\s*\/?>/gi, '\n').replace(/\n/g, '<br>');

    document.getElementById('question').innerHTML = text;
    processMath();
}

setInterval(fetchQuestion, 200);

//Update the answer when asked
document.getElementById("answerButton").addEventListener("click", () => {
    const answerval = document.getElementById("answer").value;

    fetch("/answer", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({answer:answerval})
    })
    .then(response => {
        console.log("Result was " + (response.ok ? "okay": "not okay"));
        console.log(response.json());
    });
})

//Update the correctness and work
async function fetchCorrectness() {
    const response = await fetch('/correct.txt');
    const text = (await response.text()).replace(/<br\s*\/?>/gi, '\n').replace(/\n/g, '<br>');
    console.log(text)
    document.getElementById('correctness').innerHTML = text;
    processMath();
}

setInterval(fetchCorrectness, 200);

async function fetchWork() {
    const response = await fetch('/work.txt');
    const text = (await response.text()).replace(/<br\s*\/?>/gi, '\n').replace(/\n/g, '<br>');
    document.getElementById('work').innerHTML = text;
    processMath();
}

setInterval(fetchWork, 200);