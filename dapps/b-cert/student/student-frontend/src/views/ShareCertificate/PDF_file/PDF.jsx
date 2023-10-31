import { Button } from "@material-ui/core";
import React, { createRef } from "react";
import Pdf from "react-to-pdf";
import jsPDF from "jspdf";

export default function PDF() {
    const pdfGenerate = () => {
        var doc = new jsPDF("landscape", "px", "a4", "false");
        doc.addImage("https://c4.wallpaperflare.com/wallpaper/764/505/66/baby-groot-4k-hd-superheroes-wallpaper-preview.jpg", 65, 20, 500, 400);
        doc.addPage();
        doc.setFont("Helvertica", "bold");
        doc.text(60, 80, "Quyen");
        doc.save("Bcert.pdf");
    };
    return (
        <>
            <Button onClick={pdfGenerate}>Download</Button>
        </>
    );
}
