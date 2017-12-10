function GetJSON(url, input_json, callback_on_output_json) {
    $.ajax({
        url: url,
        type: "POST",
        data: JSON.stringify(input_json),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (json_data) {
            callback_on_output_json(json_data);
        }
    });
}