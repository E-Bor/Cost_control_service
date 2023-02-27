// main const
const mainForm = document.forms[0]
const disc = mainForm.disription
const date = mainForm.date
const cost = mainForm.cost
const category = mainForm.category
const button = mainForm.button
const url = "http://127.0.0.1:8000/"


function CreateFormToSend(event) {
    console.log(disc, date, cost, category)
    
}

function resetAttention(event) {
    console.log(event)
}

function check_variables(obj){
    for (const i in obj){
        if (obj[i] == ""){
           return false
        };        
    };
    return true

}

function SendJSON (url, method, data_json){
    const response = fetch(url,{
        method: method,
        headers: {
            'Content-Type': 'application/json'
        },
        body: data_json
    })
    return response.json;
}


function SendExpenseForm(event){
    event.preventDefault()
    let formdata = {
        "cost": cost.value,
        "disc": disc.value,
        "category": (category.value == "Выберите") ? "": category.value ,
        "date": date.value,
    }
    if (check_variables(formdata)){
        let json = JSON.stringify(formdata);
        SendJSON(url, "POST", json);
        
    }

    
    console.log("knopka");
    
}







// console.log(mainForm)
console.log(disc.value)
console.log(date.value)
console.log(cost.value)
console.log(category.value)
console.log(button)


mainForm.addEventListener("input", CreateFormToSend);

button.addEventListener("click", SendExpenseForm)


