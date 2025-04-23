import React, { useState } from "react";
import ImageUploader from "./ImageUploader";
import "./Analysis.css"


function Analysis() {
    const [uploadResponse, setUploadResponse] = useState(null);

    // Функция, которую передаем в ImageUploader для обновления ответа
    const handleUploadResponse = (responseData) => {
        setUploadResponse(responseData);
    };

    const renderNestedParameters = (data) => {
        if (typeof data !== 'object' || data === null) {
            return <td className = "parameter-value" > { data } < /td>;
        }

        return ( <
            td className = "parameter-value" >
            <
            table className = "nested-parameters-table" >
            <
            tbody > {
                Object.entries(data).map(([key, value]) => ( <
                    tr key = { key } >
                    <
                    td className = "parameter-key" > { key }: < /td> { renderNestedParameters(value) } < /
                    tr >
                ))
            } <
            /tbody> < /
            table > <
            /td>
        );
    };

    const renderParameters = () => {
        if (!uploadResponse) return <p > No parameters available < /p>;

        return ( <
            div className = "parameters-container" >
            <
            table className = "parameters-table" >
            <
            tbody > {
                Object.entries(uploadResponse).map(([key, value]) => ( <
                    tr key = { key } >
                    <
                    td className = "parameter-key" > { key }: < /td> { renderNestedParameters(value) } <
                    /tr>
                ))
            } <
            /tbody> <
            /table> <
            /div>
        );
    };

    return ( < div className = "row window" >

        <
        ImageUploader onUploadResponse = { handleUploadResponse }
        /> 

        <
        div className = "col-md-6 parameters" >
        <
        h3 > Analysis Parameters < /h3> { renderParameters() }  < /
        div > <
        /div>
    );
}

export default Analysis;