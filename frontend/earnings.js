const mainForm_earnings = document.forms[0]
const date_earnings = mainForm_earnings.date
const cost_earnings = mainForm_earnings.cost
const button_earnings = mainForm_earnings.earningsButton
const url_earnings = "http://127.0.0.1:8000/" 

// console.log(earning_button)



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



function SendearningForm(event){
    event.preventDefault()
    if (event.originalTarget.name == "earningsButton"){
        let formdata = {
            "earning_value": cost_earnings.value,
            "date": date_earnings.value,
        }
        if (check_variables(formdata)){
            let json = JSON.stringify(formdata);
            SendJSON(url_earnings, "POST", json);
            console.log(event);
    }
    
}}
mainForm_earnings.addEventListener("input", CreateFormToSend);
button_earnings.addEventListener("click", SendearningForm)

