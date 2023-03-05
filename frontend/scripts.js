import {CreateJsonToSend}  from "./services/FormsScripts.js"
import { SendJSON } from "./services/sendRequest.js"

// main const
const mainForm = document.forms[0]
const disc = mainForm.disription
const date = mainForm.date
const cost = mainForm.cost
const category = mainForm.category
const button = mainForm.button

const url_expense = "http://127.0.0.1:8000/"





function CreateFormToSend(event) {
    console.log(disc, date, cost, category)

}

function resetAttention(event) {
    console.log(event)
}



function SendExpenseForm(event){
        event.preventDefault()
        const json_data = CreateJsonToSend("expense_main_form", cost.value, disc.value,
         (category.value == "Выберите") ? "": category.value, date.value)
        SendJSON(url_expense, "POST", json_data)
        }


mainForm.addEventListener("input", CreateFormToSend);
button.addEventListener("click", SendExpenseForm);

