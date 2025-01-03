//Hashes
const browserInfo = navigator.userAgent;
const timeOfAccess = new Date().toISOString();
const dataToHash = `${browserInfo}-${timeOfAccess}`;
let userHash = '';

async function generateHash(data) {
    const encoder = new TextEncoder();
    const dataBuffer = encoder.encode(data);
    const hashBuffer = await crypto.subtle.digest('SHA-256', dataBuffer);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    return hashHex;
}

// Generate the hash
generateHash(dataToHash).then(hash => {
    console.log('Hash:', hash);
    userHash = hash;
});

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
        body: JSON.stringify({subject:subjectval, user_id: userHash})
    })
    .then(response => {
    });
});

//Update the questions
async function fetchQuestion() {
    const response = await fetch(`/question.txt?user_id=${userHash}`);
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
        body: JSON.stringify({answer:answerval, user_id: userHash})
    })
    .then(response => {
    });
})

//Update the correctness and work
async function fetchCorrectness() {
    const response = await fetch(`/correct.txt?user_id=${userHash}`);
    const text = (await response.text()).replace(/<br\s*\/?>/gi, '\n').replace(/\n/g, '<br>');
    document.getElementById('correctness').innerHTML = text;
    processMath();
}

setInterval(fetchCorrectness, 500);

async function fetchWork() {
    try {
        const response = await fetch(`/work.txt?user_id=${userHash}`);
    
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

//Deal with slides
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
    fetch(`/frame.txt?user_id=${userHash}`, {
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
        body: JSON.stringify({subject:subjectval, previous_question:questionval, user_id: userHash})
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
        body: JSON.stringify({subject:subjectval, previous_question:questionval, user_id: userHash})
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
        body: JSON.stringify({subject:subjectval, previous_question:questionval, user_id: userHash})
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
        body: JSON.stringify({subject:subjectval, previous_question:questionval, user_id: userHash})
    })
    .then(response => {
    });
});