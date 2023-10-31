import React, { Fragment, useState, useRef, useCallback } from "react";
import { Container, Card, CardHeader, CardBody } from "reactstrap";
import ReactCrop from "react-image-crop";
import { useDispatch, useSelector } from "react-redux";
import { STEP1_DATA } from "src/redux/User/DApps/actionTypes";
import { NEW_DAPP_LOGO } from "src/redux/User/DApps/actionTypes";

const Imagecropper = (props) => {
    const [upImg, setUpImg] = useState();
    const imgRef = useRef(null);
    const [crop, setCrop] = useState({ unit: "px", width: 180, aspect: 1 });
    const [previewUrl, setPreviewUrl] = useState();
    const dispatch = useDispatch();
    const step1 = useSelector((state) => state.DApp.step1Data);

    const onSelectFile = (e) => {
        if (e.target.files && e.target.files.length > 0) {
            const reader = new FileReader();
            reader.addEventListener("load", () => setUpImg(reader.result));
            reader.readAsDataURL(e.target.files[0]);
        }
    };

    const onLoad = useCallback((img) => {
        imgRef.current = img;
    }, []);

    const makeClientCrop = async (crop) => {
        if (imgRef.current && crop.width && crop.height) {
            createCropPreview(imgRef.current, crop, "newFile.jpeg");
        }
    };

    const createCropPreview = async (image, crop, fileName) => {
        const canvas = document.createElement("canvas");
        const scaleX = image.naturalWidth / image.width;
        const scaleY = image.naturalHeight / image.height;
        canvas.width = crop.width;
        canvas.height = crop.height;
        const ctx = canvas.getContext("2d");

        ctx.drawImage(image, crop.x * scaleX, crop.y * scaleY, crop.width * scaleX, crop.height * scaleY, 0, 0, crop.width, crop.height);

        return new Promise((resolve, reject) => {
            canvas.toBlob((blob) => {
                if (!blob) {
                    reject(new Error("Canvas is empty"));
                    return;
                }
                blob.name = fileName;
                window.URL.revokeObjectURL(previewUrl);
                setPreviewUrl(window.URL.createObjectURL(blob));
            }, "image/jpeg");
        });
    };
    dispatch({ type: NEW_DAPP_LOGO, payload: previewUrl });

    return (
        <>
            {/* <div className="input-cropper" style={{ width: '100%', height: '40px', display: 'flex', alignItems: 'center' }}>
                <input type="file" onChange={onSelectFile} />
            </div> */}
            <div className="uploadImg">
                <div className="fa fa-file-image-o f-48" style={{ opacity: "0.5", color: "gray" }} />
                <div className="label-uploadImg">Drop an image here or click</div>
            </div>
            <ReactCrop src={upImg} crop={crop} onImageLoaded={onLoad} onChange={(c) => setCrop(c)} onComplete={makeClientCrop} />
            {previewUrl && <img alt="Crop preview" src={previewUrl} style={{ maxWidth: "100%", maxHeight: "100%" }} className="crop-portion" />}
        </>
    );
};

export default Imagecropper;
