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
    CircularProgress,
} from "@mui/material";
import { useDropzone } from "react-dropzone";
import { verifyEmail } from "../services/Requests/Classifier/verifyEmail";

const Home: React.FC = () => {
    const theme = useTheme();
    const [inputType, setInputType] = useState<"text" | "file">("text");
    const [emailContent, setEmailContent] = useState<string>("");
    const [uploadedFile, setUploadedFile] = useState<File | null>(null);
    const [loading, setLoading] = useState<boolean>(false);
    const [suggestion, setSuggestion] = useState<string>("");

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
        
        setLoading(true);
        setSuggestion("");
        try {
            let response;
            console.log(inputType, " vazia")
            if (inputType === "text") {
                response = await verifyEmail({ msg: emailContent, type: "STR" });
                console.log(response.response, " -> AQUI")
            } else if (uploadedFile) {
                const fileType = uploadedFile.type.includes("pdf") ? "PDF" : "TXT";
                response = await verifyEmail({ type: fileType, file: uploadedFile });
            }
            console.log(response.response, " -> AQUI")
            setSuggestion(response?.response || "Nenhuma sugestão gerada.");
        } catch (error) {
            setSuggestion("Erro ao processar a solicitação.");
        } finally {
            setLoading(false);
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
                <Button
                    variant="contained"
                    color="primary"
                    sx={{ mt: 2, width: "100%" }}
                    onClick={handleVerifyEmail}
                    disabled={loading}
                >
                    {loading ? <CircularProgress size={24} color="inherit" /> : "Verificar Email"}
                </Button>
                {suggestion && (
                    <Paper sx={{ mt: 2, p: 2, width: "100%" }}>
                        <Typography variant="subtitle1">Sugestão de Resposta:</Typography>
                        <Typography variant="body2">{suggestion}</Typography>
                    </Paper>
                )}
            </Container>
        </Stack>
    );
};

export default Home;
