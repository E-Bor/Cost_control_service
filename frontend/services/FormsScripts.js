import { expense_form, earning_form, auth_form} from "./Forms.js"



function check_variables(obj){
    for (const i in obj){
        if (obj[i] == ""){
           return false
        };        
    };
    return true

}

function write_obj_data(obj, data_list){
    let k = 1
    for (const i in obj){
        obj[i] = data_list[k]
        k +=1
    }
    
    return obj
}


function CreateFormObject(){
    if (arguments[0] == "expense_main_form"){
        const form_obj = write_obj_data(expense_form, arguments[1])
        return form_obj
    }
    if (arguments[0] == "earnings_main_form"){
        const form_obj = write_obj_data(earning_form, arguments[1])
        return form_obj
    }
        
    if (arguments[0] == "auth_form"){
        const form_obj = write_obj_data(auth_form, arguments[1])
        return form_obj
    }
    if (arguments[0] == "registration_form"){
        const form_obj = write_obj_data(auth_form, arguments[1])
        return form_obj
    }
}


function CreateJSON(form_object){
    if (check_variables(form_object)){
        const json = JSON.stringify(form_object)
        console.log(json)
        return json
    }
    }


export function CreateJsonToSend (name_form){
    const json = CreateJSON(CreateFormObject(name_form, arguments))
    return json
}