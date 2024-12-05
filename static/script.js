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
    });
})

//Update the correctness and work
async function fetchCorrectness() {
    const response = await fetch('/correct.txt');
    const text = (await response.text()).replace(/<br\s*\/?>/gi, '\n').replace(/\n/g, '<br>');
    document.getElementById('correctness').innerHTML = text;
    processMath();
}

setInterval(fetchCorrectness, 200);

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

setInterval(fetchWork, 200);

//Next Question button
document.getElementById("nextButton").addEventListener("click", () => {
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

//Deal with sliddes
const slideIds = ["subject-slide", "question-answer-slide", "correctness-slide"];

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
setInterval(updateSlide, 200);