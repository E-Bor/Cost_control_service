import { CreateJsonToSend} from "../FormsScripts.js"
import { SendJSON } from "../sendRequest.js"

const mainForm = document.forms[0]
const login = mainForm.login
const password_first = mainForm.password_first
const password_second = mainForm.password_second
const button = mainForm.button

const url_auth = "http://127.0.0.1:8000/"

function checkAuthForm() {
    console.log(login, password_first.value, password_second.value)
}

function sendAuthForm(event) {
    
    event.preventDefault()
    if (password_first.value == password_second.value && (password_first.value ?? password_second.value)){
        const json = CreateJsonToSend("auth_form", login.value, password_first.value)
        SendJSON(url_auth, "POST", json)
    }
}

mainForm.addEventListener("input", checkAuthForm)
button.addEventListener("click", sendAuthForm)