



export function SendJSON (url, method, data_json){
    if (data_json == undefined){
        return 0
    }

    const response = fetch(url,{
        method: method,
        headers: {
            'Content-Type': 'application/json'
        },
        body: data_json
    })
    return response.json;
}



