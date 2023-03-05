import {CreateJsonToSend}  from "./services/FormsScripts.js"
import { SendJSON } from "./services/sendRequest.js"

const mainForm_earnings = document.forms[0]
const date_earnings = mainForm_earnings.date
const cost_earnings = mainForm_earnings.cost
const button_earnings = mainForm_earnings.earningsButton
const url_earnings = "http://127.0.0.1:8000/"



function CreateFormToSend(event) {
    console.log(date_earnings.value, cost_earnings.value)

}


function check_variables(obj){
    for (const i in obj){
        if (obj[i] == ""){
           return false
        };
    };
    return true

}


function SendearningForm(event){
    event.preventDefault()
    const json_data = CreateJsonToSend("earnings_main_form", cost_earnings.value, date_earnings.value)
    SendJSON(url_earnings, "POST", json_data)
}

mainForm_earnings.addEventListener("input", CreateFormToSend);
button_earnings.addEventListener("click", SendearningForm)

