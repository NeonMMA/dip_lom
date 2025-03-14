import React, { useState } from "react";
import ImageUploader from "./ImageUploader";
import "./Processing.css"

function Processing() {
    const [uploadResponse, setUploadResponse] = useState(null);

    // Функция, которую передаем в ImageUploader для обновления ответа
    const handleUploadResponse = (responseData) => {
        setUploadResponse(responseData);
    };

    return (
        <div className="row window">
            <ImageUploader onUploadResponse={handleUploadResponse} />
            <div className="col-md-6">
                <p>{uploadResponse ? JSON.stringify(uploadResponse) : "Parameters"}</p>
            </div>
        </div>
    );
}

export default Processing;
