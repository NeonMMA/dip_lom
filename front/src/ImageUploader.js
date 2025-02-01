import React from "react";
import "./ImageUploader.css";
import axios from "axios";

class ImageUploader extends React.Component {
        state = {
            backgroundImage: null,
            imageSize: { width: 400, height: 300 },
        };

        handleImageChange = async(event) => {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    const img = new Image();
                    img.src = e.target.result;
                    img.onload = () => {
                        let newWidth = img.width;
                        let newHeight = img.height;
                        const maxWidth = 600;
                        const maxHeight = 600;

                        if (newWidth > maxWidth) {
                            const ratio = maxWidth / newWidth;
                            newWidth = maxWidth;
                            newHeight *= ratio;
                        }

                        if (newHeight > maxHeight) {
                            const ratio = maxHeight / newHeight;
                            newHeight = maxHeight;
                            newWidth *= ratio;
                        }

                        this.setState({ backgroundImage: e.target.result, imageSize: { width: newWidth, height: newHeight } });

                        // Отправляем изображение на сервер
                        this.handleUpload(file);
                    };
                };
                reader.readAsDataURL(file);
            }
        };

        handleUpload = async(file) => {
            const formData = new FormData();
            formData.append("file", file);

            axios.post("http://localhost:5000/upload", formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                })
                .then(response => {
                    console.log("Response from server:", response.data);
                    // Передаем данные обратно в родительский компонент через пропс
                    this.props.onUploadResponse(response.data);
                })
                .catch(error => {
                    console.error("Error uploading file:", error.response ? error.response.data : error.message);
                });
        };

        handleClick = () => {
            document.getElementById("fileInput").click();
        };

        render() {
            return ( <
                div className = "col-md-6 left_div" >
                <
                div className = "row" > < /div> <
                div className = "left row" >
                <
                div className = "col-md-1" > < /div> <
                div style = {
                    {
                        backgroundImage: this.state.backgroundImage ? `url(${this.state.backgroundImage})` : "none",
                        backgroundSize: "cover",
                        backgroundRepeat: "no-repeat",
                        backgroundPosition: "center",
                        borderRadius: "10px",
                        backgroundColor: "#3f5754",
                        width: `${this.state.imageSize.width}px`,
                        height: `${this.state.imageSize.height}px`,
                        display: "flex",
                        justifyContent: "center",
                        alignItems: "center",
                        cursor: "pointer",
                        transition: "all 0.3s ease-in-out",
                    }
                }
                onClick = { this.handleClick }
                className = "col-md-10 download_div" >
                {!this.state.backgroundImage && < span style = {
                        { color: "#fff" } } > + < /span>} <
                    input
                    id = "fileInput"
                    type = "file"
                    accept = "image/*"
                    style = {
                        { display: "none" } }
                    onChange = { this.handleImageChange }
                    /> <
                    /div> <
                    div className = "col-md-1" > < /div> <
                    /div> <
                    /div>
                );
            }
        };

        export default ImageUploader;