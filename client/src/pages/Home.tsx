import React, { useState, useCallback } from "react";
import {
    TextField,
    Button,
    Container,
    Typography,
    Box,
    Paper,
} from "@mui/material";
import { useDropzone } from "react-dropzone";

type FileType = File | null;

type HomeProps = object;

const Home: React.FC<HomeProps> = () => {
    const [inputType, setInputType] = useState<"text" | "file">("text");
    const [emailContent, setEmailContent] = useState<string>("");
    const [uploadedFile, setUploadedFile] = useState<FileType>(null);

    const onDrop = useCallback((acceptedFiles: File[]) => {
        const file = acceptedFiles[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => setEmailContent(e.target?.result as string);
            reader.readAsText(file);
            setUploadedFile(file);
        }
    }, []);

    const { getRootProps, getInputProps } = useDropzone({
        onDrop,
        accept: ".txt,.pdf",
        multiple: false,
    });

    return (
        <Container maxWidth="sm" sx={{ mt: 4, display: "flex", flexDirection: "column", alignItems: "center" }}>
            <Typography variant="h5" gutterBottom textAlign="center">
                Classificador de SPAM
            </Typography>
            <Box display="flex" gap={2} mb={2} width="100%" justifyContent="center">
                <Button
                    variant={inputType === "text" ? "contained" : "outlined"}
                    onClick={() => setInputType("text")}
                >
                    Escrever
                </Button>
                <Button
                    variant={inputType === "file" ? "contained" : "outlined"}
                    onClick={() => setInputType("file")}
                >
                    Upload
                </Button>
            </Box>
            {inputType === "text" ? (
                <TextField
                    label="Conteúdo do Email"
                    multiline
                    fullWidth
                    rows={6}
                    variant="outlined"
                    value={emailContent}
                    onChange={(e) => setEmailContent(e.target.value)}
                />
            ) : (
                <Paper
                    {...getRootProps()}
                    sx={{
                        p: 4,
                        textAlign: "center",
                        border: "2px dashed #ccc",
                        cursor: "pointer",
                        width: "100%",
                    }}
                >
                    <input {...getInputProps()} />
                    {uploadedFile ? (
                        <Typography>Arquivo carregado: {uploadedFile.name}</Typography>
                    ) : (
                        <Typography>Arraste um arquivo .txt ou .pdf aqui ou clique para selecionar</Typography>
                    )}
                </Paper>
            )}
        </Container>
    );
};

export default Home;
