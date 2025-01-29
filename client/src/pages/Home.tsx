import React, { useState, useCallback } from "react";
import {
    TextField,
    Button,
    Container,
    Typography,
    Box,
    Paper,
    useTheme,
    CssBaseline,
    Stack,
} from "@mui/material";
import { useDropzone } from "react-dropzone";
import { verifyEmail } from "../services/Requests/Classifier/verifyEmail";

const Home: React.FC = () => {
    const theme = useTheme();
    const [inputType, setInputType] = useState<"text" | "file">("text");
    const [emailContent, setEmailContent] = useState<string>("");
    const [uploadedFile, setUploadedFile] = useState<File | null>(null);

    const onDrop = useCallback((acceptedFiles: File[]) => {
        const file = acceptedFiles[0];
        if (file) {
            setUploadedFile(file);
            if (file.type.includes("text")) {
                const reader = new FileReader();
                reader.onload = (e) => setEmailContent(e.target?.result as string);
                reader.readAsText(file);
            }
        }
    }, []);

    const { getRootProps, getInputProps } = useDropzone({
        onDrop,
        accept: ".txt,.pdf",
        multiple: false,
    });

    const handleVerifyEmail = async () => {
        if (inputType === "text") {
            await verifyEmail({ msg: emailContent, type: { STR: emailContent, PDF: "", TXT: "" } });
        } else if (uploadedFile) {
            const formData = new FormData();
            formData.append("file", uploadedFile);
            await verifyEmail({ msg: "", type: { STR: "", PDF: uploadedFile.type.includes("pdf") ? formData : "", TXT: uploadedFile.type.includes("text") ? formData : "" } });
        }
    };

    return (
        <Stack sx={{ display: "flex", width: "100%", height: "100vh", justifyContent: "center" }}>
            <Container
                maxWidth="sm"
                sx={{
                    mt: 4,
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    justifyContent: "center",
                    bgcolor: theme.palette.background.default,
                    color: theme.palette.text.primary,
                    p: 4,
                    borderRadius: 2,
                    boxShadow: 3,
                }}
            >
                <CssBaseline />
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
                            border: "2px dashed",
                            borderColor: theme.palette.primary.main,
                            cursor: "pointer",
                            width: "100%",
                            bgcolor: theme.palette.background.paper,
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
                <Button variant="contained" color="primary" sx={{ mt: 2, width: "100%" }} onClick={handleVerifyEmail}>
                    Verificar Email
                </Button>
            </Container>
        </Stack>

    );
};

export default Home;
