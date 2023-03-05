import { CreateJsonToSend } from "../FormsScripts.js"
import { SendJSON } from "../sendRequest.js"

const url_auth = "http://127.0.0.1:8000/"


const mainForm = document.forms[0]
const login = mainForm.login
const password = mainForm.password
const button = mainForm.button


function checkAuthForm() {
    console.log(login, password)
}

function sendAuthForm(event) {
    event.preventDefault()
    const json = CreateJsonToSend("auth_form", login.value, password.value)
    SendJSON(url_auth, "POST", json)
}

mainForm.addEventListener("input", checkAuthForm)
button.addEventListener("click", sendAuthForm)