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