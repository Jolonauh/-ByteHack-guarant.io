var warrantyButton = document.getElementById("warranty-button");
var trackingButton = document.getElementById("tracking-button");
var accountButton = document.getElementById("account-button");
var contentElement = document.getElementById("content");
var links;
var registerInput = document.getElementById("register-input");
var loginInput = document.getElementById("login-input");

change("warranty"); // Initial Load
warrantyButton.addEventListener("click", () => change("warranty"));
trackingButton.addEventListener("click", () => change("tracking"));
accountButton.addEventListener("click", () => change("account"));
registerInput.addEventListener("input", (event) => {
  var inputValue = event.target.value;
});
loginInput.addEventListener("input", (event) => {
  var inputValue = event.target.value;
});

function change(str) {
  contentElement.innerHTML = "";
  var currentURL;
  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    currentURL = tabs[0].url;
    console.log(currentURL);
  });
  chrome.storage.local.get(currentURL, function (result) {
    console.log("Retrieved data from local storage:", result.currentURL);
  });
  if (!contentElement.classList.contains(str)) {
    fetch("pages/" + str + ".html")
      .then((response) => response.text())
      .then((data) => {
        var parser = new DOMParser();
        var dom = parser.parseFromString(data, "text/html");
        var page = dom.documentElement.querySelector("#main");
        if (str == "tracking") {
          trackingPage().then(() => {
            contentElement.innerHTML = dom.documentElement.innerHTML;
          });
        } else if (str == "warranty") {
          warrantyPage().then(() => {
            contentElement.innerHTML = dom.documentElement.innerHTML;
          });
        } else if (str == "account") {
          fetch("pages/account.html")
            .then((response) => response.text())
            .then((data) => {
              contentElement.innerHTML = data;
            });
        }

        contentElement.classList = str + "table-container";

        // Allows the Buttons to open a new link, buttons not onClick because
        // content security policy unsafe
        links = contentElement.querySelectorAll(".myButton");
        links.forEach((link) => {
          link.onclick = () => {
            window.open(link.getAttribute("to"));
          };
        });
      });
  }
}

async function trackingPage(page) {
  console.log("before");
  var response = await fetch("localhost:5000/warranties", { method: "GET" });
  console.log(response);
  var data = await response.json();
  console.log(data);
  console.log(data);
  for (const warranty in data) {
    const obj = JSON.parse(data);
    page.innerHTML += `<div class="warranty">
      <p>${obj.brand}</p>
      <p>${obj.name}</p>
      <p>${obj.duration}</p>
      <p>${obj.price}</p>
      <p>
        <button class="myButton" to=${obj.website}>
        <i class="material-icons" style="font-size: 24px; color: white"
            >&#xe157;
        </i>
        </button>
      </p>
      <p>
        <button></button>
      </p>
    </div>`;
  }
}

function addWarranty() {
  console.log("IT WORKS!");
}

function createURL(category = "Phone", low = 200, high = 1000) {
  return (
    "localhost:5000/" +
    "?category=" +
    category +
    "&low=" +
    low +
    "&high=" +
    high
  );
}

async function warrantyPage(page) {
  chrome.storage.local.get(currentURL, function (result) {
    console.log("Retrieved data from local storage:", result.currentURL);
  });
  if (result.currentURL != undefined) {
    var URL = createURL();

    var response = await fetch(URL, { method: "GET" });
    var data = await response.json();
    for (const warranty in data) {
      const obj = JSON.parse(data);
      page.innerHTML += `<div class="warranty">
        <p>${obj.brand}</p>
        <p>${obj.name}</p>
        <p>${obj.price}</p>
        <p>${obj.duration}</p>
        <p>
          <button class="myButton" to=${obj.website}>
          <i class="material-icons" style="font-size: 24px; color: white"
              >&#xe157;</i
          >
          </button>
        </p>
        <p><button onclick="addWarranty()">+</button></p>
      </div>`;
    }
  } else {
    page.innerHTML = "<div> This Page is Not Supported, Sorry! </div>";
  }
}
