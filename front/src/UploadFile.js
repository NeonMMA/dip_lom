import React, { Component } from "react";
import axios from 'axios';

class UploadFile extends Component {
    state = {
        selectedFile: null,
    };

    // Обработчик выбора файла
    onFileChange = (event) => {
        const file = event.target.files[0];

        if (file && file.name.endsWith('.jpg')) {
            this.setState({ selectedFile: file });
        } else {
            alert("Please select a valid image file.");
            event.target.value = null;
        }
    };

    // Обработчик загрузки файла
    onFileUpload = () => {
        const formData = new FormData();

        // Добавляем файл и динамическое имя таблицы
        formData.append("file", this.state.selectedFile);
        formData.append("test", "test is True");

        console.log("Selected file:", this.state.selectedFile);

        axios.post("http://localhost:5000/upload", formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
        .then(response => {
            console.log("Response from server:", response.data);
        })
        .catch(error => {
            console.error("Error uploading file:", error.response ? error.response.data : error.message);
        });
    };

    render() {
        return (
            <div class="col-md-6">
                <input
                    type="file"
                    onChange={this.onFileChange}
                    accept=".jpg"
                />
                <button onClick={this.onFileUpload}>
                    Upload!
                </button>
            </div>
        );
    }
}

export default UploadFile;