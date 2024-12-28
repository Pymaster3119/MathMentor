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
    });
});

//Update the questions
async function fetchQuestion() {
    const response = await fetch('/question.txt');
    const text = (await response.text()).replace(/<br\s*\/?>/gi, '\n').replace(/\n/g, '<br>');

    document.getElementById('question').innerHTML = text;
    processMath();
}

setInterval(fetchQuestion, 500);

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
    });
})

//Update the correctness and work
async function fetchCorrectness() {
    const response = await fetch('/correct.txt');
    const text = (await response.text()).replace(/<br\s*\/?>/gi, '\n').replace(/\n/g, '<br>');
    document.getElementById('correctness').innerHTML = text;
    processMath();
}

setInterval(fetchCorrectness, 500);

async function fetchWork() {
    try {
        const response = await fetch('/work.txt');
    
        if (!response.ok) {
            return;
        }
    
        const text = await response.text(); 
        if (text.includes("document not created yet"))
        {
            return;
        }
        const formattedText = text.replace(/<br\s*\/?>/gi, '\n').replace(/\n/g, '<br>');
        document.getElementById('work').innerHTML = formattedText;
        processMath();
    } catch {
        
    }
}

setInterval(fetchWork, 500);

//Deal with sliddes
const slideIds = ["subject-slide", "generating-slide", "question-answer-slide", "checking-slide", "correctness-slide"];

function showSlide(index) {
    slideIds.forEach((id, i) => {
        const slide = document.getElementById(id);
        if (i === index) {
            slide.style.display = "block";
        } else {
            slide.style.display = "none";
        }
    });
}

function updateSlide() {
    fetch('/frame.txt', {
        method: 'POST',
    })
    .then(response => response.text())
    .then(data => {
        const slideIndex = parseInt(data, 10);
        if (!isNaN(slideIndex) && slideIndex >= 0 && slideIndex < slideIds.length) {
            showSlide(slideIndex);
        } else {
            console.error("Invalid slide index received:", data);
        }
    })
    .catch(error => {
        console.error("Error fetching slide index:", error);
    });
}


showSlide(0);
setInterval(updateSlide, 500);

//Same topic button
document.getElementById("sameButton").addEventListener("click", () => {
    const subjectval = document.getElementById("subject").value;
    const questionval = document.getElementById("question").value;

    fetch("/sametopic", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({subject:subjectval, question:questionval})
    })
    .then(response => {
    });
});

//Different topic button
document.getElementById("diffButton").addEventListener("click", () => {
    const subjectval = document.getElementById("subject").value;
    const questionval = document.getElementById("question").value;

    fetch("/differenttopic", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({subject:subjectval, question:questionval})
    })
    .then(response => {
    });
});

//Harder question button
document.getElementById("hardButton").addEventListener("click", () => {
    const subjectval = document.getElementById("subject").value;
    const questionval = document.getElementById("question").value;

    fetch("/hardquestion", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({subject:subjectval, question:questionval})
    })
    .then(response => {
    });
});

//Easy question button
document.getElementById("easyButton").addEventListener("click", () => {
    const subjectval = document.getElementById("subject").value;
    const questionval = document.getElementById("question").value;

    fetch("/easyquestion", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({subject:subjectval, question:questionval})
    })
    .then(response => {
    });
});