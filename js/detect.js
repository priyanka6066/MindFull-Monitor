const apiUrl = "http://127.0.0.1:5000/stress-evaluation";
const answer = document.querySelector(".answer");
let token = localStorage.getItem("token");

document
  .getElementById("add-user-form")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const ans1 = parseInt(document.getElementById("ans1").value);
    const ans2 = parseInt(document.getElementById("ans2").value);
    const ans3 = parseInt(document.getElementById("ans3").value);
    const ans4 = parseInt(document.getElementById("ans4").value);
    const ans5 = parseInt(document.getElementById("ans5").value);

    const data = {
      answers: [ans1, ans2, ans3, ans4, ans5],
    };

    await fetch(apiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`,
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        answer.innerHTML = `
        <h1>Answer</h1>
        <h1>Stress level : ${data.stress_level}</h1>`;

     
      });
  });
